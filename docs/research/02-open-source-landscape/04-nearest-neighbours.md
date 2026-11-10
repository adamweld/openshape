# Nearest neighbours: SolidCraft and SMLib

This document looks more closely at the two projects that matter most to OpenShape's direction. It extends [01-landscape.md](01-landscape.md). Everything is from the projects' own documentation, read on 2026-11-10, and is evidence mark **[P]** for what they state. None of it has been tested here.

## Why this needs its own document

Phase 1 ended with a list of openings left by the reference commercial kernel: no persistent naming, non-uniform lineage, tolerance that only grows, operations that are not transactional, and no determinism. It also recorded positions on how an agent should work with CAD.

SolidCraft has already taken a position on most of them, in shipped code. The comparison below is the most important input to the owner's decision on [decision 0004](../../decisions/0004-ground-up-kernel.md).

## SolidCraft's agent interface

From its MCP documentation. ([docs/mcp.md](https://github.com/tangency-labs/solidcraft/blob/main/docs/mcp.md))

| Capability | How SolidCraft does it |
|---|---|
| Discover operations | `list_commands` returns the catalogue; `describe_command` returns JSON Schemas for a command's input and output |
| Run operations | `execute` runs one command; `batch` runs a list |
| Transactions | "Failures leave the design unchanged." A batch stops at the first error and undoes the completed steps by default |
| Assertions | `expect` on any call states the volume, body count or bounding box the step should produce. The server measures and flags a mismatch as an error, "so the model notices" |
| Inspect the design | `inspect_design` returns parameters, the timeline with errors and timings, bodies with volume and counts, sketches with their degrees of freedom and solve status, and joints with whether their references still resolve |
| Structured view of geometry | `body_topology` returns every edge (index, midpoint, length, ends) and face (index, name, area, centroid, normal, and a point guaranteed to lie on it). Cylinders can be returned merged, as radius, origin, axis and extent |
| Select geometry | A face is picked by its persistent name or by a point on it; an edge by its midpoint. The topology listing supplies exactly those values |
| Measure | `measure` on bodies or on picked faces and edges |
| See | `screenshot` from standard or custom views, rendered headless on a GPU or CPU |
| Compare with a picture | `compare_picture` overlays the model's silhouette on a reference image and reports the mismatch in millimetres at stations around the outline |
| Same path as the GUI | Headless, or bridged to the running application so a person can watch the agent work |

How this relates to OpenShape's open questions:

- **[Decision 0006](../../decisions/0006-geometry-references.md), selection.** SolidCraft's answer is close to the Fusion 360 Gym finding in phase 1: the agent is given a structured list of the geometry that exists and picks from it, by name or by a point the system supplied. It also has images. This is a working example of the synthesis proposed in that decision record: selection among presented geometry, stored as a durable name.
- **[Decision 0005](../../decisions/0005-single-operation-layer.md), one operation layer.** Implemented as a hard rule, with schemas.
- **Checkable intent.** `expect` covers volume, body count and bounding box only. It is an assertion on the result of a step, not a statement of engineering requirements. Nothing found covers clearance, wall thickness, loads, interfaces or manufacturing process.

## SolidCraft's persistent naming

From its naming design document. ([naming.md](https://github.com/tangency-labs/solidcraft/blob/main/docs/book/src/dev/naming.md))

The document describes replacing an earlier scheme. Names "used to be worked out from geometry", by sampling points and taking a majority, and that approach "is right most of the time, and wrong exactly when it matters: after an upstream edit that splits, merges, mirrors or shrinks a face ... a fillet or a sketch quietly re-attaches to a different face. Nothing tells the user, which is the worst thing a CAD tool can do."

The current scheme:

- "The kernel now reports, for every operation, what each face and edge of its result came from." Names follow that history, "so they are exact and deterministic".
- Faces built by a feature are named by role, for example a side face is named after the sketch curve it was swept from, and a fillet face after the edge it replaced.
- **Split faces** are told apart "by the faces around them that the others lack". The document's example is the piece of a block's top face bounded by a particular wall and a particular slot wall, which "survives the slot moving, growing or shrinking". Only pieces that nothing distinguishes are numbered.
- **Merged faces** take the name of the face they are all pieces of and answer to the others' names as aliases.
- **Edges** are named by the two faces they separate.
- "When a reference can no longer be found exactly the feature says so instead of guessing."

Set against phase 1:

- This is the design direction phase 1 identified as the opening: uniform lineage from the kernel, splits and merges as first-class cases, and a refusal in place of a silent wrong answer.
- It is the strongest counter-evidence so far to the view that references of this kind cannot work on real models. It is also unproven at scale: SolidCraft describes itself as "early but usable for simple parts", and no failure-rate data was found. The owner's objection in decision 0006 concerned complex real-world designs, and that case is still untested by anyone.
- A numbered piece that "nothing around them tells apart" is the residue of the hard problem. How often that case arises on complex parts is the measurement that would settle the question.

## SMLib's stated limits

From NVIDIA's known-issues list for USD BRep. ([KNOWN_ISSUES.md](https://github.com/NVIDIA-Omniverse/usd-brep/blob/main/KNOWN_ISSUES.md))

- Healing "can report success when a repair failed".
- Shelling "can return a result that is not a solid", with a filleted box given as an example.
- One stitching function "crashes the process on every input tried".
- The body-relationship check "looks for overlaps at sample points", so a shallow overlap "is reported as touching, not interpenetrating".
- Tessellation can produce inside-out triangles next to fillets and badly shaped triangles at sphere poles.
- Malformed input "can read out of bounds and crash the process".

Reading:

- A commercial kernel with a long history still crashes and returns non-solids on small examples. That is useful calibration: maturity does not mean the edge cases are gone.
- Several of these are the class of defect solidcore says it is designed against: sampling in place of proof, crashes on bad input, and silent wrong results. solidcore's stated rule is that "a check that samples points is not a certificate".
- The list is short and specific, and publishing it at all is a good sign about how the release is being run. It is not a robustness measurement.

## Who is behind them

From press coverage and repository pages. [S]

**SolidCraft**

- Created by a single GitHub developer and now hosted by an organisation, Tangency Labs, with 16 repositories. No founders, company or funding were identified; its continuous integration is sponsored by a CI vendor. ([repository](https://github.com/tangency-labs/solidcraft))
- Trade press describes it as one of several "vibecoded clones" of commercial CAD released as open source, meaning built largely by AI coding agents at high speed. ([3D Printing Industry](https://3dprintingindustry.com/news/vibecoded-clones-of-solidworks-and-autocad-released-as-open-source-255770/)) Its own description is a "clean-room" implementation "designed from public documentation and general CAD conventions".
- It reached version 0.30 within about a month of its first release, and its repository rules are written for many agents working in parallel.
- The licence is reported as MIT or Apache-2.0 at the user's choice.

Reading: its pace and breadth come from the same method OpenShape intends to use. Its documents show real design thought, particularly on naming and certified geometry. What nobody has shown is how well the breadth holds up on hard cases, and a project moving this fast under one maintainer carries continuity risk. Both points matter for any decision to depend on it.

**USD BRep**

- NVIDIA acquired Solid Modeling Solutions, SMLib's maker, in May 2022. ([Wikipedia](https://en.wikipedia.org/wiki/Solid_Modeling_Solutions))
- No official statement of NVIDIA's reasons was found. Coverage ties the release to OpenUSD and to AI-driven CAD, and notes it ships with an MCP server for agents. ([3D Printing Industry](https://3dprintingindustry.com/news/nvidia-opens-cad-modelling-kernel-what-could-it-mean-for-ai-assisted-design-and-3d-printing-255720/))
- The repository is not accepting outside contributions, so it is a published codebase more than a community project.

## What is not occupied

Checked against SolidCraft's README, capability list, roadmap and MCP documentation. Absence from documentation is not proof of absence in code. [S]

| OpenShape scope item | Found in SolidCraft |
|---|---|
| Encoding interfaces between parts | Joints with persistent references; nothing describing a part's interface as a reusable definition |
| Load paths and load cases | Not found |
| Manufacturing method per part | Sheet-metal and plastic rules exist as feature settings; no general process definition found |
| FEA in the loop | Not found; rigid-body dynamics and motion studies are present |
| DFM checks | Not found |
| Testing assembly, such as insertion paths | Interference and contact sets are present; assembly sequence checking not found |
| Parametric models from STEP | STEP import as a feature; reconstruction of a feature tree not found |
| Drawings | Not examined |
| Direct editing | Face commands exist (delete, offset, replace, split); extent not examined |
| Training environment for reinforcement learning | Not found in SolidCraft; vcad advertises a "gym-style RL interface" |

The closed design, test and optimise loop that is OpenShape's core hypothesis, and the intent model it needs, do not appear to be anyone's current focus.

## Gaps

- No code was read. Claims about what SolidCraft or solidcore do are their documentation's claims.
- No measurement of solidcore or SMLib. SMLib has a Python package and could be run through the benchmark in [bench/](bench/) once installing it is approved.
- SolidCraft's governance, contributor terms and the people behind it were not researched. They matter for any decision to build on or contribute to it.
- Its file format, drawings and direct editing were not examined.
