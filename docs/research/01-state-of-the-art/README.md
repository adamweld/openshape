# Phase 1: State of the art

Status: **in progress**. Every topic has a first pass. None is complete: each document ends with the gaps that remain. Scope and exit criteria are in [ROADMAP.md](../../ROADMAP.md).

## Evidence grades

Every claim in this folder carries one of these marks, because most of the systems studied are closed-source.

| Mark | Meaning |
|---|---|
| **[P]** | Primary source read in full: vendor documentation, an engineering post by the vendor, or the paper itself |
| **[S]** | Secondary source, or a primary source seen only through a search summary and not yet read |
| **[U]** | Unverified: general knowledge or inference, no source checked yet |

A vendor's description of its own product is evidence of what the vendor says, not of how well the product works. Where that distinction matters, the text says so.

## Topics

| # | Topic | Document | Status |
|---|---|---|---|
| 1 | Onshape | [01-onshape.md](01-onshape.md) | First pass written; gaps listed in the document |
| 2 | Geometric kernels | [02-kernels.md](02-kernels.md) | Parasolid covered from primary sources; other kernels and blending still thin; gaps listed in the document |
| 3 | AI for CAD and new entrants | [03-ai-and-new-entrants.md](03-ai-and-new-entrants.md) | First pass written; gaps listed in the document |
| 4 | Constraint solvers (D-Cubed and competitors) | [04-constraint-solvers.md](04-constraint-solvers.md) | First pass written; gaps listed in the document |
| 5 | Other leading CAD systems | [05-other-cad-systems.md](05-other-cad-systems.md) | Thin first pass: leads, not findings |
| 6 | Simulation, DFM and optimisation tooling | [06-simulation-dfm.md](06-simulation-dfm.md) | First pass written; gaps listed in the document |
| 7 | Reverse engineering: feature recovery from imported solids first, scan and mesh tools second | [07-reverse-engineering.md](07-reverse-engineering.md) | First pass written; gaps listed in the document |

## Findings so far that bear on open decisions

1. **Onshape pairs visual selection with stored historical references.** Its documentation says "most automatically-generated queries are historical", meaning that a pick in the interface is recorded as a description of how the entity came to exist, not as an identifier. This is direct evidence for [decision 0006](../../decisions/0006-geometry-references.md): selection and persistence are separate mechanisms in the reference product. See [01-onshape.md](01-onshape.md).
2. **A funded team has recently written a new kernel from scratch.** Zoo reports shipping a B-rep engine with GPU-based surface intersection after two years with fewer than 30 engineers. It is cloud-hosted and closed-source, and the claim of closing "decades of feature gap" is the vendor's own. It is evidence that [decision 0004](../../decisions/0004-ground-up-kernel.md) is not unprecedented, and it is not evidence about robustness. See [03-ai-and-new-entrants.md](03-ai-and-new-entrants.md).
3. **Onshape's version model was inspired by git but deliberately has no merge conflicts.** This bears on the open version-control question in the [register](../../REGISTER.md). See [01-onshape.md](01-onshape.md).
4. **Current AI integration in the reference product is code generation, not model operation.** Onshape's official MCP server lets an agent write and test FeatureScript in a sandbox. It does not give the agent a way to see or select geometry in a live model. See [03-ai-and-new-entrants.md](03-ai-and-new-entrants.md).
5. **Published benchmarks locate the weakness of current models in spatial reasoning and perception**, which supports the owner's position that text alone is not sufficient. See [03-ai-and-new-entrants.md](03-ai-and-new-entrants.md).

6. **Parasolid's designers rejected exact arithmetic on grounds of design intent, not only speed.** Their published reasoning is that exact methods create "small undesirable features in the model which do not correspond to any design intent". This challenges one of the candidate advantages listed in [decision 0004](../../decisions/0004-ground-up-kernel.md) and has to be answered in phase 3. See [02-kernels.md](02-kernels.md).
7. **No public benchmark compares kernels on robustness.** The belief that OCCT is far behind the commercial kernels is unmeasured. Phase 2 should measure it, and a reproducible benchmark is something we will need to build. See [02-kernels.md](02-kernels.md).
8. **Parasolid keeps derived geometry in exact procedural form** (intersection curves, blends, offsets) and later added mesh data as a surface type inside the B-rep. Both are design inputs for phase 3. See [02-kernels.md](02-kernels.md).

9. **Feedback-driven training already beats static training on CAD reconstruction.** Two recent papers put a CAD engine in the loop and report better results than supervised learning alone. This is direct support for the core hypothesis, and it makes kernel throughput and determinism requirements, not conveniences. See [07-reverse-engineering.md](07-reverse-engineering.md).
10. **Solver quality is mostly behaviour, not solving.** Choosing the intended solution among exponentially many, predictable dragging and clear diagnostics are what the incumbent sells, and none of it is publicly specified. See [04-constraint-solvers.md](04-constraint-solvers.md).

11. **Reliability in agent-driven design comes from the verifier.** One 2026 study raised code compliance from 56.8% to 98.6% by adding an external physics-based verifier and attributes the gain to the verifier, not the language model. The trustworthiness and failure rate of OpenShape's checks therefore matter more than which model drives them. See [06-simulation-dfm.md](06-simulation-dfm.md).
12. **Solvers that skip meshing exist commercially**, and they turn simulation into a matter of fast inside-or-outside queries on the geometry. That is a requirement to consider for the kernel. See [06-simulation-dfm.md](06-simulation-dfm.md).
13. **No standard found carries loads, load paths or functional interfaces with the geometry.** Existing standards cover tolerances and inspection. The search was not exhaustive. See [06-simulation-dfm.md](06-simulation-dfm.md).
14. **Feature rebuild in mainstream CAD is reported to be largely single-threaded.** This is the most promising lead for a performance advantage, and it is so far supported only by forum reports. See [05-other-cad-systems.md](05-other-cad-systems.md).

## Method note

The first pass was written while the session could reach only a fixed list of hosts, so several sources were seen only as search summaries and are marked [S]. Network access has since been opened. Upgrading those [S] marks by reading the sources in full is part of completing each topic.
