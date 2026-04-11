---
description: "Use when editing USERJOURNEY docs, onboarding plans, consent behavior, activation rules, route/state design, implementation slices, or delivery sequencing."
name: "USERJOURNEY Workflow"
applyTo: "USERJOURNEY/**/*.md"
---
# USERJOURNEY Workflow

The key words MUST, MUST NOT, SHOULD, SHOULD NOT, and MAY in this document are interpreted as described in [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119).

- You MUST read `USERJOURNEY/README.md`, `USERJOURNEY/PRODUCT_SPEC.md`, and `USERJOURNEY/DELIVERY_GAMEPLAN.md` before changing onboarding planning behavior.
- You MUST treat the source-of-truth chain in `USERJOURNEY/DELIVERY_GAMEPLAN.md` as binding when documents disagree.
- You MUST update authority docs before dependent docs when changing route/state rules, legal behavior, UX surfaces, or implementation sequence.
- You MUST NOT treat signup as activation.
- You MUST NOT treat skip-guided-onboarding as activation.
- You MUST NOT treat AI or data notice copy as decorative if the docs define it as a gate.
- You MUST treat `first_value_achieved` as the canonical activation event unless the authority docs explicitly change.
- You SHOULD use `scripts/programstart_status.py --system userjourney`, `scripts/programstart_validate.py --check required-files`, and `scripts/programstart_drift_check.py` when checking readiness or drift.
