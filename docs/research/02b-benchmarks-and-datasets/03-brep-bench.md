# brep-bench: an existing public kernel benchmark

Found on 2026-11-11 while answering the owner's question about where next.BREP's public test cases come from. It was missed by the first survey in this phase, which searched for papers and for "benchmark" in repository descriptions; this repository has no description and nine stars. **It changes this phase's conclusion that nothing public exists for booleans and blends, and it bears on [decision 0008](../../decisions/0008-benchmark-repository.md).**

Sources, all read on 2026-11-11: the [repository](https://github.com/bmander/brep-bench) README, case tour and kernel list, and the results data behind [brepbench.org](https://brepbench.org). Evidence mark [P] for what the project states and publishes. Nothing was run here.

## What it is

Its own description: "Rosetta Code for B-rep kernels. Each case describes a solid in plain words and gives its volume and area in closed form where one exists. Each kernel builds the cases in its own language and idioms."

Its stated reason is the one this phase arrived at independently: "People keep writing B-rep kernels from scratch, in Rust especially, many with an AI agent's help. Each invents its own tests, so none can show how it compares with the others."

| | |
|---|---|
| Started | 2026-10-29 |
| Licence | MIT or Apache-2.0 |
| Cases | 346, in 21 categories |
| Kernels with results | 13 |
| Results published | A public board, regenerated from the repository; last run 2026-11-10 |

Categories and case counts: swept solids 86, shells 31, booleans 29, tangent contact 29, fillets 21, thickened sheets 20, geometry 20, offsets 19, drafts 13, sweeps 11, singular points 10, NURBS 9, chamfers 8, primitives 8, splines 7, real parts 7, lofts 6, direct edits 5, form features 4, filled surfaces 2, and one integration test (the Utah teapot).

### How a case is graded

- A runner builds the solid, writes its triangles, and reports volume and area.
- **Pass:** volume and area within 1e-6 relative of the closed-form values, or 1e-3 for a kernel that can only measure its own mesh; and the mesh is closed, consistently oriented, and encloses the expected volume to within 2%.
- A case with no closed form is "unsettled" until two independent kernels agree to 1e-8. Until then a sound result is graded **built**.
- "**Refused** ranks above **wrong**."
- Each solid is also written as STEP by the kernel and the file judged, shown but not graded.

### Where its cases come from

- Textbook solids with closed-form volume and area.
- The [SSI corpus](https://github.com/jyviko/ssi-corpus): solids built around its intersection classes, each naming the corpus case it came from.
- A separate project by the same author, geomsolver, for exact solid sweeps and for "real parts".
- Classical named configurations, such as Viviani's curve and Villarceau circles.
- Cases contributed by kernel authors, who are asked for "hard cases ... especially ones your own kernel gets wrong".

## The published results

From the board's data, run 2026-11-10. Each kernel's implementations are written for that kernel, in most cases by its own contributors.

| Kernel | Licence | Pass | Built | Refused | Wrong | Crashed or timed out | Not implemented |
|---|---|---|---|---|---|---|---|
| cadrs | MIT or Apache-2.0 | 294 | 52 | 0 | 0 | 0 | 0 |
| next.BREP | Custom, not open source | 286 | 8 | 39 | 3 | 0 | 10 |
| OCCT 8.0.1 | LGPL-2.1 | 263 | 16 | 47 | 15 | 5 | 0 |
| cad-kernel | MIT or Apache-2.0 | 263 | 12 | 65 | 0 | 1 | 5 |
| solidcore | Apache-2.0 | 207 | 0 | 18 | 6 | 0 | 115 |
| kentron | MIT or Apache-2.0 | 187 | 0 | 16 | 18 | 0 | 125 |
| popkern | AGPL-3.0 with exception | 131 | 0 | 58 | 12 | 4 | 141 |
| geop | MIT or Apache-2.0 | 124 | 0 | 46 | 59 | 3 | 114 |
| brepkit | AGPL-3.0 or commercial | 118 | 0 | 27 | 72 | 0 | 129 |
| arris | MIT or Apache-2.0 | 104 | 0 | 44 | 1 | 0 | 197 |
| SolidCraft's kernel crate | MIT or Apache-2.0 | 99 | 0 | 34 | 14 | 2 | 197 |
| vcad | MIT | 44 | 0 | 29 | 24 | 1 | 248 |
| Aetheris | AGPL-3.0 | 25 | 0 | 70 | 2 | 1 | 248 |

SMLib is not on the board.

### Reading these with care

- **This is the first independent-of-us measurement of solidcore**: 207 of the 231 cases it implements pass, with 6 wrong and 18 refused. It has no implementation for a third of the suite.
- **OCCT is the only kernel with every case implemented and it is the board's reference for drawings.** It has 15 wrong results and 5 crashes or timeouts.
- **Scores are not comparable as a ranking, and the board says so**: "no kernel ranks above another". A kernel that implements only the cases it handles looks cleaner than one that attempts all of them.
- **Most implementations are written by the kernel's own authors.** A kernel can be developed against the suite. cadrs and next.BREP, the two highest, both joined recently and both cite the board in their own material. That does not make their results false, and it is the normal condition of any public benchmark, but it means a high score shows the cases were made to pass, not that unseen cases would.
- **A possible flaw worth raising with its maintainers.** Phase 2 found OCCT's volume integration off by up to 0.6% on curved trimmed faces at default settings, enough to mark a correct solid as wrong at a tolerance of 1e-6. Whether brep-bench's OCCT runner tightens the integration was not checked. If it does not, some of OCCT's 15 wrong results may be measurement error. This is unverified.

## How it compares with what phase 2 built

| | brep-bench | Phase 2's instruments |
|---|---|---|
| Kind | A curated library of individual cases | Generated families, run in bulk |
| Size | 346 cases | 8,400 cases |
| Breadth of operations | Wide: sweeps, lofts, shells, offsets, drafts, direct edits | Narrow: booleans, fillets, sequences of booleans |
| Ground truth | Closed-form volume and area; agreement of two kernels where none exists | Closed-form point membership |
| What a failure tells you | This solid, with this code, fails | A failure rate for a family, with its dependence on a parameter such as an offset |
| Implementation per kernel | Hand-written per case, in the kernel's idiom | Ten functions, written once |
| Catches a solid with the right volume in the wrong place | Only through the 2% mesh check | Yes |
| Sensitive to the kernel's own volume integration | Yes | No |
| Feature sequences at depth | One integration test | Yes, 12 steps, extensible |
| Near-degenerate sweeps over an offset | Individual tangent cases | Yes, 15 offsets per family |
| Kernels | 13, not SMLib | OCCT and SMLib, solidcore drafted |
| Isolation of crashes and memory blow-ups | Not examined | Yes |

They are complementary. brep-bench answers "which operations can this kernel do at all, and on which named hard cases does it fail". The generated instruments answer "how often does it fail on this kind of input, and how does that vary".

Neither has anything on reference survival, constraint solving, imperfect input, or throughput.

## What this means for decision 0008

The owner decided to create a separate, neutrally named benchmark repository and has chosen the name `cadkernelbench`. That decision was made without knowing brep-bench exists, so it should be looked at again before the repository is filled. Options:

| | Option | For | Against |
|---|---|---|---|
| 1 | Contribute to brep-bench and do not start a second board | It exists, is permissively licensed, already has 13 kernels and an active maintainer, and is where kernel authors are sending results. An SMLib runner and the point-membership check would be accepted or declined on their merits | Its design is one hand-written implementation per case. Generated families of thousands of cases, and benchmarks above the kernel such as reference survival, do not fit it without its maintainer's agreement |
| 2 | Make `cadkernelbench` only what brep-bench is not | No duplication. It would hold the generated statistical suites, reference survival and throughput, and would point to brep-bench for case-by-case coverage | Two places to look. Needs a clear statement of the difference |
| 3 | Build a full parallel suite | Full control | Duplicates work that is two weeks ahead and already adopted. This is what the owner asked to avoid |

**Recommendation:** option 2, combined with the cheap parts of option 1. Concretely:

- Do not write curated single-case tests for operations brep-bench already covers.
- Offer brep-bench an SMLib runner, and raise the volume-integration question.
- Run the candidate kernels on brep-bench as part of the kernel decision, and use its results alongside our own.
- Keep `cadkernelbench` for what is missing everywhere: generated families with failure rates, feature sequences at realistic depth, reference survival, and throughput and determinism.
- Talk to brep-bench's maintainer before publishing, so the two are designed to sit side by side.

This is the owner's call.

## Kernels found through its list

Six kernels on the board were not in [COMPARABLE-PROJECTS.md](../../COMPARABLE-PROJECTS.md) and have been added: [cad-kernel](https://crates.io/crates/cad-kernel), [arris](https://github.com/arris-labs/arris), [kentron](https://github.com/rsz269/kentron), [popkern](https://github.com/popkern-dev/popkern), [Aetheris](https://github.com/yuechen-li-dev/Aetheris) and [geop](https://github.com/geop-cad/geop). None has been examined.

## SMLib on brep-bench, 2026-11-11

The owner chose option 2 with the SMLib runner. The runner was written, offered upstream from the branch [adamweld/brep-bench `smlib-runner`](https://github.com/adamweld/brep-bench/tree/smlib-runner), and merged by the maintainer on 2026-11-11, by the owner's report. It drives `usd-brep` 1.0.1 and implements six of the suite's categories: primitives, boolean, tangent, fillet, chamfer and sweep, 106 cases. The other 240 cases are not written.

Measured locally with brep-bench's own harness, 60 s limit:

| Outcome | Cases |
|---|---|
| pass | 85 |
| built (a case with no settled answer) | 1 |
| wrong | 18 |
| crashed | 2 |
| refused | 0 |

What failed, by kind:

- **Booleans at exact tangency.** Three cases return an operand unchanged, one leaves a branch untrimmed and one raises an error. Moving one of them 0.01 off tangency gives a sensible result.
- **Thin results lost.** Two intersections return a body with no faces and report no error.
- **Meshes.** Four solids with correct volume and area tessellate to meshes that are not closed. One union of nested bodies tessellates inside out.
- **Fillet corners where four rounds meet.** Two cases.
- **Small errors in measures**, between 8e-6 and 0.9%, on helical pipes and three sliver cases.
- **One chamfer** raises an error.

This agrees with the phase 2 measurement, where SMLib failed every tangent-hole pair within a micron of tangency ([02-measurements.md](../02-open-source-landscape/02-measurements.md)).

Limits of this result:

- The implementations were written by AI agents under brep-bench's rules, not by SMLib's authors, and the maintainer's review is not recorded here.
- SMLib's volume integration fails at its tightest advised accuracy on some solids, a plain sphere among them. The runner falls back to coarser settings, down to the benchmark's 1e-6.
- No comparison with OCCT on the same 106 cases is given here. brep-bench's published board is the place to read one once the runner is merged and run there.

## Not done

- Only SMLib was run on brep-bench here, on six categories.
- Its OCCT runner was not read to check the integration settings.
- Its maintainer has been contacted only through the pull request. The volume-integration question has not been raised.
