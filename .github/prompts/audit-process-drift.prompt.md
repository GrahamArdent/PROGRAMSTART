---
description: "Audit planning-document drift. Use when checking whether canonical files and dependent files stayed synchronized after changes."
name: "Audit Process Drift"
argument-hint: "Optional changed files or area to audit"
agent: "agent"
---
Audit process drift using the repository workflow rules.

Tasks:

1. Use `config/process-registry.json` as the machine-readable rule set.
2. Run `scripts/programstart_drift_check.py` with the provided changed files if available.
3. Summarize any authority violations, missing synchronized updates, or residual risks.
4. Recommend the minimal set of files that must be updated to restore consistency.
