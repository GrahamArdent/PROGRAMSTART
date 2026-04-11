---
description: "Use when editing PROGRAMBUILD docs, starting a new product planning package, changing stage order, changing canonical ownership, or validating PROGRAMBUILD structure and required outputs."
name: "PROGRAMBUILD Workflow"
applyTo: "PROGRAMBUILD/**/*.md"
---
# PROGRAMBUILD Workflow

The key words MUST, MUST NOT, SHOULD, SHOULD NOT, and MAY in this document are interpreted as described in [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119).

- You MUST read `PROGRAMBUILD/PROGRAMBUILD_CANONICAL.md` first when authority, naming, or conflict resolution is relevant.
- You MUST read `PROGRAMBUILD/PROGRAMBUILD_FILE_INDEX.md` first when deciding whether a file is a recognized control file.
- You MUST keep the standard stage order intact unless the change explicitly updates the canonical docs.
- If a critical control file is added, renamed, or repurposed, you MUST update `PROGRAMBUILD/PROGRAMBUILD_CANONICAL.md`, `PROGRAMBUILD/PROGRAMBUILD_FILE_INDEX.md`, and `config/process-registry.json` in the same change.
- You MUST preserve the metadata block in standard output files.
- You SHOULD use `scripts/programstart_validate.py --check required-files` and `scripts/programstart_status.py --system programbuild` when checking completeness or next actions.
