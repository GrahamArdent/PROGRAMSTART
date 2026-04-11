---
status: accepted
date: 2026-03-31
deciders: [project owner]
consulted: []
informed: []
---

# 0002. Adopt Conventional Commits for All Commit Messages

## Context and Problem Statement

Commit history in this repository was freeform, making it difficult to automate changelog generation, reason about the impact of changes, or enforce a baseline standard for contributors. Pre-commit hooks already enforce code quality; commit message quality was not enforced.

## Decision Drivers

- Automate changelog and release-note generation from commit history.
- Make breaking changes explicit and searchable in git log.
- Enable consistent, readable history for any future contributors or maintainers.

## Considered Options

- Option A — Conventional Commits + `gitlint` pre-commit hook (Python-native)
- Option B — Conventional Commits + `commitlint` Node.js hook
- Option C — Custom regex check via a local pre-commit hook script
- Option D — No enforcement; rely on contributor discipline

## Decision Outcome

Chosen option: **Option A (local Python script)**, because:
- Python-native and cross-platform — no Node.js or Unix-only runtime required.
- `scripts/check_commit_msg.py` integrates with the existing `pre-commit` pipeline as a `commit-msg` stage hook.
- Zero external runtime dependency — runs via `uv run python scripts/check_commit_msg.py`.
- `.gitlint` config file documents the rule specification in a standard format.

### Consequences

- Good: Breaking changes are always explicitly flagged with `BREAKING CHANGE:` footer.
- Good: `feat`, `fix`, `docs`, `chore`, `ci`, `refactor`, `test` types provide machine-readable semantic intent.
- Bad: Minor learning curve for contributors unfamiliar with Conventional Commits.
- Neutral: `BREAKING CHANGE:` footer is recommended for schema changes, stage renames, and required-file renames per `copilot-instructions.md`.

## Confirmation

`gitlint` runs as a `commit-msg` stage pre-commit hook. Any commit with a non-conforming message is rejected before it is recorded.
Verify with: `echo "bad message" | gitlint`

## Links

- [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/)
- [gitlint documentation](https://jorisroovers.com/gitlint/)
- [.gitlint config](../../.gitlint)
- [ADR-0001](0001-use-programbuild-workflow-system.md)
