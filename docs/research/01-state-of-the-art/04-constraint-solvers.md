# Constraint solvers

Evidence marks are defined in the [phase README](README.md). This is a first pass: the product picture comes from vendor pages, the theory from one survey read in part.

## Summary

- One vendor, Siemens with D-Cubed, supplies the solver inside most commercial CAD, including the reference product. Its internals are not published.
- The published theory is mature for well-constrained 2D problems that decompose into triangles. It is weaker in 3D and for under-constrained problems, and those are the cases interactive CAD spends most of its time in.
- What separates a production solver from a textbook one is mostly behaviour, not solving: which of many valid solutions it picks, how geometry moves when dragged, and what it tells the user about a broken sketch. None of this is specified anywhere public.

## The market

| Solver | Owner | Used in | Mark |
|---|---|---|---|
| D-Cubed 2D DCM and 3D DCM | Siemens | Licensees named by Siemens include Autodesk, Onshape, PTC, Shapr3D, IronCAD and ZWCAD | [P, vendor] |
| LGS | Bricsys (developed by LEDAS) | BricsCAD, Cimatron | [S] |
| C3D Solver | C3D Labs | KOMPAS-3D | [S] |
| SolveSpace's solver, GeoSolver | Open source | Their own applications | [S]; assessed in phase 2 |

Sources: [Siemens D-Cubed](https://www.siemens.com/en-gb/products/plm-components/d-cubed/); [Wikipedia, Geometric constraint solving](https://en.wikipedia.org/wiki/Geometric_constraint_solving).

- D-Cubed was founded in 1989 and released 2D DCM in 1990. [P, vendor] ([Siemens interview](https://www.engineering.com/parasolid-d-cubed-and-siemens-the-heart-of-your-cad-software-belongs-to-another/))
- Asked for its advantages, Siemens cites being first to market "by a long time" and "the total investment over time", with a "dominant market share" for 2D DCM. [P, vendor] (same)
- Siemens claims the D-Cubed components reach "more than 4 million end users". [P, vendor]

The advantage Siemens itself names is accumulated investment, not a technique. That is the same shape of moat as the kernel.

## What D-Cubed does

### 2D DCM: sketches

From [Siemens' product page](https://www.siemens.com/en-gb/products/plm-components/d-cubed/2d-dcm/): [P, vendor]

| Capability | Detail |
|---|---|
| Geometry | Points, lines, circles, ellipses, conics, splines and parametric curves |
| Constraints | Distance, angle, radius, parallel, perpendicular, tangent, concentric, symmetric, normal, equal distance and equal radius |
| Equations | "Variable dimensions can be linked by equations that are solved simultaneously" |
| Splines | Constraints on length, tangent direction and length, second derivative, equal curvature |
| Inference | Can infer dimensions and constraints from unconstrained geometry, either from legacy drawings or as the user sketches |
| Solving preference | "Specify preferred solving outcomes, such as minimal movement of geometry" |
| Diagnostics | "Feedback is always provided about the status of the sketch, including under-constrained or over-constrained geometry" |

### 3D DCM: assemblies and more

From [Siemens' product page](https://www.siemens.com/en-gb/products/plm-components/d-cubed/3d-dcm/): [P, vendor]

- Four stated uses: positioning parts in assemblies, kinematic simulation of mechanisms, direct editing of part shape without history, and 3D sketches for routing.
- Geometry includes points, lines, planes, circles, ellipses, cylinders, tori and parametric curves and surfaces.
- Dimensions can be given a range instead of a value, which is how joint limits are expressed.
- Equations can link dimensions, "for example, linking the rotation or translation of one component with another to enable kinematic simulation".
- Solving modes include "moving the minimum number of geometries, or moving geometries the minimum amount relative to each other".
- It reports "what is well-defined, under-defined and over-defined".

### The rest of the suite

D-Cubed is six components, not two: 2D DCM, 3D DCM, AEM (motion simulation), PGM (offset profiles), CDM (collision detection and clearance) and HLM (hidden-line views for drawings). [P, vendor]

This is a useful map of what sits beside a kernel in a real CAD system. Collision and clearance, and hidden-line generation, are separate products that OpenShape's scope implies we need: the first for testing assembly, the second for drawings.

## What the theory says

From Fudos, Hoffmann and Joan-Arinyo, "Tree-decomposable and underconstrained geometric constraint problems" (2017), read in part. [P for the points below] ([arXiv 1608.05205](https://arxiv.org/pdf/1608.05205))

- **The standard approach is decompose, then solve.** Solvers "took a quantum leap in the 1990s" with methods that perform "an initial, graph-based structural analysis that extracts generic subproblems and determines how they would combine", then hand the subproblems to an algebraic solver. The survey credits this to Owen (1991). John Owen was a founder of D-Cubed, so this is very likely the origin of DCM, though no source confirms what DCM does today. [U for the link to current DCM]
- **A well-constrained problem has many solutions.** The number "can grow exponentially with the number of constraints". Picking the one the designer meant is called the root identification problem, and natural formulations of it are NP-complete.
- **Solvers may fail to find a solution that exists.** The survey accepts false negatives and rules out false positives, and calls the ability to find solutions the solver's "competence".
- **Dragging is treated as repeated static solving** along the path of the moved element, if the static solver is fast enough.

From the Wikipedia overview: equation systems are "mostly solved by iterative methods", with Newton-Raphson the most common, and a long list of decomposition techniques exists to shrink the systems first. [S]

## What this means for OpenShape

1. **The hard requirements are behavioural.** Choosing the intended solution, moving geometry predictably under drag, staying on the same solution branch as dimensions change, and explaining over- and under-constraint are what users experience as solver quality. Siemens lists all of these as features. A solver that only finds some valid solution will feel broken.
2. **Under-constrained is the normal case.** A sketch is under-constrained for most of its life, while it is being drawn. The theory is weakest exactly there.
3. **Diagnostics matter more for agents than for humans.** A human sees a sketch turn red. An agent needs to be told which constraints conflict and which degrees of freedom remain. This is one of the working positions in [decision 0005](../../decisions/0005-single-operation-layer.md), and Siemens' feature list shows the incumbent already computes this information.
4. **One solver core may serve several features.** D-Cubed uses the 3D solver for assemblies, kinematics, direct editing and 3D sketching. Whether OpenShape should design one solver for all of these or separate ones is a phase 3 or phase 5 question.
5. **Determinism needs care.** Iterative numerical solving from a starting guess makes the result depend on the previous state of the sketch. For a model that must rebuild identically on any machine from a text definition, what the solver's starting state is, and whether it is stored, has to be decided explicitly.

## Gaps to close before this topic is complete

- Read Owen (1991) and the Hoffmann, Lomonosov and Sitharam decomposition papers.
- Finish the survey above, particularly its treatment of under-constrained problems.
- 3D constraint solving theory, which the survey largely sets aside.
- LGS and C3D Solver: any published technical description.
- How Onshape, SOLIDWORKS and others behave in practice on hard sketches: no test or comparison found.
- Published benchmark problem sets for constraint solvers: not searched for yet.
- Performance: how large a sketch or assembly the incumbents solve interactively.
