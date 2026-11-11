# Onshape

Onshape is the functional reference for OpenShape. This document records how it works, as far as public sources say. Evidence marks are defined in the [phase README](README.md).

## Summary

- Onshape does not own its geometric core. The kernel (Parasolid) and constraint solver (D-Cubed) are licensed from Siemens.
- What Onshape built itself is everything around the core: the document model, the feature language, the reference mechanism, the renderer and the service architecture.
- Three of its design choices are directly relevant to OpenShape: the definition-only document model, FeatureScript as the single implementation language for features, and queries as the reference mechanism.

## Architecture

| Aspect | What Onshape does | Mark |
|---|---|---|
| Kernel | Parasolid, licensed from Siemens | [P] |
| Constraint solver | D-Cubed, licensed from Siemens | [P] |
| Where geometry runs | On "geometry servers" that rebuild geometry from feature lists and FeatureScript, solve assembly positions and compute tessellations | [P] |
| Client | Browser and mobile clients that are "not particularly thin" but are not complete CAD systems | [P] |
| What the client receives | Triangles only: neither pre-rendered images nor precise geometry | [P] |
| Renderer | Custom, on WebGL in browsers and OpenGL on mobile; no third-party scene graph | [P] |
| Transport | HTTPS/REST plus websockets with a custom wire protocol | [P] |
| Storage | A database, not files; no save action | [P] |

Source for all rows: [How Does Onshape Really Work?](https://www.onshape.com/en/blog/how-does-onshape-really-work) (Onshape, 2018).

Relevance to OpenShape: the split between an authoritative geometry process and a client that holds only display triangles is a consequence of Onshape being cloud-hosted. A local-first design is free to keep precise geometry next to the renderer. Whether it should is a phase 5 question.

## Document model

Onshape separates three kinds of data. [P] ([Under The Hood: How Collaboration Works](https://www.onshape.com/en/blog/under-the-hood-how-collaboration-works), Onshape, 2015)

| Kind | Examples | Persisted |
|---|---|---|
| UI state | Selection, camera, current tab | Generally not |
| Definition | Feature list, part names and colours, import data | Yes: this is the stored document |
| Regeneration results | B-rep, display triangles, rebuild errors | Cached; always rebuildable from the definition |

The definition is stored as a chain of immutable **microversions**. Each holds a reference to its parent and one change. [P] (same source)

- Changes are written so they apply to a state other than the one they were made against. The example given is "change the depth of Extrude 1 to 4 in", which applies as long as that feature exists. Features are identified by an internal id, so renaming does not break this.
- A version is a tag on a microversion. A workspace (branch) is a pointer to its latest microversion. Microversions form a tree.
- Undo in a shared session is implemented by applying the inverse of the user's own change on top of the latest state, not by stepping back in history.

### Branching and merging

- The design "is similar to (and was inspired by)" git: microversions correspond to commits and workspaces to branches. [P] (same source)
- Merging finds changes in the source that are absent from the target and applies them as a new microversion. [P] (same source)
- Conflicts are handled differently from git by design: "we try to never block the user". If a dimension was changed differently on both sides, the source wins. "Merge conflicts should never happen." [P] (same source)
- A later selective merge tool allows per-tab choice of what to merge. [S] ([Onshape help](https://cad.onshape.com/help/Content/Document/merging.htm))
- Branches with outdated FeatureScript versions cannot be merged. [S] (same help page)

Relevance to OpenShape: this is the main precedent for the open version-control question. Two points to carry into phase 5:

1. The unit of change is a semantic operation on the definition, not a text diff. That is what makes automatic merging possible.
2. "Source wins" removes conflicts by discarding one side's intent silently. Whether that is acceptable when an agent and a human, or several agents, work on branches of the same design is a question for phase 4.

## FeatureScript

FeatureScript is Onshape's language for defining features. Onshape states that custom features have "identical performance to standard features" and that the standard features are open-sourced and can be copied and extended. [P] ([FeatureScript MCP page](https://www.onshape.com/en/features/featurescript-mcp), Onshape)

The claim that Onshape's own built-in features are all written in FeatureScript is widely repeated but not confirmed here from a primary source. [U]

## How Onshape references geometry

This section bears directly on [decision 0006](../../decisions/0006-geometry-references.md).

FeatureScript refers to geometry through **queries**. The documentation states: [P] ([FeatureScript Standard Library documentation, query module](https://cad.onshape.com/FsDoc/library.html))

> Queries in general do not contain a list of entities in any form. Rather, they contain criteria that specify a subset of the topological entities in a context.

It distinguishes two kinds:

| Kind | Selects by | Documentation's example | Limitation stated |
|---|---|---|---|
| State-based | The current model state | "All edges adjacent to a cylindrical face which touches this point" | Cannot refer to entities that have been deleted |
| Historical | How the entity came to exist | "the edge that was generated by feature extrude_1_id from sketch vertex vertex_id from sketch sketch_id" | None stated in this passage |

And then the sentence that matters most for our purposes:

> Most automatically-generated queries are historical, while queries more commonly used in manually written code are state-based.

Reading this plainly: when a user clicks a face in the interface, Onshape does not store which face was clicked. It stores a historical query that describes the face's origin. A person never writes that query.

Other facts from the same documentation: [P]

- The order of entities a query resolves to is "deterministic but arbitrary".
- **Tracking queries** follow entities forward through later features: `startTracking` "will evaluate to entities derived from subquery in features between startTracking and when query is evaluated".
- `makeRobustQuery` "generates query robust to identity-preserving changes", and a batched form can optionally follow entities "through splits and merges".
- Feature authors can supply disambiguation hints (`setExternalDisambiguation`, `unstableIdComponent`).

From Onshape's forum, including replies from staff: [S] ([forum search results](https://forum.onshape.com/discussion/31349/the-arequeriesequivalent-method-does-not-work-when-compared-to-evaluatequery))

- Evaluating a query yields transient ids, which become invalid when the model changes. Staff advice is not to store them.
- Each operation records, for each piece of topology it creates, the dependencies that identify it.

### What this does and does not establish

Established:

- In the reference product, visual selection and durable reference are two separate mechanisms that work together. The human picks; the system writes the reference.
- The durable form is derived from modelling history, not from geometry or position.
- Onshape found it necessary to add machinery for splits, merges and ambiguity. The problem is not solved by the basic scheme alone.

Not established, and needed before decision 0006 can be settled:

- How often historical queries resolve to the wrong entity, or to nothing, on complex real models. No measurement found. This is the heart of the owner's objection and it remains open.
- Exactly what is recorded for an interface pick. The documentation says such queries are mostly historical but does not show one.
- How the kernel supports this. Parasolid's own tracking facilities have not been researched yet.

## Assemblies and mate connectors

- A mate connector is a local coordinate system located on or between entities. [S] ([Onshape help](https://cad.onshape.com/help/Content/mateconnector.htm))
- Connectors are implicit (offered at inferred points such as a circle centre when hovering during mate creation) or explicit (placed deliberately on a part). [S] ([Onshape help](https://cad.onshape.com/help/Content/mate.htm))
- A mate joins two connectors and its type states which degrees of freedom remain. Onshape's guidance is that "many assemblies require only one Onshape Mate between any two instances". [S] (same help page)

Relevance to OpenShape: a mate connector is already a small, explicit interface definition on a part. The owner's requirement for standardised interfaces between parts could extend this idea. To be examined in phase 4.

## Gaps to close before this topic is complete

- Read the remaining "Under the Hood" posts (crash isolation, mobile).
- Read the FeatureScript language guide for the feature model, id scheme and determinism rules.
- Establish from a primary source whether built-in features are written in FeatureScript.
- Find evidence, even anecdotal, on how often references break in practice.
- Drawings, configurations, variables, in-context editing, sheet metal, and import and export: not researched.
- Performance behaviour on large models: not researched.
