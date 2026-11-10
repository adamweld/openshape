# Phase 2: Open-source landscape and gaps

Status: **in progress**. Scope and exit criteria are in [ROADMAP.md](../../ROADMAP.md).

| # | Topic | Document | Status |
|---|---|---|---|
| 1 | What exists: kernels, solvers, applications, analysis, formats, datasets | [01-landscape.md](01-landscape.md) | Written from project documentation; no code read yet |
| 2 | Measurements: OCCT, SMLib, solidcore, quiddity, and the public surface-intersection corpus | [02-measurements.md](02-measurements.md) | OCCT, SMLib, quiddity and the intersection corpus final; solidcore handed off in [bench/HANDOFF.md](bench/HANDOFF.md) |
| 3 | Reuse-or-write verdict per component | [03-verdicts.md](03-verdicts.md) | Draft; waits on the remaining measurements and an owner decision |
| 4 | SolidCraft and SMLib in detail | [04-nearest-neighbours.md](04-nearest-neighbours.md) | Written from project documentation |

The benchmark is in [bench/](bench/). It is a measurement instrument, not product code.

## Headline so far

The measurements are summarised at the top of [03-verdicts.md](03-verdicts.md). In brief: OCCT's booleans are robust and its fillets and tangential intersection are weak; SMLib is the reverse on intersection and much weaker on chained booleans; solidcore is unmeasured.

Three things changed in October 2026 that the project's starting assumptions did not anticipate. They are set out in [01-landscape.md](01-landscape.md):

1. NVIDIA published the commercial SMLib kernel as open source under Apache-2.0.
2. SolidCraft, an Apache-2.0 parametric CAD application in pure Rust with a headless CLI and MCP server, launched and is developing quickly. Its kernel has a published design for certified geometry.
3. Several other from-scratch Rust B-rep kernels were started during 2026.

These bear directly on [decision 0004](../../decisions/0004-ground-up-kernel.md) and need an owner decision before the verdicts can be written.
