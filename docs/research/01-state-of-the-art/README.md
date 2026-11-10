# Phase 1: State of the art

Status: **in progress**. Scope and exit criteria are in [ROADMAP.md](../../ROADMAP.md).

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
| 2 | Geometric kernels | [02-kernels.md](02-kernels.md) | Market picture written; technical depth not started |
| 3 | AI for CAD and new entrants | [03-ai-and-new-entrants.md](03-ai-and-new-entrants.md) | First pass written; gaps listed in the document |
| 4 | Constraint solvers (D-Cubed and competitors) | not written | A few facts gathered, recorded below |
| 5 | Other leading CAD systems | not written | Not started |
| 6 | Simulation, DFM and optimisation tooling | not written | A few facts gathered, recorded below |
| 7 | Reverse-engineering tools: feature recovery from imported solids first, scan and mesh tools second | not written | A few facts gathered, recorded below |

## Findings so far that bear on open decisions

1. **Onshape pairs visual selection with stored historical references.** Its documentation says "most automatically-generated queries are historical", meaning that a pick in the interface is recorded as a description of how the entity came to exist, not as an identifier. This is direct evidence for [decision 0006](../../decisions/0006-geometry-references.md): selection and persistence are separate mechanisms in the reference product. See [01-onshape.md](01-onshape.md).
2. **A funded team has recently written a new kernel from scratch.** Zoo reports shipping a B-rep engine with GPU-based surface intersection after two years with fewer than 30 engineers. It is cloud-hosted and closed-source, and the claim of closing "decades of feature gap" is the vendor's own. It is evidence that [decision 0004](../../decisions/0004-ground-up-kernel.md) is not unprecedented, and it is not evidence about robustness. See [03-ai-and-new-entrants.md](03-ai-and-new-entrants.md).
3. **Onshape's version model was inspired by git but deliberately has no merge conflicts.** This bears on the open version-control question in the [register](../../REGISTER.md). See [01-onshape.md](01-onshape.md).
4. **Current AI integration in the reference product is code generation, not model operation.** Onshape's official MCP server lets an agent write and test FeatureScript in a sandbox. It does not give the agent a way to see or select geometry in a live model. See [03-ai-and-new-entrants.md](03-ai-and-new-entrants.md).
5. **Published benchmarks locate the weakness of current models in spatial reasoning and perception**, which supports the owner's position that text alone is not sufficient. See [03-ai-and-new-entrants.md](03-ai-and-new-entrants.md).

## Notes held for topics not yet written

These are recorded so they are not lost. None has been checked against a primary source.

**Constraint solvers**

- Onshape uses D-Cubed, licensed from Siemens. [P] ([Onshape](https://www.onshape.com/en/blog/how-does-onshape-really-work))
- Siemens describes 2D DCM as the sketch solver and 3D DCM as the solver for assembly positioning, mechanism kinematics and direct editing. [S] ([Siemens 2D DCM](https://www.siemens.com/en-gb/products/plm-components/d-cubed/2d-dcm/), [3D DCM](https://www.siemens.com/en-gb/products/plm-components/d-cubed/3d-dcm/))
- The academic root of this solver family is J. Owen, "Algebraic solution for geometry from dimensional constraints", ACM Symposium on Foundations of Solid Modeling, 1991: graph-based structural analysis that splits a problem into generic subproblems solved algebraically and recombined. [S] ([survey](https://arxiv.org/pdf/1608.05205), [Wikipedia](https://en.wikipedia.org/wiki/Geometric_constraint_solving)) No source found yet ties D-Cubed's current internals to this method.

**Simulation and DFM**

- Ansys Discovery offers GPU-based near-real-time simulation and is positioned by the vendor as rapid analysis, not a replacement for full CAE. [S] ([Digital Engineering](https://www.digitalengineering247.com/article/going-live-with-real-time-simulation))
- aPriori derives cost and manufacturability feedback from geometric features of a CAD model ("geometric cost drivers") using bottom-up process simulation. [S] ([aPriori](https://www.apriori.com/dfm-plus))

**Reverse engineering**

- Geomagic Design X converts scan data to feature-based CAD with guided and automatic feature extraction, and transfers the feature history to mainstream CAD systems. [S] ([reseller page](https://prototypingsolutions.com/product/geomagic-design-x/)) No independent accuracy comparison found yet.

## Method note

The first pass was written while the session could reach only a fixed list of hosts, so several sources were seen only as search summaries and are marked [S]. Network access has since been opened. Upgrading those [S] marks by reading the sources in full is part of completing each topic.
