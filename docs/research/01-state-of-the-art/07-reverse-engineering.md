# Reverse engineering

Evidence marks are defined in the [phase README](README.md). This is a first pass.

The scope set by the owner is, first, creating parametric solid models from STEP files and similar imported solids, and much later, working with mesh and scan data (see [VISION.md](../../VISION.md)). This document follows that order.

## Summary

- Commercial CAD offers two answers to an imported solid with no history: recognise features and rebuild a tree, or skip the tree and edit the faces directly. The second has largely won in practice.
- Recovering a construction sequence from a B-rep is an active research area, and the field's own stated bottleneck is a shortage of real data with construction history.
- Recent research supports the project's core hypothesis directly: training with feedback from a CAD engine in the loop beats supervised training alone.

## What commercial tools do with an imported solid

### Feature recognition

SOLIDWORKS FeatureWorks is the long-standing example. [S] ([SOLIDWORKS help](https://help.solidworks.com/2018/English/SolidWorks/fworks/c_Overview_of_FeatureWorks.htm))

- It recognises features on an imported body, and the results are ordinary native features.
- It offers automatic and step-by-step modes. In step-by-step mode the user picks faces and says what kind of feature they belong to.
- Documented limits include that "partial imprints of features cannot be recognized", and multi-body parts are handled one body at a time.
- User reports describe partial results on complex parts, with only a few features recognised. [S, anecdotal]

A point made by practitioners is worth recording: recognising that a pocket exists is not the same as recovering design intent. A recognised tree may reproduce the shape while dimensioning it in a way no designer would. [S] ([CATI](https://www.cati.com/blog/design-intent-part-ii/))

### Direct editing

Siemens' synchronous technology takes the other route: do not reconstruct history at all. [S] ([Siemens](https://www.sw.siemens.com/en-US/technology/synchronous-technology/))

- The user moves, resizes or rotates faces directly, and adds dimensions to an imported model after the fact.
- Siemens describes dimensions, parameters and design rules being defined "at the time of creation or edit, without ordering or reordering a history".
- This is driven by a 3D constraint solver. Siemens lists "controlling the shape of parts without relying on a design history" as a use of D-Cubed 3D DCM. [P, vendor] (see [04-constraint-solvers.md](04-constraint-solvers.md))

### What this means for OpenShape

The owner's requirement is specifically a parametric model, which is the feature-recognition route. The existence and success of direct editing still matters in two ways:

1. It is the incumbent answer to "I have a STEP file and need to change it", so it sets the baseline that reconstruction has to beat to be worth using.
2. A reconstruction will often be partial. Something has to happen to the geometry that was not recognised. Direct editing on the remainder is the obvious complement.

The owner has since confirmed direct editing is in scope, at lower priority ([decision 0003](../../decisions/0003-scope.md)).

## Research on recovering construction history

### Datasets

| Dataset | Content | Has construction history | Mark |
|---|---|---|---|
| ABC | One million CAD models with explicit curve and surface parameterisations | No | [P, abstract] ([arXiv 1812.06216](https://arxiv.org/abs/1812.06216)) |
| DeepCAD | 178,238 models with CAD construction sequences | Yes, sketch and extrude | [P, abstract] ([arXiv 2105.09492](https://arxiv.org/abs/2105.09492)) |
| Fusion 360 Gallery | 8,625 human design sequences | Yes, sketch and extrude only | [P, abstract] ([arXiv 2010.02392](https://arxiv.org/abs/2010.02392)) |
| Zero-to-CAD | About one million synthetic executable sequences, with operations beyond sketch and extrude | Yes, synthetic | [P, abstract] ([arXiv 2604.24479](https://arxiv.org/abs/2604.24479)) |

The pattern is that large real datasets lack history, and datasets with history are either small or limited to sketch and extrude. Zero-to-CAD states the problem plainly: existing large datasets "predominantly consist of boundary representations (B-Reps) or meshes, stripping away this critical procedural information".

### Methods

Three of these papers were read in full by a delegated reader. [P] unless marked.

**Fusion 360 Gallery and Gym (2020)** ([arXiv 2010.02392](https://arxiv.org/abs/2010.02392))

- The task is recovering a sketch-and-extrude program for a known target solid. The engine in the loop is the Fusion 360 application itself.
- **How the agent points at geometry.** The agent sees the target as a graph whose nodes are faces, each described by a 10 by 10 grid of sampled points and normals, a trimming mask and a surface type. An action is a triple: a start face, an end face, and an operation (new body, join, cut, intersect). The start face's outline is the profile and the end face sets the distance. The agent never writes a coordinate and never names a face of its own model.
- Results: the best agent reconstructs 67.5% of test designs exactly within 100 steps. An agent choosing at random reaches 53.8%, because selecting among faces with invalid actions masked makes the search space small. The authors estimate a ceiling of about 80% for this representation.
- It fails when the face needed is not in the target, such as a face merged away by a later feature, and on sequences of four or more steps.
- **Speed is the stated bottleneck.** Each design takes 5 to 35 seconds, "the majority of evaluation time is spent inside the Fusion 360 Gym", and the step budget was capped for that reason. Some designs crash the application or hit a ten-minute limit.
- The authors warn that volume overlap "should be a secondary metric", because a high score can hide a missing hole.

**cadrille (2025)** ([arXiv 2505.22914](https://arxiv.org/abs/2505.22914))

- A model writes CadQuery programs from images, point clouds or text. It is trained on examples, then by reinforcement learning with a reward of volume overlap with the target, minus a penalty for programs that fail to run.
- Results from images, overlap and share of invalid programs:

| Dataset | After supervised training | After online reinforcement learning |
|---|---|---|
| DeepCAD | 86.1%, 1.5% invalid | 92.2%, 0.0% invalid |
| Fusion 360 | 77.6%, 3.2% invalid | 84.6%, 0.0% invalid |
| CC3D, real scans | 56.1%, 7.7% invalid | 65.0%, 0.1% invalid |

- Online learning with the engine in the loop improved everything. An offline variant mostly only reduced invalid programs.
- The reward needs only a target shape, not a target program, so training can use any solid.
- Limits: fine detail is missed, real scans stay at 65 to 68%, and the programs shown are chains of hard-coded numbers with no named parameters. Editability is asserted and not measured.

**Zero-to-CAD (2026)** ([arXiv 2604.24479](https://arxiv.org/abs/2604.24479))

- A language model in a tool-using loop writes CadQuery programs for part descriptions, with no target shape. Its tools are execute-and-validate and two documentation searches. Validation requires that the code runs, yields exactly one connected valid solid with at least seven faces, and exports to STL and STEP.
- About one million accepted programs took 3.8 million executions. First-attempt success was 22.3%, with a mean of 3.3 attempts before success. The run used up to 3,000 CPU cores for about a week.
- The vocabulary is wide: revolve, fillet, chamfer, loft, sweep, shell, patterns and holes as well as extrude.
- **The loop used no visual feedback.** The authors tried it and found current models "struggle to reliably detect these defects". Typical failures are thin features that break connectivity, misplaced holes and compositions that are "locally plausible but globally incoherent", which they attribute to text-only reasoning without spatial grounding.
- Readability is enforced by prompt rules (named parameters, logical steps) and is not validated by any study.
- A small model fine-tuned on the data produced runnable code 82% of the time on similar parts and 61% on real ABC parts.

**CADCL / Brep2Seq (2025)** reconstructs a feature sequence from a B-rep using a graph encoding. [S] ([JCDE](https://academic.oup.com/jcde/article/12/10/176/8272673)) Not read.

### What this means for OpenShape

1. **The core hypothesis has measured support.** Putting the CAD engine in the training loop raised reconstruction quality by 6 to 9 points and removed nearly all invalid output, across three datasets.
2. **Engine throughput is the limiting resource, and the papers say so.** One capped its search because each design took up to 35 seconds in the engine. Another needed 3.8 million executions and thousands of cores. This gives concrete meaning to the owner's statement that reconstruction "will be critical for RL improvements to the kernel": a fast, headless, crash-free, deterministic kernel is the thing these methods are short of. Throughput in executions per core-second belongs among the kernel's phase 3 requirements.
3. **Selecting faces beats writing coordinates.** The Fusion Gym agent picks faces from a graph and never emits a number, and that alone makes a random agent succeed more than half the time. This is evidence for the owner's position in [decision 0006](../../decisions/0006-geometry-references.md) that selection should be a pick among presented geometry. It also shows a form of "visual" selection that is not an image: a structured description of each face. The same paper shows the limit, since a pick can only choose what exists to be picked.
4. **Images alone are not yet a reliable feedback channel.** Zero-to-CAD dropped visual feedback because models could not spot the defects. Together with the benchmark finding in [03-ai-and-new-entrants.md](03-ai-and-new-entrants.md), this says an agent's view of geometry should include computed facts, such as connectivity, wall thickness and what changed, alongside any rendering.
5. **Reconstruction has an automatic score, with a known flaw.** Volume overlap is cheap and exact, and it hides missing small features. Scoring should also compare topology, for example face counts and types.
6. **Nobody measures editability.** None of the three checks whether an output program survives a parameter change, and the CadQuery programs refer to geometry by direction filters and absolute positions. A reconstruction that produces a robust, parametric feature tree is an open problem, and a native feature system with durable references is what it would need.
7. **Data provenance matters.** The Fusion 360 Gallery is licensed for non-commercial research. The same paper notes that the ABC dataset's construction information is in a proprietary Onshape format. Licences for the others are not stated in the papers. Any use of these for training or benchmarking needs a licence check first.

## Scan and mesh tools

Deferred by the owner. One note held for later: Geomagic Design X converts scan data to feature-based CAD with guided and automatic feature extraction and transfers the result to mainstream CAD systems. [S] ([reseller page](https://prototypingsolutions.com/product/geomagic-design-x/)) Parasolid's approach of admitting mesh data as a surface type inside the B-rep is recorded in [02-kernels.md](02-kernels.md).

## Gaps to close before this topic is complete

- The CADCL / Brep2Seq paper, which is the closest to reconstruction from a B-rep and was not read.
- Classical feature-recognition literature (graph-based, volume decomposition, hint-based): not searched.
- Reconstruction results specifically from B-rep input, with success rates on realistic parts.
- Any measure of the editability or intent quality of a reconstructed tree.
- Licences and provenance of ABC, DeepCAD and Fusion 360 Gallery.
- Feature recognition in NX, Creo and Fusion, and third-party translators that claim to transfer feature history between CAD systems.
