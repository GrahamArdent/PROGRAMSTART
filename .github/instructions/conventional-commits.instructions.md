---
description: "Commit message format rules for PROGRAMSTART. Use when writing, reviewing, or generating any git commit message."
name: "Conventional Commits"
applyTo: "**"
---
# Conventional Commits

The key words MUST, MUST NOT, SHOULD, SHOULD NOT, and MAY in this document are interpreted as described in [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119).

All commit messages in this repository MUST follow the [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/) specification.

## Format

```
<type>[optional scope]: <description>

[optional body]

[optional footers]
```

## Valid types

| Type | When to use |
|---|---|
| `feat` | New stage, phase, script capability, or workflow feature |
| `fix` | Bug fix in a script, broken validation, or incorrect state behavior |
| `docs` | Planning document updates, ADR creation, README edits |
| `chore` | Registry/config maintenance, dependency updates, housekeeping |
| `ci` | CI workflow changes (`.github/workflows/`) |
| `refactor` | Script refactor with no behavior change |
| `test` | New or changed tests only |

## Breaking changes

When a commit introduces a breaking change (schema change, stage rename, required-file rename), you MUST include a `BREAKING CHANGE:` footer:

```
feat(schema): add commit_hash to signoff

BREAKING CHANGE: programbuild-state.schema.json now includes commit_hash field.
Existing state files without it remain valid (field is optional).
```

## Scope (optional)

Scope MAY be used to identify the subsystem affected:

- `(programbuild)` — PROGRAMBUILD workflow files or scripts
- `(userjourney)` — USERJOURNEY workflow files or scripts
- `(schema)` — JSON schema changes
- `(ci)` — CI/CD pipeline changes
- `(config)` — process-registry or config changes

## Rules enforced by gitlint

- Subject line MUST NOT exceed 100 characters.
- Body lines MUST NOT exceed 120 characters.
- Merge commits are exempt from type enforcement.
- WIP commits are exempt from type enforcement.

## Examples

```
docs(programbuild): add RFC 2119 preamble to instruction files

feat(schema): add commit_hash to signoff for staleness detection

fix(validate): correct missing-file check for optional systems

chore: add gitlint to dev dependencies

ci: add commit-msg hook stage to pre-commit config

BREAKING CHANGE: stage rename from 'discovery' to 'scoping' — update STATE.json
```
