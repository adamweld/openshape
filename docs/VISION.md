# Vision

## Goal

Build a fully featured mechanical CAD program with most of the functionality of Onshape, designed to be exceptionally fast and extensible, and usable by both humans and AI agents as first-class users.

## Core hypothesis

Mechanical design has not taken off with AI the way software has because an agent cannot close the loop. In software an agent can write, run, test and revise. In mechanical design the equivalents of "run" and "test" (simulation, manufacturability checks, assembly checks) sit in separate tools, and the information they need (what a part is for, how it is loaded, how it will be made) lives in engineers' heads and is lost at every handoff.

OpenShape's hypothesis is that letting an AI close the loop of **design → simulated test → optimise** inside one platform is what unlocks AI-enabled mechanical design.

## Scope

Everything expected of a modern CAD program, without the inherited technical debt.

### Modelling

- Multi-body part modelling with complex features, including fillets and surfacing
- 2D sketches with constraints, dimensions and variables
- Assemblies with mate connectors
- Drawings
- Import and export of standard formats
- Integration with version control (whether that is git itself is [an open question](REGISTER.md))

### Reverse engineering

- **Initial:** creating parametric solid models from STEP files and similar imported solids, which arrive with no feature history. This serves two purposes: moving an existing project onto the platform, and supplying data for reinforcement-learning improvements to the kernel.
- **Later, much further down the road:** working quickly with mesh and scan data, and reverse engineering from scans.

### Lower priority and out of initial scope

- **Sheet metal** is in scope at low priority.
- **Real-time multi-user collaboration** is out of initial scope, with a constraint on the architecture. See [decision 0007](decisions/0007-real-time-collaboration.md).

### Platform features for AI

- Connectors that let AI agents drive the software
- A way to encode what is currently missing from the human-to-AI handoff:
  - standardised definition of **interfaces** between parts
  - **load paths** and load cases
  - **manufacturing methods** specified per part
  - hooks into **FEA** and **DFM** analysis and optimisation
  - the ability to **test** manufacturability and assembly, not just assert it

### Deployment

Local-first. See [decision 0002](decisions/0002-local-first.md).

## Build-versus-reuse stance

Write components from the ground up where existing open-source software is not at the state of the art. The working expectation is that this includes the geometric kernel, since OCCT is well behind the commercial kernels. That expectation is tested in research phases 1 and 2 before it is acted on. See [decision 0004](decisions/0004-ground-up-kernel.md).

## Human and AI interaction

Text alone is not enough for three-dimensional work. Selecting edges, faces and other geometry needs a visual mechanism that both humans and agents can use. How selections are made and how they are stored so they survive model changes is the subject of [decision 0006](decisions/0006-geometry-references.md), which is open.
