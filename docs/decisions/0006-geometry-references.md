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
- When this record was written, no measurement of reference failure rates existed for any system. A benchmark to produce one was designed in [reference survival](../research/02b-benchmarks-and-datasets/01-reference-survival.md) and has since been built and run.

From the first reference-survival run, 2026-11-12 ([results](https://github.com/adamweld/cadkernelbench/blob/main/docs/RESULTS.md#reference-survival)). The models are boxes, cylinders and spheres joined by Booleans, 10 to 200 features deep, and every reference is to a face:

- A reference with no naming, the face's position in the kernel's list, resolves silently to the wrong face for 35% of surviving faces at 10 features and 50% at 200.
- A label on each primitive face, carried through every Boolean by what OCCT 8.0.1 reports became of the face, was exact: 7,129 of 7,129 surviving faces found, 320 of 320 deleted faces reported lost, every piece of a divided face returned, at 200 features as at 10.
- FreeCAD 1.1.4's own links, at 10 and 50 features, were correct for about 94% of surviving faces. About 5.6% were reported lost though the face was still there, most often where a neighbouring feature changed the face's outline. 51 of about 7,200 references resolved silently to a wrong face, all in 50-feature models. A reference lost by an edit stayed lost when the edit was undone.

What this does and does not show:

- It shows that for Boolean-only models of this depth, kernel-reported history is enough to keep face references exact, and that a shipping open-source product does measurably worse than that on the same models. The second point is support for the owner's position as it applies to an existing system.
- It does not test the owner's position on complex real designs. There are no fillets, sketches, coincident faces, patterns or edge references in these models, and those are where Parasolid's own documentation says lineage is ambiguous. Exactness here is necessary and far from sufficient.
- It does not answer which piece of a divided face a designer meant. The history scheme returns all of them.
- No commercial product has been measured, and none will be until the terms-of-use question in the [register](../REGISTER.md) is answered.

## What is needed to decide

- Phase 1: how Onshape, Parasolid-based systems and others store references, and how often those references break in practice.
- Phase 3: what the kernel can guarantee about topology identity across regeneration.
- Phase 4: what visual selection looks like for an agent (for example rendered views it can pick from), tested on complex parts, not toy ones.
