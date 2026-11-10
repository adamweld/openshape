# Kernel robustness instruments

Measurement tools written for phase 2. They are research instruments, not product code. Results and method are in [../02-measurements.md](../02-measurements.md); what remains to run is in [HANDOFF.md](HANDOFF.md).

## Files

| File | What it does |
|---|---|
| `occt_robustness.py` | The cases, the closed-form ground truth and the scoring. Runs them on OCCT. Every other adapter imports it |
| `bench_driver.py` | Runs cases in worker subprocesses so a crash, hang or memory blow-up is charged to one case |
| `occt_paired.py` | OCCT on the reduced case list the other adapters use, for case-by-case comparison |
| `smlib_robustness.py` | Adapter for SMLib (NVIDIA USD BRep) |
| `solidcore_robustness.py` | Adapter for solidcore. **Never run** |
| `solidcore_server/` | A small Rust program the solidcore adapter talks to. **Never compiled** |
| `occt_ssi_runner.py` | Lets the public [SSI corpus](https://github.com/jyviko/ssi-corpus) score OCCT's surface intersection |
| `quiddity_eval.py` | Generates STEP parts with known features, for checking a feature recogniser |
| `results/` | Raw outputs of every completed run |

## How a kernel is plugged in

An adapter replaces ten functions in `occt_robustness` and calls the shared driver:

| Function | Purpose |
|---|---|
| `build(kind, frame, position, *dims)` | Make a box, cylinder, sphere, cone or torus, placed in space |
| `boolean(op, a, b, fuzzy)` | Union, subtraction or intersection; returns status, result and volume |
| `volume(shape)`, `bbox(shape)` | Measures |
| `valid(shape)` | The kernel's own validity check |
| `has_solid(shape)` | Whether the result is non-empty |
| `inside(shape, point)` | Point classification against a result: true, false, or undecided |
| `sharp_edges(shape)` | Edges where two faces meet at more than 5 degrees, with length and angle |
| `fillet(shape, edges, radius)` | Round those edges |
| `reraise_unless_kernel(exception)` | Says which exceptions are the kernel's; anything else stops the run |

`smlib_robustness.py` is the shortest complete example.

## Rules these instruments follow

1. Ground truth comes from closed forms, never from another kernel.
2. The inside test of every adapter is validated on the input primitives before any result is recorded.
3. Only exceptions raised by the kernel count as kernel errors.
4. A worker killed from outside is retried once before its case counts as lost.
5. Cases whose exact answer is not a valid solid are not scored as pass or fail.

## Known limits

- Analytic primitives only. No freeform surfaces.
- Fillet failure rates are upper bounds: the existence of each fillet is not proved.
- About 150 sample points per result, so a defect below roughly 1% of the sampled volume can be missed.
- The near-degenerate family `cyl_tangent_inside` is ill-posed at offsets below a kernel's tolerance and should be read separately, as the write-up does.
