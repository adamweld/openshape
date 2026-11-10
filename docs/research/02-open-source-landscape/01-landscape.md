# Open-source landscape

Evidence marks are as in phase 1: **[P]** primary source read, **[S]** secondary or summary, **[U]** unverified. Repository facts (licence, stars, dates) were read from GitHub on 2026-11-10 and are [P] for that date.

## Summary

The landscape changed in October 2026, after the project's assumptions were formed, in three ways that bear directly on [decision 0004](../../decisions/0004-ground-up-kernel.md):

1. **A commercial-lineage kernel is now open source under a permissive licence.** NVIDIA published SMLib, a long-established commercial NURBS B-rep kernel, as "USD BRep" under Apache-2.0 on 2026-10-08, with booleans, fillets, sweeps, offsets, healing and a Python package.
2. **A project very close to OpenShape's vision exists and is moving fast.** SolidCraft is an Apache-2.0 parametric CAD application in pure Rust, with desktop, browser, headless CLI and MCP server "all running the same commands". Its kernel, solidcore, began as a Rust port of SMLib and has a published robustness design based on certified approximations.
3. **Writing a B-rep kernel from scratch has become common.** At least eight new Rust kernels or kernel-based CAD applications were started in 2026.

The premise "OCCT is the only open option, and it is far behind" no longer describes the field. Whether OCCT is behind is measured in [02-occt-measurement.md](02-occt-measurement.md). What OpenShape should do in response is the owner's decision and is set out in [03-verdicts.md](03-verdicts.md).

## Kernels and geometry libraries

| Project | Licence | Language | Started | Last push | Stars | What it is |
|---|---|---|---|---|---|---|
| [OCCT](https://github.com/Open-Cascade-SAS/OCCT) | LGPL-2.1 | C++ | 1990s | 2026-11-10 | 3.2k | The long-standing full B-rep kernel. Version 8.0 in 2026 |
| [USD BRep / SMLib](https://github.com/NVIDIA-Omniverse/usd-brep) | Apache-2.0 | C++ | published 2026-10 | 2026-10-22 | 2.1k | Commercial-lineage NURBS B-rep kernel, newly open |
| [solidcore](https://github.com/tangency-labs/solidcore) | Apache-2.0 | Rust | 2026-10 | 2026-11-10 | 0.4k | Rust kernel that began as a port of SMLib |
| [truck](https://github.com/ricosjp/truck) | Apache-2.0 | Rust | 2020 | 2026-11-02 | 1.7k | Modular B-rep and NURBS kernel |
| [vcad](https://github.com/muni-works/vcad) | Apache-2.0 | Rust | 2026-01 | 2026-11-10 | 0.4k | B-rep kernel and CAD app, browser-first |
| [Fornjot](https://github.com/hannobraun/fornjot) | (archived) | Rust | 2021 | 2026-06-19 | 2.5k | Shut down; see below |
| [Manifold](https://github.com/elalish/manifold) | Apache-2.0 | C++ | 2019 | 2026-11-10 | 2.4k | Mesh booleans with guaranteed manifold output; not B-rep |
| [CGAL](https://github.com/CGAL/cgal) | GPL / LGPL by package | C++ | 1990s | 2026-11-05 | 6.1k | Computational geometry algorithms with exact arithmetic; no NURBS B-rep |
| [libfive](https://github.com/libfive/libfive) | MPL-2.0 / GPL parts [U] | C++ | 2015 | 2026-10-16 | 1.7k | Implicit (function-based) modelling |
| [SISL](https://github.com/SINTEF-Geometry/SISL) | AGPL-3.0 | C | 2013 | 2026-09-21 | 0.2k | NURBS library including surface intersection |
| [OpenNURBS](https://github.com/mcneel/opennurbs) | permissive [U] | C++ | 2018 | 2026-11-10 | 0.6k | Reads and writes Rhino files; geometry types without modelling operations |

Smaller 2026 entrants seen in search, not assessed: cadcore, brepkit (AGPL-3.0), kerf, rusted-geom, and the kernels inside the cadrs and Mitcad applications.

### OCCT

- Version 8.0.0 is described by its maintainers as the largest release in years, with more than 500 changes since 7.9, a move to C++17, exception and memory handling aligned with standard C++, and a move to a modern test framework. [S] ([release notes](https://dev.opencascade.org/content/open-cascade-technology-800-release))
- The 8.0.1 notes report one benchmark, a part with 2,000 holes, improving from 9.21 to 1.11 seconds. [S]
- It is under active modernisation, which matters for any comparison: opinions formed against 7.x may be out of date.
- LGPL-2.1 allows linking from MPL-2.0 code. It is the most restrictive licence among the serious candidates, and SolidCraft forbids its contributors from even reading it, to keep its own code clean-room. [P] ([SolidCraft AGENTS.md](https://github.com/tangency-labs/solidcraft/blob/main/AGENTS.md))

### USD BRep (SMLib)

From its README. [P] ([NVIDIA-Omniverse/usd-brep](https://github.com/NVIDIA-Omniverse/usd-brep))

- "The SMLib kernel ... creates and edits BRep solids, with booleans, fillets, sweeps and offsets", plus a healer, a tessellator and a validity checker.
- Faces and edges "can be NURBS or analytic geometry".
- A Python package is published for Linux and Windows.
- The repository includes guidance written for coding agents: what each error code means and how to fix it, and a guide per operation area.
- "This project is currently not accepting contributions." Copyright runs from 2020 to 2026.
- It includes converters to and from OCCT.

SMLib was a commercial kernel from Solid Modeling Solutions, listed in phase 1's kernel table. Its quality relative to Parasolid or OCCT is not established here. It could not be measured in this session: installing the package was blocked by the session's safety policy, pending the owner's approval.

What matters for OpenShape: this is a complete kernel, with a commercial history, under a licence compatible with MPL-2.0, that can be read, forked and learned from without restriction.

### solidcore and SolidCraft

From their READMEs, roadmap and design documents. [P] ([solidcore](https://github.com/tangency-labs/solidcore), [SolidCraft](https://github.com/tangency-labs/solidcraft))

**SolidCraft** describes itself as "an open-source parametric 3D CAD application built in pure Rust". The repository was created on 2026-10-07 and had 15.5k stars a month later.

| Aspect | What SolidCraft states |
|---|---|
| Features | Sketches with its own constraint solver; extrude, revolve, sweep, loft, fillet, chamfer, shell, draft, holes, threads, patterns on a parametric timeline; parameters and configurations; assemblies with joints and interference; sheet metal; STEP and other formats |
| Interfaces | "Desktop app, browser app, headless CLI and MCP server, all running the same commands" |
| Maturity | "Early but usable for simple parts" |
| Correctness evidence | 90 reference parts checked against analytic values or against FreeCAD run as an external program |
| Naming | "Faces and edges keep their names through edits", named "from their exact kernel-reported history" |
| Rules | Clean-room; no GPL or LGPL code, "not even reading it"; no panics on hostile input; "everything is a command"; model decisions use exact geometry, never a mesh |
| Architecture | Layered crates: geometry, then sketch solver and kernel, then document and timeline with "incremental evaluation", then file formats, then a command engine, then UI and MCP |

**solidcore** states its goals as "no `unsafe` in the kernel, no panics on bad input, deterministic results, no global state (one `Kernel` per thread)", WebAssembly builds, "and exact or certified geometry". Its status: "Every SMLib kernel module has a Rust counterpart ... Integration remains in progress: deferred paths still limit coverage."

Its robustness design is the most relevant technical document found in either phase so far: [P] ([definitions and certificates](https://github.com/tangency-labs/solidcore/blob/main/docs/definitions-and-certificates.md))

- "A surface is its definition S", evaluated on demand, such as a rolling-ball blend between two supports. This is the procedural representation phase 1 found in Parasolid.
- "Its B-spline B is a certified approximation of S, never the truth." B is stored beside S with a bound that "is proved", using interval methods: "a check that samples points is not a certificate".
- "A construction that cannot be proved within its bound is refused, naming the size that would build; a tolerance is never widened to let it pass."
- Final answers are solved on S, so approximation error does not stack across operations.

Set against phase 1's findings, this design answers three of the weaknesses recorded for Parasolid: tolerance that ratchets upward, failures that return no usable information, and non-determinism. It is a design document and a young implementation; no robustness measurement of it was found or made.

Overlap with OpenShape's recorded decisions:

| OpenShape position | SolidCraft |
|---|---|
| Local-first ([0002](../../decisions/0002-local-first.md)) | Yes, with a browser build as well |
| One operation layer for GUI and agents ([0005](../../decisions/0005-single-operation-layer.md)) | Yes, as a stated hard rule |
| Deterministic, diffable model | Deterministic results stated; file format not examined |
| Diagnostic failures | Refusals that name a size that would work |
| Sheet metal, assemblies, direct editing, drawings | Sheet metal and assemblies present; drawings and direct editing not examined |
| Engineering intent: interfaces, load paths, manufacturing method | Not found |
| Closed loop with FEA and DFM | Rigid-body dynamics present; no FEA or DFM found |
| Reconstruction of parametric models from STEP | Not found; see quiddity below for recognition |
| Agent perception and selection of geometry | Not examined |

### truck, vcad, Fornjot

- **truck** provides B-rep topology, NURBS geometry, booleans on solids and shape healing in separate crates. A secondary source says it supports only single-edge fillets. [S] ([CADFrontier](https://cadfrontier.com/articles/occt-open-source-cad-kernel?lang=en)) SolidCraft uses truck inside its kernel boundary alongside solidcore. [P] A fork, monstertruck, adds further features. [S]
- **vcad** lists primitives, booleans, fillets, chamfers and shell, constraint sketching, assemblies, STEP import, a physics simulation with "gym-style RL interface", and cloud sync. [P, README] It calls itself "open-source parametric CAD for the AI era".
- **Fornjot** was archived on 2026-06-19 with the notice: "This project has been shut down. Its goals were never reached." [P, README] It ran for about five years as a largely single-developer effort with reliability as its stated first principle. It is the clearest cautionary case in the field.

### Mesh and implicit libraries

- **Manifold** computes booleans on triangle meshes with a guarantee of manifold output. It is not a B-rep kernel but is the reference for robust mesh booleans, and is relevant to the later mesh and scan scope.
- **CGAL** offers exact arithmetic kernels and many algorithms, under GPL for most packages relevant here, which would bring the GPL into any distribution that links them.

## Constraint solvers

| Project | Licence | Language | Notes |
|---|---|---|---|
| [SolveSpace](https://github.com/solvespace/solvespace) | GPL-3.0 | C++ | Constraints as symbolic equations solved "by a modified Newton's method"; when several solutions exist, the sketch's initial position picks one. [S] ([SolveSpace](https://solvespace.com/tech.pl)) Available as a library |
| planegcs (FreeCAD) | LGPL-2.1 | C++ | 2D solver using DogLeg by default, with Levenberg-Marquardt and BFGS as alternatives. [S] ([planegcs](https://github.com/Salusoft89/planegcs)) |
| [ezpz](https://github.com/KittyCAD/ezpz) | MIT | Rust | Zoo's solver, opened in 2025. Small; a Newton-type core with degree-of-freedom analysis in progress. [S] |
| SolidCraft's solver | Apache-2.0 | Rust | Part of the application; not examined |

None of these is documented as using the graph decomposition that phase 1 found to be the basis of the commercial solvers. All found are numerical solvers started from the current sketch position. [S] That is consistent with phase 1's reading that the behavioural qualities of a solver, not the solving, are where the commercial product is ahead.

## Applications

| Project | Licence | Kernel | Notes |
|---|---|---|---|
| [FreeCAD](https://github.com/FreeCAD/FreeCAD) | LGPL-2.1 | OCCT | The established open CAD system. Version 1.0 shipped a mitigation for the topological naming problem; see below |
| [SolidCraft](https://github.com/tangency-labs/solidcraft) | Apache-2.0 | solidcore, truck | See above |
| [CadQuery](https://github.com/CadQuery/cadquery), [build123d](https://github.com/gumyr/build123d) | Apache-2.0 | OCCT | Code-first CAD in Python. The libraries used by the research in phase 1 |
| [Zoo Design Studio](https://github.com/KittyCAD/modeling-app) | MIT (app only) | Closed, hosted | See phase 1 |
| [OpenSCAD](https://github.com/openscad/openscad) | GPL | CGAL, Manifold | Code-first, mesh-based |

### FreeCAD and the topological naming problem

- FreeCAD 1.0 was the first stable release with a new naming algorithm, developed over years in a fork by one contributor and then merged. [S] ([FreeCAD wiki](https://wiki.freecad.org/Topological_naming_problem))
- The wiki states the algorithm "is not intended to fix every failure" caused by naming ambiguity, and users describe it as "a mitigation, not a full solution", with fillets and chamfers made mid-design still fragile. [S]

This is direct evidence for [decision 0006](../../decisions/0006-geometry-references.md), from the open-source side: a decade-long problem in the leading open CAD system, mitigated but not solved, on a kernel that reports limited lineage.

## Feature recognition

- [quiddity](https://github.com/pzfreo/quiddity) (Apache-2.0, Rust, started 2026-10) finds "holes, pockets, slots, bosses, steps, fillets, patterns" in a STEP model "from the B-rep geometry alone, with no CAD system", deterministically, matches features between two revisions of a part, and reads and writes AP242 tolerances and datums. [P, README]

This is the recognition half of the owner's reverse-engineering requirement, available under a compatible licence. It recognises features; it does not build an editable feature tree.

## Meshing, analysis and formats

| Project | Licence | Use | MPL-2.0 compatibility |
|---|---|---|---|
| [fTetWild](https://github.com/wildmeshing/fTetWild) | MPL-2.0 | Robust tetrahedral meshing | Same licence |
| gmsh | GPL-2.0+ | General meshing; used by the research in phase 1 | Linking brings the GPL; usable as a separate program |
| [netgen](https://github.com/NGSolve/netgen) | LGPL-2.1 | Meshing | Linkable |
| [MFEM](https://github.com/mfem/mfem) | BSD-3-Clause | Finite element library | Compatible |
| [dolfinx](https://github.com/FEniCS/dolfinx) | LGPL-3.0 | Finite element framework | Linkable |
| [CalculiX](https://github.com/Dhondtguido/CalculiX) | GPL-2.0 | Structural FEA solver | Separate program only |
| [STEPcode](https://github.com/stepcode/stepcode) | BSD-style [U] | STEP schema tooling | Compatible |
| [ruststep](https://github.com/ricosjp/ruststep) | Apache-2.0 | STEP parsing in Rust; last push 2025-03 | Compatible |
| [wgpu](https://github.com/gfx-rs/wgpu) | Apache-2.0 / MIT | Graphics API | Compatible |

No open-source solver of the meshless or immersed kind described in phase 1 was looked for yet.

## Dataset licences

Checked at source on 2026-11-10. [P]

| Dataset | Licence as stated by its publisher | Consequence |
|---|---|---|
| ABC | "The copyright of the CAD models is owned by their creators", with a pointer to Onshape's terms of use. The models came from public Onshape documents. ([ABC](https://deep-geometry.github.io/abc-dataset/)) | No licence is granted by the dataset itself. Rights rest with a million individual authors under Onshape's terms. Unsuitable to redistribute or to build a shipped corpus on without legal advice |
| DeepCAD | "Parsed from Onshape public documents with links from ABC dataset". No separate licence stated. ([DeepCAD](https://github.com/ChrisWu1997/DeepCAD)) | Same position as ABC |
| Fusion 360 Gallery | "Only for non-commercial research purposes", revocable by Autodesk at any time, with an indemnity. ([licence](https://github.com/AutodeskAILab/Fusion360GalleryDataset/blob/master/LICENSE.md)) | Research measurement only; nothing derived from it can ship |
| Zero-to-CAD | Apache-2.0. Synthetic CadQuery programs. ([dataset card](https://huggingface.co/datasets/ADSKAILab/Zero-To-CAD-1M)) | Usable. One million executable programs with operations beyond sketch and extrude |

So the only large corpus that is clean to build on is synthetic. Two sources of test and training data carry no licence doubt: generated cases, as in [02-occt-measurement.md](02-occt-measurement.md), and Zero-to-CAD. Zero-to-CAD's programs are CadQuery code, so using them means either running CadQuery on OCCT to produce STEP files or translating the programs into our own operations.

## Not yet covered

- CAM libraries.
- Rendering beyond wgpu.
- Open-source meshless or immersed analysis.
- Code-level reading of solidcore, SMLib, truck or vcad. Everything above is from project documentation.
- Measurement of any kernel other than OCCT.
