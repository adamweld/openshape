# Simulation, DFM and optimisation

Evidence marks are defined in the [phase README](README.md). This is a first pass.

This topic covers the "test" and "optimise" halves of the loop in [VISION.md](../../VISION.md): what exists for analysing a design automatically, and what is known about putting an AI agent in that loop.

## Summary

- The step that stops analysis being automatic is geometry preparation: simplifying the model and meshing it. A group of commercial solvers now avoids that step and works on the CAD geometry directly. This is the most important development for a closed loop.
- Published agent research shows that external verification, not a better model, is what makes generated designs reliable. One study raised code compliance from 56.8% to 98.6% by adding a physics-based verifier and attributes the gain to the verifier.
- Manufacturability checking exists commercially as rule and feature analysis attached to quoting. Its rules are not published.
- No standard found carries load cases, load paths or functional interfaces alongside geometry. The standards that exist cover tolerances and inspection. This is the gap the owner identified, and the search supports that it is real.

## Structural simulation

### The conventional workflow and its bottleneck

Finite element analysis needs a mesh that conforms to the geometry. Getting one usually means removing small features first. Altair describes geometry simplification and meshing as "the two most time-consuming, and error-prone tasks involved with traditional structural analysis". [S, vendor] ([Altair](https://altair.com/resource/revolutionizing-structural-simulation-with-altair-simsolid))

There is one measured data point on how fragile meshing is: an open-source mesher fails on 1.56% to 8.82% of models across public CAD datasets (see [02-kernels.md](02-kernels.md)). For a loop that runs unattended thousands of times, a failure rate of a few percent at one step is a serious obstacle.

### Solvers that skip meshing

| Product | Approach as described by the vendor | Mark |
|---|---|---|
| Intact.Simulation | Embeds the geometry in a uniform background grid whose cells "do not need to conform to the shape of the geometry". Elements are conventional; the integration rule for each cell is computed from the geometry inside it. Accepts B-reps, surface meshes, implicits, voxels and CT data. | [S, vendor documentation via summary] ([Intact](https://intact-solutions.com/intact_docs/about/core_technology.html)) |
| Altair SimSolid | "Always uses fully featured, not simplified, solid geometry models" and "does not use a mesh". Adaptive refinement. | [S, vendor] ([Altair whitepaper](https://altair.com/docs/default-source/resource-library/altair_whitepaper_simsolid-technology-overview_10_30_2020.pdf)) |
| Onshape Simulation | "A unique, proprietary, and cloud-native approach to finite element analysis". Loads and constraints are applied to parts and faces with no meshing step shown to the user. | [P, vendor] for the quote ([Onshape](https://www.onshape.com/en/features/simulation)); [S] for the rest |
| Ansys Discovery | GPU-based near-real-time simulation, positioned as rapid analysis and not a replacement for full CAE. | [S] ([Digital Engineering](https://www.digitalengineering247.com/article/going-live-with-real-time-simulation)) |

All accuracy claims here are the vendors' own. No independent comparison was found. Intact's own guidance warns against comparing stress near singularities. [S]

What matters for OpenShape is the shape of the idea in the first row. If the solver only needs to ask the geometry "what part of this cell is inside the solid", then simulation depends on the kernel answering point and volume queries quickly and reliably, not on a mesher succeeding. That is a requirement on the kernel that phase 3 should consider.

### Assembly-level setup

Onshape derives simulation connections from mates: fastened, revolute and slider mates become connections automatically. [S] ([Onshape blog](https://www.onshape.com/en/blog/kinematics-assemblies-mates-simulation)) An Onshape employee notes limits: mate limits do not inform boundary conditions, and friction is not modelled. [S, forum]

This is a small working example of what the owner asked for. The mate, defined once for assembly, is reused as analysis input, so intent entered for one purpose serves another. It stops short of loads, which still have to be entered by hand per study.

### Learned surrogates

- Companies such as PhysicsX and Neural Concept train models that predict simulation results from geometry in seconds. [S] ([IEEE Spectrum](https://spectrum.ieee.org/large-physics-models-design-engineering))
- Practitioners caution that a surrogate can do well on shapes like its training set and "wobble" on a new product family, and Neural Concept's own leadership says surrogates will not fully replace simulation. [S]

Reading: surrogates are a speed layer inside a loop that still needs a trusted solver for verification. They are not a substitute for one.

## Manufacturability

- **Quoting services.** Protolabs and Xometry run automated manufacturability analysis as part of instant quoting. Advisories cited include thin walls, small gaps and size limits. [S] ([Protolabs](https://protolabs.com/en-gb/help-centre/manufacturing-analysis))
- **Cost and DFM tools.** aPriori derives cost and manufacturability from geometric features it calls geometric cost drivers, using bottom-up simulation of the manufacturing process, and reports a severity-ranked list of issues. [S, vendor] ([aPriori](https://www.apriori.com/dfm-plus))
- No source found documents the actual rules or thresholds any of these tools apply, or how they compute tool access for machining or draft and undercuts for moulding.

Reading: the capability exists and is commercially valuable, and its content is proprietary. For OpenShape the open question is less the checks themselves than where their inputs come from. A wall-thickness check needs to know the process and material, which is exactly the "manufacturing method specified per part" in the owner's scope.

## Assembly

- Research derives assembly sequences from CAD by searching for collision-free disassembly paths, using mating information to propose candidates and interference checks to validate them. [S] ([Stevens](https://researchwith.stevens.edu/en/publications/automatic-disassembly-plan-generation-from-cad-assembly-models/))
- A 2024 paper trains a reinforcement-learning agent in a physics environment to find feasible sequences, explicitly to give designers assembly feedback before release. [S] ([Design Society](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/423CA3D33AF5D3DCD1F2419C81C4A905/S2732527X24002207a.pdf/automating-the-assembly-planning-process-to-enable-design-for-assembly-using-reinforcement-learning.pdf))
- Siemens sells collision detection and clearance measurement as a separate component, D-Cubed CDM. [P, vendor] (see [04-constraint-solvers.md](04-constraint-solvers.md))

Reading: "test assembly" in the owner's sense is achievable as "does a collision-free insertion path exist for each part in some order". That reduces to fast, exact collision and clearance queries on the kernel plus search. No commercial CAD system found offers this as a built-in check.

## Standards for engineering intent

| Standard | Carries | Mark |
|---|---|---|
| STEP AP242 with semantic PMI | Dimensions, tolerances and datums in computer-interpretable form, bound to faces and edges | [S] ([NIST](https://nvlpubs.nist.gov/nistpubs/gcr/2016/NIST.GCR.16-003.pdf)) |
| QIF (ISO 23952) | Inspection plans and measurement results linked to the specification | [S] ([Chalmers](https://research.chalmers.se/publication/545319/file/545319_Fulltext.pdf)) |

Nothing found in either covers loads, load paths, functional interfaces between parts, or intended manufacturing process. The search was not exhaustive: systems-engineering standards such as SysML and the simulation data standards were not checked. Until they are, "no standard exists" is a provisional reading. [U]

What the existing standards do show is the pattern to follow: semantic PMI works because each tolerance is attached to specific faces and is machine-readable. Intent that is a free-text note is invisible to tools.

## Agents in the loop

| Work | What it does | Result reported | Mark |
|---|---|---|---|
| Physics-in-the-Loop (IJCAI 2026) | Agents "iteratively plan, generate, evaluate, and revise engineering designs" from a load case, with engineering tools as the feedback signal | 4.2 times higher structural complexity than comparable agentic methods | [P, abstract] ([IJCAI](https://ijcai.org/proceedings/2026/714)) |
| Verification-driven structural design (2026) | Feeds results from an external finite-element and code-checking verifier into a repair loop | Code compliance from 56.8% to 98.6% across 44 cases; no detectable difference between the two language models tested | [P, abstract] ([arXiv 2608.07978](https://arxiv.org/abs/2608.07978)) |
| MDO Agent (2025) | Language model orchestrates parametric modelling, knowledge retrieval and FEA-driven optimisation | Three worked cases, described as semi-automated | [P, abstract] ([arXiv 2511.17511](https://arxiv.org/abs/2511.17511)) |
| VFEAgent (2026) | Builds complete FEA setups from images and problem text | "High success rate", no figure in the abstract | [P, abstract] ([arXiv 2605.28978](https://arxiv.org/abs/2605.28978)) |

Two statements from these abstracts are worth quoting.

From Physics-in-the-Loop: "Instead of attempting to implicitly learn physical laws from data, we propose a Hybrid Agentic-Physical Architecture that embeds validated knowledge-based engineering tools directly into the decision-making loop."

From the verification-driven paper: the improvement is "attributed to the external verifier rather than the LLM".

### What this means for OpenShape

1. **The core hypothesis is the direction the research field is already moving.** Several independent groups in 2025 and 2026 report that closing the loop with real verification is what makes agent-produced designs reliable. Together with the reconstruction results in [07-reverse-engineering.md](07-reverse-engineering.md), this is the strongest evidence gathered in phase 1.
2. **These systems are assembled from separate tools.** Each paper wires a language model to a CAD library and a separate solver through scripts. None works inside a CAD platform where geometry, intent and analysis share one model. That integration is what OpenShape proposes, and no evidence was found that anyone has built it.
3. **The load case is the starting input in this research**, and it is supplied by hand, outside the CAD model. Encoding it in the model is the unsolved piece.
4. **Verifier quality sets the ceiling.** If reliability comes from the verifier, then the trustworthiness, speed and failure rate of OpenShape's checks matter more than which model drives them. A check that fails to run a few percent of the time, or that returns a result with no indication of its accuracy, undermines the whole loop.

## Gaps to close before this topic is complete

- Read the four agent papers in full, including how each represents loads and what fails.
- Topology optimisation and generative design products (Fusion, nTop, Altair Inspire), which are the existing commercial form of an automated design loop. Not researched.
- Independent accuracy assessments of meshless and immersed solvers.
- Open literature on machining accessibility analysis, draft and undercut analysis, and additive manufacturability.
- Tolerance analysis tools.
- SysML v2, simulation data standards and any other standard that might carry loads or interfaces.
- CAM: toolpath generation as the ultimate manufacturability test. Not researched.
- Thermal, fluid and other physics beyond structural. Not researched.
