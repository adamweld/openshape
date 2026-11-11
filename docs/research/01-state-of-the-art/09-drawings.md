# Drawings

Evidence marks are defined in the [phase README](README.md). Drawings are in scope ([decision 0003](../../decisions/0003-scope.md)). This is a first pass aimed at one question: what do drawings require of the kernel and the document model, so that phases 3 and 5 do not design them out?

## Summary

- Drawings are not going away. Model-based definition is advancing among large manufacturers, and suppliers remain the obstacle, so a serious CAD system needs both.
- The kernel requirement is exact hidden-line computation: projecting a model to 2D curves, classified as visible or hidden, with silhouettes. The incumbents provide this in the kernel or as a dedicated component.
- The document-model requirement is associativity: dimensions and annotations on a drawing attach to model geometry and must survive model changes. This is the same durable-reference problem as [decision 0006](../../decisions/0006-geometry-references.md), with a second consumer.

## Are drawings still needed

- 2D drawings remain widely used "despite MBD", with regulatory compliance and suppliers of differing capability given as reasons. [S, vendor] ([Siemens](https://blogs.sw.siemens.com/solidedge/why-engineering-teams-are-rethinking-2d-drawings-in-a-model-based-world/))
- Supplier readiness is reported as the main barrier to model-based definition. [S] ([Belcan](https://www.belcan.com/2023/01/01/why-supply-networks-may-struggle-to-support-mbd/))
- Some large buyers are moving the other way: ASML is reported to have a zero-drawing policy requiring annotated 3D models, and Lockheed Martin to require suppliers to consume model-based data. [S] ([Bits and Chips](https://bits-chips.com/magazine/bc202507-state-of-semicon/?pagenr=18))
- No survey with an adoption percentage was found.

Reading: both forms are required for the foreseeable future. The annotations are the same information either way: dimensions, tolerances and notes attached to geometry. If OpenShape stores them once, semantically, on the model, a drawing becomes one presentation of that data and a STEP AP242 file with semantic PMI becomes another. That is a design hypothesis for phase 5, and it would also make the annotations machine-readable for the checks described in [06-simulation-dfm.md](06-simulation-dfm.md).

## What generating a view requires

- **Hidden-line computation in the kernel.** Parasolid's rendering function produces "hidden-line drawings" as polylines and circular and elliptical arcs approximating edges and surface boundaries to a caller-supplied curve tolerance, with options that "divide the rendered data into hidden and visible line segments" and add silhouette lines, blend boundaries and smoothness data. [P] (Parasolid functional description p1753-1754; see [08-parasolid-in-depth.md](08-parasolid-in-depth.md) for the source)
- That output is explicitly approximate: it is computed "to curve tolerance accuracy and not to modeling accuracy" and must not be used for modelling. [P] (same, p1754)
- Siemens also sells hidden-line generation as a separate component, D-Cubed HLM. [P, vendor] (see [04-constraint-solvers.md](04-constraint-solvers.md))
- BricsCAD describes "analytical hidden line removal" producing 2D lines and arcs, and warns it "can take a while for complex 3D models", recommending automatic view updates be turned off. [S] ([Bricsys](https://help.bricsys.com/en-us/document/bricscad/viewing-your-drawing/generated-drawing-views))

Reading: view generation is a known performance problem in existing systems, to the point that a vendor advises disabling automatic updates. Views of a large assembly are independent of each other and of most model edits, so this is another candidate for the parallel and incremental computation discussed in [05-other-cad-systems.md](05-other-cad-systems.md).

One design point to settle in phase 3: a dimension on a drawing must measure the true model geometry, not the approximated polyline. So each 2D segment in a view has to carry a reference back to the model edge or silhouette it came from.

## What a drawing environment contains

From vendor documentation and general practice. None of this was verified against the standards themselves. [S] for the listed sources, otherwise [U].

- Views: orthographic and isometric base views, projected views that inherit scale and alignment from a parent, section views including offset sections whose cutting plane jogs, detail views, broken views. ([Bricsys](https://help.bricsys.com/en-us/document/bricscad/viewing-your-drawing/generated-drawing-views))
- Two projection conventions: third-angle, standard in North America, and first-angle, standard in Europe.
- Dimensions and tolerances under two families of standards: ASME Y14.5, and ISO 1101 with ISO 2768 for general tolerances.
- Annotations: notes, surface finish, weld symbols, datum symbols, feature control frames, balloons.
- Tables: bill of materials, hole tables, revision tables, title blocks.
- Sheets, formats and templates.
- Output: PDF and DXF or DWG.

## Requirements for later phases

| For | Requirement |
|---|---|
| Phase 3, kernel | Exact hidden-line and silhouette computation, with each output segment traceable to its source edge or face |
| Phase 3, kernel | Section computation, which is a boolean with a plane and so inherits boolean robustness |
| Phase 4, intent | Dimensions and tolerances stored semantically on the model, usable by both drawings and analysis |
| Phase 5, document model | Drawing annotations reference model geometry durably; a drawing is a dependent of the model in the rebuild graph |
| Phase 5, performance | View regeneration is incremental and parallel |

## Gaps

- The standards themselves (ASME Y14.5, ISO 128, 129, 1101) were not read.
- How any system stores the link from a drawing dimension to model geometry, and how often those links break.
- Hidden-line algorithms in the research literature.
- Onshape's drawing implementation, which is reported to have been built on a licensed component. [U]
- Drawing exchange formats.

These are carried into phases 3 and 5 through the [register](../../REGISTER.md).
