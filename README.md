# OpenShape

OpenShape is an open-source, local-first mechanical CAD platform built for both human and AI use. The goal is a state-of-the-art parametric modeler with an interface that lets an AI agent close the loop of design, simulated test and optimisation.

The project is in its research and design stage. There is no code here yet, by intent.

## Where to start

| | |
|---|---|
| [docs/VISION.md](docs/VISION.md) | Goals, core hypothesis and scope |
| [docs/PRINCIPLES.md](docs/PRINCIPLES.md) | How we work and the standard every decision must meet |
| [AGENTS.md](AGENTS.md) | Rules for AI agents working in this repository |

## Measurement comes first

Before choosing or building a geometric kernel, the project is measuring the open ones.

- [cadkernelbench](https://github.com/adamweld/cadkernelbench): generated robustness benchmarks for B-rep kernels, with results.
- [brep-bench](https://github.com/bmander/brep-bench): a public library of curated kernel test cases, maintained independently, to which this project contributes.

Working notes, research drafts and decision records are kept outside this repository until they are in a state worth publishing.

## License

[Mozilla Public License 2.0](LICENSE).
