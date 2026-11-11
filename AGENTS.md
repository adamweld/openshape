# Rules for AI agents

Read [docs/PRINCIPLES.md](docs/PRINCIPLES.md) before doing anything. It is the authority; this file is the short form.

1. **This is not a proof of concept.** Do not take the shortest path to something that mostly works. Every component is either the best known design, with evidence, or explicitly marked as not yet that.
2. **Research and design come before code.** Do not write implementation code for a component until its research phase in [docs/ROADMAP.md](docs/ROADMAP.md) is complete and a design in `docs/design/` covers it.
3. **Every decision gets a record** in `docs/decisions/`, using the template in [docs/decisions/README.md](docs/decisions/README.md), with a status of Settled, Provisional, Temporary or Open.
4. **Anything not Settled goes in [docs/REGISTER.md](docs/REGISTER.md)** with the trigger or requirement that would close it. Add the entry in the same commit as the decision or shortcut.
5. **Do not settle the project owner's decisions for them.** Record your recommendation, mark the item Open and ask.
6. **Claims need sources.** Research documents cite where each claim comes from and say plainly when something is inference or unverified. Much of the state of the art is closed-source; do not present guesses about it as fact.
7. **Work one phase at a time**, in roadmap order, unless the owner says otherwise.
8. **Check [docs/COMPARABLE-PROJECTS.md](docs/COMPARABLE-PROJECTS.md) before building a component**, and add any overlapping project you find to it.
9. **Do not run, script or automate any commercial CAD product for comparison** until the owner has settled the terms-of-use question in [docs/REGISTER.md](docs/REGISTER.md). Reading public documentation is as far as it goes.
10. **New source files carry the MPL-2.0 header notice** (Exhibit A of [LICENSE](LICENSE)).
