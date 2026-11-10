# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
# /// script
# requires-python = "==3.12.*"
# dependencies = ["usd-brep==1.0.1", "numpy"]
# ///
"""Run the cases of occt_robustness.py against SMLib (NVIDIA USD BRep).

The cases, seeds and closed-form inside tests are the ones in
occt_robustness.py. Only the kernel calls are replaced.

Two differences from the OCCT run, both forced by what the Python API
offers:

  * SMLib exposes no point-in-solid query. A point is classified by the
    winding number of SMLib's own tessellation of the result (chord
    height 3e-3 mm, inside the 1e-2 mm band of unused points), which is independent of how the solid was built.
  * SMLib exposes no general validity checker, so "invalid" here means
    the result is not a closed manifold solid, or could not be
    tessellated. OCCT's checker is stricter.

SMLib's booleans take no tolerance argument, so only the cases with
fuzzy value 0 are run.

Usage:
    uv run smlib_robustness.py --out results.jsonl [--jobs 4]
    uv run smlib_robustness.py --summarise results.jsonl
"""
import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import occt_robustness as m  # noqa: E402  (pure Python at import time)


RECYCLE = 15


def _u():
    import usd_brep
    return usd_brep


def build(kind, fr, p, *dims):
    u = _u()
    p = tuple(float(x) for x in p)
    mk = {"box": u.create_box, "cyl": u.create_cylinder, "sph": u.create_sphere,
          "cone": u.create_cone, "torus": u.create_torus}[kind]
    b = mk(p, *[float(d) for d in dims])
    # Primitives are made in the case's local frame, then placed: global = o + R * local.
    x = tuple(fr.R[i][0] for i in range(3))
    y = tuple(fr.R[i][1] for i in range(3))
    u.transform(b, u.Axis2Placement(tuple(fr.o), x, y))
    return b


def volume(shape):
    return _u().compute_volume(shape, 1e-6) if shape.face_count() else 0.0


def valid(shape):
    return shape.face_count() == 0 or bool(shape.is_manifold_solid())


def bbox(shape):
    (x0, y0, z0), (x1, y1, z1) = shape.bounding_box()
    return x0, y0, z0, x1, y1, z1


def has_solid(shape):
    return shape.face_count() > 0


_mesh_cache = {}


def _mesh(shape):
    key = id(shape)
    if key not in _mesh_cache:
        _mesh_cache.clear()
        t = _u().tessellate(shape, chord_height_tolerance=3e-3)
        a = t.to_numpy_arrays()
        pts = np.asarray(a["points"], dtype=np.float64)
        f = np.asarray(a["faces"]).reshape(-1, 4)
        if not (f[:, 0] == 3).all():
            raise RuntimeError("tessellation returned non-triangles")
        _mesh_cache[key] = (shape, pts[f[:, 1]], pts[f[:, 2]], pts[f[:, 3]])
    return _mesh_cache[key][1:]


def inside(shape, g):
    """Generalised winding number of the tessellated boundary about g.
    Near 1 inside, near 0 outside. None when it is neither."""
    A, B, C = _mesh(shape)
    q = np.asarray(g, dtype=np.float64)
    total = 0.0
    for i in range(0, len(A), 200_000):      # in blocks, to bound memory on fine meshes
        a, b, c = A[i:i + 200_000] - q, B[i:i + 200_000] - q, C[i:i + 200_000] - q
        la, lb, lc = (np.linalg.norm(v, axis=1) for v in (a, b, c))
        num = np.einsum("ij,ij->i", a, np.cross(b, c))
        den = la * lb * lc + np.einsum("ij,ij->i", a, b) * lc + np.einsum("ij,ij->i", b, c) * la + np.einsum("ij,ij->i", c, a) * lb
        total += float(np.arctan2(num, den).sum())
    w = abs(total / (2 * math.pi))
    return True if abs(w - 1) < 0.1 else False if w < 0.1 else None


def boolean(op, A, B, fuzzy):
    import time
    u = _u()
    f = {"fuse": u.boolean_union, "cut": u.boolean_difference, "common": u.boolean_intersection}[op]
    t = time.perf_counter()
    out = {"status": "ok"}
    try:
        s = f(u.brep_copy(A), u.brep_copy(B))   # the operation consumes its inputs
        out["shape"] = s
        out["vol"] = volume(s)
        if not valid(s):
            out["status"] = "invalid"
        elif has_solid(s):
            _mesh(s)                              # a result that cannot be tessellated is not usable
    except Exception as e:
        m.reraise_unless_kernel(e)
        out["status"] = "error"
        out["exc"] = type(e).__name__
        out.setdefault("vol", 0.0)
    out["ms"] = round((time.perf_counter() - t) * 1e3, 2)
    return out


def reraise_unless_kernel(e):
    """The binding reports kernel failures as RuntimeError."""
    if not isinstance(e, RuntimeError):
        raise e


def sharp_edges(shape):
    """Edges where two different faces meet at more than 5 degrees."""
    out = []
    for e in shape.edges():
        fs = e.faces()
        if len(fs) != 2:
            continue
        t0, t1 = e.parameter_range()
        angles = []
        for t in (0.1, 0.5, 0.9):
            pt = e.point_at(t0 + t * (t1 - t0))
            ns = []
            for f in fs:
                uv = _u().surface_closest_point(f.surface(), pt)[1][0]
                uv = (uv.x, uv.y) if hasattr(uv, "x") else (uv[0], uv[1])
                ns.append(f.outward_normal_at_uv(uv[0], uv[1]))
            dot = max(-1.0, min(1.0, sum(a * b for a, b in zip(*ns))))
            angles.append(math.degrees(math.acos(dot)))
        if min(angles) < 5.0:
            continue
        length = e.length()
        if length > 1e-6:
            out.append((e, length, min(angles), max(angles)))
    return out


def fillet(shape, edges, radius):
    u = _u()
    try:
        u.fillet_edges(shape, [x[0] for x in edges], radius=float(radius))   # in place
        if not valid(shape):
            return "invalid"
        _mesh(shape)
        return "ok"
    except Exception as e:
        m.reraise_unless_kernel(e)
        return "error"


for name in ("build", "volume", "valid", "bbox", "has_solid", "inside", "boolean",
             "reraise_unless_kernel", "sharp_edges", "fillet"):
    setattr(m, name, globals()[name])
m.FUZZY = [0.0]

_all_cases = m.case_list


def case_list():
    """The same ids as the OCCT run, keeping only the cases with fuzzy value 0."""
    return [c for c in _all_cases() if c.get("fuzzy", 0.0) == 0.0]


if __name__ == "__main__":
    import argparse
    import json
    import subprocess
    import time
    ap = argparse.ArgumentParser()
    ap.add_argument("--out")
    ap.add_argument("--jobs", type=int, default=os.cpu_count() or 1)
    ap.add_argument("--stall", type=float, default=180.0)
    ap.add_argument("--kinds", default="near,generic,fillet,chain")
    ap.add_argument("--resume", action="store_true", help="keep existing part files and continue")
    ap.add_argument("--summarise")
    ap.add_argument("--worker", nargs=3)
    a = ap.parse_args()
    kinds = set(a.kinds.split(","))
    cases = [c for c in case_list() if c["kind"] in kinds]
    if a.summarise:
        m.case_list = _all_cases
        m.summarise(a.summarise)
    elif a.worker:
        off, step, out = int(a.worker[0]), int(a.worker[1]), a.worker[2]
        done = set()
        if os.path.exists(out):
            for line in open(out):
                d = json.loads(line)
                if "begin" not in d:
                    done.add(d.get("lost", d.get("case", {}).get("id")))
        ran = 0
        with open(out, "a") as f:
            for c in cases[off::step]:
                if c["id"] in done:
                    continue
                if ran == RECYCLE:           # SMLib's memory use grows with every case; start a fresh process
                    sys.exit(4)
                ran += 1
                f.write(json.dumps({"begin": c["id"]}) + "\n")
                f.flush()
                try:
                    res = (m.run_fillet_case(c) if c["kind"] == "fillet" else
                           m.run_chain_case(c) if c["kind"] == "chain" else m.run_boolean_case(c))
                except Exception as e:      # a bug in this script, not a kernel failure
                    f.write(json.dumps({"harness_error": c["id"], "exc": repr(e)}) + "\n")
                    f.flush()
                    sys.exit(3)
                f.write(json.dumps({"case": c, "res": res}) + "\n")
                f.flush()
    else:
        # A worker that dies or stalls is restarted; it skips every case already begun,
        # and the case it was on is recorded as lost.
        parts = [f"{a.out}.part{j}" for j in range(a.jobs)]
        for p in parts:
            if os.path.exists(p) and not a.resume:
                os.remove(p)
        procs, seen, finished = [None] * a.jobs, [None] * a.jobs, [False] * a.jobs
        retried = set()
        while not all(finished):
            for j in range(a.jobs):
                if finished[j]:
                    continue
                if procs[j] is None:
                    procs[j] = subprocess.Popen([sys.executable, __file__, "--kinds", a.kinds, "--worker", str(j), str(a.jobs), parts[j]],
                                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    seen[j] = (-1, time.time())
                size = os.path.getsize(parts[j]) if os.path.exists(parts[j]) else 0
                if size != seen[j][0]:
                    seen[j] = (size, time.time())
                rc = procs[j].poll()
                stalled = rc is None and time.time() - seen[j][1] > a.stall
                if stalled:
                    procs[j].kill()
                    procs[j].wait()
                if rc == 3:
                    raise SystemExit(f"harness error, see {parts[j]}")
                if rc == 0:
                    finished[j] = True
                elif rc == 4:
                    procs[j] = None
                elif rc is not None or stalled:
                    begun, closed = None, set()
                    for line in open(parts[j]):
                        d = json.loads(line)
                        if "begin" in d:
                            begun = d["begin"]
                        else:
                            closed.add(d.get("lost", d.get("case", {}).get("id")))
                    if rc == -9 and begun not in retried:
                        retried.add(begun)   # killed from outside, usually for memory: try the case once more
                    elif begun is not None and begun not in closed:
                        with open(parts[j], "a") as f:
                            f.write(json.dumps({"lost": begun, "why": "timeout" if stalled else f"crash rc={rc}"}) + "\n")
                    procs[j] = None
            time.sleep(0.5)
        with open(a.out, "w") as o:
            for p in parts:
                for line in open(p):
                    if '"begin"' not in line:
                        o.write(line)
                os.remove(p)
