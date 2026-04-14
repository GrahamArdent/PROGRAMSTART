---
description: "Start a new planning package using PROGRAMBUILD and an optional USERJOURNEY attachment decision. Use when kicking off a new product or reusable project starter."
name: "Start PROGRAMSTART Project"
argument-hint: "Destination folder, project name, variant, product shape, and whether onboarding planning is needed"
agent: "agent"
version: "1.0"
---
Create a new planning package using this repository's workflow assets.

Tasks:

1. Run `scripts/programstart_step_guide.py --kickoff` first and follow the referenced files, scripts, and prompts.
2. Choose the dominant `PRODUCT_SHAPE` first.
3. Confirm whether the new project needs only PROGRAMBUILD or an additional USERJOURNEY attachment.
4. Prefer `scripts/programstart_create.py` as the primary project-factory entry point so recommendation, stamping, optional attachment, and generated kickoff guidance stay aligned.
5. If USERJOURNEY is needed, require an explicit attachment source instead of assuming the template repo should always be copied.
6. Summarize what was created, including the generated factory plan path.
7. Recommend the first documents to open next.

Use `config/process-registry.json` and the authority docs instead of inventing file lists.
