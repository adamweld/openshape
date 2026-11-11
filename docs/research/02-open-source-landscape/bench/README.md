# The measurement instruments have moved

The benchmark code, raw results and running instructions that were here now live in their own repository, as [decision 0008](../../../decisions/0008-benchmark-repository.md) requires:

**[github.com/adamweld/cadkernelbench](https://github.com/adamweld/cadkernelbench)**

| Was here | Now |
|---|---|
| `occt_robustness.py`, `bench_driver.py`, `occt_paired.py` | [`ckb/core.py`, `ckb/driver.py`, `ckb/kernels/occt.py`](https://github.com/adamweld/cadkernelbench/tree/main/ckb) |
| `smlib_robustness.py`, `solidcore_robustness.py` | [`ckb/kernels/`](https://github.com/adamweld/cadkernelbench/tree/main/ckb/kernels) |
| `solidcore_server/` | [`solidcore_server/`](https://github.com/adamweld/cadkernelbench/tree/main/solidcore_server) |
| `occt_ssi_runner.py` | [`ssi/`](https://github.com/adamweld/cadkernelbench/tree/main/ssi) |
| `quiddity_eval.py` | [`recognition/`](https://github.com/adamweld/cadkernelbench/tree/main/recognition) |
| `results/` | [`results/2026-11-10/`](https://github.com/adamweld/cadkernelbench/tree/main/results/2026-11-10) |
| `HANDOFF.md` | [`docs/RUNNING.md`](https://github.com/adamweld/cadkernelbench/blob/main/docs/RUNNING.md) |

The write-up of what the measurements mean for OpenShape stays here, in [../02-measurements.md](../02-measurements.md) and [../03-verdicts.md](../03-verdicts.md).
