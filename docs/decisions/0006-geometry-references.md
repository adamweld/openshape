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

## What is needed to decide

- Phase 1: how Onshape, Parasolid-based systems and others store references, and how often those references break in practice.
- Phase 3: what the kernel can guarantee about topology identity across regeneration.
- Phase 4: what visual selection looks like for an agent (for example rendered views it can pick from), tested on complex parts, not toy ones.
