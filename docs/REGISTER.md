# Register

Every item that is not Settled. An item leaves this list only when its decision record becomes Settled or Superseded.

## Open

| Item | What is needed to decide | Where |
|---|---|---|
| How geometry is selected and how references are stored | Phase 4 dialogue, informed by phase 1 findings on how existing systems handle it | [0006](decisions/0006-geometry-references.md) |
| Version control mechanism: git itself, or something else | Phase 5, after the document model is understood | [ROADMAP](ROADMAP.md) phase 5 |
| Implementation language | Phase 5 | [ROADMAP](ROADMAP.md) phase 5 |
| Kernel: build independently, build on an existing open kernel, or join another project | Solid benchmark coverage, with every candidate kernel run on it. It may be chosen provisionally, but changing it later breaks part files ([0009](decisions/0009-kernel-not-replaceable.md)) | [0004](decisions/0004-ground-up-kernel.md) |
| Whether and how commercial CAD products may be measured: Onshape's terms forbid using the service for purposes competitive to it | Owner, with legal advice. No commercial product is to be run for comparison until this is answered | [COMPARABLE-PROJECTS](COMPARABLE-PROJECTS.md) |
| Reference-survival benchmark: how to score a system that guesses which piece of a split face was meant | Results now exist and record every outcome separately. The rule is wanted when a naming scheme for OpenShape is designed in phase 4 | [design](research/02b-benchmarks-and-datasets/01-reference-survival.md) |
| Reference-survival benchmark covers faces of Boolean-only models. Edges, fillets, sketches, coincident faces and SolidCraft's scheme are not covered | Before the benchmark is used as evidence for or against any naming design in phase 4 | [design](research/02b-benchmarks-and-datasets/01-reference-survival.md) |

## Provisional

| Item | Revisit trigger | Where |
|---|---|---|
| License is MPL-2.0 | Before the first outside contribution is accepted, or before the first public release, whichever is first | [0001](decisions/0001-license-mpl-2.0.md) |
| GUI and agents share one operation layer | End of phase 4 | [0005](decisions/0005-single-operation-layer.md) |

## Temporary

None.

## Research carried forward

Gaps left open when a research phase closed. Each must be closed, or explicitly dropped with a reason, before its owning phase closes.

| Item | From | Owner |
|---|---|---|
| Measure OCCT failure rates for booleans, blends and meshing on a public corpus | Phase 1 | Phase 2 |
| Measure rebuild and large-assembly behaviour in existing systems where it can be run | Phase 1 | Phase 2 |
| Licences and provenance of ABC, DeepCAD, Fusion 360 Gallery and Zero-to-CAD | Phase 1 | Phase 2 |
| Robustness literature since 1995 | Phase 1 | Phase 3 |
| Blending literature; persistent-naming papers read in full | Phase 1 | Phase 3 |
| Parasolid functional description chapters not read | Phase 1 | Phase 3 |
| Constraint solver theory | Phase 1 | Phase 3 |
| Hidden-line algorithms; sheet metal; surfacing requirements | Phase 1 | Phase 3 |
| AP209, AP243 and SysML v2 read directly | Phase 1 | Phase 4 |
| Classical feature recognition; Brep2Seq; a measure of editability for reconstructed trees | Phase 1 | Phase 4 |
| Manufacturability analysis methods; tolerance analysis; CAM | Phase 1 | Phase 4 |
| Topology optimisation and generative design products | Phase 1 | Phase 4 |
| Drawing standards; interaction design of newer CAD products; feature models of other systems | Phase 1 | Phase 5 |
