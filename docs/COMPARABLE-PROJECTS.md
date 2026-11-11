# Comparable projects

A living register of projects and products that overlap with OpenShape. It serves two purposes:

- **Open-source projects**, so that work others have already done is found before it is repeated.
- **Commercial products**, because they set the bar. The owner's standard is that OpenShape is not good enough until it is at least as good as what is already on the market.

Add an entry when one is found; update a row when it is looked at more closely.

Repository facts (licence, stars, dates) were read from GitHub on 2026-11-10. Descriptions are the projects' own unless a deeper review is linked. "Reviewed" says how far anyone here has looked:

- **Listed**: found, description read.
- **Docs**: its documentation was read.
- **Measured**: it was run and measured here.

Before starting any component, check the row for it in the last section.

## The pattern to know about

Most of the projects started in 2026 were built largely by AI coding agents, quickly, by one person or a small team. Several publish their rules for agents. That is the same method OpenShape intends to use, so two things follow:

- Breadth is cheap now. A project listing fifty features after two months is normal. What nobody has shown is depth: whether those features hold up on hard cases. A trade article on these projects put it this way: "The barrier to entry is shifting from the kernel to the evidence." ([3D Printing Industry](https://3dprintingindustry.com/news/vibecoded-clones-of-solidworks-and-autocad-released-as-open-source-255770/))
- A project's own feature list is not evidence that the feature works. Only the measured rows below are.

## Parametric CAD applications

The closest comparables: a history-based modeller a person can use, mostly also drivable by an agent.

| Project | Licence | Started | Stars | Stack and kernel | Agents | Reviewed |
|---|---|---|---|---|---|---|
| [FreeCAD](https://github.com/FreeCAD/FreeCAD) | LGPL-2.1 | 2012 | 35.3k | C++ and Python on OCCT | Community MCP servers; scripting | Docs. [Notes](research/02-open-source-landscape/01-landscape.md) |
| [SolidCraft](https://github.com/tangency-labs/solidcraft) | Apache-2.0 or MIT | 2026-10 | 15.5k | Rust; truck and its own solidcore | Built-in MCP server, headless CLI, same commands as the GUI | Docs, in depth. [Notes](research/02-open-source-landscape/04-nearest-neighbours.md) |
| [Chili3D](https://github.com/xiangechen/chili3d) | AGPL-3.0 | 2022 | 5.0k | TypeScript in the browser, on OCCT | "AI-assisted" | Listed |
| [SolveSpace](https://github.com/solvespace/solvespace) | GPL-3.0 | 2015 | 4.2k | C++; its own small kernel and constraint solver | None | Docs |
| [Dune 3D](https://github.com/dune3d/dune3d) | GPL-3.0 | 2023 | 2.1k | C++ on OCCT, with SolveSpace's solver | None | Listed |
| [JSketcher](https://github.com/xibyte/jsketcher) | Not standard | 2016 | 1.8k | JavaScript | None | Listed |
| [Zoo Design Studio](https://github.com/KittyCAD/modeling-app) | MIT, app only | 2023 | 1.3k | TypeScript app; closed, hosted kernel | Built-in agent | Docs. [Notes](research/01-state-of-the-art/03-ai-and-new-entrants.md) |
| [QymCAD](https://github.com/QymIs-Tech/QymCAD) | AGPL-3.0 | 2026-08 | 0.9k | Rust on OCCT | Not checked | Listed |
| [PartMode](https://github.com/BOMWiki/partmode) | AGPL-3.0 | 2026-08 | 0.5k | Browser, on OCCT through replicad | "People and permissioned typed agents"; human and agent changes use the same path | Listed |
| [vcad](https://github.com/muni-works/vcad) | Apache-2.0 | 2026-01 | 0.4k | Rust and WebAssembly; its own kernel | "For the AI era"; a reinforcement-learning style interface to its physics | Docs |
| [materializr](https://github.com/materializr-cad/materializr) | GPL-3.0 | 2026-05 | 0.4k | C++; for makers | Not checked | Listed |
| [next.BREP](https://github.com/mmiscool/next.BREP.io_RUST_BREP_KERNEL) | **Not open source**: modifications must be assigned to the vendor | 2026-09 | 27 | Rust; its own kernel; mechanical and electronics CAD together | Built-in MCP server | Docs. [Notes](research/02-open-source-landscape/01-landscape.md) |
| [PaliCAD](https://github.com/braydennilsen/PaliCAD) | Not standard | 2026-09 | 0.3k | Dart; its own kernel; direct modelling | Not checked | Listed |
| [MitCad](https://github.com/mitcad/Mitcad) | MIT | 2026-10 | 0.2k | Rust | Not checked | Listed |
| [cadrs](https://github.com/rvdende/cadrs) | Apache-2.0 | 2026-09 | 0.1k | Rust with a Bevy interface; its own kernel; parts, assemblies and drawings | Not checked | Listed |

Worth a closer look, for specific reasons:

- **MitCad** says FreeCAD, Fusion (`.f3d`), SolidCraft and Inventor (`.ipt`) files "open with their history". Importing another system's feature history is a different route to the owner's migration requirement than reconstructing it from a STEP file. Unverified.
- **PartMode** states the same principle as [decision 0005](decisions/0005-single-operation-layer.md), and includes drawings.
- **cadrs** lists drawings alongside parts and assemblies on its own kernel.
- **next.BREP** is the only one combining mechanical and electronics design.

2D drafting only, listed for completeness: [CADCraft](https://github.com/storytold/cadcraft) (Apache-2.0, 7.9k stars, a sister project to SolidCraft), [OpenCADStudio](https://github.com/HakanSeven12/OpenCADStudio) (GPL-3.0), [LibreCAD](https://github.com/LibreCAD/LibreCAD).

## Kernels and geometry libraries

| Project | Licence | Started | Stars | What it is | Reviewed |
|---|---|---|---|---|---|
| [OCCT](https://github.com/Open-Cascade-SAS/OCCT) | LGPL-2.1 | 1990s | 3.2k | The long-standing full B-rep kernel | **Measured.** [Results](research/02-open-source-landscape/02-measurements.md) |
| [USD BRep / SMLib](https://github.com/NVIDIA-Omniverse/usd-brep) | Apache-2.0 | 2026-10, open | 2.1k | Commercial-lineage NURBS B-rep kernel from NVIDIA | **Measured.** Same |
| [truck](https://github.com/ricosjp/truck) | Apache-2.0 | 2020 | 1.7k | Modular Rust B-rep and NURBS kernel | Listed |
| [OpenGeometry](https://github.com/OpenGeometry-io/OpenGeometry) | MPL-2.0 | 2024 | 0.5k | Rust and WebAssembly kernel "for the web": exact B-rep, booleans, extrude, sweep, revolve, STEP export, "for humans and AI agents" | Listed |
| [solidcore](https://github.com/tangency-labs/solidcore) | Apache-2.0 | 2026-10 | 0.4k | Rust kernel that began as a port of SMLib; certified geometry by design | Docs, in depth. Not yet measured |
| vcad's kernel | Apache-2.0 | 2026-01 | | Rust B-rep with booleans, fillets, shell | Listed |
| [csgrs](https://github.com/timschmidt/csgrs) | MIT | 2025 | 0.3k | "Multi-modal exact geometric computation" kernel in Rust | Listed |
| [cad-kernel](https://crates.io/crates/cad-kernel) | MIT or Apache-2.0 | | | Rust kernel. On brep-bench: 263 of 346 pass, none wrong | Listed |
| [kentron](https://github.com/rsz269/kentron), [arris](https://github.com/arris-labs/arris), [geop](https://github.com/geop-cad/geop) | MIT or Apache-2.0 | | | Rust kernels with results on brep-bench | Listed |
| [popkern](https://github.com/popkern-dev/popkern), [Aetheris](https://github.com/yuechen-li-dev/Aetheris) | AGPL-3.0 | | | Kernels with their own modelling languages, with results on brep-bench | Listed |
| [cadcore](https://github.com/YATSKOVSKYI/cadcore) | MIT | 2026-05 | 48 | Pure-Rust B-rep with analytic surfaces | Listed |
| [brepkit](https://github.com/andymai/brepkit) | AGPL-3.0 | 2026-03 | 38 | Rust B-rep engine for brepjs | Listed |
| [Fornjot](https://github.com/hannobraun/fornjot) | Archived | 2021 | 2.5k | Shut down in June 2026: "its goals were never reached" | Docs |
| [Manifold](https://github.com/elalish/manifold) | Apache-2.0 | 2019 | 2.4k | Mesh booleans with guaranteed manifold output | Listed |
| [CGAL](https://github.com/CGAL/cgal) | GPL or LGPL by package | 1990s | 6.1k | Computational geometry with exact arithmetic; no NURBS B-rep | Listed |
| [PicoGK](https://github.com/leap71/PicoGK) | Apache-2.0 | 2023 | 1.2k | Voxel-based kernel for computational engineering | Listed |
| [libfive](https://github.com/libfive/libfive), [sdfx](https://github.com/deadsy/sdfx), [sdf](https://github.com/fogleman/sdf) | Mixed | | | Implicit, function-based modelling | Listed |
| [BRL-CAD](https://github.com/BRL-CAD/brlcad) | Mixed | 1980s | 1.0k | Constructive solid geometry system from the US Army | Listed |

OpenGeometry shares OpenShape's licence and part of its stated aim, and has not been looked at beyond its description. It should be read next.

## Code-first CAD

Models written as programs. These are what most AI-for-CAD research runs on.

| Project | Licence | Stars | Kernel | Reviewed |
|---|---|---|---|---|
| [OpenSCAD](https://github.com/openscad/openscad) | GPL | 10.6k | CGAL and Manifold; meshes | Listed |
| [CadQuery](https://github.com/CadQuery/cadquery) | Apache-2.0 | 6.1k | OCCT | Docs; the engine in most published benchmarks |
| [build123d](https://github.com/gumyr/build123d) | Apache-2.0 | 3.7k | OCCT | Listed |
| [CascadeStudio](https://github.com/zalo/CascadeStudio) | MIT | 1.5k | OCCT in the browser | Listed |
| [replicad](https://github.com/sgenoud/replicad) | MIT | 0.7k | OCCT in the browser | Listed |
| [FluidCAD](https://github.com/Fluid-CAD/FluidCAD) | MIT | 0.7k | JavaScript | Listed |
| [Cadova](https://github.com/tomasf/Cadova) | MIT | 0.4k | Swift | Listed |
| [brepjs](https://github.com/andymai/brepjs) | Apache-2.0 | 0.1k | "Exact B-Rep CAD in TypeScript", with a plugin that lets agents write parts and check them | Listed |

## AI agents and connectors for CAD

| Project | Licence | Stars | What it does | Reviewed |
|---|---|---|---|---|
| [text-to-cad](https://github.com/earthtojake/text-to-cad) | MIT | 26.0k | Installs skills into coding agents to "design physical products with AI" | Listed |
| [CADAM](https://github.com/Adam-CAD/CADAM) | GPL-3.0 | 5.4k | Open-source text-to-CAD web application | Listed |
| [solidworks-automation-skill](https://github.com/wzyn20051216/solidworks-automation-skill) | MIT | 1.9k | Skill and MCP toolkit for driving desktop CAD | Listed |
| [Multi-Agent-CAD](https://github.com/Pan-Chera/Multi-Agent-CAD) | MIT | 1.1k | Multi-agent text-to-CAD framework | Listed |
| [cad-skill](https://github.com/flowful-ai/cad-skill) | Not standard | 0.7k | Agent skill for 3D-printable parts with CadQuery | Listed |
| [smlibpy](https://github.com/awv-informatik/smlibpy) | MIT | 0.2k | Python modelling interface and MCP server on SMLib | Listed |
| [agentcad](https://github.com/jdilla1277/agentcad) | Apache-2.0 | 0.2k | "CAD CLI and MCP server for AI agents" | Listed |
| Onshape FeatureScript MCP server | Proprietary | | Agents write and test FeatureScript | Docs. [Notes](research/01-state-of-the-art/03-ai-and-new-entrants.md) |

text-to-cad has more stars than any CAD application here except FreeCAD and has not been examined. It should be read next: its skills encode how someone else gets agents to do mechanical design today.

## Constraint solvers

| Project | Licence | Notes | Reviewed |
|---|---|---|---|
| SolveSpace's solver | GPL-3.0 | Numerical; available as a library | Docs |
| planegcs, from FreeCAD | LGPL-2.1 | 2D numerical solver | Docs |
| [ezpz](https://github.com/KittyCAD/ezpz) | MIT | Zoo's solver, in Rust | Docs |
| [CAD Sketcher](https://github.com/hlorus/CAD_Sketcher) | GPL-3.0 | Constraint sketching for Blender, on SolveSpace's solver | Listed |
| The solvers inside SolidCraft, cadrs and vcad | Apache-2.0 | Not examined | Listed |

## Recognition, reconstruction and conversion

| Project | Licence | What it does | Reviewed |
|---|---|---|---|
| [quiddity](https://github.com/pzfreo/quiddity) | Apache-2.0 | Deterministic feature recognition from STEP; revision comparison; AP242 tolerances | **Measured**: exact on 60 generated parts. [Results](research/02-open-source-landscape/02-measurements.md) |
| [stl2step](https://github.com/BlinkingSun/stl2step) | Not standard | Mesh to B-rep solid, on OCCT | Listed |
| [cadmpeg](https://github.com/cadmpeg/cadmpeg) | Apache-2.0 | "Convert all CAD formats" | Listed |
| MitCad's importers | MIT | Other systems' files opened with their history | Listed |

## Commercial and closed-source products

These set the bar. What is known about each is in phase 1; this table says what each is the reference for and how it could be measured.

### CAD systems

| Product | Vendor | Kernel and solver | The reference for | Reviewed |
|---|---|---|---|---|
| Onshape | PTC | Parasolid, D-Cubed | The functional reference for OpenShape: document model, FeatureScript, branching, mate connectors, cloud collaboration | Docs, in depth. [Notes](research/01-state-of-the-art/01-onshape.md) |
| Zoo Design Studio | Zoo | Its own, GPU-based, hosted | A new kernel with a code-backed model and a built-in agent | Docs. [Notes](research/01-state-of-the-art/03-ai-and-new-entrants.md) |
| SOLIDWORKS | Dassault Systèmes | Parasolid, D-Cubed | The most widely used mid-range system; feature recognition on imported bodies | Listed |
| Fusion | Autodesk | ShapeManager | CAD, CAM, simulation and generative design in one product; the timeline model | Listed |
| NX | Siemens | Parasolid, D-Cubed | Large assemblies; direct editing (synchronous technology); mesh and solid in one model | Listed |
| Solid Edge | Siemens | Parasolid, D-Cubed | Direct editing | Listed |
| Creo | PTC | Granite | High-end parametric modelling | Listed |
| CATIA | Dassault Systèmes | CGM | High-quality freeform surfacing | Listed |
| Inventor | Autodesk | ShapeManager | Mid-range parametric modelling | Listed |
| Shapr3D | Shapr3D | Parasolid, D-Cubed | Interaction design on the same kernel as the incumbents | Listed |
| Plasticity | Plasticity | Parasolid | Direct modelling and interaction design | Listed |
| nTop | nTop | Its own, implicit | Implicit modelling for lattices and field-driven design | Listed. [Notes](research/01-state-of-the-art/05-other-cad-systems.md) |

### Components

| Component | Vendor | The reference for | Reviewed |
|---|---|---|---|
| Parasolid | Siemens | Kernel robustness and breadth | Documentation read in depth. [Notes](research/01-state-of-the-art/08-parasolid-in-depth.md) |
| ACIS, CGM | Dassault Systèmes, through Spatial | Alternative commercial kernels | Listed |
| C3D | C3D Labs | A commercial kernel written since 1995 | Listed |
| D-Cubed 2D and 3D DCM | Siemens | Constraint solving for sketches and assemblies | Docs. [Notes](research/01-state-of-the-art/04-constraint-solvers.md) |
| D-Cubed CDM, HLM | Siemens | Collision and clearance; hidden-line views for drawings | Listed |

### Analysis, manufacturability and reverse engineering

| Product | The reference for | Reviewed |
|---|---|---|
| Onshape Simulation | Analysis set up from assembly mates, with no meshing step shown | Docs |
| Ansys Discovery | Near-real-time simulation on a GPU | Listed |
| Altair SimSolid, Intact.Simulation | Structural analysis without meshing | Docs. [Notes](research/01-state-of-the-art/06-simulation-dfm.md) |
| aPriori, Protolabs, Xometry | Automated manufacturability and cost feedback | Listed |
| Geomagic Design X | Scan to parametric CAD | Listed |

### What "at least as good" has to mean

"As good as the market" is not one number. For each area, the comparison that matters:

| Area | Compared against | How |
|---|---|---|
| Kernel robustness | Parasolid, through a product that uses it | The benchmark suite of [decision 0008](decisions/0008-benchmark-repository.md), run through that product's scripting interface, where its terms allow |
| Constraint solving | D-Cubed, through a product that uses it | The solver benchmark proposed in phase 2B |
| Reference survival after edits | Onshape, SOLIDWORKS, Fusion | The reference-survival benchmark designed in phase 2B |
| Feature coverage | Onshape's feature list | A checklist, feature by feature |
| Rebuild and large-assembly speed | Any of the above | Timed rebuilds of the same model |
| Agent usability | Zoo's agent; Onshape's MCP server | The public agent benchmarks, with OpenShape as the engine |

### A constraint on measuring commercial products: their terms of use

This needs the owner's attention before any commercial product is run for comparison.

**Onshape.** Its terms of use, read on 2026-11-11, say a user shall not: ([terms](https://www.onshape.com/en/legal/terms-of-use))

> Analyze the Service, Software or Documentation for purposes competitive to Onshape, or access or otherwise use the Service, Software or Documentation in order to build a similar or competitive service offering

and separately bar using "any robot, spider, scraper or other automated means to access the Service". Access other than through the unmodified client is also subject to a separate API agreement, which was not read.

**Zoo.** Its terms bar reverse engineering and access by automated tools "other than software or Services features provided by" Zoo. No clause against competitive analysis or publishing benchmarks was found in the passages read. Its API and MCP server are offered features, billed per use. The whole document was not read. ([terms](https://zoo.dev/terms-and-conditions))

What this means in practice:

- **Running OpenShape's benchmarks through Onshape, under an Onshape account, would be using the service to build a competitor.** That is what the terms prohibit. It should not be done without legal advice or Onshape's permission.
- Phase 1's research on Onshape used only public web pages and documentation, read without an account. Whether the clause on "Documentation" reaches a reader who never accepted the terms is a legal question this project has not had answered. If the owner holds an Onshape account, the owner has accepted them.
- This is very likely why SolidCraft's rules say its contributors may "never drive or take data from commercial CAD" and may observe one only "as a black box".
- Other vendors' licences commonly contain similar clauses, and some forbid publishing benchmark results at all. Each must be read before its product is measured.

Routes that do not depend on a vendor's permission:

1. **Published results by others.** Papers and independent reviews that report a commercial product's behaviour.
2. **Files, not services.** Models that users have exported to STEP are the user's own content. Their quality can be measured without touching the product.
3. **The feature bar from public documentation**, as phase 1 did, subject to the legal question above.
4. **Asking.** A vendor may agree to have its kernel run on a neutral public benchmark. A benchmark that does not carry a competitor's name is easier to say yes to, which is a further reason for decision 0008.
5. **Licensing a kernel for evaluation.** Siemens and Spatial sell evaluation licences; their terms would govern what can be published.

## Benchmarks and test data

Covered in [phase 2B](research/02b-benchmarks-and-datasets/README.md). The reusable ones: [brep-bench](https://github.com/bmander/brep-bench) (346 kernel cases with results for 13 kernels; [notes](research/02b-benchmarks-and-datasets/03-brep-bench.md)), the [SSI corpus](https://github.com/jyviko/ssi-corpus), Parametric CAD Bench, Hephaestus-CCX, and the Zero-to-CAD dataset.

## Check here before building

| Component | Look at first | Why |
|---|---|---|
| Kernel | solidcore, OCCT, SMLib, OpenGeometry, truck | Two are measured; the decision waits on benchmark coverage ([decision 0004](decisions/0004-ground-up-kernel.md)) |
| Persistent naming | SolidCraft's naming design; FreeCAD's algorithm | The only two described in detail |
| Agent interface | SolidCraft's MCP tools; PartMode; text-to-cad's skills | SolidCraft's already covers schemas, transactions, assertions, structured topology and screenshots |
| Constraint solver | ezpz, SolidCraft's, cadrs's | Permissively licensed and in Rust |
| Feature recognition | quiddity | Measured, exact on easy cases |
| Importing models with history | MitCad | Claims to do it for four formats |
| Mesh to solid | stl2step, next.BREP's reconstruction | For the later scan scope |
| Drawings | PartMode, cadrs, FreeCAD's TechDraw | The open implementations that exist |
| Sheet metal | SolidCraft, next.BREP | Both list it |
| Mechanical with electronics | next.BREP | Reference reading only, because of its licence |
| Structural analysis in the loop | Hephaestus-CCX's harness; StructBench | Working loops, assembled from separate tools |
| Benchmarks | brep-bench; the SSI corpus; phase 2's instruments | brep-bench already holds a curated case library and results for 13 kernels |

## Not yet looked for

- Projects hosted outside GitHub.
- Projects not described in English. Several Chinese-language efforts exist, and one survey paper cites national policy as a driver.
- Open-source CAM.
- University research kernels.
