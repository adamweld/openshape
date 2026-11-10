# 0001: License is MPL-2.0

- **Status:** Provisional
- **Date:** 2026-11-10
- **Decided by:** Project owner ("MPL for now")

## Context

The repository was created under GPL-3.0. The project aims to be extensible and to have its kernel adopted widely, and a CAD kernel is the kind of component other software embeds.

## Decision

The whole project is licensed under the Mozilla Public License 2.0, without the "Incompatible With Secondary Licenses" notice, so it stays compatible with the GPL family.

MPL-2.0 is file-level copyleft: changes to our files must be published, but proprietary software may link to and embed the code.

## Alternatives considered

- **GPL-3.0 (the starting point).** Blocks proprietary embedding and makes plugin licensing ambiguous, yet does not cover hosted services. It carries the adoption cost of copyleft without the hosting protection.
- **AGPL-3.0.** Protects against closed hosted forks, but blocks embedding even more firmly. Less relevant for a local-first product.
- **Apache-2.0 or MIT/Apache dual.** Maximum adoption and an explicit patent grant, but improvements need not be shared.
- **Split licensing by layer** (permissive or MPL kernel, AGPL application). Not chosen for now; a single license is simpler at this stage.

## Evidence

Owner's choice after discussion. Comparable projects: OCCT and FreeCAD use LGPL, Manifold and truck use Apache-2.0.

Unverified and worth legal advice before the license becomes commercially important: copyright in largely AI-written code is unsettled, and copyleft depends on enforceable copyright.

## Consequences

- New source files carry the MPL-2.0 header notice (Exhibit A of the license).
- GPL-licensed dependencies (for example CGAL's GPL packages or SolveSpace's solver) cannot be linked into MPL-licensed distributions without the combined work falling under the GPL. Phase 2 checks license compatibility for every reuse candidate.

## Revisit trigger

Before the first outside contribution is accepted, or before the first public release, whichever comes first. Changing license after outside contributors hold copyright requires their consent.
