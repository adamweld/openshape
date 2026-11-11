# Other CAD systems

Evidence marks are defined in the [phase README](README.md). This is the thinnest topic in the phase. Almost everything here is from reviews, forums or vendor material, and it should be read as a list of leads, not findings.

The question for this topic is narrow: where does another system do something better than Onshape, or show a weakness that all of them share?

## Summary

- The clearest shared weakness is rebuild performance. Feature regeneration in mainstream CAD is reported to be largely single-threaded, because each feature depends on the one before it. This is the most promising place to look for the performance advantage the project wants.
- Two newer Parasolid-based products, Plasticity and Shapr3D, compete on interaction design alone, using the same kernel as their larger rivals. Interface quality is a differentiator independent of the kernel.
- Implicit modelling, as in nTop, is a different representation with real strengths where B-reps are weakest, and a known weakness in getting back to B-rep.

## Rebuild performance

- Users and reviewers report that feature-tree regeneration is largely single-threaded, since "each feature typically depends on the geometry produced by the features before it". [S, forum] ([discussion](https://engineersuniverse.com/studios/engineering-software/why-cad-prioritizes-clock-speed-over-cores))
- A Creo user reports about 6% CPU use on a 16-core machine during regeneration, in a thread requesting multithreading. [S, forum] ([PTC community](https://community.ptc.com/t5/3D-Part-Assembly-Design/Creo-Feature-Request-Multithreading/td-p/806764))
- SOLIDWORKS documents multicore use for regenerating assembly graphics and for assembly features affecting several components. [S] ([SOLIDWORKS help](https://help.solidworks.com/2016/English/WhatsNew/c_parallel_tessellation_when_rendering_Assembly_graphics.htm))
- A forum post states that Parasolid is multithreaded internally but that parent-child dependencies between features limit the benefit. [S, forum] Parasolid's thread safety is separately recorded in [02-kernels.md](02-kernels.md).
- Standard advice for speed is to buy clock speed over core count, group parts into subassemblies, and freeze the upper part of the tree. [S]

Reading, as hypothesis: a feature list is presented as a sequence, but the true dependencies form a graph. Two features that touch different bodies, or different regions of one body, do not depend on each other. A system that tracks dependencies precisely could rebuild independent features in parallel and skip those unaffected by an edit. Zoo lists "eliminate full-world rebuilds" as roadmap work (see [03-ai-and-new-entrants.md](03-ai-and-new-entrants.md)), which suggests that it is not trivial and not yet common.

No measurement of rebuild behaviour in any system was found. This needs real data before it supports a design decision. It also connects to [decision 0006](../../decisions/0006-geometry-references.md): precise dependency tracking and durable geometry references are close to the same mechanism.

## Interaction design

- **Plasticity** is a direct modeller aimed at artists and product designers, built on Parasolid. Reviewers describe edits that are "laborious and unpredictable" elsewhere as straightforward. [S] ([Creative Bloq](https://www.creativebloq.com/3d/3d-software/forget-what-you-know-about-cad-plasticity-has-made-3d-modelling-fun-again))
- **Shapr3D** also runs on Parasolid and markets adaptive parametric modelling. [S, vendor] Nothing technical was found.

Reading: both show that a product can win users on the same kernel as its competitors through interaction alone. The lesson for OpenShape is that kernel quality is necessary and not sufficient. The human interface is a phase 5 subject and has had no research yet.

## Implicit modelling

All points are nTop's own statements. [S, vendor] ([nTop](https://www.ntop.com/resources/blog/understanding-the-basics-of-b-reps-and-implicits/))

- A solid is represented by a function whose sign says inside or outside, not by faces joined together.
- nTop's case against B-reps: "common modeling operations such as rounds, offsets, and even booleans often fail", and containment requires checking against the model's topology, where for an implicit it is a single evaluation.
- Strengths claimed: lattices and other geometry with very large numbers of small features, and driving geometry from fields such as simulation results.
- Getting back to B-rep goes through a mesh and is lossy; nTop describes outputting simplified B-reps for documentation.

Reading: implicits make booleans, offsets and containment trivially robust, which are exactly the operations where B-rep kernels struggle, and they pay for it in precision of sharp features, interoperability and drawings. Two things follow for phase 3. First, a kernel that can answer fast inside-or-outside queries gets some of the benefit without changing representation, and that same query is what meshless simulation needs (see [06-simulation-dfm.md](06-simulation-dfm.md)). Second, generative and optimisation tools tend to produce implicit or mesh output, so the closed loop will meet this representation whether or not OpenShape models in it.

## Notes on the large incumbents

- **CATIA** is regarded as strongest for high-quality freeform surfacing, used for automotive exteriors and aircraft skins. [S] ([comparison](https://www.advancedengineeringuk.com/en/news/comparison-of-two-different-approaches-of-class-a-surface-creation-and-quality-verification-icem-surf-vs-catia-63740))
- **NX** is described in a 2026 guide as excellent for large assemblies. [S]
- **Onshape** user reviews mention slow large assemblies, some imported STEP solids arriving as surfaces, and weaker complex surfacing. [S, anecdotal] ([Capterra](https://www.capterra.com/p/164681/Onshape/reviews/))
- **Fusion** integrates CAD, CAM, simulation and generative design in one product. Nothing substantive was found in this pass.

None of this is strong enough to act on.

## Gaps to close before this topic is complete

- Measured rebuild and large-assembly performance in any system.
- How each system's feature model differs: Fusion's timeline, Creo's and NX's history trees, CATIA's specification tree, and SOLIDWORKS' configurations.
- Drawings: what a production-quality drawing environment requires. Not researched at all, and it is in scope.
- Surfacing: what high-quality surfacing demands of a kernel.
- Sheet metal, in scope at low priority. Not researched.
- Interaction design of Plasticity and Shapr3D in detail.
- Fusion in any depth.
