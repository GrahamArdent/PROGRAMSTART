---
status: accepted
date: 2026-10-05
deciders: [solo operator]
consulted: []
informed: []
---

# 0026. Use Owner-Routed Convergence Packets for Material Challenge Results

## Context and Problem Statement

Repeated PROGRAMSTART design, planning, and handoff work increasingly uses iterative Challenge/re-Challenge cycles to refine a candidate until no new material corrective delta survives. The resulting reasoning is valuable beyond the chat/session where it was produced, but keeping all detail in chat makes resumption fragile, while storing every result in one central PROGRAMSTART or portfolio location would create a shadow decision system.

The operator also wants the conversational surface to stay concise when a complete durable artifact exists.

## Decision Drivers

- Preserve reconstructable reasoning without depending on chat history.
- Keep the operator-facing response concise.
- Preserve one owner-native authority per real concern/project.
- Reuse the existing Challenge Gate instead of creating a second review protocol.
- Avoid a central packet queue, backlog, decision database, or new repository.
- Keep the method usable across hosts that differ in attachment/download capabilities.
- Let project-specific, PROGRAMSTART-methodology, cross-project, and owner-unclear results route differently without losing the common output contract.

## Considered Options

1. **Chat-only output.** Keep detailed Challenge reasoning and final recommendations in the conversation.
2. **One central PROGRAMSTART archive.** Store every final packet in the methodology repository.
3. **New global convergence repository/database.** Create a dedicated durable packet system.
4. **Owner-routed Convergence Packets.** Standardize the derived Markdown result while routing durability according to semantic ownership and retaining current owner authority.

## Decision Outcome

Chosen option: **4 — Owner-routed Convergence Packets.**

For material design, plan, recommendation, handoff, or similar convergence work that warrants durable reconstruction:

- produce a concise operator-facing result plus one complete Markdown Convergence Packet;
- preserve only material Challenge findings that changed the candidate/boundary rather than every intermediate draft;
- treat the packet as derived/non-authoritative unless it is genuinely the recognized owner artifact;
- when a Challenge materially changes the candidate, re-Challenge the revised exact candidate before reporting the boundary clear;
- stop at the first fresh clear current candidate rather than accumulating identical passes;
- route durable project-specific packets to the owning project;
- route PROGRAMSTART-methodology packets to appropriate non-authoritative PROGRAMSTART evidence/design surfaces;
- route genuine cross-project/operator-reference packets to an existing external non-authoritative workspace when such storage is actually warranted;
- keep owner-unclear outcomes on existing owner-search/capture/Authority-Gap paths rather than using a packet archive as a catch-all inbox.

The methodology remains host-neutral. A host may provide a downloadable file, repository path, inline artifact, or another supported delivery surface. The file-delivery mechanism is presentation, not authority.

### Consequences

- Good: a future chat/agent/person can reconstruct the material result without replaying the original conversation.
- Good: short operator responses no longer require sacrificing detailed durable reasoning.
- Good: storage convenience cannot silently replace owner-native decision authority.
- Good: the existing Challenge Gate remains the single adversarial review owner.
- Good: no new repository, queue, lifecycle, Work Packet type, Matrix projection, or runtime service is required.
- Bad: consumers must still resolve the correct durable owner; there is intentionally no universal packet folder.
- Bad: a downloadable delivery copy and a repository reference copy require discipline not to diverge into separately maintained truths.
- Neutral: genuine cross-project archive instantiation remains a downstream external-workspace concern and is not created by this decision.

## Pros and Cons of the Options

### Option 1 — Chat-only output

- Good, because it adds no repository ceremony.
- Bad, because detailed decisions and Challenge rationale are difficult to recover reliably across sessions/handoffs.

### Option 2 — One central PROGRAMSTART archive

- Good, because all packets are easy to find in one place.
- Bad, because PROGRAMSTART would accumulate filled project-specific state and become a shadow cross-project authority.

### Option 3 — New global convergence repository/database

- Good, because packet storage could be standardized independently.
- Bad, because it adds another component, ownership model, retrieval surface, and likely decision/currentness confusion without evidence that such infrastructure is needed.

### Option 4 — Owner-routed Convergence Packets

- Good, because output format is consistent while authority remains federated.
- Good, because the same pattern works for project, methodology, and cross-project reference work.
- Bad, because routing is contextual and cannot be reduced to one universal filesystem path.

## Confirmation

This decision is implemented when:

- the Planning Operating Model owns Convergence Packet activation/output/authority/routing semantics;
- the existing Challenge Gate requires a fresh Challenge after a material candidate correction;
- one workflow guidance/task prompt renders the packet without copying a competing Challenge checklist;
- the prompt is registered and distributed to generated repositories;
- a focused contract test proves registration, bootstrap distribution, owner binding, derived authority, and anti-ceremony invariants;
- DEC-023 and this ADR are linked;
- repository validation/drift and exact-head PR gates pass.

## Links

- <!-- DEC-023 -->
- [Planning Operating Model](../../PROGRAMBUILD/PROGRAMBUILD_PLANNING_OPERATING_MODEL.md)
- [Challenge Gate](../../PROGRAMBUILD/PROGRAMBUILD_CHALLENGE_GATE.md)
- [Decision log](../../PROGRAMBUILD/DECISION_LOG.md)
