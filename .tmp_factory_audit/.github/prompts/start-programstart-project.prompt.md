---
description: "Start a new planning package using PROGRAMBUILD and an optional USERJOURNEY attachment decision. Use when kicking off a new product or reusable project starter."
name: "Start PROGRAMSTART Project"
argument-hint: "Destination folder, project name, variant, product shape, and whether onboarding planning is needed"
agent: "agent"
---
Create a new planning package using this repository's workflow assets.

Tasks:

1. Run `scripts/programstart_step_guide.py --kickoff` first and follow the referenced files, scripts, and prompts.
2. Choose the dominant `PRODUCT_SHAPE` first.
3. Confirm whether the new project needs only PROGRAMBUILD or an additional USERJOURNEY attachment.
4. Choose the correct PROGRAMBUILD variant: lite, product, or enterprise.
5. Run `scripts/programstart_bootstrap.py` with the destination, project name, and selected variant.
6. If USERJOURNEY is needed, note that it must be attached separately from a project-specific source instead of being scaffolded from this template repo.
7. Summarize what was created.
8. Recommend the first documents to open next.

Use `config/process-registry.json` and the authority docs instead of inventing file lists.
