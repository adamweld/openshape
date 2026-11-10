# Phase 2: Open-source landscape and gaps

Status: **in progress**. Scope and exit criteria are in [ROADMAP.md](../../ROADMAP.md).

| # | Topic | Document | Status |
|---|---|---|---|
| 1 | What exists: kernels, solvers, applications, analysis, formats, datasets | [01-landscape.md](01-landscape.md) | Written from project documentation; no code read yet |
| 2 | Measuring OCCT's robustness | 02-occt-measurement.md | Benchmark written and running; results not yet recorded |
| 3 | Reuse-or-write verdict per component | 03-verdicts.md | Not written; waits on topic 2 and on an owner decision |

The benchmark is in [bench/](bench/). It is a measurement instrument, not product code.

## Headline so far

Three things changed in October 2026 that the project's starting assumptions did not anticipate. They are set out in [01-landscape.md](01-landscape.md):

1. NVIDIA published the commercial SMLib kernel as open source under Apache-2.0.
2. SolidCraft, an Apache-2.0 parametric CAD application in pure Rust with a headless CLI and MCP server, launched and is developing quickly. Its kernel has a published design for certified geometry.
3. Several other from-scratch Rust B-rep kernels were started during 2026.

These bear directly on [decision 0004](../../decisions/0004-ground-up-kernel.md) and need an owner decision before the verdicts can be written.
