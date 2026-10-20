# Research Delta - LLM, retrieval, and agent tooling

Review date: 2026-10-19
Owner: ai-platform
Outcome: recommendation changed
Confidence: high

## Source changes

- Reviewed the official OpenAI API changelog: <https://developers.openai.com/api/docs/changelog>.
- Current provider guidance continues moving tool-capable applications toward the Responses API; recent changes add stronger workload identity and broader file-input support, while model-specific reasoning and sampling constraints remain material.

## Decision

Keep provider adapters capability-driven rather than model-name-driven. Prefer Responses for new OpenAI tool-calling integrations, feature-detect reasoning/sampling controls, and preserve explicit identity and file-ingestion limits. This sharpens existing guidance but does not justify a new framework default.

## Follow-up

- Audit provider profiles when a project actually adopts X.509 workload identity or expanded document inputs.
