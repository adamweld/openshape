# Phase 1: State of the art

Status: **complete**, closed on 2026-11-10 on the basis agreed with the owner: gaps that later phases depend on were closed, and the rest are carried forward as named items in the [register](../../REGISTER.md). Individual documents still list their own gaps.

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
| 8 | Parasolid in depth | [08-parasolid-in-depth.md](08-parasolid-in-depth.md) | Written from the vendor's functional description; about 600 of 2,094 pages read |
| 9 | Drawings | [09-drawings.md](09-drawings.md) | First pass aimed at kernel and document-model requirements |
| 7 | Reverse engineering: feature recovery from imported solids first, scan and mesh tools second | [07-reverse-engineering.md](07-reverse-engineering.md) | First pass written; gaps listed in the document |

## Conclusions: the bar to clear

What phase 1 established, in order of confidence.

**Well supported**

1. The incumbents' advantage is accumulated cases and application-side know-how, not a secret technique. Parasolid's blending alone has 45 fault codes and fifteen pages of default tables, and its booleans rely on hints supplied by the calling application.
2. The reference kernel leaves real openings: no persistent naming, lineage reporting that is non-uniform and ambiguous, tolerance that only grows, operations that are not transactional, internal parallelism capped at eight threads, and no determinism of ordering.
3. Closing the loop with a real engine or real physics works. Four studies measured it: reconstruction quality up 6 to 9 points with invalid output near zero; acceptable designs up from 22% to 59%; code compliance up from 57% to 99%.
4. That loop is limited by the engine, on throughput and on reliability. Papers cap their search because the CAD engine is slow, and meshing fails on 12 to 24% of agent-built parts.
5. Agents do better choosing among presented geometry than writing coordinates, and current models cannot yet be trusted to judge geometry from images alone.

**Plausible, not yet measured**

6. OCCT is well behind the commercial kernels in robustness. No public comparison exists.
7. Feature rebuild in mainstream CAD is largely single-threaded, and precise dependency tracking would allow parallel and partial rebuilds.
8. Stored geometry references fail often on complex real models. This is the owner's position and the evidence about the foundations is consistent with it, but no failure rate was found.

**Open questions phase 1 raised**

9. Exact arithmetic or tolerant modelling, or a hybrid. Parasolid's designers rejected exact arithmetic for a reason that still holds: it produces slivers no designer intended.
10. Where engineering intent attaches. Existing standards put loads on analysis models and interfaces on system models; one research schema anchors loads to regions of space; nothing puts them on the design geometry.
11. How much of each kernel behaviour must be frozen forever once models depend on it.

## Carried forward

These were not closed in phase 1. Each is in the [register](../../REGISTER.md) with the phase that owns it.

| Item | Owner |
|---|---|
| Measure OCCT failure rates for booleans, blends and meshing on a public corpus | Phase 2 |
| Measure rebuild and large-assembly behaviour in existing systems where it can be run | Phase 2 |
| Licences and provenance of ABC, DeepCAD, Fusion 360 Gallery and Zero-to-CAD | Phase 2 |
| Robustness literature since 1995: exact predicates, interval methods, tolerant modelling | Phase 3 |
| Blending literature; persistent-naming papers read in full | Phase 3 |
| Parasolid chapters not read: sweeping, lofting, offsetting, local operations, sewing, import, faceting | Phase 3 |
| Constraint solver theory: Owen 1991, decomposition papers, 3D solving, under-constrained problems | Phase 3 |
| Hidden-line algorithms; sheet metal; surfacing requirements | Phase 3 |
| AP209, AP243 and SysML v2 read directly | Phase 4 |
| Classical feature recognition; Brep2Seq; a measure of editability for reconstructed trees | Phase 4 |
| Machining, moulding and additive manufacturability analysis; tolerance analysis; CAM | Phase 4 |
| Topology optimisation and generative design products | Phase 4 |
| Drawing standards; interaction design of Plasticity and Shapr3D; feature models of other systems | Phase 5 |

## Findings that bear on open decisions

1. **Onshape pairs visual selection with stored historical references.** Its documentation says "most automatically-generated queries are historical", meaning that a pick in the interface is recorded as a description of how the entity came to exist, not as an identifier. This is direct evidence for [decision 0006](../../decisions/0006-geometry-references.md): selection and persistence are separate mechanisms in the reference product. See [01-onshape.md](01-onshape.md).
2. **A funded team has recently written a new kernel from scratch.** Zoo reports shipping a B-rep engine with GPU-based surface intersection after two years with fewer than 30 engineers. It is cloud-hosted and closed-source, and the claim of closing "decades of feature gap" is the vendor's own. It is evidence that [decision 0004](../../decisions/0004-ground-up-kernel.md) is not unprecedented, and it is not evidence about robustness. See [03-ai-and-new-entrants.md](03-ai-and-new-entrants.md).
3. **Onshape's version model was inspired by git but deliberately has no merge conflicts.** This bears on the open version-control question in the [register](../../REGISTER.md). See [01-onshape.md](01-onshape.md).
4. **Current AI integration in the reference product is code generation, not model operation.** Onshape's official MCP server lets an agent write and test FeatureScript in a sandbox. It does not give the agent a way to see or select geometry in a live model. See [03-ai-and-new-entrants.md](03-ai-and-new-entrants.md).
5. **Published benchmarks locate the weakness of current models in spatial reasoning and perception**, which supports the owner's position that text alone is not sufficient. See [03-ai-and-new-entrants.md](03-ai-and-new-entrants.md).

6. **Parasolid's designers rejected exact arithmetic on grounds of design intent, not only speed.** Their published reasoning is that exact methods create "small undesirable features in the model which do not correspond to any design intent". This challenges one of the candidate advantages listed in [decision 0004](../../decisions/0004-ground-up-kernel.md) and has to be answered in phase 3. See [02-kernels.md](02-kernels.md).
7. **No public benchmark compares kernels on robustness.** The belief that OCCT is far behind the commercial kernels is unmeasured. Phase 2 should measure it, and a reproducible benchmark is something we will need to build. See [02-kernels.md](02-kernels.md). *Superseded in part by phase 2, which found a public surface-intersection corpus and measured OCCT directly.*
8. **Parasolid keeps derived geometry in exact procedural form** (intersection curves, blends, offsets) and later added mesh data as a surface type inside the B-rep. Both are design inputs for phase 3. See [02-kernels.md](02-kernels.md).

9. **Feedback-driven training already beats static training on CAD reconstruction.** Two recent papers put a CAD engine in the loop and report better results than supervised learning alone. This is direct support for the core hypothesis, and it makes kernel throughput and determinism requirements, not conveniences. See [07-reverse-engineering.md](07-reverse-engineering.md).
10. **Solver quality is mostly behaviour, not solving.** Choosing the intended solution among exponentially many, predictable dragging and clear diagnostics are what the incumbent sells, and none of it is publicly specified. See [04-constraint-solvers.md](04-constraint-solvers.md).

11. **Verification by real physics is what makes agent-produced designs reliable, up to a ceiling.** In two studies read in full, adding it raised acceptable designs from 22% to 59% and from 57% to 99%. Both report that the loop converges on parameter changes and stalls when the fix needs a change of structure. One finding on model independence is underpowered and should not be leaned on. See [06-simulation-dfm.md](06-simulation-dfm.md).
12. **Solvers that skip meshing exist commercially**, and they turn simulation into a matter of fast inside-or-outside queries on the geometry. That is a requirement to consider for the kernel. See [06-simulation-dfm.md](06-simulation-dfm.md).
13. **Standards carry loads at the analysis level and interfaces at the system level, not on the design geometry.** AP209 holds load cases for a finite element model and SysML v2 holds ports and requirements for a system. None found attaches design loads, load paths or functional interfaces to CAD faces the way AP242 attaches tolerances. Provisional: the standards were not read directly. See [06-simulation-dfm.md](06-simulation-dfm.md).
14. **Feature rebuild in mainstream CAD is reported to be largely single-threaded.** This is the most promising lead for a performance advantage, and it is so far supported only by forum reports. See [05-other-cad-systems.md](05-other-cad-systems.md).

15. **The reference kernel has no persistent-naming solution.** Parasolid calls its tracking tools "low-level building blocks" and declines to recommend a naming strategy. Its lineage reporting differs per function and has no split or merge relation. This supports the owner's scepticism in [decision 0006](../../decisions/0006-geometry-references.md) and identifies the foundation, not only the naming layer, as the place to improve. See [08-parasolid-in-depth.md](08-parasolid-in-depth.md).
16. **Parasolid's operations are not transactional, its internal parallelism is capped at eight threads, and result ordering is not deterministic.** Each is a concrete opening for a new design. See [08-parasolid-in-depth.md](08-parasolid-in-depth.md).
17. **Kernel behaviour must be versioned per feature.** Parasolid keeps every past behaviour selectable so old models still rebuild. OpenShape needs the same from its first file format. See [08-parasolid-in-depth.md](08-parasolid-in-depth.md).

## Method note

The first pass was written while the session could reach only a fixed list of hosts, so several sources were seen only as search summaries and are marked [S]. Network access has since been opened. Upgrading those [S] marks by reading the sources in full is part of completing each topic.
