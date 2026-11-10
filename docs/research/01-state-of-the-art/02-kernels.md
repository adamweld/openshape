# Geometric kernels

Evidence marks are defined in the [phase README](README.md). This document currently covers only who makes and uses which kernel. The technical comparison that matters for [decision 0004](../../decisions/0004-ground-up-kernel.md) has not been started.

## The market

| Kernel | Owner | Licensed to others | Notable users | Mark |
|---|---|---|---|---|
| Parasolid | Siemens | Yes | NX, Solid Edge, SOLIDWORKS, Onshape, Shapr3D, and many CAM and CAE tools | [S] for the list; [P] for Onshape |
| ACIS | Dassault Systèmes, through Spatial | Yes | BricsCAD, SpaceClaim, KeyCreator and others | [S] |
| CGM | Dassault Systèmes, through Spatial | Yes | CATIA | [S] |
| ShapeManager | Autodesk (forked from ACIS in 2001) | No | Inventor, Fusion | [S] |
| Granite | PTC | Not researched | Creo | [S] |
| C3D | C3D Labs (ASCON) | Yes | KOMPAS-3D, nanoCAD | [S] |
| Open CASCADE (OCCT) | Open Cascade | Open source | FreeCAD and others | [S] |

Sources: [Wikipedia, Geometric modeling kernel](https://en.wikipedia.org/wiki/Geometric_modeling_kernel); [TransMagic kernel list](https://transmagic.com/which-geometric-modeling-kernel/); [Onshape](https://www.onshape.com/en/blog/how-does-onshape-really-work).

Observations:

- Wikipedia states the market "is dominated by Parasolid and ACIS, which were introduced in the late 1980s". [S] No current market-share figures were found.
- Dassault owns ACIS but uses CGM in its own flagship product. [S]
- A Spatial conference talk in 2022 reportedly put about one third of Spatial's customers on CGM and two thirds on ACIS. [S] ([upFront.eZine](https://upfrontezine.substack.com/p/upfrontezine-1129-spatial-3d-insiders))
- New kernels do get written. Recent examples are C3D, the Russian Geometric Kernel, and Zoo's engine (see [03-ai-and-new-entrants.md](03-ai-and-new-entrants.md)). [S]

## Parasolid: facts gathered so far

- Vendor material describes more than 900 functions covering solid modelling, direct editing, and free-form surface and sheet modelling. [S] ([reseller summary](https://techsoft3d.com/products/parasolid))
- **Tolerant modelling** is the vendor's name for handling imported data whose edges and vertices do not meet to full precision. [S] (same source)
- **Convergent modelling** extends B-rep operations to faceted (mesh) data in the same model, including mixed bodies with both facet and classic surfaces, mesh intersection with classic surface types, and blends on such models. Siemens positions it for generative design and reverse engineering. [S] ([Siemens](https://news.siemens.com/nl-nl/parasolid-convergent-modeling-mixed-models/))
- A fixed linear precision of 1.0e-8 units, with points closer than that treated as coincident, is reported in documentation from Parasolid licensees. [S] ([Bentley MicroStation help](https://docs.bentley.com/LiveContent/web/MicroStation%20Help-v28/en/AdvancedUnitSettings.html))
- A model size limit of 1000 units per axis (the "size box") is reported in a third-party article. [S] ([ProtoTech](https://prototechsolutions.com/?p=34620))

The last two points, if confirmed, describe a fixed-precision design: a bounded model space and one absolute tolerance, giving a fixed ratio between the largest and smallest representable features. That is a foundational choice and a candidate for a different answer in a new kernel. To be confirmed from Siemens documentation and examined in phase 3.

Relevance of convergent modelling to OpenShape: the owner's scope includes reverse engineering. The market leader's answer was to make mesh data a first-class citizen inside the B-rep kernel, not to bolt a separate mesh tool alongside. That is a design input for phase 3.

## Not yet researched

This is most of the topic.

- What each kernel can do: operation coverage for booleans, blending, offsetting, shelling, lofting and sweeping, direct editing.
- How each handles numerical robustness. Parasolid and ACIS documentation is partly public and needs reading.
- Blending specifically, since it is widely regarded as the hardest area. [U]
- Topology tracking and persistent naming support at kernel level, needed for [decision 0006](../../decisions/0006-geometry-references.md).
- Threading and performance characteristics.
- Any published benchmark or failure-rate comparison between kernels, including against OCCT. None found so far.
- Team size and effort behind each kernel, as a calibration for decision 0004.
- CGM, Granite and C3D in any technical depth.
