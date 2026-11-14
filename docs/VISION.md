# Vision

## Goal

Build a fully featured mechanical CAD program with most of the functionality of Onshape, designed to be exceptionally fast and extensible, and usable by both humans and AI agents as first-class users.

## The bar

OpenShape is not good enough until it is at least as good as what is already on the market, commercial products included. Open-source projects show what can be reused; commercial ones set the standard to meet. Both are tracked as part of the project's research.

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
- Integration with version control (whether that is git itself is an open question)

### Reverse engineering

- **Initial:** creating parametric solid models from STEP files and similar imported solids, which arrive with no feature history. This serves two purposes: moving an existing project onto the platform, and supplying data for reinforcement-learning improvements to the kernel.
- **Later, much further down the road:** working quickly with mesh and scan data, and reverse engineering from scans.

### Lower priority and out of initial scope

- **Sheet metal** is in scope at low priority.
- **Direct editing** (changing faces of a solid without relying on feature history) is in scope, not at high priority. It is an expected feature of any serious CAD system.
- **Real-time multi-user collaboration** is out of initial scope, with a constraint on the architecture.

### Platform features for AI

- Connectors that let AI agents drive the software
- A way to encode what is currently missing from the human-to-AI handoff:
  - standardised definition of **interfaces** between parts
  - **load paths** and load cases
  - **manufacturing methods** specified per part
  - hooks into **FEA** and **DFM** analysis and optimisation
  - the ability to **test** manufacturability and assembly, not just assert it

### Deployment

Local-first.

## Build-versus-reuse stance

Reuse existing open-source components where they are at the state of the art, and write from the ground up where they are not. Whether that includes the geometric kernel is being decided on measured evidence. The measurements are public: see [cadkernelbench](https://github.com/adamweld/cadkernelbench) and [brep-bench](https://github.com/bmander/brep-bench).

## Human and AI interaction

Text alone is not enough for three-dimensional work. Selecting edges, faces and other geometry needs a visual mechanism that both humans and agents can use. How selections are made and how they are stored so they survive model changes is an open design question.
