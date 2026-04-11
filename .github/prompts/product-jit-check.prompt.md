---
description: "Pre-coding alignment check against product authority docs. Use before implementing any feature, endpoint, or auth change."
name: "Product JIT Check"
---

# Product-JIT Alignment Check

Before writing or modifying feature code, complete this checklist.

## 1. Re-read ARCHITECTURE.md contracts

Open `PROGRAMBUILD/ARCHITECTURE.md` and locate every contract, endpoint definition, or trust boundary relevant to the current task. Confirm that:

- The contract you are about to implement (or change) is documented.
- The auth model in the code matches the auth model in the doc.
- No new endpoint or route is being added without a corresponding entry.

If a contract is missing or contradicted: **update ARCHITECTURE.md first**, record the change in `DECISION_LOG.md`, then proceed with implementation.

## 2. Re-read REQUIREMENTS.md for the current feature

Open `PROGRAMBUILD/REQUIREMENTS.md` and find the requirement(s) tied to this task. Confirm that:

- The requirement is still marked as in-scope and achievable.
- No P0 requirement is made impossible by the planned change.
- The acceptance criteria are still aligned with current design.

If a requirement needs updating: **update REQUIREMENTS.md first**, then implement.

## 3. Check DECISION_LOG.md

Open `PROGRAMBUILD/DECISION_LOG.md` and scan for decisions affecting this area. Confirm that:

- No prior decision contradicts what you are about to build.
- Any new architecture-level decision made during this task is recorded.

## 4. Confirm alignment

Before proceeding with code changes, state:

- [ ] ARCHITECTURE.md contracts are current for this task.
- [ ] REQUIREMENTS.md entries are achievable and in-scope.
- [ ] DECISION_LOG.md has no contradicting decisions.
- [ ] No authority doc needs updating before I write code.

If any box cannot be checked, resolve the authority doc issue first.
