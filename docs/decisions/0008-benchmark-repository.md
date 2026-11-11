# 0008: Benchmarks live in a separate, neutrally named repository

- **Status:** Settled
- **Date:** 2026-11-10
- **Decided by:** Project owner

## Context

Phase 2 built instruments that measure kernel robustness against exact answers and found that almost nothing of the kind is public. Phase 2B proposed a wider suite. The question was where it should live and under whose name its results should appear.

## Decision

1. The benchmark suite gets its own repository, separate from OpenShape.
2. It does not carry the OpenShape name. It is a neutral resource that any kernel project can adopt.
3. It must be reproducible: every case generated from a seed, every checker validated before use, every run repeatable from the published instructions.
4. Results for all open-source kernels are published, not only favourable ones and not only OpenShape's.

## Reasons

- A benchmark carrying one project's name reads as that project's marketing, and other projects are less likely to adopt it or accept its results.
- Publishing every kernel's results, with the means to reproduce them, is what makes any single result credible.
- The existing public corpus for surface intersection made the same choices: its own repository and a permissive licence.

## Still to settle

- The name.
- The licence. MIT or Apache-2.0 would match the corpus it sits beside and place no condition on adopters. MPL-2.0 would match OpenShape. A recommendation is in [phase 2B](../research/02b-benchmarks-and-datasets/README.md).
- Who creates the repository. An agent session cannot create one; the owner does.

## Consequences

- The instruments in `docs/research/02-open-source-landscape/bench/` move to the new repository once it exists. OpenShape keeps the write-ups and refers to the results.
- Adapters for each kernel live in the benchmark repository, so results can be reproduced without OpenShape.
