---
description: "Use when editing USERJOURNEY docs, onboarding plans, consent behavior, activation rules, route/state design, implementation slices, or delivery sequencing."
name: "USERJOURNEY Workflow"
applyTo: "USERJOURNEY/**/*.md"
---
# USERJOURNEY Workflow

- Read `USERJOURNEY/README.md`, `USERJOURNEY/PRODUCT_SPEC.md`, and `USERJOURNEY/DELIVERY_GAMEPLAN.md` before changing onboarding planning behavior.
- Treat the source-of-truth chain in `USERJOURNEY/DELIVERY_GAMEPLAN.md` as binding when documents disagree.
- Update authority docs before dependent docs when changing route/state rules, legal behavior, UX surfaces, or implementation sequence.
- Do not treat signup as activation.
- Do not treat skip-guided-onboarding as activation.
- Do not treat AI or data notice copy as decorative if the docs define it as a gate.
- Treat `first_value_achieved` as the canonical activation event unless the authority docs explicitly change.
- Prefer `scripts/programstart_status.py --system userjourney`, `scripts/programstart_validate.py --check required-files`, and `scripts/programstart_drift_check.py` when checking readiness or drift.
