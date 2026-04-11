---
description: "Show the correct files, scripts, and prompts for a specific PROGRAMSTART step. Use when starting a new project stage or USERJOURNEY phase and you want authoritative guidance instead of memory-driven sequencing."
name: "PROGRAMSTART Stage Guide"
argument-hint: "Use kickoff, a PROGRAMBUILD stage name, or a USERJOURNEY phase key if USERJOURNEY is attached"
agent: "agent"
---
Determine the correct assets to use for a specific PROGRAMSTART step.

Tasks:

1. Use `scripts/programstart_step_guide.py` with the requested kickoff, PROGRAMBUILD stage, or USERJOURNEY phase.
2. Return the authoritative files to open first.
3. Return the scripts to run first.
4. Return the prompts that should be used instead of relying on chat memory.
5. If the requested step is missing from the registry, say so explicitly instead of inventing a sequence.
6. For the implementation_loop stage: remind the operator that ARCHITECTURE.md, REQUIREMENTS.md, and USER_FLOWS.md are living authorities during coding. They must be re-read before each feature, not just at stage entry. If the guide output includes these files, call them out as "re-read before each feature" rather than "read once at stage start."

Prefer the registry-backed guide output over ad hoc step ordering.
