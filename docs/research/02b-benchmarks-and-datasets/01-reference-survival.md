# A benchmark for reference survival

Status: **design proposal.** Nothing here is built. It is written to be argued with, in particular by the owner, whose objection in [decision 0006](../../decisions/0006-geometry-references.md) it is meant to test.

## The question

A feature in a parametric model refers to geometry made by earlier features: round this edge, sketch on that face, mate to this hole. When an earlier feature changes, the model is rebuilt and each reference has to find its geometry again.

The owner's position is that references of this kind work on toy designs and fall apart on complex real ones. Phase 1 found that the commercial kernel leaves the problem to each CAD vendor, and that FreeCAD's long-standing version of it is mitigated and not solved. SolidCraft claims an exact scheme based on kernel-reported history. Nobody has published a failure rate for any system.

So the question this benchmark answers is: **for a given system, after a given kind of upstream edit, what fraction of references resolve to the right geometry, what fraction are correctly reported as lost, and what fraction silently resolve to the wrong geometry?**

The last fraction is the one that matters most. SolidCraft's own design document puts it well: a reference that "quietly re-attaches to a different face" with nothing telling the user "is the worst thing a CAD tool can do".

## Why this can have exact answers

Phase 2's feature sequences are built only from analytic primitives combined by booleans, and that gives every face of the true solid a known origin.

- Every point on the boundary of the result lies on the surface of exactly one primitive, apart from points on edges. Which one is computable in closed form from the same inside tests phase 2 already uses.
- So a face of the true solid has a **semantic identity** that does not depend on any kernel: which primitive, and which of that primitive's surfaces (a box has six, a cylinder three, a sphere one).
- An edge has the identity of the two surfaces it separates.
- When a surface contributes several disconnected faces, for example a top face cut in two by a slot, they share a semantic identity. That is the genuinely ambiguous case, and the benchmark knows it is ambiguous by construction.

This is the same trick as the rest of the suite: build the case so that the right answer is known without asking a kernel.

## A case

1. **Build.** A feature sequence of the phase 2 kind: a block, then holes, pockets, bosses, ribs and cuts.
2. **Refer.** After a chosen step, pick some faces and edges of the model as it then stands. Each pick is given to the system under test as a point on the entity, which is how a person or an agent picks. The system returns whatever it uses as a durable reference: a name, a query, an id. The benchmark records the pick's semantic identity from the closed form.
3. **Edit.** Change something upstream of the pick. The edit is drawn from the classes below.
4. **Rebuild.**
5. **Resolve.** Ask the system to resolve each stored reference in the rebuilt model. It returns an entity, or several, or reports the reference lost. For each returned entity the system supplies a point on it, and the benchmark computes that point's semantic identity.
6. **Score** against what the edit, by construction, did to the referenced geometry.

Step 2 uses a point and step 5 returns a point, so the benchmark never needs to understand the system's naming scheme. That keeps the contract engine-neutral.

## What an edit does to a reference, and the right response

| Effect of the edit on the referenced geometry | Right response | Wrong responses |
|---|---|---|
| Unchanged, or only moved or resized | The same semantic identity | A different identity (silent wrong); reported lost (false loss) |
| Still present, and now one of several pieces of its surface | Either all pieces, or a report that the reference is ambiguous. A single piece is right only if the benchmark's stated rule picks the same one | A piece chosen silently by an arbitrary rule |
| Several pieces merged into one | The merged face | Reported lost |
| Gone: its surface no longer bounds the solid | Reported lost | Any entity returned (silent wrong) |
| Gone and later restored by a second edit | The original identity again | Lost for good, or a different identity |

"Which piece" needs a stated rule to be scoreable. The proposal is the one SolidCraft's naming document describes, because it is the only precise one found: pieces are told apart by which other surfaces bound them. A piece whose set of neighbours is unchanged by the edit is the same piece. Where no such distinction exists, the case is marked ambiguous and only "all pieces" or "reported ambiguous" count as right.

## Classes of edit

Ordered roughly by how hard they are expected to be.

| Class | Example | What it tests |
|---|---|---|
| A. Dimension change, same topology | A hole's radius goes from 5 to 6 | The baseline. Any failure here is disqualifying |
| B. Unrelated topology change | A new hole appears far from the referenced face | Whether identity depends on entity counts or order |
| C. Move across a boundary | A boss slides until it overhangs an edge | Faces appearing and disappearing next to the reference |
| D. Split | A slot is lengthened until it cuts the referenced face in two | The ambiguous case |
| E. Merge | The slot is shortened again | Recovery of the original identity |
| F. Deletion | A feature that created the referenced face is suppressed | Whether loss is reported |
| G. Insertion upstream | A new feature is added before the one that made the reference | Whether identity depends on feature position |
| H. Reordering | Two independent features swap places | The same |
| I. Pattern count | A row of 4 holes becomes 5 | Identity of repeated instances |
| J. Round trip | Any of the above applied and then exactly undone | Whether the model returns to an identical state |

Each class is generated at several model sizes: 10, 50 and 200 features. The owner's claim is specifically about scale, so the result that matters is how the failure rates change from 10 to 200.

## Scores

Reported per class and per model size, never as one number:

- **Correct**: resolved to the right identity.
- **Correctly lost**: reported lost when the geometry is gone.
- **Silent wrong**: resolved to something else with no warning. Reported on its own line in every table.
- **False loss**: reported lost when the geometry is there.
- **Ambiguity handled**: for the split class, ambiguity reported or all pieces returned.
- **Round-trip identity**: for class J, whether every reference and the model itself are identical to the start.

A system with 2% false losses and no silent wrong answers is better than one with 0.5% of each. The reporting should make that visible.

## The contract for a system under test

Following the surface-intersection corpus, a system is driven by a separate runner that reads a case and writes a result. The runner must support five operations:

1. Build a model from a list of primitive and boolean steps.
2. Given a point on the model, return a durable reference to the face or edge there.
3. Change a parameter of a step, insert a step, remove a step, or reorder steps.
4. Rebuild.
5. Resolve a reference to zero or more entities, with one point on each, or report it lost or ambiguous.

That is small enough to implement for FreeCAD through its Python interface, for SolidCraft through its command interface, and for OpenShape. CadQuery and build123d have no durable references at all, only selectors re-evaluated each time, and they can be measured the same way as a baseline for the "write a query" approach.

## What it cannot measure

- **Freeform geometry.** Identity by source primitive only works for analytic primitives. Lofts, sweeps and fillets create faces with no such closed-form origin. Fillets can be handled, since a fillet face has the identity of the edge it replaced. Freeform surfaces need a different construction and are out of the first version.
- **Sketch-based features.** Real models are mostly extruded sketches, where a face's origin is a sketch curve. That fits the same scheme, with the sketch curve as the source, and should be the second version.
- **Real engineering models.** Generated models are not designed by engineers, and the owner's objection is about real designs. The benchmark can show whether a scheme fails on generated models of realistic depth. It cannot prove a scheme works on real ones. Clean real models would be needed for that, and phase 2 found none that are cleanly licensed.
- **Whether a reference means what the designer meant.** A reference can resolve to the geometrically correct face and still not be the one a person would have wanted after a large redesign. That is a question of intent, not identity.

## What it would settle

- If today's best schemes show silent wrong answers rising steeply with model size, the owner's position is confirmed with data, and durable references built on kernel history are not enough. Phase 4 would then need a different primary mechanism, or references that carry intent.
- If a scheme based on exact kernel lineage holds at 200 features with only correct and correctly-lost outcomes, then the weakness the owner observed belongs to particular implementations, and the design direction in decision 0006's synthesis is sound.
- Either way, the result is new. No such measurement exists for any system.

## Open design questions

1. Is "all pieces or report ambiguous" the right standard for a split face, or should a system be rewarded for a good guess? The proposal says no: a guess that is usually right is exactly the failure being measured.
2. How should a reference by an agent differ from one by a person? An agent could attach a statement of intent to a reference, such as "the mounting face", which a person rarely does. The benchmark could later score references that carry such statements separately.
3. Should the first version include sketch-based features, at the cost of needing each runner to drive a sketcher?

## Dependencies

- The feature-sequence generator from phase 2, extended with parameters that can be edited and with patterns.
- A closed-form attribution of boundary points to source surfaces, which is a small addition to the existing inside tests.
- Runners for at least two existing systems, so the benchmark is validated on something before OpenShape has a kernel. FreeCAD and SolidCraft are the natural pair.
