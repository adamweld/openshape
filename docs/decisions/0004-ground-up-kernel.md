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

## Evidence gathered since this record was written

From phase 1, [kernel research](../research/01-state-of-the-art/02-kernels.md):

- The first candidate advantage above is contested. Parasolid's designers considered exact arithmetic and rejected it, partly because it produces sliver features that do not reflect design intent. Phase 3 must address that objection directly.
- No measured comparison of OCCT against commercial kernels exists in public. The premise of this decision is still unverified.
- A recent precedent exists: Zoo reports a new B-rep kernel built by fewer than 30 engineers in two years, with no published robustness data.

From phase 2, [measurements](../research/02-open-source-landscape/02-measurements.md) and [verdicts](../research/02-open-source-landscape/03-verdicts.md):

- The premise that OCCT is the only open option no longer holds. SMLib was published as open source in October 2026 and solidcore, a Rust kernel derived from it, is being developed in the open.
- Measured, OCCT's booleans on analytic geometry are robust, and its fillets and tangential surface intersection are weak. SMLib is the reverse on intersection and much weaker on chained booleans.
- No measured kernel is good enough at everything to build on without reservation, and the most promising candidate, solidcore, is unmeasured.
- The decision is now a choice among three options set out in the verdicts document, awaiting the owner.

## Revisit trigger

End of phase 2, when the reuse-or-write verdict for each component is written with evidence.
