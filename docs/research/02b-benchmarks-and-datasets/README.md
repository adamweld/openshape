# Phase 2B: Benchmarks and datasets

Status: **in progress**. Added on 2026-11-10 at the owner's request, after phase 2 showed how little measured evidence exists about CAD kernels.

Evidence marks are as in phase 1: **[P]** primary source read, **[S]** secondary or summary, **[U]** unverified. For papers, [P] means the abstract was read unless the text says otherwise.

## Why this phase exists

Every later decision depends on being able to measure. Phase 1 found that claims about kernel robustness rest on anecdote. Phase 2 had to build its own instrument to say anything about OCCT, and found two errors in that instrument before the numbers could be trusted. The project's core hypothesis, that closing the loop makes AI mechanical design work, is itself a claim that needs a benchmark.

This phase answers three questions:

1. What benchmarks and datasets exist, for which layer of the problem, and under what licence?
2. Where are the gaps?
3. What should OpenShape build, adopt and publish?

## The short answer

The field is uneven, not uniformly thin.

| Layer | State of public benchmarks | Detail |
|---|---|---|
| AI producing CAD from text, images or meshes | Crowded and growing fast | At least eight benchmarks published in 2025 and 2026 |
| AI agents doing engineering with simulation in the loop | New, a handful, all from 2026 | Small task counts, each tied to one toolchain |
| Feature recognition and reconstruction | Several datasets, licences mostly restrictive | Synthetic data is the clean route |
| Geometric kernel: surface intersection | One corpus, published October 2026 | 119 cases with exact answers |
| Geometric kernel: booleans, blends, offsets, feature sequences | Nothing public found | Phase 2's instrument is a first attempt |
| Persistent naming and rebuild robustness | Nothing found | The literature describes the problem and offers no shared test |
| Constraint solvers | Nothing found for solver quality | One large dataset of sketches exists, built for learning |
| Engineering intent: loads, interfaces, manufacturability | Fragments | One load-case benchmark; NIST's tolerance test models |
| Kernel throughput and rebuild performance | Nothing found | Individual projects report their own figures |

The gaps are at the foundation. Many groups measure whether a model can write CAD code. Almost nobody measures whether the engine underneath gives the right answer, and nobody measures whether references survive an edit. Those are the layers OpenShape depends on most and the ones where a careful, openly published benchmark would be new.

## What exists

### Geometric kernels

| Benchmark | What it measures | Size | Licence | Mark |
|---|---|---|---|---|
| [SSI corpus](https://github.com/jyviko/ssi-corpus) | Surface/surface intersection against exact answers, with a scorer and a runner contract any engine can implement | 119 cases | MIT or Apache-2.0 | [P], used in phase 2 |
| SolidCraft reference parts | Whole-part volume, area, centre of mass and bounding box against analytic values or FreeCAD | 90 parts | With the project | [P], documentation only |
| solidcore goldens and "kernel rig" | Per-unit expected outputs for the port, and operation cases | Not counted | Apache-2.0 | [P], documentation only |
| OpenShape phase 2 instrument | Booleans, fillets and 12-step feature sequences against closed-form answers | 8,400 cases | MPL-2.0 | Built here; see [02-measurements](../02-open-source-landscape/02-measurements.md) |

Nothing else was found. A search for published work on fuzzing or differential testing of CAD kernels returned only a project plan in one repository's issue tracker and the general software-fuzzing literature. [S]

What the SSI corpus gets right, and what any OpenShape benchmark should copy:

- **Ground truth by construction.** Cases are built so the exact answer is known, not computed by another kernel.
- **An engine-neutral contract.** The engine under test is a separate program that reads a case and writes a result. Phase 2 scored OCCT on it with a 190-line runner.
- **Graded verdicts.** Crash, error, incomplete, wrong topology, inaccurate and pass are distinguished, most severe first.
- **Cases grouped by difficulty class**, so a score can be read as "passes everything transversal, fails at tangency".

### AI producing CAD

| Benchmark | Task | Size | Engine | Mark |
|---|---|---|---|---|
| [BenchCAD](https://arxiv.org/abs/2605.10865) | Visual and code question answering, image to code, code editing | 17,900 programs, 106 part families | CadQuery | [P] |
| [CADBench](https://arxiv.org/abs/2605.10873) | Program generation from meshes and renders, across five input kinds | 18,000 samples | Various | [P] |
| [Parametric CAD Bench v3](https://arxiv.org/abs/2611.02659) | Text to CAD, create and edit, reconstruction from drawings; agents submit native CAD files to a separate verifier | 100 tasks | FreeCAD | [P] |
| [CADWorld](https://arxiv.org/abs/2609.16251) | Long-horizon use of a CAD application through its GUI, across sketching, parts, assembly, CAM, FEM and drawings | 200 tasks | FreeCAD | [P] |
| [CADENA-Bench](https://arxiv.org/abs/2608.00799) | Mesh to parametric program, by category of mechanical part | Not stated in abstract | Not stated | [P] |
| Text2CAD-Bench | Text to parametric CAD | Not read | CadQuery | [S] |

Findings these report that matter here:

- CADWorld's best agent succeeds on 17.5% of tasks against an expert reference of 87.0%. Agents driving a GUI are far from reliable.
- Parametric CAD Bench reports "complete systems, not isolated model capabilities", with the best scoring 61%. It scores geometry and specification consistency together.
- CADBench finds "model rankings change across metrics", which is a warning against any single score.

All of these run on OCCT, through CadQuery or FreeCAD. So every one of them is also, implicitly, a measurement of OCCT's reliability on whatever the model generates, and none separates the two.

### Agents with simulation in the loop

| Benchmark | Task | Size | Checks | Mark |
|---|---|---|---|---|
| [CADEngBench](https://arxiv.org/abs/2608.09296) | Parametric parts and assemblies judged on engineering behaviour | 600 part tasks, 150 body pairs | B-rep validity, engineering and DFM checks, behaviour under parameter changes, functional edits, matched linear-static FEA in CalculiX; for assemblies, exact face-and-edge grounding of joints | [P] |
| [StructBench](https://ijcai.org/proceedings/2026/714) (Physics-in-the-Loop) | Design a part for a load case | 20 load cases, 500 scaled variants | Safety factor from FEA, design-space compliance | [P], read in full in phase 1 |
| [Hephaestus-CCX](https://arxiv.org/abs/2605.17448) | Multi-part assembled STEP file from an engineering brief, validated by FEA | 50 cases | Typed requirements checked with CalculiX | [P] |
| [EngDesign](https://arxiv.org/abs/2509.16204) | Design tasks across nine engineering domains with simulation-based evaluation | Not stated in abstract | Per-task simulation | [P] |

Findings that matter:

- CADEngBench's title is its thesis: "It Looks Like CAD, but Does It Work?" It finds editing supplied CAD "substantially easier than generating it", with complex edits and matched FEA remaining hard, and assembly predictions that "often locate the relevant region but fail to recover the recorded joint or mating entities". That last point is the geometry-reference problem of [decision 0006](../../decisions/0006-geometry-references.md), measured.
- Hephaestus reports that two leading coding agents "do not produce a single strict-passing artifact" on first attempt, meeting about 20% of typed requirements, and that adding a rendered multi-view inspection and a text blueprint improved results.
- CADEngBench tests "parameter-family perturbations": whether a model still behaves when its parameters change. It is the only benchmark found that tests anything like rebuild robustness, and it tests the model's design, not the engine's references.

This is the closest existing work to OpenShape's core hypothesis. All of it is under a year old, each benchmark is small, and each wires its own toolchain together from CadQuery or FreeCAD and CalculiX.

### Datasets of CAD models

| Dataset | Content | Licence, as checked at source | Usable to ship or train on |
|---|---|---|---|
| ABC | One million B-reps from public Onshape documents | Copyright rests with each model's creator under Onshape's terms; the dataset grants no licence. Papers often cite its code's MIT licence, which does not cover the models | No, without legal advice |
| DeepCAD | 178,000 sketch-and-extrude sequences parsed from the same Onshape documents | None stated for the data | No, same position |
| SketchGraphs | 15 million constrained 2D sketches from Onshape | Not confirmed | Not established; same origin as ABC |
| Fusion 360 Gallery | 8,625 human design sequences, plus segmentation and assembly sets | Non-commercial research only, revocable | Research measurement only |
| Zero-to-CAD | One million synthetic CadQuery programs | Apache-2.0 | Yes |
| FllumaOne | Synthetic programs with feature trees and STEP, from an OCCT-based system | Not read | Not established |
| MFCAD, MFCAD++ | Synthetic parts labelled with machining features | Not checked | Not established |
| NIST PMI test cases | A small set of parts with full tolerance annotation, as CAD models and STEP AP242 files | Published by NIST for testing; exact terms not confirmed | Probably, to be confirmed |

Sources: [ABC](https://deep-geometry.github.io/abc-dataset/), [DeepCAD](https://github.com/ChrisWu1997/DeepCAD), [SketchGraphs](https://arxiv.org/abs/2007.08506), [Fusion 360 Gallery licence](https://github.com/AutodeskAILab/Fusion360GalleryDataset/blob/master/LICENSE.md), [Zero-to-CAD](https://huggingface.co/datasets/ADSKAILab/Zero-To-CAD-1M), [FllumaOne](https://arxiv.org/abs/2606.17696), [NIST](https://pages.nist.gov/CAD-PMI-Testing/models.html).

The pattern holds across the table: real-world CAD data traces back to other people's Onshape or Fusion documents and is not cleanly licensed, and the cleanly licensed data is synthetic. Any corpus OpenShape ships or trains on should be generated.

## The gaps

In order of how much OpenShape depends on them.

1. **Booleans, blends and offsets against exact answers.** No public corpus. Phase 2's instrument covers analytic primitives only.
2. **Freeform geometry beyond intersection.** The SSI corpus covers intersection of NURBS surfaces. Nothing covers booleans or blends on freeform bodies.
3. **Reference survival.** No test exists for whether a face or edge reference still resolves, and resolves to the right entity, after an upstream edit. This is the central question of decision 0006 and nobody can currently answer it with data for any system.
4. **Feature sequences at realistic depth.** Real models have hundreds of features. Phase 2 tested 12.
5. **Constraint solver behaviour.** Nothing measures which solution a solver picks, how geometry moves under drag, or the quality of its diagnostics.
6. **Imported and imperfect geometry.** Nothing public measures healing or tolerant modelling.
7. **Throughput.** No common measure of operations per second for a headless kernel, though phase 1 showed training loops are limited by it.
8. **Intent.** One benchmark supplies load cases. None supplies interfaces, manufacturing process or assembly requirements in machine-readable form.

## Plan

A proposal for the owner. It becomes a decision record once agreed.

### Principles

1. **Ground truth by construction, never by another kernel.** Closed-form where possible; otherwise a construction whose answer is known, as the SSI corpus does for its fitted cases.
2. **Engine-neutral.** Each benchmark defines a runner contract. OpenShape's kernel is one engine among several, and results for OCCT, SMLib and solidcore are published beside it.
3. **Validate the instrument first.** Every checker is tested against known-good inputs before any result is recorded, and that validation is published with the results. Phase 2's two instrument errors are the reason.
4. **Separate failure kinds.** Crash, error, invalid result and wrong result are different outcomes. A silent wrong result is the worst and is reported on its own.
5. **Exclude ill-posed cases, and say so.** A case whose exact answer is not a valid solid cannot be scored pass or fail. Phase 2's tangent-hole family is the example.
6. **Generated, seeded, and openly licensed.** No dependence on datasets with licence doubt.
7. **Report by class of difficulty**, not one number.
8. **Publish everything**: cases, generators, runners, raw results and the instrument's own validation.

### Proposed suite

| # | Benchmark | Ground truth | Status |
|---|---|---|---|
| 1 | Surface intersection | Adopt the SSI corpus as it is | Exists; OCCT scored in phase 2 |
| 2 | Booleans on analytic solids | Closed-form point membership | Exists as phase 2's instrument; needs more families and the ill-posed cases removed |
| 3 | Feature sequences | Closed-form membership of a known combination of primitives | Exists at 12 steps; extend to hundreds of steps and to patterns and shells |
| 4 | Blends | Analytic volume and face checks where a closed form exists (straight edges, constant radius on planar and cylindrical faces); existence proved before a failure counts | To design. The fillet figures in phase 2 are upper bounds because existence was not proved |
| 5 | Freeform booleans | Solids bounded by NURBS patches built from known implicit surfaces, so membership is still exact | To design |
| 6 | Reference survival | Generate a model, record references, apply an upstream edit whose correct effect on each reference is known by construction, rebuild, and check each reference resolves to the right entity or is correctly reported lost | To design. New |
| 7 | Constraint solving | Sketches generated from a known solution, checked for the solution chosen, stability under small dimension changes, and correct detection of over- and under-constraint | To design |
| 8 | Imperfect input | Take exact solids, perturb their edges and vertices by known amounts, and require import, healing and booleans to still give the known answer | To design |
| 9 | Throughput and determinism | Operations per second headless; identical results across runs, thread counts and machines | To design |
| 10 | Closed-loop design tasks | Adopt CADEngBench and StructBench as external measures; add tasks that need interfaces, manufacturing constraints and assembly checks | Later, in phase 4 |

Items 2 to 5 and 8 measure a kernel. Items 6 and 7 measure the layers above it. Item 9 measures what a training environment needs. Item 10 measures the hypothesis.

### Order

1. Harden what exists (items 2 and 3) and publish it with the phase 2 results for OCCT and SMLib. This is cheap and already more than is public.
2. Design item 6, reference survival. It decides decision 0006 and nobody else has it.
3. Design items 4 and 5, which need the most geometric care.
4. Items 7, 8 and 9 alongside the corresponding parts of phase 3.

### Open questions for the owner

- Should the suite live in this repository or in its own, so other projects can adopt it without taking OpenShape? A separate repository under a permissive licence would make adoption easier; the SSI corpus chose MIT or Apache-2.0.
- Should results for other kernels be published under OpenShape's name? They would be accurate and reproducible, and they could also be read as criticism by those projects.

## Not yet done in this phase

- Papers read beyond their abstracts: none of the benchmark papers above.
- Licences confirmed at source for SketchGraphs, MFCAD, FllumaOne and the NIST test cases.
- FEA benchmarks (the NAFEMS standard problems) and meshing benchmarks, which belong with item 10.
- A search of the solver and naming literature for test sets hidden inside individual papers.
- The internal test suites of OCCT and FreeCAD, which are large and public and may contain reusable cases.
