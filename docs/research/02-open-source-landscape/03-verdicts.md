# Reuse-or-write verdicts

Status: **draft, awaiting an owner decision.** The kernel verdict is a question of direction, not only of evidence, and is set out as options. Verdicts for other components are provisional recommendations.

Evidence is in [01-landscape.md](01-landscape.md), [02-measurements.md](02-measurements.md) and [04-nearest-neighbours.md](04-nearest-neighbours.md).

## The kernel

[Decision 0004](../../decisions/0004-ground-up-kernel.md) said to plan on writing the kernel from scratch, on the expectation that OCCT was the only open option and was well behind. Its revisit trigger is the end of this phase. Both halves of that expectation need restating.

**What the evidence now says**

1. OCCT is not the only option. A commercial-lineage kernel (SMLib) is available under Apache-2.0, and a Rust kernel derived from it (solidcore) is being developed in the open with a design that targets the weaknesses phase 1 found in Parasolid.
2. OCCT's booleans on analytic geometry are robust in direct measurement. Its fillets are not. Figures are in [02-measurements.md](02-measurements.md).
3. One published measurement exists for SMLib: it passes 81 of 119 cases on a public surface-intersection corpus, failing mostly at tangency. solidcore's new intersector is reported by its authors to pass 118. Neither has been measured independently, and neither has been measured on booleans or blends.
4. A from-scratch kernel is now a crowded activity, with one prominent failure (Fornjot) and several young projects.
5. The parts of OpenShape's vision that nobody is building are the intent model, the closed design, test and optimise loop, reconstruction of parametric models, and a kernel built as a high-throughput training environment.

**Options**

| | Option | What OpenShape builds | Main advantage | Main risk |
|---|---|---|---|---|
| A | Independent kernel, as planned | Everything, using SMLib and solidcore as openly readable references | Full control of the kernel's design: lineage, determinism, throughput, behaviour versioning | Years of work duplicating what others are doing in the open, before reaching the parts that are new |
| B | Build on an existing open kernel | The layers above the kernel, plus whatever the chosen kernel lacks, contributed or forked | Effort goes to what is unoccupied; a kernel exists on day one | Dependence on a young codebase and its maintainers; the kernel may not meet our requirements for throughput, determinism or lineage, and changing someone else's kernel is slower than designing one |
| C | Join SolidCraft | The closed-loop and intent work, inside or on top of that project | A working application, an agent interface and a community exist already | Loss of control over direction and standards; that project's pace and method may not fit the standard in [PRINCIPLES.md](../../PRINCIPLES.md) |

Under option B the candidates are:

| Kernel | For | Against |
|---|---|---|
| solidcore | Rust, Apache-2.0, deterministic and certified by design, built for agent-driven development, WebAssembly-capable | A month old; "integration remains in progress"; unmeasured; one organisation |
| SMLib (USD BRep) | Decades of commercial use; Apache-2.0; complete feature set | C++; not accepting contributions; documented crashes and sampling-based checks; a process-global context |
| OCCT | Mature and measured; active modernisation; large user base | LGPL-2.1, which the permissively licensed projects refuse to touch; weak fillets; limited lineage reporting, which is the root of FreeCAD's naming problem |
| truck | Rust, Apache-2.0, five years old | Limited blending; smaller scope |

**Recommendation, held until two measurements are in**

Option B is the better fit for the stated goal, which is to make AI-driven mechanical design work, if a candidate kernel is good enough. The project's distinctive value is in the loop and the intent model, and no evidence suggests a kernel written here would be better than solidcore's design direction within a comparable time.

That recommendation depends on facts not yet established:

- how SMLib and solidcore perform on the benchmark in [bench/](bench/), which needs the owner's approval to install them;
- whether a candidate can meet requirements that phase 1 derived and that OpenShape cannot compromise on. These are listed below.

If no candidate can meet those requirements, option A stands, and it stands on better ground than before, because the requirements will have been tested against real alternatives.

**Requirements a kernel must meet, from phase 1**

| Requirement | Why | Source |
|---|---|---|
| Uniform lineage for every operation, including splits and merges | Durable references, drawings, reconstruction | [08-parasolid-in-depth](../01-state-of-the-art/08-parasolid-in-depth.md) |
| Identical results at any thread count and on any machine | A model defined by text must rebuild identically | same |
| Every operation succeeds or leaves the model unchanged | Agents run many speculative operations | same |
| Failures return the entities, the location and where possible a value that would work | The loop needs magnitude and direction | [06-simulation-dfm](../01-state-of-the-art/06-simulation-dfm.md) |
| High throughput headless, with no crashes | The kernel is the training environment | [07-reverse-engineering](../01-state-of-the-art/07-reverse-engineering.md) |
| Fast inside-or-outside and distance queries | Meshless analysis, clearance and assembly checks | [06-simulation-dfm](../01-state-of-the-art/06-simulation-dfm.md) |
| Behaviour versioned per feature | Old models must keep rebuilding | [08-parasolid-in-depth](../01-state-of-the-art/08-parasolid-in-depth.md) |
| Exact hidden-line output traceable to source edges | Drawings | [09-drawings](../01-state-of-the-art/09-drawings.md) |

solidcore's documentation claims the second and third and part of the fourth. None has been verified.

## Other components

Provisional. Each becomes a decision record once the kernel direction is settled, because several depend on it.

| Component | Verdict | Reason |
|---|---|---|
| Constraint solver | Write, or adopt ezpz or SolidCraft's solver as a starting point | No open solver documents the decomposition approach of the commercial ones, and solver behaviour is where quality lies. The permissively licensed Rust solvers are small enough to study or extend. SolveSpace's is GPL and planegcs is LGPL |
| Feature recognition | Evaluate quiddity before writing anything | It does the recognition half of reconstruction, deterministically, under a compatible licence |
| Reconstruction of a feature tree | Write | Not found anywhere |
| Intent model: interfaces, loads, manufacturing method | Write, exporting to AP242 and AP209 where they overlap | Not found anywhere |
| Structural analysis | Reuse a finite element library (MFEM is BSD-licensed) behind our own geometry queries; investigate an immersed method | Solvers exist; the unreliable step in published loops is meshing, which an immersed method avoids |
| Tetrahedral meshing, where needed | Reuse fTetWild | Same licence as OpenShape, designed for robustness |
| Manufacturability and assembly checks | Write | Commercial rules are unpublished; nothing open was found |
| STEP import and export | Depends on the kernel | SMLib and SolidCraft each have their own; ruststep is inactive |
| Rendering | Reuse wgpu | Standard choice; SolidCraft does the same |
| Mesh booleans, for the later scan scope | Reuse Manifold | The reference implementation, permissively licensed |
| Drawings | Write | Depends on kernel hidden-line support; nothing reusable was identified |
| Agent interface | Write, taking SolidCraft's as the baseline to exceed | Theirs already covers schemas, transactions, assertions, structured topology and screenshots |

## What remains before this phase can close

- The owner's choice among options A, B and C, or a request for more evidence first.
- Approval to install and measure SMLib, and a build of solidcore to measure.
- A test of quiddity on real STEP files.
- Licence checks at source for the public datasets.
- Rebuild-performance measurement, which is carried from phase 1 and has not been started.
