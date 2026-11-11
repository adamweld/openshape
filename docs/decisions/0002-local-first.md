# 0002: Deployment is local-first

- **Status:** Settled
- **Date:** 2026-11-10
- **Decided by:** Project owner

## Context

Onshape, the functional reference for this project, is cloud-native: the kernel runs on servers and the browser is a thin client. The deployment model drives the choice of language, document model, rendering stack and version control approach.

## Decision

OpenShape is local-first. The software and the user's data run and live on the user's own machine.

## Alternatives considered

- **Cloud-native, like Onshape.** Gives real-time collaboration and zero install, but requires running a service, puts latency between the user and the kernel, and makes headless agent use depend on a server.
- **One core for both** (native plus a browser build). Not ruled out as a later addition; the decision here is which one the design optimises for.

## Evidence

Owner's product choice.

## Consequences

- Collaboration and versioning are built on files and version control, not a central database. The mechanism is an open item for phase 5.
- Agents can run the software headless and locally, with no network dependency.
- Whether a browser build is also wanted later is a phase 5 question; nothing here forbids it.
