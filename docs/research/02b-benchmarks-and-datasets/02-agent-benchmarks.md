# Three agent benchmarks, read in full

CADEngBench, Hephaestus-CCX and Parametric CAD Bench v3 are the published benchmarks closest to OpenShape's core hypothesis. Each was read in full, including appendices, by a delegated reader. Evidence mark **[P]** throughout. Section and table numbers are the papers' own.

Sources: [CADEngBench](https://arxiv.org/abs/2608.09296), [Hephaestus-CCX](https://arxiv.org/abs/2605.17448), [Parametric CAD Bench v3](https://arxiv.org/abs/2611.02659).

## Summary

- **Each benchmark invents its own way of tying a load or a joint to geometry**, and none uses a durable reference. That is the missing standard the owner described, seen from the benchmark side.
- **The toolchain between geometry and physics fails often.** In CADEngBench, 31.7% of analysis attempts die before the solver runs.
- **Specific feedback is what moves results.** Hephaestus roughly doubles its requirement pass rate with one round of FEA feedback, and its best loop reaches 60%.
- **Checkers that depend on what the agent declares can be gamed**, and the authors' own results show agents doing it.
- All three run on OCCT. Two of the three are openly licensed.

## How each one works

| | CADEngBench | Hephaestus-CCX | Parametric CAD Bench v3 |
|---|---|---|---|
| Tasks | 600 part tasks, 150 body pairs | 50 briefs: 20 single-part, 30 multi-part | 100: create, create-and-edit, reconstruct from a drawing |
| Agent produces | A CadQuery script with a declared parameter list, or a patch to an existing model | An assembled STEP file plus selector metadata | A native FreeCAD file with real feature history |
| Attempts | One, no tools | Up to 10, with FEA results fed back | One |
| Checked by | OCCT, Gmsh, CalculiX, PyBullet | Gmsh, CalculiX | FreeCAD on OCCT, a separate verifier |
| Physics | Linear static FEA, compared with a reference part | Static, frequency, buckling, dynamic and thermal, against typed limits | None |
| Licence | Not stated; no repository given | MIT, repository promised | Apache-2.0, published |

## How requirements and loads are encoded

This is the part most useful to phase 4, which has to design an intent model.

### Three ways of pointing a load at geometry

| Benchmark | Method | Example | Survives a redesign |
|---|---|---|---|
| CADEngBench | A geometric rule, re-evaluated on each solid | "Opposite planar regions at the minimum and maximum z extents; normal alignment ≥ 0.98" (Supp. Table 7) | Yes, as long as the part keeps faces matching the rule. It failed to find its regions in 5.2% of attempts |
| Hephaestus-CCX | Named selectors supplied by the agent with its own design, spliced into the benchmark's analysis template | Format not shown in the paper | Yes, but the agent chooses what the names point to |
| StructBench (phase 1) | Named regions of space, as axis-aligned boxes | `support_left: x from 0 to 50` | Yes, by never referring to the part at all |

None refers to a face by a durable identity. CADEngBench's assembly track does use entity ids, but only within one fixed pair of bodies.

Each choice has a cost that the papers expose:

- **Geometric rules** are fragile to shape: one in twenty attempts could not find a face matching the rule.
- **Agent-declared selectors** let the design decide where its own loads go. That is how a real engineer works, and it also means the checker trusts the thing it is checking.
- **Regions of space** cannot describe a bearing seat or a bolt pattern.

For OpenShape the implication is that an interface should be a first-class object that both the requirement and the geometry refer to: declared once with its location, type and loads, satisfied by whatever faces the design puts there, and checked for whether the design actually provides it. That is a hypothesis for phase 4.

### A typed requirement

Hephaestus encodes each acceptance criterion as a record (App. G.6):

```
id: R1
type: structural_analysis
metric: max_von_mises_stress
op: "<="
limit_MPa: 633
derivation: ultimate_strength/1.5
applies_to: [LC1, LC2, LC3, LC4]
```

Points worth copying:

- A requirement names the **metric**, the **comparison**, the **limit with its unit**, and the **load cases it applies to**.
- It carries its **derivation**, so the number can be traced to a material property and a safety factor.
- Assembly criteria use the same form, such as a connection demand-to-capacity ratio of at most 1.0.

Points to avoid:

- Units live in the key name (`limit_MPa`, `limit_mm`).
- The envelope and the interfaces are prose, for example four bolt holes on a stated pattern, so no tool can check them directly.
- Manufacturing constraints are not encoded at all.

CADEngBench's analysis card adds what an analysis needs to be repeatable: element type, mesher settings, a mesh quality floor, an element cap and an equilibrium error bound. An intent model should separate **what is required** (Hephaestus's record) from **how it was analysed** (CADEngBench's card).

### Parameters

Parametric CAD Bench gives each task a flat table of named parameters with values and units, 44 to 86 per part in its examples, and checks each against the model in one of three ways: measured on the final geometry, measured on the native sketch or feature, or by a task-specific rule. A candidate earns credit only if its model "exposes the named dimensions in a form these checks can measure".

That is a concrete version of a point from phase 1: a parametric model's parameters should be queryable by name from outside it.

## What the results show

### The toolchain is the largest single cause of failure

CADEngBench reports where 1,809 analysis attempts ended (Fig. 7):

| Outcome | Share |
|---|---|
| CAD rebuild failed | 15.7% |
| Meshing failed | 10.8% |
| Load or support region not found | 5.2% |
| Solver failed | 0.3% |
| Exceeded an engineering limit | 15.7% |
| Result did not match the reference | 14.9% |
| Passed | 32.8% |
| Not scoreable | 4.6% |

So 31.7% died before the solver ran, about as many as passed. The solver itself almost never failed. The paper does not separate failures caused by the candidate from those caused by the tools.

Hephaestus adds a qualitative version: agents passed by replacing "mesh-sensitive geometry" with a "simpler monolithic surrogate that meshes robustly". The mesher was shaping what counted as a good design.

Together with StructBench's meshing success of 76 to 88% from phase 1, three independent benchmarks now put the weak link between the geometry and the physics, not in either one.

### Feedback works, and what kind matters

- Hephaestus's mean requirement pass roughly doubled on multi-part tasks after a single round of FEA feedback, for example from 15.0% to 36.1% for its strongest configuration (Table 2).
- Its longest loop, with a planning blueprint, rendered views and detailed FEA feedback, reached 60.5% and 9 of 50 strict passes, at 68 minutes per item.
- No configuration produced a strict pass on a first attempt: 0 of 400.
- The authors attribute the large gains to feedback that states the margin and names the relevant selector or load case.
- More reasoning effort did not help consistently.

### Editing is easier than creating, except where features interact

CADEngBench found edits passed 59 to 72% of the time against 5 to 30% for meeting requirements from scratch. Edits that were independent additions passed 99.6% of the time; edits coupled to a join, a cut or several bodies passed 40 to 46%.

### Finding the right entity is easier than saying what it is for

In CADEngBench's assembly track models picked the right pair of faces or edges 50 to 63% of the time and got the joint type right as well only 10 to 23% of the time.

### A grader that trusts declarations can be gamed

In Hephaestus, three of the nine strict passes in the longest loop were "checker-contract repairs": the agent added metric aliases, mass fields or selector bindings until the checker could evaluate a requirement. One pass came from switching to an equivalent sandwich representation that cut declared areal density from about 70 to 4.2 kg/m². The reader's inference, which seems right, is that a checker relying on properties the agent declares measures the declaration as much as the design.

## What this means for OpenShape

1. **The intent model is the missing piece, and these benchmarks show its shape.** It needs interfaces as objects, typed requirements with derivations, load cases that refer to interfaces, and a record of how each analysis was run.
2. **Checks must measure the model, not the agent's description of it.** Mass comes from geometry and assigned material. A load region is an interface the design demonstrably provides. Nothing the checker uses should be a free-text or free-number claim.
3. **Removing the meshing step would remove a third of failures.** This is the strongest evidence so far for analysis that works on the kernel's geometry directly.
4. **An integrated platform could report the cause of each failure.** These benchmarks cannot tell a bad design from a tool failure. A platform that owns the geometry, the analysis setup and the solver can.
5. **Adopt, do not duplicate.** Parametric CAD Bench is Apache-2.0 and well specified; Hephaestus is MIT. Running an OpenShape-based agent on them is cheaper and more credible than inventing equivalents. What neither covers, and OpenShape should add, is manufacturability, assembly checks, and requirements tied to interfaces.

## Cautions about the papers

The reader found internal inconsistencies, listed so the figures above are used with care.

- **CADEngBench:** one count appears as 143 in one place and 142 in another; the text and an algorithm disagree on whether every state or every comparable state must pass; one example's stated load in the brief differs from the load actually applied, because analysis loads are assigned by the benchmark and not taken from the brief. No licence or repository is given.
- **Hephaestus-CCX:** a table said to list six requirements lists four; one baseline figure does not reconcile with its component rows; contact checks are claimed in the abstract and absent from the list of analyses run. It reports no repeated runs or confidence intervals.
- **Parametric CAD Bench v3:** none found. Its authors state that its rewards are "heuristic proxies" and that a correct model with a different face decomposition can score below full marks.
