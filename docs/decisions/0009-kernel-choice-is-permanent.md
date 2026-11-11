# 0009: The kernel choice is treated as permanent

- **Status:** Settled
- **Date:** 2026-11-11
- **Decided by:** Project owner

## Context

The phase 2 verdicts suggested that the layers above the kernel could be written against a narrow interface so that the kernel could be replaced later, and that this was worth deciding on its own. The owner asked how hard replacing a kernel is once chosen.

The answer given: it depends on whether stored models contain anything only that kernel can interpret. Keeping the kernel replaceable costs something. Kernel-specific features cannot be used without wrapping them, and the interface must carry lineage (what each operation created, split and merged), which kernels report very differently.

## Decision

The kernel choice is treated as effectively permanent. OpenShape is not designed so that its kernel can be swapped.

If the kernel ever does have to change, that is a breaking change to part files.

## How to apply this

- Designs may use the chosen kernel's features, identifiers and lineage reporting directly. A kernel-neutral abstraction layer is not a requirement.
- Document formats may depend on the kernel's behaviour. A design that does so says so.
- This raises the stakes of [decision 0004](0004-ground-up-kernel.md). The kernel decision cannot be made provisionally with the intent of changing it later.
- It does not excuse sloppy boundaries. Ordinary modularity still applies; what is dropped is the promise that another kernel could be fitted behind the same boundary.
- The benchmark repository keeps its kernel-neutral adapter. That serves measurement, not OpenShape's architecture.

## Alternatives considered

- **A replaceable kernel behind a narrow interface.** The agent's suggestion. It would make the kernel decision reversible at a cost of months. Rejected by the owner.

## Evidence

- Owner's choice.
- The cost of lock-in is real: FreeCAD's topological naming problem came from references tied to OCCT's output ([research](../research/02-open-source-landscape/01-landscape.md)).
- The agent's statement that industry kernel changes have taken years, citing SolidWorks and CGM, was from memory and has no checked source.

## Revisit trigger

None set. A proposal to change kernels would reopen it.
