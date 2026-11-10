# 0003: Product scope

- **Status:** Settled
- **Date:** 2026-11-10
- **Decided by:** Project owner

## Context

"Most of the functionality of Onshape" needed pinning down before research could be scoped.

## Decision

In scope:

- Multi-body part modelling with complex features, including fillets and surfaces
- 2D sketches with constraints, dimensions and variables
- Assemblies with mate connectors
- Drawings
- Import and export
- Integration with version control
- Reverse engineering: initially, parametric solid models from STEP files and similar; mesh and scan data much later
- Sheet metal, at low priority
- AI connectors
- Encoding of engineering intent: interfaces, load paths, manufacturing methods
- Connections to FEA and DFM optimisation, and the ability to test manufacturability and assembly

The summary is "everything you would expect from modern CAD software, minus the technical debt", plus the features that make it a platform for AI-driven design. The full statement is in [VISION.md](../VISION.md).

## Alternatives considered

- **Core part modelling and assemblies first, the rest later.** Rejected as a definition of scope. Sequencing is a separate matter for the implementation roadmap in phase 5; the design must account for the full scope from the start.

## Evidence

Owner's product choice.

## Out of initial scope

- Real-time multi-user collaboration. See [decision 0007](0007-real-time-collaboration.md) for the constraint this still places on the architecture.

## Notes on reverse engineering

The owner gave two reasons for the initial form (parametric models from STEP and similar files): it is an important feature when moving a project onto the platform, and it will be critical for reinforcement-learning improvements to the kernel.
