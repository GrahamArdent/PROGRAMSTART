# Knowledge Ops

PROGRAMSTART treats deep research as a recurring maintenance activity, not a one-time document dump.

## Operating Model

Run a weekly KB review on a fixed day and force every review to end with one of three outcomes:

- recommendation changed
- recommendation unchanged
- blocked pending evidence

That constraint keeps research from becoming an ever-growing archive with no decision impact.

## Weekly Review Contract

Use `programstart research --track <name>` to generate a dated delta template in `outputs/research/`. That keeps weekly reviews consistent and forces each pass to produce comparable artifacts.

Each weekly pass should produce four outputs:

1. what changed in the source material
2. whether the recommendation changed
3. what KB sections were updated
4. what still needs follow-up or lower-confidence review

If a review does not change a recommendation, record that explicitly. "No change" is still a useful result because it confirms the current guidance remains valid.

## Recommended Tracks

- Python runtime and packaging: CPython release notes, typing/runtime changes, uv workflow changes, CI/base-image compatibility
- LLM, retrieval, and agent tooling: provider API changes, structured output changes, evaluation patterns, retrieval framework guidance
- Web and platform delivery: framework releases, deployment guidance, observability baseline changes, security advisories

## Update Rules

- Add version deltas as structured comparisons before editing broad stack summaries.
- Keep speculative or experimental findings clearly marked with lower confidence.
- Prefer official release notes, migration guides, and maintained vendor documentation.
- Only update canonical stack guidance when the recommendation or operational baseline actually changes.

## Why This Matters

The KB is only useful if it keeps producing current decisions. Weekly research is justified because the AI, retrieval, and Python runtime landscape moves quickly, but only if the process stays bounded, reviewable, and tied to recommendations.
