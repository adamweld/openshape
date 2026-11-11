# Principles

## The standard

We are not building a quick proof of concept and we are not following the shortest path to a mostly working solution. We work slowly, diligently and relentlessly towards state-of-the-art software.

Every piece of the system must be one of two things:

- the best known design, supported by evidence, or
- explicitly marked as not yet that, with a written requirement to come back and improve it.

Nothing is allowed to be an unexamined shortcut.

## Decision statuses

"Provably optimal" is the aim, but much of CAD design cannot be proved: some trade-offs are unsettled even in the research literature. So every decision carries a status that says honestly how well supported it is.

| Status | Meaning | Required content |
|---|---|---|
| **Settled** | The best known option. Supported by proof, benchmark or citation, or it is a product choice made by the project owner. | Alternatives considered and the evidence |
| **Provisional** | Best current judgment, not yet backed by enough evidence. | A revisit trigger: the event or evidence that forces a re-examination |
| **Temporary** | A known shortcut, taken deliberately. | The requirement that replaces it |
| **Open** | Not decided. | The competing positions and what is needed to decide |

A decision may also be **Superseded**, with a link to the record that replaced it. Records are never deleted.

Every item that is not Settled is listed in [REGISTER.md](REGISTER.md).

## Working rules

1. **Research before design, design before code.** No implementation of a component begins until its research phase is complete and a design document covers it.
2. **One record per decision**, in [decisions/](decisions/README.md).
3. **Evidence over assertion.** Research cites its sources. Inference and unverified claims are labelled as such. This matters most for closed-source systems, where public information is thin.
4. **Performance claims are measured.** A design chosen for performance names the benchmark that will confirm it.
5. **Single-threaded phases.** Phases run one at a time in roadmap order, so each builds on the finished output of the last.
6. **The owner decides product questions.** Agents and contributors recommend; they do not settle matters of scope, licensing or direction on their own.
