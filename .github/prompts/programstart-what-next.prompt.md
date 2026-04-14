---
description: "Summarize what to do next in PROGRAMSTART. Use when asking for current stage, blockers, next files to open, or whether the repo is ready to move forward."
name: "PROGRAMSTART What Next"
argument-hint: "Optional system: programbuild, userjourney, or all"
agent: "agent"
version: "1.0"
---
Summarize the next recommended action using the repository's durable workflow assets.

Tasks:

1. Use `scripts/programstart_status.py` for the requested system when available.
2. Use `scripts/programstart_step_guide.py` when the current stage or phase is known so the answer references the authoritative files, scripts, and prompts for that step.
3. Read only the source-of-truth docs needed to explain the current stage, blockers, and next steps.
4. Return a concise answer that identifies:
   - current stage or phase
   - blockers
   - next file or files to open
   - recommended next action

Prefer the repository registry and scripts over chat memory.
