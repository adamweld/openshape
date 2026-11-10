# Measurements

Direct measurements made for phase 2. All were run in this project's session on 2026-11-10 on a 4-core Linux machine. The instruments are in [bench/](bench/) and every case is generated from a seed, so each run can be repeated.

Status: OCCT and quiddity results are final. SMLib, solidcore and the surface-intersection scores are being added as the runs finish.

## What was measured, and how

### The cases

| Set | Size | What it is |
|---|---|---|
| Near-degenerate booleans | 2,100 pairs | Two primitives in a configuration that is degenerate when an offset is zero: a block resting on another's face, a block with one face flush with another's, a hole tangent to a wall, coaxial cylinders of equal radius, a sphere touching a face, a cylinder whose axis lies on an edge, and a solid built twice. The offset takes 15 values from zero to one micron and from there to one millimetre, in both directions |
| Generic booleans | 600 pairs | Two random primitives (box, cylinder, sphere, cone, torus) in random positions and orientations |
| Fillets | 3,000 cases | A primitive, or a boolean of two, with one sharp edge or all sharp edges rounded at 2%, 5% or 15% of the shortest sharp edge. 456 had no sharp edge and were skipped |
| Feature sequences | 300 | A block with 12 booleans applied in turn (holes, pockets, bosses, ribs, spherical cuts), about half placed flush with or tangent to existing faces, followed by one fillet. This is the shape of a real feature tree |

Every solid is placed in a random orientation, so coincidences hold only up to floating-point rounding, as they do in real models. Union, subtraction and intersection are each run on every pair.

### The check

No second kernel is used as a reference. Every input is an analytic primitive, so whether a point is inside it is known in closed form, and so is the correct answer for any combination of them. For each result:

1. The kernel's own validity check is run.
2. Sample points are classified against the result and compared with the closed-form answer. Points within 0.01 mm of any input's boundary are not used.

A result is counted as **error** if the kernel reported failure, **invalid** if it returned a solid that fails its own check, and **wrong** if it returned a valid-looking solid that misclassifies a point or is empty when it cannot be. Wrong is the worst outcome, because nothing tells the user.

The closed-form inside tests were themselves validated against each kernel on the input primitives before use: 23,954 points with OCCT and 2,397 with SMLib, with no disagreement.

### Two mistakes found in the instrument, and fixed

They are recorded because they show how easily a benchmark produces false failures.

1. The first version judged booleans by a volume identity. It flagged 0.8% of generic pairs as wrong. Dense re-checking showed the solids were right and OCCT's volume integration on curved trimmed faces was off by up to 0.6%. The point test replaced it.
2. The first version caught exceptions too broadly, so a mistake in the benchmark script was counted as a kernel error. Exceptions are now counted only when the kernel raised them, and anything else stops the run.

A third hazard applies to SMLib: its Python package's memory use grows with every operation, by roughly 100 MB per case, until the process is killed. A process killed for memory would look like a kernel crash. Workers are restarted every 15 cases, and a case whose process was killed is retried in a fresh one before it counts.

### Limits of this measurement

- **Analytic primitives only.** No freeform NURBS surfaces, where the literature and the kernels' own documentation place most of the difficulty. The surface-intersection corpus below covers that for intersection, not for booleans.
- **Clean input.** No imported geometry with gaps or tolerances.
- **Small models.** At most 13 bodies' worth of faces.
- **Fillet existence is not proved.** Radii are small relative to the edges, but a fillet at 15% of the shortest edge may be geometrically impossible on some solids. The fillet figures are an upper bound on kernel failure. The single-edge, 2% figure on well-angled edges is the closest to a true failure rate.
- **About 150 sample points per result.** A defect smaller than about 1% of the sampled volume can be missed.

## OCCT 8.0.1

### Booleans

| Set | Pairs | Operations reporting an error | Returning an invalid solid | Returning the wrong solid | Hung | Pairs with any failure |
|---|---|---|---|---|---|---|
| Near-degenerate | 2,100 | 0 | 1 of 6,300 | 0 | 0 | 0.05% |
| Near-degenerate, with a fuzzy tolerance of 1e-6 | 2,100 | 0 | 0 | 0 | 0 | 0.00% |
| Generic position | 600 | 0 | 0 | 0 | 1 | 0.17% |

- The one near-degenerate failure is a sphere exactly tangent to a face, united with the block. The correct result is two solids touching at a point, which is not a manifold solid; OCCT returned something its own checker rejects.
- The hung case exceeded 180 seconds. It was not established whether the boolean or the point classification was slow.
- Median time per boolean: 4 ms on the near-degenerate set, 21 ms on the generic set, with the slowest 1% taking 185 ms or more.

### Feature sequences

| Fuzzy tolerance | Sequences | Completed all 12 booleans | Stopped: invalid solid | Stopped: wrong solid | Final fillet failed |
|---|---|---|---|---|---|
| none | 300 | 99.0% | 1 | 2 | 19.9% |
| 1e-6 | 300 | 99.7% | 1 | 0 | 17.7% |

- All four boolean failures happened on a tool placed flush or tangent: three through holes tangent to a wall, and one spherical cut centred on an edge.
- **Both "wrong solid" cases returned an empty result with no error.** A subtraction that should have removed a small hole or a spherical bite returned nothing at all, and OCCT reported success and a valid shape. With the fuzzy tolerance set, neither occurred.
- Median time for a 12-step sequence was 159 ms, so about 6 sequences per second per core.

### Fillets

| Edges rounded | Radius, as a fraction of the shortest sharp edge | Cases | Failed |
|---|---|---|---|
| One | 2% | 441 | 4.5% |
| One | 5% | 424 | 5.2% |
| One | 15% | 425 | 10.4% |
| All | 2% | 422 | 5.9% |
| All | 5% | 424 | 9.7% |
| All | 15% | 408 | 26.7% |

| Edges rounded | Solid | Cases | Failed |
|---|---|---|---|
| One | A single primitive | 338 | 0.0% |
| One | Union of two | 368 | 6.8% |
| One | Subtraction | 315 | 9.2% |
| One | Intersection | 269 | 11.9% |

| Edges rounded | Angle between the faces along the edge | Cases | Failed |
|---|---|---|---|
| One | Between 45 and 135 degrees throughout | 1,125 | 4.4% |
| One | Shallower or sharper somewhere | 165 | 22.4% |
| All | Between 45 and 135 degrees throughout | 668 | 9.3% |
| All | Shallower or sharper somewhere | 586 | 19.3% |

Of 2,544 fillet attempts, 207 reported an error and 54 returned a solid that failed the validity check.

### Reading the OCCT results

1. **OCCT's booleans on analytic geometry are robust.** One failure in 4,200 deliberately degenerate pairs, and 99% of 12-step sequences completing, is far better than the reputation that [decision 0004](../../decisions/0004-ground-up-kernel.md) started from. Version 8 follows a large modernisation, and opinions formed on earlier versions may be out of date.
2. **Its rare boolean failures include the worst kind.** Two sequences in 300 silently lost the whole body. For an agent that runs thousands of operations and trusts a success code, a silent wrong answer at that rate matters more than a visible error at ten times the rate. This supports the phase 1 requirement that an operation must succeed or change nothing, and shows why every result needs an independent check.
3. **Setting a tolerance removed the silent failures in this test.** That matches what phase 1 found in Parasolid's documentation: robustness depends partly on hints the caller supplies.
4. **Fillets are where OCCT is weak.** About one in twenty single fillets fails on a well-conditioned edge of a two-primitive solid, and about one in five after a 12-step sequence. Zero fail on plain primitives. The failures appear with curved intersection edges, which is consistent with phase 1's finding that blending is the largest reservoir of hard cases.
5. **Throughput is modest.** Six 12-step models per second per core is workable for an interactive tool and slow for the training loops described in phase 1, which ran millions of executions.

## quiddity 0.4.9: feature recognition

Sixty plates were generated with features placed on a grid so none overlap: through holes, blind holes, rectangular pockets, cylindrical bosses and rounded corners, each plate in a random orientation. They were written to STEP by OCCT and given to quiddity with no other information. The generator is [bench/quiddity_eval.py](bench/quiddity_eval.py).

| Feature | In the 60 parts | Parts where quiddity's answer matched exactly |
|---|---|---|
| Through holes, with diameters | 99 | 60 of 60 |
| Blind holes, with diameters | 97 | 60 of 60 |
| Rectangular pockets | 94 | 60 of 60 |
| Cylindrical bosses, with diameters | 87 | 60 of 60 |
| Rounded corner edges | 116 | 60 of 60 |

Median time was 0.13 seconds per part, with no errors.

Reading:

- On clean, well-separated features, recognition is exact, including diameters and whether a hole is through or blind. That is the recognition half of the owner's reverse-engineering requirement, working today under Apache-2.0.
- This is an easy test. Features do not interact, there are no freeform faces, and no feature is cut by another. Real parts are harder, and this says nothing about them.
- quiddity reports features. It does not build an editable feature tree or decide the order of operations, which is the part of reconstruction still to be written.
