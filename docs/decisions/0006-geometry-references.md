# 0006: How geometry is selected and referenced

- **Status:** Open
- **Date:** 2026-11-10
- **Decided by:** Not decided. To be worked through in phase 4.

## Context

Features act on geometry: fillet these edges, mate these faces. Two questions follow, and they are easy to conflate.

1. **Selection:** how does a user, human or agent, indicate which edges or faces they mean?
2. **Persistence:** how is that choice stored, so it still identifies the right geometry after an upstream change regenerates the model?

## Positions so far

**Claude's initial proposal:** agents reference geometry semantically, through queries such as "the edges created by this extrude's end cap", not through face identifiers.

**Owner's position:** semantic references work for simple, toy designs and fall apart in complex real-world engineering. Working in three dimensions, text alone is not enough. Selection of edges, faces and so on needs a visual mechanism, accessible to both humans and agents.

**Claude's response, for discussion:** agreed that selection should be visual, and that asking an agent to write query expressions as its main way of pointing at geometry will not scale. The persistence question remains whichever way selection is done: a face picked in one evaluation of the model has no inherent identity in the next. Existing systems answer it differently, and with varying success. A possible synthesis is visual selection that the system records in a durable form behind the scenes, but that is a hypothesis, not a finding.

## Evidence gathered since this record was written

From phase 1 research:

- Onshape stores a historical query for each interface pick; a person never writes it. Selection and persistence are separate mechanisms in the reference product. ([Onshape](../research/01-state-of-the-art/01-onshape.md))
- Parasolid provides no persistent-naming scheme and declines to recommend one. Its lineage reporting is non-uniform across operations, has no split or merge relation, and is documented as ambiguous for blend faces. Picking returns a transient handle with no link to durable identity. ([Parasolid in depth](../research/01-state-of-the-art/08-parasolid-in-depth.md))
- Published benchmarks find current models weakest at spatial reasoning. ([AI for CAD](../research/01-state-of-the-art/03-ai-and-new-entrants.md))

Taken together: the owner's objection is well founded for references built on today's kernels, and the cause is in the kernel's reporting as much as in the naming layer. Still not established: how often stored references actually fail on complex models.

From phase 2 and 2B:

- SolidCraft names faces from kernel-reported history, tells split pieces apart by their neighbours, and reports a lost reference instead of guessing. It is untested on complex models.
- FreeCAD's naming problem, on a kernel with limited lineage reporting, was mitigated in version 1.0 and is described by its own documentation as not fully solved.
- CADEngBench finds that models asked to attach joints "often locate the relevant region but fail to recover the recorded joint or mating entities".
- No measurement of reference failure rates exists for any system. A benchmark to produce one is designed in [reference survival](../research/02b-benchmarks-and-datasets/01-reference-survival.md).

## What is needed to decide

- Phase 1: how Onshape, Parasolid-based systems and others store references, and how often those references break in practice.
- Phase 3: what the kernel can guarantee about topology identity across regeneration.
- Phase 4: what visual selection looks like for an agent (for example rendered views it can pick from), tested on complex parts, not toy ones.
