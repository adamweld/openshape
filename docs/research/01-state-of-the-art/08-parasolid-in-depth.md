# Parasolid in depth

This document records what the *Parasolid V35.0 Functional Description* (Siemens, July 2022, 2,094 pages) says about the kernel's design. It extends [02-kernels.md](02-kernels.md).

## About the source

- The document is proprietary to Siemens and is **not** in this repository and must not be added to it. The owner supplied a copy for reading. Notes here paraphrase it; quotes are short and carry page numbers.
- Page numbers are the printed ones. `(p227)` means printed page 227.
- About 600 pages were read, by five delegated readers working from the extracted text, each on assigned chapters. Fourteen of their key quotes were checked against the text; thirteen matched exactly and one could not be located as worded and is not used here. Figures were not available.
- Everything here is evidence mark **[P]** unless marked as inference. It describes what Parasolid does, as its vendor documents it. It does not say how often those things work.
- Chapters not read include sweeping, lofting, offsetting, hollowing, local operations (model editing), sewing, import, and faceting.

## Summary

| Area | What Parasolid does | What it means for OpenShape |
|---|---|---|
| Identity of faces and edges | Provides tags, identifiers, per-function tracking, attributes and groups, and tells the application to build persistent naming itself | The reference kernel has no naming solution. A kernel designed with one would be a real advance |
| Precision | Fixed 1e-8 linear and 1e-11 angular, in a 1,000-unit box, effectively unchangeable | Confirms the fixed-resolution design; its costs are documented |
| Tolerance | Grows as a side effect of operations and never shrinks automatically | Tolerance accumulation is a known weakness to design against |
| Booleans | Exposed as stages, with a long list of options that hand hard cases to the caller | Much of the robustness is the caller supplying hints |
| Blending | 17 edge-blend and 28 face-blend fault codes, four overflow strategies, and several vertex rules | Confirms blending as the largest single area; the failure taxonomy is a design input |
| Failure | No automatic rollback; a failed operation can leave the model invalid or corrupt | Transactional operations would be a clear improvement |
| Parallelism | At most 8 internal threads, in a short list of areas; booleans only in face-face clashing | Large headroom for a design that is parallel throughout |
| Stability across versions | Applications record a kernel version per feature and replay with that version's behaviour | Behaviour versioning is a requirement for any history-based system |
| Ordering | Result order is not guaranteed, even within one version, and changes with threading | Determinism is not something the incumbent offers |

## Identity and tracking

This is the section most relevant to [decision 0006](../../decisions/0006-geometry-references.md).

### The mechanisms

| Mechanism | What it is | Survives save and load | Notes |
|---|---|---|---|
| Tag | Integer handle, unique in a session, never reused | No (p71) | Higher tag means newer entity (p73) |
| Identifier | Integer unique within a part | Yes (p73) | Reassigned when an entity moves between parts |
| Tracking returns | Data returned by a modelling function relating new entities to originals | n/a | Undefined if the function returns an error (p122) |
| Attributes | Application data on entities, with rules for what happens on split, merge and so on | Yes | Seven behaviour classes, or callbacks (p1663) |
| Groups | Named sets of entities with integer labels | Yes (p1701) | Split pieces inherit membership |
| Bulletin board | Session log of low-level events | n/a | "Not typically recommended for new application implementations" (p124) |

### What Parasolid says about persistent naming

The document is direct about the limits of what it offers:

- The tools are "low-level building blocks" (p126).
- On strategies for persistent naming: "We do not endorse or recommend any particular strategy over another" (p126). It then lists academic papers, starting with Kripac.
- No single mechanism is sufficient; applications should combine several (p121).

So the leading kernel deliberately leaves persistent naming to each CAD vendor. Onshape's queries, SOLIDWORKS' internal naming and the rest are each built on these primitives separately.

### How tracking actually works

- **It is not uniform.** Each function family reports differently: sweeps return lateral and base arrays, blends return blend faces with their underlying faces, booleans have their own options, and some functions write to a session report instead (p121, p133, p135).
- **The vocabulary is thin.** Tracking records carry only create, derive and delete. There is no split or merge value: an edge produced by splitting or merging is reported as derived (p1317).
- **Booleans track only imprinted edges**, linking each to the target topology it was imprinted on and optionally the tool topology that caused it (p887-888). No general face-to-face lineage is described.
- **Splits.** One piece keeps the original tag and the others are new (p72). The document does not say which piece.
- **Merges.** The result keeps one original's tag; which one "depends on the operation" (p122).
- **Blend tracking is admitted to be ambiguous.** With the fuller tracking option the document warns the result does not uniquely identify blend faces (p1394-1395).
- **Order is not stable.** Entity order returned by functions is not guaranteed "within a particular version", patches included (p125). Applications are told not to rely on it.

### Picking

`PK_BODY_pick_topols` takes a ray and returns the faces it hits and the edges and vertices within a given distance of it, with ordering options (p1875-1878). It returns tags. Nothing connects a pick to a persistent identity; that link is again the application's job.

### What this means

1. The owner's scepticism about semantic references has a concrete basis. The information a naming scheme is built from is, in the reference kernel, non-uniform, coarse and ambiguous in exactly the hard cases: splits, merges and blends.
2. The weakness is in the foundation, not only in the naming schemes above it. A kernel that reported lineage uniformly, with split and merge as first-class relations and a defined rule for which piece is which, would give any naming scheme much better inputs. This is a place where designing the kernel and the feature system together can beat the incumbent structurally.
3. Picking and identity are separate in Parasolid, which matches the finding in [01-onshape.md](01-onshape.md): visual selection yields a transient handle, and something else must make it durable.

## Precision and tolerance

### Fixed precision

- Linear precision 1.0e-8, angular precision 1.0e-11 radians, model space 1,000 units cubed, with the metre "highly recommended" as the unit (p227). This upgrades the figures in [02-kernels.md](02-kernels.md) to primary-source.
- The functions that change session precision are listed as undocumented and not to be used (p119). Precision is in effect a constant.
- Stated consequences (p228-230):
  - Coincidence must be transitive or the body is invalid. Three points can each be within tolerance of the next while the first and last are not.
  - Near-tangent intersections collapse to a single point.
  - A cone sharper than the angular precision becomes a cylinder.
  - Scaling an imported part can invalidate it.
- Recommended margins: keep unrelated vertices more than 100 times the linear precision apart (p228).

### Tolerant modelling in practice

- A tolerant edge has no 3D curve. It has one parameter-space curve per adjacent face, and these need only agree to within the edge's tolerance (p193).
- A vertex's tolerance is at least that of every edge meeting it (p233).
- **Tolerance appears without being asked for.** Parasolid applies local precision itself in some operations, "for instance, many involving B-surfaces" (p231). Booleans take a default tolerance of 1.0e-5 and blends a maximum edge tolerance of 1.0e-5 (p833, p1372), a thousand times coarser than session precision.
- **Tolerance does not go away on its own.** Every way of reducing it is an explicit call, and resetting an edge to exact "may not always be successful if the adjacent surfaces are tangent or nearly tangent" (p236-237). That it never shrinks automatically is an inference from the absence of any such statement.
- **Tolerance has costs.** Tight tolerances make parameter-space curves with many segments and slow operations (p234). Exact geometry is "usually faster" to query (p238). Large tolerances can "consume features incorrectly" (p418).
- **Nominal geometry** lets a tolerant edge keep a reference to the simple exact curve it used to have, such as a circle, though that curve no longer defines its shape (p311).

### What this means

Tolerant modelling is how Parasolid survives imperfect geometry, and it comes with a ratchet: operations introduce tolerance, tolerance degrades later operations, and nothing removes it automatically. A long feature history on freeform geometry accumulates it. This is a specific weakness that phase 3 can aim at, for example by tracking the true error of each edge and tightening it whenever an operation makes that possible. It does not settle the exact-versus-tolerant question in [02-kernels.md](02-kernels.md), but it shows the tolerant approach has a real cost, and where.

## Geometry

- Curves: line, circle, ellipse, B-curve, intersection curve, SP-curve, foreign curve, and polyline for mesh edges (p184).
- Surfaces: plane, cylinder, cone, torus, sphere, B-surface, rolling-ball blend, offset, swept, spun, foreign surface, and mesh (p184).
- **Simplification is systematic.** Offsets of a plane are stored as planes; rolling-ball blends are simplified "to tori and cylinders" wherever possible (p308, p1334). Parasolid works to keep geometry in the simplest exact form.
- **Applications must not rely on which type they get back**, because it can change between versions (p182).
- An intersection curve has no closed form; its parameterisation is based on a polyline approximation and it is C1 but generally not C2 (p249, p257).
- Validity rules are detailed: no self-intersection, G1 required to attach geometry to a face or edge (otherwise it is split), degeneracies only on boundaries, and a list of legal but "undesirable" properties such as first derivatives above 1,000 or below 0.001 (p186, p304-306).
- **Checking** has about 150 distinct fault states (reader's count, approximate). The checker stops at the first failing group, so it "does not guarantee to find all the faults", and one fault state means the checker itself failed numerically (p410, p421).
- Most functions assume valid input and do not check it (p409).

## Booleans

- **Stages are exposed.** Imprint, classify face sets, delete, and join are each callable, so applications can build custom booleans with previews (p795-806).
- **Global and local.** A local boolean on selected faces is faster but does "not guarantee topological consistency" (p830).
- **Coincidence is partly the caller's problem.** The caller can supply matched regions: pairs of entities declared coincident, with a type and a tolerance per pair (p851-854). The document's own examples show a mirrored copy united on a shared face failing until the matching face pair is supplied (p854-856).
- **Advice in place of robustness.** If the model is not exact, coincidences "can be missed", so the document advises oversizing tool bodies so they protrude (p897-898).
- "Any boolean operation has the potential to fail" (p905).
- **Failure reporting is a status code** (success, no clash, no effect, failed and a few others). A failed status can accompany a no-error return, and then "the model might be left in an invalid state" (p830, p893).
- Over thirty options control a boolean, covering tolerance, matching, selection, material side, merging and result type (p832-838).
- **Clash detection** classifies pairs as interfering, abutting or contained (p405-408), and minimum-distance queries exist with an option to trade accuracy for speed (p395-404). These are the primitives an assembly check needs.

Reading: a production boolean is less a single algorithm than an algorithm plus a large surface of hints the calling application has learned to supply. Some of Parasolid's observed robustness inside SOLIDWORKS or Onshape is those products feeding it matched regions and oversized tools. A new kernel compared against "Parasolid" is really compared against Parasolid plus decades of application-side knowledge.

## Blending

- **Workflow.** Blend data is first attached to edges, then all of it is "fixed" in one operation (p1324). A preview mode returns the blend as a separate sheet without changing the body (p1390).
- **Range.** Constant and variable rolling-ball, circular, conic and curvature-continuous cross-sections, three kinds of chamfer, cliff-edge blends, and for face-face blending also disc blends, holdlines and chordal-width control (p1336-1355, p1432-1461).
- **Representation.** A fixed rolling-ball blend is a procedural surface defined by its two supporting surfaces, the radii and a spine curve, which is the intersection of the two offset surfaces (p1334, p1531).
- **Overflows.** When a blend runs off the faces next to its edge, there are four strategies, tried in order: smooth (carry the blend onto the neighbouring face), cliff, cliff-end and notch (p1403-1409). Defaults depend on whether the edge met is sharp or smooth and of the same or opposite convexity, tabulated over fifteen pages (p1408-1423).
- **Vertices.** Rules of thumb govern which combinations of blended edges at a vertex work, and a vertex with four or more edges where some but not all are blended is "too complex" (p1328-1333, p1530).
- **Order matters.** "The order in which blends are applied can be significant" (p1392).
- **Topology is consumed.** Features wholly overlapped by a blend, such as a small hole, are deleted by default (p1365).
- **Faults.** 17 edge-blend fault codes and 28 face-face fault codes (p1529-1543). The dominant cause given is a radius too large for its surroundings. One code is for an "unclassified numerical failure" where changing the radius may help (p1530).
- **Face-face faults are the more informative.** They return the entities involved, positions and distances, and two of them return a suggested range that would work (p1541-1542). Edge-blend faults mostly return only the code.
- A feature that suggests where to stop a failing blend is "not guaranteed to produce a successful blend" (p1390).

Reading: the volume is 220 pages and the complexity is in the cases, not the core mathematics. Each overflow type, vertex rule and fault code is a situation someone met and handled. This is the clearest picture so far of what "decades of edge cases" consists of, and it is the best argument for the testing-at-scale strategy in [decision 0004](../../decisions/0004-ground-up-kernel.md): these cases can be enumerated from this taxonomy and generated systematically. It also shows that diagnostic failures are possible, since the face-face blend already returns a suggested fix, and that Parasolid does this inconsistently.

## Failure handling

- **Three severities.** Mild leaves parts unaltered. Serious means parts "may have been altered, and may be invalid". Fatal means the session is corrupt and must be restarted (p1946).
- **The kernel does not restore the model.** After a serious error the application must roll back every affected partition itself (p1946).
- A failed local operation may leave a model so damaged that even deleting it could crash (p1959).
- Under multiple threads, after a serious error the session "may be corrupt" and other threads are barred until the failing thread rolls back (p1895).
- The same error code can be mild in one case and serious in another (p1946).

Reading: operations are not transactional. The application wraps each one in a rollback mark. For an agent running thousands of speculative operations, and for the verifier-driven loop in [06-simulation-dfm.md](06-simulation-dfm.md), an operation that either succeeds or leaves the model exactly as it was is a much better contract.

## Rollback and partitions

- A partition is a set of bodies that rolls back and forward independently. A pmark records a partition's state (p1675).
- **Partition history is a tree.** A pmark has one predecessor and any number of followers, so history can branch (p1684-1686). Session-wide marks are strictly linear.
- Changes between marks are stored as deltas, which the kernel hands to the application to store (p1695).
- Partitioned rollback is "essential for a feature-based modelling application" (p124).
- Operations across partitions are forbidden: a boolean between bodies in different partitions is not allowed (p1677).
- Rolling to a mark returns lists of new, deleted and modified entities. The first two are guaranteed; the modified list is not reliable and can vary between versions (p1686-1687).

Reading: branching state with cheap rollback is already how the reference kernel supports history-based modelling, which fits the working position in [decision 0005](../../decisions/0005-single-operation-layer.md) that speculative exploration should be cheap.

## Parallelism

- **From the application:** many threads may call the kernel. Functions are classed as concurrent, exclusive or locally exclusive, and threads can lock partitions to work on them in parallel (p1887-1889). The unit of concurrency is the partition.
- **Inside the kernel:** "Parasolid can create a maximum of 8 threads" for its own parallel work (p1898).
- The areas parallelised are listed: validity checking per face, the face-face clashing part of booleans, rendering, closest approach, faceting per body, mass properties, spline fitting and a few others (p1901-1902). The document says the list is not a guarantee.
- Speed-up is not linear, and some functions get slightly slower (p1900-1901).
- **Threading changes results' order.** With it enabled, the order of bodies from a boolean, and which result body inherits the target's tag, are not guaranteed (p1900). A debug facility exists to shuffle orders so applications can test they do not depend on them (p1900).
- Whether geometric results are identical across thread counts is not stated.

Reading: this is direct evidence for the performance lead in [05-other-cad-systems.md](05-other-cad-systems.md). Internal parallelism is capped at eight threads and applied in patches. And it costs determinism: turning threading on can change which body keeps its identity. A kernel designed so that results are identical at any thread count would offer something the incumbent explicitly does not.

## Stability across versions

- **The problem, in the document's own example:** a newer release stops creating a redundant edge; a later feature in a user's model referenced that edge; the model no longer rebuilds (p1926-1928).
- **The solution:** the application records the kernel version with each feature and asks the kernel to behave as that version when rebuilding it (p1912, p1924-1926).
- Since V28.1 one call selects the behaviour of "any release of Parasolid in V28.1 or later, including patch releases" (p1909). Before that, a separate switch per version had to be set, some reaching back to V9.0 (p1913-1921).
- Individual algorithms also have "update" options selecting older generations, added whenever a change "might alter the results in cases that previously succeeded" (p1933).
- There is no blanket promise that the same input gives the same output across releases. The promise is conditional on replaying with the recorded version. (Inference from p1921 and p1926.)

Reading: this means the kernel carries every past behaviour of every algorithm forever, selectable at run time. It is the price of improving a kernel underneath history-based models, and OpenShape will pay it too. Three consequences:

1. Onshape's rule that branches with outdated FeatureScript versions cannot be merged ([01-onshape.md](01-onshape.md)) is the same mechanism surfacing in the product.
2. Each feature in an OpenShape model needs to record the kernel behaviour version it was built with, from the first file format.
3. The cost of this grows with the number of behaviour changes. The more a kernel's results follow from a stated specification rather than from incidental algorithm details, such as whether a redundant edge is produced, the fewer such changes there are. That argues for specifying canonical results precisely.

## Mesh geometry

- A mesh is "a sub-class of surface" attached to a face, and a polyline is a curve type attached to an edge. The topology is unchanged (p1559-1562).
- Bodies are classic, facet or mixed (p1549).
- Supported on facet bodies: booleans, extrude, sectioning, imprinting, offset and thicken, hole filling, edge blending, sewing, and the enquiries (p1550).
- Not all functions support mesh geometry; the reference marks each as none or partial, and the feature is separately licensed and off by default (p1554-1555).
- **Going from mesh back to classic geometry is manual and per-face**: one function fits one trimmed surface to one mesh. No whole-body conversion is described (p1579-1581).

Reading: this confirms the design noted in [02-kernels.md](02-kernels.md), and it shows the market leader has no automatic mesh-to-solid reconstruction in its kernel. That is consistent with the owner placing scan work far down the road.

## Design inputs added by this document

These extend the table in [02-kernels.md](02-kernels.md).

| # | Finding | Question for OpenShape |
|---|---|---|
| 6 | Lineage reporting is non-uniform and has no split or merge relation | Can the kernel report lineage uniformly for every operation, with a defined rule for which piece of a split is which? |
| 7 | Tolerance ratchets upward | Can edge error be tracked exactly and tightened automatically? |
| 8 | Operations are not transactional | Can every operation be all-or-nothing by construction? |
| 9 | Internal parallelism is capped and breaks ordering | Can results be identical at any thread count? |
| 10 | Every past behaviour is kept and selected by version | How is behaviour versioned from the first release, and how is the number of behaviour changes kept small? |
| 11 | Boolean robustness depends on caller-supplied hints | Which hints can the kernel derive itself, given that it will know the feature history? |
| 12 | Blend failure information is uneven | What should every failure return? At minimum the entities, the location, and where possible a value that would succeed |
