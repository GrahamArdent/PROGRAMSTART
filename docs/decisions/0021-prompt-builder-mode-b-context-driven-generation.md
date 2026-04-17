---
status: accepted
date: 2026-04-19
deciders: [solo operator]
consulted: []
informed: []
---

# 0021. Prompt Builder Mode B — Context-Driven Generation

## Context and Problem Statement

`programstart prompt-build` (Mode A) generates stage-specific `.prompt.md` files
from the process registry. It requires a bootstrapped PROGRAMBUILD project and
registry data to function. Users who want to use PROGRAMSTART's structured prompt
generation on arbitrary repos — without bootstrapping — have no way to do so.

## Decision Drivers

- Enable prompt generation for any project, not just PROGRAMSTART-bootstrapped ones.
- Preserve Mode A (registry) as the default, unchanged.
- Keep the implementation minimal — reuse existing helpers and patterns.

## Considered Options

1. **CLI `--mode context` with `--context key=value` pairs** — arbitrary
   key-value context fields; no registry dependency.
2. **`--repo <path>` auto-discovery** — scan a repo directory for README,
   pyproject.toml, etc. and infer context automatically.
3. **Template file input** — accept a YAML/JSON context file instead of CLI flags.

## Decision Outcome

Chosen option: **1 — CLI `--mode context` with `--context key=value` pairs**.

Rationale: Key-value pairs are the simplest interface, require no file system
access, and compose well with shell scripts. Auto-discovery (option 2) can be
layered on later if demand arises. Template files (option 3) add complexity
without clear benefit for the initial feature.

### Implementation

- `build_context_prompt(context: dict[str, str]) -> str` generates a
  `.prompt.md` from arbitrary context. Required key: `goal`.
- `_render_context_frontmatter()` and `_render_context_body()` produce the
  prompt structure (Data Grounding Rule, Context, Protocol, Verification).
- CLI: `--mode registry` (default) | `--mode context`; `--context key=value`
  (repeatable).
- Well-known keys: `project`, `goal`, `stage`, `stack`, `shape`. Any other
  keys are rendered as custom context fields.

### Consequences

- Good: Any repo can now use PROGRAMSTART prompt generation without bootstrapping.
- Good: Mode A is completely unchanged.
- Neutral: Mode B prompts are simpler than Mode A (no sync rules, kill criteria,
  or stage gating) — this is intentional for non-PROGRAMSTART projects.

## Related

- <!-- DEC-018 -->
- DEC-018 in `PROGRAMBUILD/DECISION_LOG.md`
- Hardening gameplan J-5 (STR-02 / S-5)
- Upgrade gameplan Phase J, J-1
