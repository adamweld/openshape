# AI for CAD and new entrants

Evidence marks are defined in the [phase README](README.md).

## Summary

- Every shipping approach found so far has the AI produce code or a finished artefact. None gives an agent a way to perceive and point at geometry inside a live model.
- The closest existing product to OpenShape's goals is Zoo: a new kernel, a code-backed model, and both a GUI and an agent on top. It differs on deployment (cloud-hosted engine) and openness (engine is closed).
- Published benchmarks put the weakness of current models in spatial reasoning and perception, not in code syntax.

## Zoo (formerly KittyCAD)

All points below are the vendor's own statements. [P] ([Zoo Design Studio v1](https://zoo.dev/blog/zoo-design-studio-v1), Zoo, May 2025)

| Aspect | What Zoo states |
|---|---|
| What they built | Their own geometry engine, programming language (KCL), ML model and CAD GUI |
| Effort | "Two years, fewer than 30 engineers" |
| Representation | B-rep with "exact NURBS and analytic surfaces" throughout |
| Stated technical bet | Surface/surface intersection reformulated "as a parallelizable root-finding problem that runs on modern GPUs", in place of "thousands of if/else branches" |
| Stated motivation | "Real-time ML workflows and sub-second Boolean ops" |
| Shipped in v1 | Primitives, sketch constraints, patterns, shell, helix, extrude, revolve, fillet, chamfer, loft, sweep, GPU-accelerated booleans, assemblies, STEP export |
| On the roadmap at v1 | "Constraints 2.0 and assembly mates", engine-side caching to "eliminate full-world rebuilds", drawings and GD&T |
| Model as code | Every model is KCL; the GUI is optional to use but everything it does is expressed as code |
| Benchmarks | "We'll publish detailed benchmarks as further optimizations land" |

Further points from secondary sources: [S]

- The engine is hosted; the 3D view reaches the client as a video stream over websockets. ([Zoo documentation index](https://docsearch.algolia.com/mcp/docs/repo/kittycad/modeling-app))
- The application layer is open source; the engine is not. (same source)
- A conversational agent, Zookeeper, is integrated in the application, and all GUI, text-to-CAD and agent actions produce KCL. ([Develop3D](https://develop3d.com/cad/zoo-ecosystem-lays-foundation-for-modern-hardware-design-toolkit/))

### Reading this carefully

What it supports:

- A new B-rep kernel reaching a usable feature list is achievable by a small team in years, not decades.
- A GPU-oriented formulation of surface intersection is at least workable. This is a design input for phase 3.
- A code-backed model with a GUI on top is a shipped pattern, consistent with [decision 0005](../../decisions/0005-single-operation-layer.md).

What it does not support:

- Robustness. No failure-rate data or benchmark is published. A feature list says an operation exists, not how often it succeeds on hard geometry. The same launch post lists engine-side caching and mates as future work, which indicates the distance still to go at that date.
- The phrase "close decades of feature gap" is a marketing claim.

What OpenShape would do differently, on current decisions: run locally, and keep the engine open.

Gaps: how KCL refers to faces and edges (it has a tagging mechanism [U]); how the GUI's picks are written into code; the current state of the product eighteen months after this post; any independent evaluation.

## Onshape

- **FeatureScript MCP Server.** Released through Onshape Labs. An external AI client writes FeatureScript; the server offers "tools to search FeatureScript documentation, create, insert, test, and evaluate custom features". Code is "evaluated in a sandbox workspace rather than against live design data", errors are returned, and the model iterates. [P] ([Is CAD Data Safe When AI Connects to Onshape?](https://www.onshape.com/en/blog/cad-data-ai-mcp-client-server), Onshape, November 2026)
- Onshape frames the AI's role as ending once the feature is written: "AI is involved only while the feature is being written, not every time it's used." [P] (same source)
- Onshape notes that FeatureScript is a language "which LLMs have already learned", because it and the standard features are open. [P] ([FeatureScript MCP page](https://www.onshape.com/en/features/featurescript-mcp))
- **AI Advisor** is an in-product assistant grounded in Onshape's documentation and training material. It gives guidance and does not operate on the model. [S] ([Digital Engineering](https://www.digitalengineering247.com/article/onshape-ai-advisor-now-embedded-directly-in-the-design-environment))

Reading: the reference product's AI integration is a tool-building loop (write a feature, test it, fix it), which is a real closed loop but a narrow one. It closes on "does the code run", not on "is the design good". Nothing found gives the agent rendered views, picking, or analysis results.

## Autodesk

- "Neural CAD", announced at Autodesk University 2025, is a foundation model intended to generate editable B-rep geometry directly, as opposed to an LLM calling tools in an existing modeller. [S] ([Develop3D](https://develop3d.com/cad/autodesks-ai-blueprint-for-cad/))
- Availability is unclear, and Autodesk reportedly "cannot yet guarantee perfect precision". [S] (same source, June 2026)

Reading: this is the opposite bet from Zoo and Onshape, with geometry coming from the model's weights and not from a kernel executing a program. Precision is the stated difficulty, which is what one would expect.

## Other integrations

- Community MCP servers exist for FreeCAD, Fusion, SOLIDWORKS and Blender. Many reduce to "get scene info" plus "run arbitrary script". [S] ([dev.to survey](https://dev.to/grove_chatforest/cad-3d-modeling-mcp-servers-blender-freecad-autocad-kicad-solidworks-and-more-20ja))
- Viewport screenshots were found documented only for the Blender server. [S] (same source) Nothing was found on how any of these servers lets an agent select a face or edge.

## What benchmarks say about current models

**BenchCAD** (May 2026): 17,900 execution-verified CadQuery programs across 106 industrial part families, testing more than ten frontier models on visual questions, code questions, image-to-code and code editing. [P for the abstract] ([arXiv 2605.10865](https://arxiv.org/abs/2605.10865))

From the abstract:

- Models "often recover coarse outer geometry but fail to produce faithful parametric CAD programs".
- Common failures: "missing fine 3D structure, misinterpreting industrial design parameters, and replacing essential operations such as sweeps, lofts, and twist-extrudes with simpler sketch-and-extrude patterns".
- Fine-tuning helps in-distribution, but "generalization to unseen part families remains limited".

From a summary of the full paper, not yet read: spatial reasoning is the weakest axis for most models even with code access, and models score markedly lower answering from images than from code. [S] ([review](https://www.themoonlight.io/en/review/benchcad-a-comprehensive-industry-standard-benchmark-for-programmatic-cad))

**Text2CAD-Bench** reportedly finds performance degrades substantially on advanced features. [S]

### What this implies for OpenShape

- The benchmarks test one-shot generation into a code-only CAD library with no feedback. That is the setting least like the closed loop in OpenShape's hypothesis, so poor results there do not refute the hypothesis. They do show where a model needs help.
- The weak point is spatial understanding. This supports the owner's position in [decision 0006](../../decisions/0006-geometry-references.md) that text alone is not enough, and it raises a harder question for phase 4: if models also perceive images less reliably than code, then plain screenshots are not sufficient either. The interface probably needs views that are built for an agent to read and pick from, not views built for a human eye. That is a hypothesis to test, not a finding.
- The tendency to fall back on sketch-and-extrude suggests an agent needs the tool to make advanced operations as easy to reach and to check as simple ones.

## Gaps to close before this topic is complete

- Read the BenchCAD and Text2CAD-Bench papers in full.
- Survey agentic, feedback-driven CAD research (as opposed to one-shot generation), which is the work closest to our hypothesis. A start is in [07-reverse-engineering.md](07-reverse-engineering.md): cadrille and Zero-to-CAD both report gains from putting a CAD engine in the loop.
- SOLIDWORKS, Siemens NX and Creo AI features: not researched.
- Startups working on AI mechanical design: not researched.
- Generative design and topology optimisation products, which are the existing form of "design, test, optimise" and belong with topic 6.
