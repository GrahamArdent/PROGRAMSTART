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

Use `programstart research --status` before each weekly pass. That status report is the fast health check for the KB itself: which research tracks are due, which ones are fresh, and which broad coverage domains are still marked `partial` or `seed`.

Use `programstart research --status --fail-on-due` in automation when you want the command to return a non-zero exit code for overdue or unreviewed tracks.

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
- Mobile and cross-platform delivery: Expo/React Native/Flutter releases, build/signing flow changes, analytics/push/crash tooling changes
- Data platform and analytics tooling: warehouse and OLAP engines, orchestration frameworks, DataFrame/query-engine releases
- Integrations and product infrastructure: payments, subscriptions, messaging, CRM, analytics, and support-platform API changes
- Desktop and local-first delivery: Tauri/Electron releases, packaging and updater changes, local database and sync-engine guidance, offline-first patterns
- Developer tooling and monorepo delivery: pnpm/npm changes, Turborepo/Nx behavior, cargo and dotnet workflow updates, CI and supply-chain tooling shifts
- Realtime and event-driven systems: broker releases, managed pubsub changes, collaborative-state tooling, schema and transport guidance
- Commerce and customer platforms: CRM/support platform changes, CDP shifts, shipping and tax provider updates, subscription-platform guidance

## Coverage Discipline

- Treat `coverage_domains` in the KB as the system's scope map, not marketing copy.
- `strong` means the KB has actionable stack guidance and update coverage for that domain.
- `partial` means the KB can guide some common builds in that domain, but important categories or providers are still missing.
- `seed` means the domain is recognized as important, but the KB should not pretend to offer comprehensive guidance there yet.
- Move a domain upward only when representative tools, rules, and recurring research coverage actually exist.

## Update Rules

- Add version deltas as structured comparisons before editing broad stack summaries.
- Keep speculative or experimental findings clearly marked with lower confidence.
- Prefer official release notes, migration guides, and maintained vendor documentation.
- Only update canonical stack guidance when the recommendation or operational baseline actually changes.

## Why This Matters

The KB is only useful if it keeps producing current decisions. Weekly research is justified because the AI, retrieval, and Python runtime landscape moves quickly, but only if the process stays bounded, reviewable, and tied to recommendations.
