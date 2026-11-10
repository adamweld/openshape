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
- Solid-model reverse-engineering features
- AI connectors
- Encoding of engineering intent: interfaces, load paths, manufacturing methods
- Connections to FEA and DFM optimisation, and the ability to test manufacturability and assembly

The summary is "everything you would expect from modern CAD software, minus the technical debt", plus the features that make it a platform for AI-driven design. The full statement is in [VISION.md](../VISION.md).

## Alternatives considered

- **Core part modelling and assemblies first, the rest later.** Rejected as a definition of scope. Sequencing is a separate matter for the implementation roadmap in phase 5; the design must account for the full scope from the start.

## Evidence

Owner's product choice.

## Not yet specified

- Sheet metal, and real-time multi-user collaboration, were raised and not explicitly answered. Treat as unspecified until the owner says.
- The boundary of "reverse engineering" is listed as open in [REGISTER.md](../REGISTER.md).
