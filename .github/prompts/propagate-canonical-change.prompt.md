---
description: "Propagate a canonical authority document change to all dependent files. Use when an authority file has changed and its dependent files must be brought into alignment."
name: "Propagate Canonical Change"
argument-hint: "The authority file that changed, e.g. PROGRAMBUILD/PROGRAMBUILD_CANONICAL.md or USERJOURNEY/LEGAL_AND_CONSENT.md"
agent: "agent"
---
Propagate a change from an authority document to all files that depend on it.

## Tasks

### 1. Confirm the baseline is captured

Run `scripts/programstart_drift_check.py` (or `programstart drift`) before any edits. Record the current violations (if any) so you know which delta is yours.

### 2. Identify the authority file and its dependents

Open `config/process-registry.json` and locate the `sync_rules` entry whose `authority_files` list contains the changed file. Note:

- The `name` of the rule
- Every file listed in `dependent_files`
- The `description` which explains what must stay in sync

### 3. Read the authority document in full

Read the authority file in its current (post-change) state. Extract specifically:

- What changed versus the previous version
- Which concepts or decisions are now different or newly defined
- Which downstream claims those changes invalidate

### 4. For each dependent file

Read the dependent file. Then answer:

- Does it contain any statement that contradicts the authority doc?
- Does it reference a concept the authority doc has now changed?
- Does it omit something the authority doc now requires?

If any answer is yes:

1. Quote the specific conflict.
2. State what the authority doc now says.
3. Propose the minimal edit to make them consistent.
4. Apply the edit.

Do not rephrase or expand dependent files beyond what alignment requires.
Do not invent policy or behaviour not present in the authority doc.

### 5. Check upstream authority chain

If the changed authority file itself depends on a higher authority (check `sync_rules` for rules where it appears as a `dependent_file`), flag it. The higher authority must have been updated first.

### 6. Verify

After all edits, run:

```
programstart validate --check all
programstart drift
```

Both must pass. If `programstart drift` still reports violations for this rule, report which dependent file still has a gap.

### 7. Produce a summary

Output a table:

| Dependent file | Action taken | Conflict resolved |
|---|---|---|
| (file) | (updated / no change needed) | (what was resolved, or "none") |

Then state: **consistent** or **still has gaps** (with what remains).
