# 0007: Real-time collaboration is deferred but protected

- **Status:** Settled
- **Date:** 2026-11-10
- **Decided by:** Project owner

## Context

Onshape's defining feature is several users editing the same model at once. OpenShape is local-first ([decision 0002](0002-local-first.md)), which makes this harder, and the question was whether it is in scope.

## Decision

Real-time multi-user collaboration is out of initial scope.

Architectural decisions must not imperil adding it later, unless the decision that would do so gives a large performance benefit.

## How to apply this

- Any design document that touches the document model, the change representation, undo, or identity of features and geometry states whether it keeps real-time collaboration possible.
- A design that would close it off needs a measured performance case, recorded in its own decision record. "Large" is the owner's call.

## Alternatives considered

- **In scope from the start.** Rejected for the initial product.
- **Out of scope with no constraint.** Rejected: retrofitting collaboration onto a data model not designed for it is the failure Onshape describes in older CAD systems (see [research](../research/01-state-of-the-art/01-onshape.md)).

## Evidence

Owner's product choice. Phase 1 research records how Onshape's design achieves collaboration: an immutable chain of semantic changes that can be applied to a state other than the one they were made against.
