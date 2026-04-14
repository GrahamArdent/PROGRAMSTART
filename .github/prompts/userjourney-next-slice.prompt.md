---
description: "Summarize the next USERJOURNEY slice to execute. Use when deciding what engineering should do next for onboarding, consent, callback routing, or first-run activation."
name: "USERJOURNEY Next Slice"
argument-hint: "Optional focus area or blocker"
agent: "agent"
version: "1.0"
---
Determine the next USERJOURNEY implementation slice.

Tasks:

1. Read `USERJOURNEY/DELIVERY_GAMEPLAN.md`, `USERJOURNEY/EXECUTION_SLICES.md`, `USERJOURNEY/IMPLEMENTATION_TRACKER.md`, and `USERJOURNEY/OPEN_QUESTIONS.md`.
2. Use `scripts/programstart_status.py --system userjourney` if available.
3. Report the current phase, active blockers, and the next slice that should be executed.
4. List the first source-of-truth docs and repo surfaces that should be reviewed before coding.
5. Call out drift risks if unresolved decisions still block implementation.
