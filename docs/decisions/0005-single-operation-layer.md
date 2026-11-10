# 0005: GUI and agents share one operation layer

- **Status:** Provisional
- **Date:** 2026-11-10
- **Decided by:** Proposed by Claude; owner agreed in general terms with the AI-usage suggestions, apart from geometry references (see [0006](0006-geometry-references.md))

## Context

In most CAD systems the scripting interface is a second-class path that lags the GUI. If agents are first-class users, anything a human can do must be available to an agent, and the reverse.

## Decision

The GUI and the agent interface are two clients of one operation layer. Neither has a privileged path. Associated working positions, each to be tested in phase 4:

- The model's source of truth is deterministic and diffable.
- Failures are diagnostic: they say what failed, where and why, in a form an agent can act on.
- Introspection is cheap: measurement, mass properties, interference checks, rendered views, and fast headless evaluation.
- Design intent is checkable: requirements are assertions the system can evaluate.
- Speculative exploration is cheap, through branching.

## Alternatives considered

- **GUI-first with a scripting API added on.** The pattern in existing CAD; produces the second-class path this decision exists to avoid.
- **Code-first with a viewer** (the CadQuery or OpenSCAD pattern). Works for agents on simple parts but gives humans a poor direct-manipulation experience, and the owner's position is that text alone does not suffice in three dimensions.

## Evidence

Reasoned position, not yet evidenced. Phase 1 surveys how current AI-for-CAD attempts fail; phase 4 tests these positions against real engineering tasks.

## Revisit trigger

End of phase 4.
