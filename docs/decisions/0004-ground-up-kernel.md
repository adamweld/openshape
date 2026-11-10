# 0004: Kernel is written from the ground up

- **Status:** Provisional
- **Date:** 2026-11-10
- **Decided by:** Project owner (working expectation)

## Context

The project's rule is to write components from scratch where existing open-source software is not at the state of the art. The geometric kernel is the largest such component.

## Decision

Plan on writing the geometric kernel from scratch, not building on OCCT. The same rule applies to any other component where the open-source option falls short, which probably includes the constraint solver.

## Alternatives considered

- **Build on OCCT.** The only mature open-source B-rep kernel. Believed to be well behind Parasolid in robustness, particularly for booleans and blending.
- **Build on a newer open kernel** (truck, Fornjot and others). Believed to be far from feature-complete.
- **License a commercial kernel.** Incompatible with an open-source project.

## Evidence

Not yet gathered. The claims above are widely held views, not measurements. Phase 1 establishes what the commercial kernels do; phase 2 measures the open options against that.

## Risks recorded

A commercial kernel represents decades of accumulated edge-case handling. A new kernel only wins with a structural advantage. Candidates, to be examined in phase 3:

- a principled numerical robustness strategy designed in from the start
- differential testing and fuzzing at scale
- determinism and parallelism as first-class goals

## Revisit trigger

End of phase 2, when the reuse-or-write verdict for each component is written with evidence.
