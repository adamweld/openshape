# Geometric kernels

Evidence marks are defined in the [phase README](README.md). This document covers the commercial kernels. Open-source kernels are phase 2.

## Summary

- Parasolid is the kernel to measure against. It is the most widely licensed, it sits under the reference product, and it is the best documented in public.
- Five of its design choices are foundational, and each is a question a new kernel has to answer deliberately. They are listed under [Design inputs for phase 3](#design-inputs-for-phase-3).
- One finding cuts against an assumption recorded in [decision 0004](../../decisions/0004-ground-up-kernel.md). Parasolid's designers considered exact arithmetic and rejected it for reasons of design intent, not only speed. See [Tolerant modelling](#tolerant-modelling).
- No public benchmark compares kernels on robustness. Every statement that one kernel is more robust than another, including the premise that OCCT is far behind, rests on anecdote. We will have to measure this ourselves.

## The market

| Kernel | Owner | Licensed to others | Notable users | Mark |
|---|---|---|---|---|
| Parasolid | Siemens | Yes | NX, Solid Edge, SOLIDWORKS, Onshape, Shapr3D, and many CAM and CAE tools | [P] for Onshape, SOLIDWORKS and Siemens products; [S] for the rest |
| ACIS | Dassault Systèmes, through Spatial | Yes | BricsCAD, SpaceClaim, KeyCreator and others | [S] |
| CGM | Dassault Systèmes, through Spatial | Yes | CATIA | [S] |
| ShapeManager | Autodesk (forked from ACIS in 2001) | No | Inventor, Fusion | [S] |
| Granite | PTC | Not researched | Creo | [S] |
| C3D | C3D Labs (ASCON) | Yes | KOMPAS-3D, nanoCAD | [S] |
| Open CASCADE (OCCT) | Open Cascade | Open source | FreeCAD and others | [S] |

Sources: [Wikipedia, Geometric modeling kernel](https://en.wikipedia.org/wiki/Geometric_modeling_kernel); [TransMagic kernel list](https://transmagic.com/which-geometric-modeling-kernel/); [Siemens interview, Engineering.com](https://www.engineering.com/parasolid-d-cubed-and-siemens-the-heart-of-your-cad-software-belongs-to-another/); [Onshape](https://www.onshape.com/en/blog/how-does-onshape-really-work).

- Siemens states it licenses Parasolid to "over 130 independent software vendors" and estimates four million daily heavy users. [P, vendor's own figures] (Engineering.com interview)
- Wikipedia states the market "is dominated by Parasolid and ACIS". [S] No independent market-share figures were found.
- C3D has been developed since 1995 by a team in Russia and was offered for licence from 2012. [S] ([C3D Labs](https://c3dlabs.com/en/products/modeler/))
- New kernels do get written: C3D, the Russian Geometric Kernel, and Zoo's engine (see [03-ai-and-new-entrants.md](03-ai-and-new-entrants.md)). [S]

## Parasolid

Sources used in this section:

- **XT reference:** *Parasolid XT Format Reference*, Siemens, April 2008, read in full for the passages cited. [P] ([copy hosted on cad.de](https://ww3.cad.de/foren/ubb/uploads/schulze/XT_Format_April_2008_tcm73-62642.pdf)) It describes the stored data model, which reveals a great deal about the kernel's design. It is 18 years old; later additions such as facet geometry are not in it.
- **Jackson 1995:** D. J. Jackson, "Boundary representation modelling with local tolerances", ACM Solid Modeling 1995. Written from inside the Parasolid team. [P] ([PDF](https://ftp1.cs.wisc.edu/pub/users/prem/jackson-SM-95.pdf))
- **Siemens interview:** Engineering.com, as above. [P, vendor statements]
- **Functional description:** an unofficial mirror of the Parasolid V35 (2022) documentation exists at q-solid.com. It could not be fetched from this session, so anything from it is marked [S] and comes from search summaries.

### Lineage

- Parasolid 1.0 was released in 1988 by Shape Data in Cambridge, superseding ROMULUS (1978), the first commercial B-rep modeller. [P] (Siemens interview)
- ROMULUS was single precision with analytic geometry only. Parasolid moved to double precision and added NURBS. [P] (same)
- "Models from Parasolid v1.0, and even ROMULUS, can still be loaded and used in the latest version." [P] (same)

That last statement describes more than thirty years of unbroken backward compatibility of the data format. It is part of what licensees buy, and it is a constraint the Parasolid team carries on every change.

### Topology

The XT reference describes a model that "can represent wireframe, surface, solid, cellular and general non-manifold models". [P]

- Entity hierarchy: body, region, shell, face, loop, fin, edge, vertex. A fin is one use of an edge by a face. [P]
- Regions are solid or void, which is how one body can hold several cells. [P]
- Body types include solid, sheet, wire, acorn (isolated points) and general. General bodies drop the manifold constraints. [P]
- Entities carry attributes, groups and node-ids. [P]

### Geometry

The stored geometry types are: [P] (XT reference, table of contents and type definitions)

| Curves | Surfaces |
|---|---|
| Line, circle, ellipse | Plane, cylinder, cone, sphere, torus |
| B-curve (NURBS) | B-surface (NURBS) |
| Intersection curve | Rolling-ball blend surface, and its boundary surface |
| SP-curve (a curve in a surface's parameter space) | Offset surface |
| Trimmed curve | Swept surface, spun surface |
| Foreign geometry | Foreign geometry |

Three things stand out.

**Analytic shapes are kept as analytic shapes.** A cylinder is stored as a cylinder, not as a NURBS approximation of one.

**Derived geometry is kept procedurally.** The clearest case is the intersection curve. The reference says:

> An intersection curve is one of the branches of a surface / surface intersection. Parasolid represents these curves exactly; the information held in an intersection curve node is sufficient to identify the particular intersection branch involved, to identify the behavior of the curve at its ends, and to evaluate precisely at any point in the curve.

What is stored is the two surfaces, the two end points, and a "chart": an ordered array of points that the reference describes as "a piecewise-linear (chordal) approximation to the true curve". The chart identifies the branch and gives a parameterisation; exact points are computed from the surfaces on demand. Blend, offset, swept and spun surfaces are likewise stored as a definition plus references to the geometry they derive from.

**Facet geometry was later added as one more surface type.** Siemens describes the decision: "After extensive prototyping, we decided to fully integrate facet data into Parasolid's data model and algorithms as a new surface type alongside analytics and NURBS. This is the most elegant technical solution, but also the most challenging to implement, as it involves enhancing every algorithm that handles surfaces." [P] (Siemens interview) Siemens calls this convergent modelling and has since extended it to bodies mixing facet and classic faces. [S] ([Siemens](https://news.siemens.com/nl-nl/parasolid-convergent-modeling-mixed-models/))

### Precision

- The XT reference records two session values with every file: the size box, "normally 1000", and the modeller linear precision, "normally 1.0e-8". [P]
- Points are treated as coincident "to Parasolid tolerance (1.0e-8 by default)". [P] (XT reference)

This is a fixed-resolution design: a bounded model space and one absolute resolution, eleven orders of magnitude apart. The unit is commonly stated to be the metre, which would mean a one-kilometre box resolved to ten nanometres. [U]

### Tolerant modelling

This is Parasolid's answer to numerical robustness, described by Jackson in 1995 as "a foundation on which reliable solid modelling can be built". [P]

The problem as Jackson states it: "Conventional boundary representation solid modellers perform all computations to a single global tolerance." No single value works, and "given that different modellers invariably operate to different modelling tolerances, global tolerances are also a major roadblock to the robust exchange of b-rep models between systems". [P]

The mechanism:

- An edge or vertex may carry its own tolerance. Without one it is "accurate and is regarded as having a tolerance of half the modeller linear resolution". [P] (XT reference)
- A tolerant edge has no 3D curve. Each fin carries an SP-curve on its own face, and those curves need only agree with each other to within the edge tolerance. [P] (XT reference)
- The Parasolid documentation's mental model is edges as tubes and vertices as spheres, with a vertex's tolerance at least as large as that of any edge meeting it. [S] (functional description, via search summary)

Jackson also explains why the alternatives were rejected. This matters to us because decision 0004 lists "exact or filtered predicates" among the candidate advantages of a new kernel. [P]

| Alternative | Jackson's objection |
|---|---|
| Exact rational arithmetic | "Suffers from the build-up of complexity of the numerical values", and "it may create small undesirable features in the model which do not correspond to any design intent" |
| Perturbing geometry to avoid ambiguous cases | "Creates small edges and faces, and removes coincidences which were probably intentional" |
| Symbolic reasoning about consistency | "The difficulty here is describing all the consistency requirements in the general case; so far this is limited to special cases" |

The second half of the objection to exact arithmetic is the important one. It is not about speed. In mechanical design, two faces that are nearly coplanar are almost always meant to be coplanar, and an exact method that faithfully reports a sliver between them gives a correct answer to the wrong question. Thirty years of faster hardware do not remove that objection.

This paper is from 1995 and from one side of the argument. The research literature on robust geometric computation since then has to be read in phase 3 before drawing a conclusion.

### Tracking

- Parasolid's modelling functions return tracking records describing how entities in the result relate to entities in the input. The documentation gives "tracking entities in a feature-based system" as a purpose. [S] (functional description and API reference, via search summary)
- The functional description has a section on "tag persistence during local operations". [S] Not read.

So the kernel reports what happened to topology in each operation, and the application builds persistent naming on top. This matches what Onshape's documentation implies (see [01-onshape.md](01-onshape.md)). The detail of what is reported for splits and merges was not obtained.

### Threading and session

- Parasolid has been thread-safe since V23 in 2010, letting several threads call any function concurrently. [S] ([press coverage](https://www.digitalengineering247.com/article/siemens-plm-software-delivers-parasolid-v23))
- It provides "session and partitioned rollback" as the basis for undo and history. [S] (Siemens product sheet, via search summary)

How much work inside a single operation runs in parallel was not established.

## ACIS

- The default modelling tolerance is 1e-6, coarser than Parasolid's 1e-8. [S] ([Sandia Cubit documentation](https://cubit.sandia.gov/files/cubit/17.10/help_manual/WebHelp/geometry/cleanup_and_defeaturing/geometry_accuracy.htm))
- ACIS also has tolerant edges and vertices, applied on import to curves that miss their surfaces by more than the default tolerance. [S] (same)
- The same source says to "expect parts that were not made with ACIS to have errors as large as 1E-3". [S]

Spatial's documentation is behind a login and was not read. CGM, Granite and ShapeManager were not researched beyond the market table.

## Persistent naming in the literature

- The foundational paper is J. Kripac, "A mechanism for persistently naming topological entities in history-based parametric solid models" (1997), built on a graph recording how faces originate and propagate. [S] ([Semantic Scholar](https://www.semanticscholar.org/paper/A-mechanism-for-persistently-naming-topological-in-Kripac/a5e40e5ac256c3d3c9beb7678ab9ffe6ac3d1e6f))
- A 2018 review classifies methods as topology-based, geometry-based or hybrid, and recommends combining the two: topology for the basic name, geometry to resolve ambiguity. [S] ([Farjana and Han](https://www.sciencedirect.com/science/article/pii/S1110016818300814))
- The same body of work identifies splitting and merging of topology as the source of ambiguity and treats it as an open problem. [S]

This is consistent with Onshape adding explicit handling for splits and merges, and it supports keeping [decision 0006](../../decisions/0006-geometry-references.md) open. None of these papers has been read in full.

## What is known about relative robustness

Very little that is measured.

- No published head-to-head benchmark of boolean or blend failure rates across kernels was found.
- One measured figure exists for OCCT, for a different operation. A 2025 dataset paper reports that OCCT's meshing fails on 1.56% of models in the ABC dataset and 8.82% of an assemblies dataset, and describes the algorithm as "not fully robust". [P] ([Better STEP, arXiv 2506.05417](https://arxiv.org/pdf/2506.05417))
- Developer forums contain many reports of OCCT boolean and fillet failures. These are anecdotes. [S]

Consequences:

1. The premise of decision 0004, that OCCT is well behind the commercial kernels, is plausible and widely believed but unmeasured. Phase 2 should measure OCCT on a public corpus rather than cite opinion.
2. A reproducible robustness benchmark does not exist publicly. Building one is a prerequisite for claiming anything about our own kernel, and would be a contribution in its own right.
3. Large public B-rep corpora exist to build it from. The ABC dataset holds one million CAD models with explicit curve and surface parameterisations. [P for the abstract] ([arXiv 1812.06216](https://arxiv.org/abs/1812.06216)) This also connects to the owner's point that reconstructing parametric models from STEP files will feed reinforcement-learning improvement of the kernel.

## Design inputs for phase 3

Each of these is a choice Parasolid made. Phase 3 has to decide, with evidence, whether to make the same choice.

| # | Parasolid's choice | Question for OpenShape |
|---|---|---|
| 1 | Keep analytic and derived geometry in exact procedural form; do not convert to NURBS | Almost certainly the same. Zoo also states "exact NURBS and analytic surfaces". What is the full set of procedural types, and how are they evaluated quickly? |
| 2 | Tolerant modelling: local tolerances on edges and vertices, in floating point | The central robustness decision. Tolerant, exact, or a hybrid such as exact predicates with tolerant construction? Jackson's design-intent objection must be answered, not just the performance one. |
| 3 | Fixed resolution: one absolute precision and a bounded model space | Fixed, or scale-relative? Fixed is simple and makes coincidence well defined. Its cost is a hard limit on the ratio of largest to smallest feature. |
| 4 | Facet data as a first-class surface type inside the B-rep | Relevant to the later mesh and scan scope. Siemens says retrofitting this meant "enhancing every algorithm that handles surfaces". Designing the surface abstraction to allow it from the start would avoid that retrofit. |
| 5 | Operations return tracking records; naming is the application's job | Where should the boundary sit? A kernel designed together with its feature system could carry identity natively. |

Two further inputs that are not about geometry:

- **Format stability.** Parasolid still loads files from 1988. For a local-first tool whose files live in users' repositories for decades, the equivalent promise needs to be designed for from the first file format.
- **Non-manifold and cellular topology** are in Parasolid's base model. Whether OpenShape's topology should be general from the start is a phase 3 question; it bears on multi-body modelling and on meshing for FEA.

## Gaps to close before this topic is complete

- Read the Parasolid functional description (tracking, blending, local operations, threading, facet geometry). The mirror was unreachable from this session.
- Blending in any depth. Nothing gathered beyond the existence of the rolling-ball blend surface type.
- Operation coverage per kernel: booleans, offsetting, shelling, lofting, sweeping, direct editing.
- CGM, Granite, ShapeManager and C3D technical detail.
- Effort and team size behind each kernel. Not found for Parasolid; Zoo reports fewer than 30 engineers over two years.
- The persistent-naming papers, read in full.
- Performance characteristics of any kernel.
