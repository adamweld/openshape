# 0009: The kernel is not designed to be replaceable

- **Status:** Settled
- **Date:** 2026-11-11
- **Decided by:** Project owner

## Context

The phase 2 verdicts suggested that the layers above the kernel could be written against a narrow interface so that the kernel could be replaced later, and that this was worth deciding on its own. The owner asked how hard replacing a kernel is once chosen.

The answer given: it depends on whether stored models contain anything only that kernel can interpret. Keeping the kernel replaceable costs something. Kernel-specific features cannot be used without wrapping them, and the interface must carry lineage (what each operation created, split and merged), which kernels report very differently.

## Decision

OpenShape is not designed so that its kernel can be swapped. No architecture is built to make a swap cheap.

If the kernel does change, that is a breaking change to part files, and work built on the old kernel has to be redone.

The kernel may still be chosen provisionally. It is not yet known whether any existing kernel fits the project's needs, so a first selection can be made and later changed, with clear eyes about that cost.

## How to apply this

- Designs may use the chosen kernel's features, identifiers and lineage reporting directly. A kernel-neutral abstraction layer is not a requirement.
- Document formats may depend on the kernel's behaviour. A design that does so says so.
- [Decision 0004](0004-ground-up-kernel.md) may be made as Provisional. Its record must then state the cost of changing it: part files break and dependent work is redone. That cost grows with everything built on the kernel, so the revisit trigger should come early.
- It does not excuse sloppy boundaries. Ordinary modularity still applies; what is dropped is the promise that another kernel could be fitted behind the same boundary.
- The benchmark repository keeps its kernel-neutral adapter. That serves measurement, not OpenShape's architecture.

## Alternatives considered

- **A replaceable kernel behind a narrow interface.** The agent's suggestion. It would make the kernel decision reversible at a cost of months. Rejected by the owner.

## Evidence

- Owner's choice.
- The cost of lock-in is real: FreeCAD's topological naming problem came from references tied to OCCT's output ([research](../research/02-open-source-landscape/01-landscape.md)).
- The agent's statement that industry kernel changes have taken years, citing SolidWorks and CGM, was from memory and has no checked source.

## Correction, 2026-11-11

The first version of this record said the kernel decision could not be made provisionally. That was the agent's inference and went further than the owner's decision. The owner corrected it: a provisional selection is allowed, with the cost of changing it understood.

## Revisit trigger

None set. A proposal to build a kernel-neutral layer would reopen it.
