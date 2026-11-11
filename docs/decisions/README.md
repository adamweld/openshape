# Decisions

One file per decision, numbered in the order they were made. Statuses are defined in [PRINCIPLES.md](../PRINCIPLES.md). Anything not Settled also appears in [REGISTER.md](../REGISTER.md).

## Index

| # | Decision | Status |
|---|---|---|
| [0001](0001-license-mpl-2.0.md) | License is MPL-2.0 | Provisional |
| [0002](0002-local-first.md) | Deployment is local-first | Settled |
| [0003](0003-scope.md) | Product scope | Settled |
| [0004](0004-ground-up-kernel.md) | Whether to write the kernel from the ground up | Open |
| [0005](0005-single-operation-layer.md) | GUI and agents share one operation layer | Provisional |
| [0006](0006-geometry-references.md) | How geometry is selected and referenced | Open |
| [0007](0007-real-time-collaboration.md) | Real-time collaboration is deferred but protected | Settled |
| [0008](0008-benchmark-repository.md) | Benchmarks live in a separate, neutrally named repository | Settled |
| [0009](0009-kernel-choice-is-permanent.md) | The kernel choice is treated as permanent | Settled |

## Template

```markdown
# NNNN: Title

- **Status:** Settled | Provisional | Temporary | Open | Superseded by NNNN
- **Date:** YYYY-MM-DD
- **Decided by:** who

## Context

Why this needs deciding.

## Decision

What was decided. For an Open record, the competing positions.

## Alternatives considered

Each alternative and why it was not chosen.

## Evidence

Proof, benchmark, citation or owner's choice. Say plainly what is unverified.

## Revisit trigger or replacement requirement

Required unless Settled.
```
