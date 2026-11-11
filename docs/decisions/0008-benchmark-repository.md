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

## Amendment, 2026-11-11: commercial products

The owner added that closed-source products, such as Onshape and Zoo's, belong in the comparison, because OpenShape must end up at least as good as what is on the market.

The intent is recorded. The means are constrained: Onshape's terms of use forbid using the service for purposes competitive to it, and other vendors' terms commonly restrict benchmarking. The position, the routes that remain open and the question for the owner are in [COMPARABLE-PROJECTS.md](../COMPARABLE-PROJECTS.md). No commercial product is to be run through the benchmark until that question is answered.

## To revisit, 2026-11-11: an existing benchmark

After this decision the project found [brep-bench](../research/02b-benchmarks-and-datasets/03-brep-bench.md), a public, permissively licensed kernel benchmark with 346 cases and results for 13 kernels, started two weeks earlier. The decision to create a separate repository was made without knowing it exists. The owner chose the name `cadkernelbench`. Before that repository is filled, the owner should choose between contributing to brep-bench, limiting `cadkernelbench` to what brep-bench does not cover, or building in parallel. The recommendation is the second, with contributions to the first.

## Done, 2026-11-11

- The repository is [adamweld/cadkernelbench](https://github.com/adamweld/cadkernelbench). The owner chose the name.
- After being told of brep-bench, the owner confirmed the scope: `cadkernelbench` holds what brep-bench does not (generated families with failure rates, feature sequences, and later reference survival and throughput), and an SMLib runner is to be offered to brep-bench.
- The instruments and results were moved there, restructured into a kernel-neutral core with one adapter per kernel, and verified to reproduce the stored results.
- Licence: MIT or Apache-2.0. Recommended by the agent and confirmed by the owner on 2026-11-11.

## Still to settle

Nothing. The name, the licence and the repository itself are done, above.

## Consequences

- The instruments in `docs/research/02-open-source-landscape/bench/` move to the new repository once it exists. OpenShape keeps the write-ups and refers to the results.
- Adapters for each kernel live in the benchmark repository, so results can be reproduced without OpenShape.
