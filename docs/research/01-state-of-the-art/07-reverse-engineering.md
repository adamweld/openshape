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

- **Fusion 360 Gym** (2020) framed reconstruction as a Markov decision process: an environment that "exposes the sequential construction of a CAD program", with the task of "recovering a CAD program from a target geometry". [P, abstract]
- **CADCL / Brep2Seq** (2025) reconstructs a feature sequence from a B-rep using a graph encoding of the B-rep aligned with sequence embeddings. [S] ([JCDE](https://academic.oup.com/jcde/article/12/10/176/8272673))
- **cadrille** (2025) trains a model with supervised fine-tuning, then with "reinforcement learning (RL) fine-tuning using online feedback, obtained programatically". The authors report that online RL beats offline alternatives and that the RL stage sets the state of the art on three datasets, including a real-world one. Its inputs are point clouds, images and text, not B-reps. [P, abstract] ([arXiv 2505.22914](https://arxiv.org/abs/2505.22914))
- **Zero-to-CAD** (2026) generates its dataset by "embedding a large language model within a feedback-driven CAD environment" that "iteratively generates, executes, and validates code". [P, abstract]

### What this means for OpenShape

1. **The core hypothesis has direct support.** Two independent lines of work found that putting a CAD engine in the loop, so the model's output is executed and scored, outperforms learning from static examples. That is the closed loop in [VISION.md](../../VISION.md), demonstrated on a narrower task.
2. **The kernel is the training environment.** In these papers the engine in the loop is an open CAD library, and the vocabulary of operations the model can learn is whatever that engine executes reliably. A fast, deterministic, headless kernel with a rich operation set is the limiting resource for this kind of training. This gives concrete meaning to the owner's statement that reconstruction "will be critical for RL improvements to the kernel", and it turns kernel throughput and determinism into requirements for phase 3, not only conveniences.
3. **Reconstruction has an exact, automatic score.** Given a STEP file, a proposed feature tree can be rebuilt and compared geometrically with the original. Few CAD tasks have a ground truth this clean, which makes reconstruction a natural first closed-loop task.
4. **Shape match is not the whole objective.** A tree can reproduce the geometry and still be useless to edit. Any scoring has to include some measure of whether the tree is one a designer would build. No source found defines such a measure.
5. **The reference product is the source of much of this data.** Whether ABC and DeepCAD were collected from public Onshape documents is commonly stated but was not confirmed here. [U] If so, their licence terms need checking before we rely on them.

## Scan and mesh tools

Deferred by the owner. One note held for later: Geomagic Design X converts scan data to feature-based CAD with guided and automatic feature extraction and transfers the result to mainstream CAD systems. [S] ([reseller page](https://prototypingsolutions.com/product/geomagic-design-x/)) Parasolid's approach of admitting mesh data as a surface type inside the B-rep is recorded in [02-kernels.md](02-kernels.md).

## Gaps to close before this topic is complete

- Read the cadrille, Zero-to-CAD, Fusion 360 Gallery and CADCL papers in full. Only abstracts were read.
- Classical feature-recognition literature (graph-based, volume decomposition, hint-based): not searched.
- Reconstruction results specifically from B-rep input, with success rates on realistic parts.
- Any measure of the editability or intent quality of a reconstructed tree.
- Licences and provenance of ABC, DeepCAD and Fusion 360 Gallery.
- Feature recognition in NX, Creo and Fusion, and third-party translators that claim to transfer feature history between CAD systems.
