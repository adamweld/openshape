# Roadmap

The project is in the research and design stage. Phases run one at a time, in order. Each phase writes its findings into its folder under [research/](research/) and ends with the decision records it supports.

No implementation roadmap exists yet. It is an output of phase 5.

| # | Phase | Status |
|---|---|---|
| 1 | State of the art | Complete: see [research/01-state-of-the-art](research/01-state-of-the-art/README.md). Open items carried forward in the [register](REGISTER.md) |
| 2 | Open-source landscape and gaps | In progress |
| 3 | Kernel foundations | Not started |
| 4 | Agent interface and engineering intent | Not started |
| 5 | System architecture | Not started |

## Phase 1: State of the art

Folder: [research/01-state-of-the-art/](research/01-state-of-the-art/)

What the best existing systems do and how, as far as public information allows.

- Geometric kernels: Parasolid, ACIS, CGM, C3D and others
- Constraint solvers: D-Cubed 2D and 3D DCM and competitors
- Onshape: architecture, FeatureScript, version model, mate connectors
- Other leading CAD systems where they do something better
- Simulation, DFM and optimisation tooling that a closed design loop would need to match or connect to
- Reverse-engineering tools
- Current AI-for-CAD efforts and where they fail

Exit: a written picture of the bar we have to clear, with every claim sourced or labelled as inference.

## Phase 2: Open-source landscape and gaps

Folder: [research/02-open-source-landscape/](research/02-open-source-landscape/)

What exists in the open, how good it is, and what we would have to write ourselves.

- Kernels and geometry libraries: OCCT, truck, Fornjot, Manifold, CGAL and others
- Constraint solvers: SolveSpace, planegcs and others
- CAD applications: FreeCAD, SolveSpace and others
- Meshing, FEA, CAM and DFM tooling
- File format support: STEP, IGES and others
- License compatibility of each candidate with MPL-2.0
- Measurement, carried from phase 1: OCCT failure rates on a public corpus, and rebuild behaviour where it can be run
- Licences and provenance of the public CAD datasets

Exit: a reuse-or-write verdict per component, with evidence. This confirms or overturns [decision 0004](decisions/0004-ground-up-kernel.md).

## Phase 3: Kernel foundations

Folder: [research/03-kernel-foundations/](research/03-kernel-foundations/)

The technical basis for a kernel, if phase 2 confirms we are writing one.

- Boundary representation and topology data structures
- Curve and surface representations: analytic, NURBS and procedural
- Numerical robustness: tolerant modelling, exact and filtered predicates, interval arithmetic
- Core algorithms: surface intersection, booleans, blending, offsetting, tessellation
- Persistent naming of topology across model changes
- Determinism and parallelism
- Test strategy: differential testing, fuzzing, benchmark corpora

Exit: a design basis for the kernel, with the unsettled trade-offs named.

## Phase 4: Agent interface and engineering intent

Folder: [research/04-agent-interface/](research/04-agent-interface/)

How an AI agent uses the software to do real engineering, and how engineering intent is encoded.

- How agents and humans select and reference geometry, including visual selection ([decision 0006](decisions/0006-geometry-references.md))
- The operation layer shared by the GUI and agents ([decision 0005](decisions/0005-single-operation-layer.md))
- What an agent needs to perceive: rendered views, measurements, diagnostics
- Encoding interfaces, load paths, load cases and manufacturing methods
- Connecting FEA and DFM so that manufacturability and assembly can be tested
- The design → test → optimise loop end to end

This phase is run as a dialogue with the project owner.

Exit: an interface specification and an intent model.

## Phase 5: System architecture

Folder: [research/05-architecture/](research/05-architecture/)

- Implementation language and build targets
- Document model and version control integration
- Component boundaries and the extension mechanism
- Rendering and UI stack
- Profiling methodology and performance budgets
- The implementation roadmap

Exit: an architecture document and a sequenced implementation plan.
