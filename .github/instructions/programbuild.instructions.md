---
description: "Use when editing PROGRAMBUILD docs, starting a new product planning package, changing stage order, changing canonical ownership, or validating PROGRAMBUILD structure and required outputs."
name: "PROGRAMBUILD Workflow"
applyTo: "PROGRAMBUILD/**/*.md"
---
# PROGRAMBUILD Workflow

- Read `PROGRAMBUILD/PROGRAMBUILD_CANONICAL.md` first when authority, naming, or conflict resolution is relevant.
- Read `PROGRAMBUILD/PROGRAMBUILD_FILE_INDEX.md` first when deciding whether a file is a recognized control file.
- Keep the standard stage order intact unless the change explicitly updates the canonical docs.
- If a critical control file is added, renamed, or repurposed, update `PROGRAMBUILD/PROGRAMBUILD_CANONICAL.md`, `PROGRAMBUILD/PROGRAMBUILD_FILE_INDEX.md`, and `config/process-registry.json` in the same change.
- Preserve the metadata block in standard output files.
- Prefer `scripts/programstart_validate.py --check required-files` and `scripts/programstart_status.py --system programbuild` when checking completeness or next actions.
