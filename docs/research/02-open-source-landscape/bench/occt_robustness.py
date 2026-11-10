# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
# /// script
# requires-python = ">=3.11"
# dependencies = ["cadquery-ocp==8.0.1.1.0"]
# ///
"""Measure OCCT boolean and fillet failure rates on generated cases.

This is a research instrument, not part of the product. It needs no
second kernel as an oracle. Every input solid is an analytic primitive,
so whether a point lies inside it is known in closed form. For each
boolean result, sample points are classified by OCCT against the result
and compared with the closed-form answer for A | B, A - B and A & B.
Points within a small band of either input's boundary are not used.
OCCT's own validity checker is also run on every result. The volume
identities V(A | B) + V(A & B) = V(A) + V(B) and V(A - B) = V(A) -
V(A & B) are recorded as residuals but not used to judge a result,
because OCCT's volume integration on curved trimmed faces is itself
only accurate to a few parts in ten thousand.

Every case is generated from a seed, so a run is reproducible.

Usage:
    uv run occt_robustness.py --out results.jsonl [--jobs 4]
    uv run occt_robustness.py --summarise results.jsonl
"""
import argparse, json, math, os, random, subprocess, sys, time

# ----------------------------------------------------------------- cases

EPS = [0.0] + [s * 10.0 ** e for e in range(-9, -2) for s in (1, -1)]
NEAR_FAMILIES = ["stacked", "flush_side", "cyl_tangent_inside", "coaxial_cyl",
                 "sphere_tangent", "cyl_on_edge", "identical"]
NEAR_REPS = 20
GENERIC_PAIRS = 2000
FILLET_CASES = 3000
FUZZY = [0.0, 1e-6]
FILLET_FRACTIONS = [0.02, 0.05, 0.15]
FILLET_MODES = ["one_edge", "all_edges"]


def case_list():
    cases = []
    for fam in NEAR_FAMILIES:
        for eps in EPS:
            for rep in range(NEAR_REPS):
                for fz in FUZZY:
                    cases.append({"kind": "near", "family": fam, "eps": eps,
                                  "rep": rep, "fuzzy": fz})
    for i in range(GENERIC_PAIRS):
        cases.append({"kind": "generic", "rep": i, "fuzzy": 0.0})
    for i in range(FILLET_CASES):
        cases.append({"kind": "fillet", "rep": i,
                      "frac": FILLET_FRACTIONS[i % len(FILLET_FRACTIONS)],
                      "mode": FILLET_MODES[(i // len(FILLET_FRACTIONS)) % 2]})
    for n, c in enumerate(cases):
        c["id"] = n
    return cases


# ------------------------------------------------------------ geometry

def _rot(rng):
    """Uniform random rotation matrix (from a random unit quaternion)."""
    while True:
        q = [rng.gauss(0, 1) for _ in range(4)]
        n = math.sqrt(sum(x * x for x in q))
        if n > 1e-6:
            break
    w, x, y, z = (v / n for v in q)
    return [[1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
            [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
            [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)]]


class Frame:
    """A rigid frame. Local coordinates are mapped to global ones in plain
    floating point, so that exact local coincidences become coincidences up
    to rounding, as they are in real models."""

    def __init__(self, rng, identity=False):
        if identity:
            self.R = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
            self.o = [0.0, 0.0, 0.0]
        else:
            self.R = _rot(rng)
            self.o = [rng.uniform(-200, 200) for _ in range(3)]

    def pt(self, p):
        return [self.o[i] + sum(self.R[i][j] * p[j] for j in range(3)) for i in range(3)]

    def vec(self, v):
        return [sum(self.R[i][j] * v[j] for j in range(3)) for i in range(3)]

    def local(self, g):
        d = [g[i] - self.o[i] for i in range(3)]
        return [sum(self.R[i][j] * d[i] for i in range(3)) for j in range(3)]

    def ax2(self, p, z=(0, 0, 1), x=(1, 0, 0)):
        from OCP.gp import gp_Ax2, gp_Pnt, gp_Dir
        return gp_Ax2(gp_Pnt(*self.pt(p)), gp_Dir(*self.vec(z)), gp_Dir(*self.vec(x)))


class Solid:
    """An OCCT shape together with a closed-form inside test. margin(g) is
    positive inside, negative outside, and its size is about the distance
    to the boundary."""

    def __init__(self, shape, margin):
        self.shape, self.margin = shape, margin


def box(fr, p, d):
    from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox
    def margin(g):
        q = fr.local(g)
        return min(min(q[i] - p[i], p[i] + d[i] - q[i]) for i in range(3))
    return Solid(BRepPrimAPI_MakeBox(fr.ax2(p), *d).Shape(), margin)


def cyl(fr, p, r, h):
    from OCP.BRepPrimAPI import BRepPrimAPI_MakeCylinder
    def margin(g):
        q = fr.local(g)
        rho = math.hypot(q[0] - p[0], q[1] - p[1])
        return min(r - rho, q[2] - p[2], p[2] + h - q[2])
    return Solid(BRepPrimAPI_MakeCylinder(fr.ax2(p), r, h).Shape(), margin)


def sph(fr, p, r):
    from OCP.BRepPrimAPI import BRepPrimAPI_MakeSphere
    def margin(g):
        q = fr.local(g)
        return r - math.dist(q, p)
    return Solid(BRepPrimAPI_MakeSphere(fr.ax2(p), r).Shape(), margin)


def cone(fr, p, r1, r2, h):
    from OCP.BRepPrimAPI import BRepPrimAPI_MakeCone
    k = math.cos(math.atan2(abs(r1 - r2), h))
    def margin(g):
        q = fr.local(g)
        z = q[2] - p[2]
        rho = math.hypot(q[0] - p[0], q[1] - p[1])
        return min((r1 + (r2 - r1) * z / h - rho) * k, z, h - z)
    return Solid(BRepPrimAPI_MakeCone(fr.ax2(p), r1, r2, h).Shape(), margin)


def torus(fr, p, r1, r2):
    from OCP.BRepPrimAPI import BRepPrimAPI_MakeTorus
    def margin(g):
        q = fr.local(g)
        rho = math.hypot(q[0] - p[0], q[1] - p[1])
        return r2 - math.hypot(rho - r1, q[2] - p[2])
    return Solid(BRepPrimAPI_MakeTorus(fr.ax2(p), r1, r2).Shape(), margin)


def near_pair(family, eps, rng):
    """Two solids in a configuration that is degenerate at eps = 0."""
    fr = Frame(rng)
    ax, ay, az = (rng.uniform(20, 60) for _ in range(3))
    A = box(fr, (0, 0, 0), (ax, ay, az))
    if family == "stacked":            # B rests on A's top face
        B = box(fr, (ax * 0.3, ay * 0.2, az + eps), (ax, ay, rng.uniform(10, 30)))
    elif family == "flush_side":       # B overlaps A, one side face coplanar
        B = box(fr, (eps, ay * 0.4, az * 0.5), (ax * 0.6, ay, az))
    elif family == "cyl_tangent_inside":  # hole tangent to a side face
        r = min(ax, ay) * rng.uniform(0.1, 0.3)
        B = cyl(fr, (r + eps, ay * 0.5, -5.0), r, az + 10.0)
    elif family == "coaxial_cyl":      # equal-radius coaxial cylinders
        r = rng.uniform(5, 20)
        A = cyl(fr, (0, 0, 0), r, az)
        B = cyl(fr, (0, 0, az * 0.5), r + eps, az)
    elif family == "sphere_tangent":   # sphere touching the top face
        r = rng.uniform(5, 20)
        B = sph(fr, (ax * 0.5, ay * 0.5, az + r + eps), r)
    elif family == "cyl_on_edge":      # cylinder axis along a box edge
        r = min(ax, ay) * rng.uniform(0.1, 0.4)
        B = cyl(fr, (eps, 0.0, 0.0), r, az)
    elif family == "identical":        # the same box built twice
        B = box(fr, (0, 0, 0), (ax + eps, ay, az))
    else:
        raise ValueError(family)
    return A, B


def random_prim(rng, centre_spread):
    fr = Frame(rng)
    fr.o = [rng.uniform(-centre_spread, centre_spread) for _ in range(3)]
    k = rng.choice(["box", "cyl", "sph", "cone", "torus"])
    s = rng.uniform(10, 40)
    if k == "box":
        d = [rng.uniform(0.5, 1.5) * s for _ in range(3)]
        return box(fr, [-x / 2 for x in d], d)
    if k == "cyl":
        h = rng.uniform(0.5, 2) * s
        return cyl(fr, (0, 0, -h / 2), 0.5 * s, h)
    if k == "sph":
        return sph(fr, (0, 0, 0), 0.6 * s)
    if k == "cone":
        h = rng.uniform(0.5, 2) * s
        return cone(fr, (0, 0, -h / 2), 0.6 * s, rng.uniform(0, 0.4) * s, h)
    return torus(fr, (0, 0, 0), 0.6 * s, rng.uniform(0.1, 0.25) * s)


# ---------------------------------------------------------- measurement

def volume(shape):
    from OCP.GProp import GProp_GProps
    from OCP.BRepGProp import BRepGProp
    g = GProp_GProps()
    BRepGProp.VolumeProperties_s(shape, g)
    return g.Mass()


def valid(shape):
    from OCP.BRepCheck import BRepCheck_Analyzer
    return bool(BRepCheck_Analyzer(shape).IsValid())


def boolean(op, A, B, fuzzy):
    from OCP.BRepAlgoAPI import BRepAlgoAPI_Fuse, BRepAlgoAPI_Cut, BRepAlgoAPI_Common
    from OCP.collections import List_TopoDS_Shape
    from OCP.Standard import Standard_Failure
    cls = {"fuse": BRepAlgoAPI_Fuse, "cut": BRepAlgoAPI_Cut, "common": BRepAlgoAPI_Common}[op]
    t = time.perf_counter()
    out = {"status": "ok"}
    try:
        b = cls()
        la, lb = List_TopoDS_Shape(), List_TopoDS_Shape()
        la.Append(A)
        lb.Append(B)
        b.SetArguments(la)
        b.SetTools(lb)
        if fuzzy > 0:
            b.SetFuzzyValue(fuzzy)
        b.Build()
        if not b.IsDone():
            out["status"] = "error"
        else:
            s = b.Shape()
            out["shape"] = s
            out["vol"] = volume(s)
            if not valid(s):
                out["status"] = "invalid"
    except Standard_Failure as e:  # kernel exceptions only; harness bugs must propagate
        out["status"] = "error"
        out["exc"] = type(e).__name__
    out["ms"] = round((time.perf_counter() - t) * 1e3, 2)
    return out


BAND = 1e-2          # mm; sample points nearer than this to an input boundary are skipped
SAMPLES = 150


def sample_points(rng, A, B):
    """Points in the bounding boxes of A and B, half each."""
    from OCP.Bnd import Bnd_Box
    from OCP.BRepBndLib import BRepBndLib
    pts = []
    for S in (A, B):
        bb = Bnd_Box()
        BRepBndLib.Add_s(S.shape, bb)
        lo, hi = bb.CornerMin(), bb.CornerMax()
        x0, y0, z0, x1, y1, z1 = lo.X(), lo.Y(), lo.Z(), hi.X(), hi.Y(), hi.Z()
        for _ in range(SAMPLES // 2):
            pts.append((rng.uniform(x0, x1), rng.uniform(y0, y1), rng.uniform(z0, z1)))
    return pts


def inside(shape, g):
    """OCCT's own point classification against a result. None means the
    point was reported as on the boundary."""
    from OCP.BRepClass3d import BRepClass3d_SolidClassifier
    from OCP.gp import gp_Pnt
    from OCP.TopAbs import TopAbs_IN, TopAbs_OUT
    st = BRepClass3d_SolidClassifier(shape, gp_Pnt(*g), 1e-7).State()
    return True if st == TopAbs_IN else False if st == TopAbs_OUT else None


def has_solid(shape):
    from OCP.TopExp import TopExp_Explorer
    from OCP.TopAbs import TopAbs_SOLID
    return TopExp_Explorer(shape, TopAbs_SOLID).More()


def run_boolean_case(c):
    from OCP.Standard import Standard_Failure
    rng = random.Random(1_000_003 * c["id"] + 17)
    if c["kind"] == "near":
        A, B = near_pair(c["family"], c["eps"], rng)
    else:
        A, B = random_prim(rng, 0), random_prim(rng, 25)
    va, vb = volume(A.shape), volume(B.shape)
    r = {"va": va, "vb": vb}
    res = {op: boolean(op, A.shape, B.shape, c.get("fuzzy", 0.0)) for op in ("fuse", "cut", "common")}
    pts = [(g, A.margin(g), B.margin(g)) for g in sample_points(rng, A, B)]
    pts = [(g, ma > 0, mb > 0) for g, ma, mb in pts if abs(ma) > BAND and abs(mb) > BAND]
    r["n_pts"] = len(pts)
    expect = {"fuse": lambda a, b: a or b, "cut": lambda a, b: a and not b, "common": lambda a, b: a and b}
    for op, x in res.items():
        shape = x.pop("shape", None)
        if shape is not None:
            miss = 0
            solid = has_solid(shape)
            for g, a, b in pts:
                want = expect[op](a, b)
                try:
                    got = inside(shape, g) if solid else False
                except Standard_Failure:
                    got = None
                if got is not None and got != want:
                    miss += 1
            x["miss"] = miss
            if miss and x["status"] == "ok":
                x["status"] = "wrong"
        r[op] = x
    f, k, m = r["fuse"], r["cut"], r["common"]
    if all("vol" in x for x in (f, k, m)):
        r["res_union"] = f["vol"] + m["vol"] - va - vb
        r["res_cut"] = k["vol"] - va + m["vol"]
    r["overlap"] = any(a and b for _, a, b in pts)
    return r


def sharp_edges(shape):
    """Edges where two different faces meet at an angle. Seams, degenerate
    edges and smooth joins are excluded: they are not edges a designer
    could ask to fillet."""
    from OCP.TopExp import TopExp
    from OCP.TopAbs import TopAbs_EDGE, TopAbs_FACE
    from OCP.TopoDS import TopoDS
    from OCP.BRep import BRep_Tool
    from OCP.BRepAdaptor import BRepAdaptor_Surface
    from OCP.BRepLProp import BRepLProp_SLProps
    from OCP.GProp import GProp_GProps
    from OCP.BRepGProp import BRepGProp
    from OCP.gp import gp_Pnt2d
    from OCP.TopAbs import TopAbs_REVERSED
    from OCP.collections import IndexedDataMap_TopoDS_Shape_List_TopoDS_Shape_TopTools_ShapeMapHasher as AncMap
    m = AncMap()
    TopExp.MapShapesAndAncestors_s(shape, TopAbs_EDGE, TopAbs_FACE, m)
    out = []
    for i in range(1, m.Extent() + 1):
        e = TopoDS.Edge(m.FindKey(i))
        faces = [TopoDS.Face(f) for f in m.FindFromIndex(i)]
        if BRep_Tool.Degenerated_s(e) or len(faces) != 2 or faces[0].IsSame(faces[1]):
            continue
        # Angle between the two face normals at three points along the edge.
        # 0 degrees is a smooth join, 90 a square corner, 180 a knife edge.
        angles = []
        for t in (0.1, 0.5, 0.9):
            normals = []
            for f in faces:
                c2d = BRep_Tool.CurveOnSurface_s(e, f, 0.0, 0.0)
                uv = c2d.Value(c2d.FirstParameter() + t * (c2d.LastParameter() - c2d.FirstParameter()))
                pr = BRepLProp_SLProps(BRepAdaptor_Surface(f), uv.X(), uv.Y(), 1, 1e-9)
                if not pr.IsNormalDefined():
                    break
                n = pr.Normal()
                sgn = -1.0 if f.Orientation() == TopAbs_REVERSED else 1.0
                normals.append((sgn * n.X(), sgn * n.Y(), sgn * n.Z()))
            if len(normals) != 2:
                angles = None
                break
            dot = max(-1.0, min(1.0, sum(a * b for a, b in zip(*normals))))
            angles.append(math.degrees(math.acos(dot)))
        if angles is None or min(angles) < 5.0:   # undefined, or smooth to within 5 degrees
            continue
        g = GProp_GProps()
        BRepGProp.LinearProperties_s(e, g)
        if g.Mass() > 1e-6:
            out.append((e, g.Mass(), min(angles), max(angles)))
    return out


def run_fillet_case(c):
    """Fillet sharp edges of a solid with a small radius. The radius is a
    small fraction of the shortest sharp edge, so a fillet should nearly
    always exist geometrically; the reported rate is still an upper bound
    on kernel failure, because existence is not proved case by case."""
    from OCP.BRepFilletAPI import BRepFilletAPI_MakeFillet
    from OCP.Standard import Standard_Failure
    rng = random.Random(2_000_003 * c["id"] + 29)
    A = random_prim(rng, 0).shape
    base, how = A, "primitive"
    if rng.random() < 0.75:
        B = random_prim(rng, 20).shape
        op = rng.choice(["fuse", "cut", "common"])
        from OCP.BRepAlgoAPI import BRepAlgoAPI_Fuse, BRepAlgoAPI_Cut, BRepAlgoAPI_Common
        b = {"fuse": BRepAlgoAPI_Fuse, "cut": BRepAlgoAPI_Cut, "common": BRepAlgoAPI_Common}[op](A, B)
        if b.IsDone() and valid(b.Shape()) and volume(b.Shape()) > 1.0 \
                and abs(volume(b.Shape()) - volume(A)) > 1e-6 * volume(A):
            base, how = b.Shape(), op
    edges = sharp_edges(base)
    r = {"base": how, "n_sharp": len(edges), "mode": c["mode"]}
    if not edges:
        r["status"] = "skipped"
        return r
    radius = c["frac"] * min(x[1] for x in edges)
    chosen = [rng.choice(edges)] if c["mode"] == "one_edge" else edges
    r["radius"] = radius
    r["ang_min"] = round(min(x[2] for x in chosen), 2)
    r["ang_max"] = round(max(x[3] for x in chosen), 2)
    t = time.perf_counter()
    try:
        mk = BRepFilletAPI_MakeFillet(base)
        for x in chosen:
            mk.Add(radius, x[0])
        mk.Build()
        if not mk.IsDone():
            r["status"] = "error"
        else:
            s = mk.Shape()
            r["status"] = "ok" if valid(s) else "invalid"
    except Standard_Failure as e:
        r["status"] = "error"
        r["exc"] = type(e).__name__
    r["ms"] = round((time.perf_counter() - t) * 1e3, 2)
    return r


# ------------------------------------------------- crash-proof execution

def worker(lo, hi, step, offset, out):
    cases = case_list()
    with open(out, "a") as f:
        for c in cases[lo:hi]:
            if c["id"] % step != offset:
                continue
            f.write(json.dumps({"begin": c["id"]}) + "\n")
            f.flush()
            try:
                res = run_fillet_case(c) if c["kind"] == "fillet" else run_boolean_case(c)
            except Exception as e:  # a bug in this script, not a kernel failure
                f.write(json.dumps({"harness_error": c["id"], "exc": repr(e)}) + "\n")
                f.flush()
                sys.exit(3)
            f.write(json.dumps({"case": c, "res": res}) + "\n")
            f.flush()


def last_begun(path):
    done, begun = set(), None
    if os.path.exists(path):
        for line in open(path):
            d = json.loads(line)
            if "begin" in d:
                begun = d["begin"]
            elif "case" in d:
                done.add(d["case"]["id"])
            elif "lost" in d:
                done.add(d["lost"])
    return done, begun


def drive(out, jobs, stall_s):
    """Run workers as subprocesses. If one crashes or stalls inside the
    kernel, record the case it was on and restart after it."""
    n = len(case_list())
    parts = [f"{out}.part{j}" for j in range(jobs)]
    for p in parts:
        if os.path.exists(p):
            os.remove(p)
    lo = [0] * jobs
    procs = [None] * jobs
    seen = [(0, time.time())] * jobs
    while True:
        alive = False
        for j in range(jobs):
            p = procs[j]
            if p is None and lo[j] < n:
                procs[j] = subprocess.Popen(
                    [sys.executable, __file__, "--worker", str(lo[j]), str(n), str(jobs), str(j), parts[j]],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                seen[j] = (os.path.getsize(parts[j]) if os.path.exists(parts[j]) else 0, time.time())
                alive = True
                continue
            if p is None:
                continue
            size = os.path.getsize(parts[j]) if os.path.exists(parts[j]) else 0
            if size != seen[j][0]:
                seen[j] = (size, time.time())
            rc = p.poll()
            stalled = rc is None and time.time() - seen[j][1] > stall_s
            if stalled:
                p.kill()
                p.wait()
            if rc == 3:
                for q in procs:
                    if q is not None and q.poll() is None:
                        q.kill()
                raise SystemExit(f"harness error, see {parts[j]}")
            if rc is not None or stalled:
                done, begun = last_begun(parts[j])
                if rc == 0 and not stalled:
                    lo[j] = n
                else:
                    if begun is not None and begun not in done:
                        with open(parts[j], "a") as f:
                            f.write(json.dumps({"lost": begun, "why": "timeout" if stalled else f"crash rc={rc}"}) + "\n")
                        lo[j] = begun + 1
                    else:
                        lo[j] = (begun + 1) if begun is not None else n
                procs[j] = None
                alive = alive or lo[j] < n
            else:
                alive = True
        if not alive:
            break
        time.sleep(0.5)
    with open(out, "w") as o:
        for p in parts:
            for line in open(p):
                if '"begin"' not in line:
                    o.write(line)
            os.remove(p)


# ---------------------------------------------------------------- report

def summarise(path):
    cases = {c["id"]: c for c in case_list()}
    rows, lost = [], {}
    for line in open(path):
        d = json.loads(line)
        if "lost" in d:
            lost[d["lost"]] = d["why"]
        else:
            rows.append(d)

    def pct(a, b):
        return f"{100 * a / b:.2f}%" if b else "n/a"

    def bool_stats(sel, label):
        rs = [r for r in rows if sel(r["case"])]
        ls = [i for i in lost if sel(cases[i])]
        ops = 3 * len(rs)
        err = sum(r["res"][o]["status"] == "error" for r in rs for o in ("fuse", "cut", "common"))
        inv = sum(r["res"][o]["status"] == "invalid" for r in rs for o in ("fuse", "cut", "common"))
        wrong = sum(r["res"][o]["status"] == "wrong" for r in rs for o in ("fuse", "cut", "common"))
        anybad = sum(any(r["res"][o]["status"] != "ok" for o in ("fuse", "cut", "common")) for r in rs)
        ms = sorted(r["res"][o]["ms"] for r in rs for o in ("fuse", "cut", "common"))
        med = ms[len(ms) // 2] if ms else 0
        p99 = ms[int(len(ms) * 0.99)] if ms else 0
        print(f"| {label} | {len(rs) + len(ls)} | {pct(err, ops)} | {pct(inv, ops)} | {pct(wrong, ops)} | {len(ls)} | {pct(anybad + len(ls), len(rs) + len(ls))} | {med:.1f} / {p99:.1f} |")

    hdr = "| Set | Pairs | Ops reporting error | Ops returning an invalid solid | Ops returning the wrong solid | Crashed or hung | Pairs with any failure | Time per op, median / p99 (ms) |\n|---|---|---|---|---|---|---|---|"
    print("### Booleans by set\n\n" + hdr)
    bool_stats(lambda c: c["kind"] == "generic", "Generic position")
    gen = [r for r in rows if r["case"]["kind"] == "generic"]
    ov = sum(bool(r["res"].get("overlap")) for r in gen)
    for fz in FUZZY:
        bool_stats(lambda c, fz=fz: c["kind"] == "near" and c["fuzzy"] == fz, f"Near-degenerate, fuzzy {fz:g}")
    for fz in FUZZY:
        print(f"\n### Near-degenerate by family, fuzzy {fz:g}\n\n" + hdr)
        for fam in NEAR_FAMILIES:
            bool_stats(lambda c, fam=fam, fz=fz: c["kind"] == "near" and c["family"] == fam and c["fuzzy"] == fz, fam)
        print(f"\n### Near-degenerate by offset magnitude, fuzzy {fz:g}\n\n" + hdr)
        for e in sorted({abs(x) for x in EPS}):
            bool_stats(lambda c, e=e, fz=fz: c["kind"] == "near" and abs(c["eps"]) == e and c["fuzzy"] == fz, f"{e:g}")

    print("\n### Fillets on sharp edges, small radius\n")
    print("| Edges filleted | Radius as fraction of shortest sharp edge | Cases | Error | Invalid result | Crashed or hung | Any failure | Median time (ms) |\n|---|---|---|---|---|---|---|---|")
    for mode in FILLET_MODES:
        for fr in FILLET_FRACTIONS:
            sel = lambda c: c["kind"] == "fillet" and c["frac"] == fr and c["mode"] == mode
            rs = [r for r in rows if sel(r["case"]) and r["res"]["status"] != "skipped"]
            ls = [i for i in lost if sel(cases[i])]
            e = sum(r["res"]["status"] == "error" for r in rs)
            v = sum(r["res"]["status"] == "invalid" for r in rs)
            ms = sorted(r["res"].get("ms", 0) for r in rs)
            n = len(rs) + len(ls)
            print(f"| {mode} | {fr} | {n} | {pct(e, n)} | {pct(v, n)} | {len(ls)} | {pct(e + v + len(ls), n)} | {ms[len(ms) // 2] if ms else 0:.1f} |")
    print("\n| Edges filleted | Base solid | Cases | Any failure |\n|---|---|---|---|")
    for mode in FILLET_MODES:
        for how in ("primitive", "fuse", "cut", "common"):
            rs = [r for r in rows if r["case"]["kind"] == "fillet" and r["case"]["mode"] == mode and r["res"].get("base") == how and r["res"]["status"] != "skipped"]
            bad = sum(r["res"]["status"] != "ok" for r in rs)
            print(f"| {mode} | {how} | {len(rs)} | {pct(bad, len(rs))} |")
    sk = sum(r["res"]["status"] == "skipped" for r in rows if r["case"]["kind"] == "fillet")
    print(f"\nFillet cases skipped because the solid had no sharp edge: {sk}")
    print(f"\nGeneric pairs whose solids overlap: {ov} of {len(gen)}")
    print("\n| Edges filleted | Face angle along the edges | Cases | Any failure |\n|---|---|---|---|")
    for mode in FILLET_MODES:
        for label, sel in (("all between 45 and 135 degrees", lambda x: x["ang_min"] >= 45 and x["ang_max"] <= 135),
                           ("some outside 45 to 135 degrees", lambda x: not (x["ang_min"] >= 45 and x["ang_max"] <= 135))):
            rs = [r for r in rows if r["case"]["kind"] == "fillet" and r["case"]["mode"] == mode and "ang_min" in r["res"] and sel(r["res"])]
            bad = sum(r["res"]["status"] != "ok" for r in rs)
            print(f"| {mode} | {label} | {len(rs)} | {pct(bad, len(rs))} |")
    print(f"\nTotal cases recorded: {len(rows)}; lost to crash or hang: {len(lost)}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out")
    ap.add_argument("--jobs", type=int, default=os.cpu_count() or 1)
    ap.add_argument("--stall", type=float, default=120.0)
    ap.add_argument("--summarise")
    ap.add_argument("--worker", nargs=5)
    a = ap.parse_args()
    if a.worker:
        lo, hi, step, off, out = a.worker
        worker(int(lo), int(hi), int(step), int(off), out)
    elif a.summarise:
        summarise(a.summarise)
    else:
        drive(a.out, a.jobs, a.stall)
