# Automation And Human-Error Review — 2026-04-15

Purpose: Capture the April 15, 2026 critical review of PROGRAMSTART with emphasis on removing human loops, collapsing duplicated operational ceremony into code, and converting advisory workflow rules into enforced controls.
Status: **Open backlog** for near-term implementation planning.
Authority: Non-canonical working report derived from direct codebase and workflow review on 2026-04-15.
Last updated: 2026-04-15

---

## 1. Executive Summary

The repository has improved materially, but several high-value controls still depend on operators remembering to do the right thing:

1. The Challenge Gate remains advisory in code even though it is mandatory in canonical docs.
2. Governance close-out is defined in standards but duplicated manually across multiple operator prompts.
3. Drift enforcement is still asymmetric for some authority changes.
4. Prompt registration and prompt authority loading are still maintained partly as prose rather than machine-checked data.
5. Several generated-project setup paths still terminate in manual follow-up rather than executable provisioning.

The core pattern is consistent: PROGRAMSTART often has the rule, the note, and the prompt, but not always the single executable control that makes the human step optional.

---

## 2. Prioritized Findings

### AUTO-01 — Challenge Gate Is Still Advisory

**Severity**: HIGH

**Current state**:
- `PROGRAMBUILD/PROGRAMBUILD_CHALLENGE_GATE.md` says the gate is required before every stage transition.
- `scripts/programstart_workflow_state.py` only prints a warning when the log row is missing.
- `--skip-gate-check` bypasses even that warning path.

**Why this is a real risk**:
The Challenge Gate is the only durable mechanism that forces re-checking kill criteria, scope drift, and assumption decay between stages. In code, it is still optional behavior.

**Human loop still required today**:
The operator must remember to run the gate, record it manually in Markdown, and self-police whether the warning should block progress.

**Recommended automation**:
Move Challenge Gate evidence into workflow state and make `programstart advance` block unless the prior transition has structured gate completion evidence.

**Best implementation shape**:
- Add Challenge Gate state fields to `PROGRAMBUILD_STATE.json`
- Add a guided command to record gate completion
- Make advance fail, not warn, when the gate is missing

---

### AUTO-02 — Governance Close-out Is Duplicated Instead Of Executable

**Severity**: HIGH

**Current state**:
- `.github/prompts/OPERATOR_PROMPT_STANDARD.md` defines the governance close-out loop.
- Four long-form operator prompts duplicate the same command sequence and checkpoint prose.

**Why this is a real risk**:
Any future change to the close-out rule must be propagated across multiple prompts. That is the same class of human-sync problem the repo is trying to eliminate elsewhere.

**Human loop still required today**:
The operator must manually run the command set, manually perform ADR triage, and manually write checkpoint evidence.

**Recommended automation**:
Introduce a single `programstart closeout` or `programstart checkpoint` command that runs the required verification commands, evaluates ADR evidence requirements, and writes machine-readable close-out evidence.

**Best implementation shape**:
- One command for durable-checkpoint close-out
- Optional `--phase` / `--context` metadata
- Output written to structured evidence rather than freeform phase notes

---

### AUTO-03 — Drift Enforcement Still Relies On Strict Mode For Some Important Cases

**Severity**: HIGH

**Current state**:
- `scripts/programstart_drift_check.py` fails when dependents change without authority files for rules that request it.
- Authority-only changes without dependent updates are still notes unless `--strict` is used.

**Why this is a real risk**:
Canonical changes can still leave downstream dependents stale while the default drift run passes.

**Human loop still required today**:
The operator must interpret notes correctly and choose to escalate them.

**Recommended automation**:
Add bidirectional enforcement options per sync rule so selected authority changes must update dependents in normal mode, not just strict mode.

**Best implementation shape**:
- Per-rule `require_dependents_when_authority_changes`
- Hard-fail for high-value rules: prompt standards, ADR template, canonical/file-index alignment

---

### AUTO-04 — Decision Reversal Symmetry Is Not Fully Validated

**Severity**: MEDIUM-HIGH

**Current state**:
- ADR coherence is now validated.
- DECISION_LOG reversal invariants are still not checked directly.

**Why this is a real risk**:
`REVERSED` and `SUPERSEDED` pairs still rely on paired manual edits and can drift independently.

**Human loop still required today**:
The operator must remember to update both rows and keep the `Replaces` linkage coherent.

**Recommended automation**:
Add decision-log invariant validation for reversal pairing, orphaned replacements, and cycles.

---

### AUTO-05 — Prompt Registration Completeness Is Not A Hard Gate

**Severity**: MEDIUM-HIGH

**Current state**:
- Prompt classes are listed in `config/process-registry.json`.
- `scripts/lint_prompts.py` loads the registry but still falls back to `workflow` classification for unregistered public prompts.

**Why this is a real risk**:
An on-disk prompt can exist, lint, and still be invisible or misclassified from the registry perspective.

**Human loop still required today**:
Authors must remember to register prompts by hand and keep class assignment synchronized.

**Recommended automation**:
Add a prompt-registry completeness validator that diffs the filesystem against `prompt_registry` and fails on missing or dangling entries.

---

### AUTO-06 — Prompt Authority Loading Is Still Maintained As Prose

**Severity**: MEDIUM

**Current state**:
- `PROMPT_STANDARD.md` instructs authors to list authority files.
- Prompt files maintain those lists manually.

**Why this is a real risk**:
Authority coverage can drift silently because the prompt structure is not yet machine-readable enough to verify against stage guidance.

**Human loop still required today**:
Prompt authors must keep authority file lists synchronized with `workflow_guidance` and `sync_rules`.

**Recommended automation**:
Add machine-readable `authority_files` metadata to workflow prompts or generate the section directly from registry-backed prompt-build data.

---

### AUTO-07 — Placeholder Scanning Is Useful But Still Too Narrow

**Severity**: MEDIUM

**Current state**:
- `check_content_quality()` exists.
- Only selected stage files are scanned, and only as non-blocking warnings.

**Why this is a real risk**:
Canonical docs, decision records, and other planning surfaces can still ship with placeholder residue outside the curated stage-file list.

**Human loop still required today**:
Operators must visually inspect many planning surfaces for TODO/TBD residue.

**Recommended automation**:
Add a repo-wide placeholder-content validator with severity driven by file role.

---

### AUTO-08 — Prompt Generation Exists, But The Source Of Truth Is Still Split

**Severity**: MEDIUM

**Current state**:
- `programstart_prompt_build.py` can generate prompts.
- Public prompts are still maintained manually while standards, rule references, and authority-loading patterns are also maintained separately.

**Why this is a real risk**:
This is duplicated truth: generator logic, standards, registry metadata, and prompt bodies can all drift.

**Human loop still required today**:
The operator must decide which prompts are generated versus hand-maintained and keep those choices synchronized mentally.

**Recommended automation**:
Decide which prompt families are generated artifacts and enforce regeneration for those families instead of manual edits.

---

### AUTO-09 — Generated Repo Provisioning Still Ends In Manual Setup

**Severity**: MEDIUM

**Current state**:
- Some services can be provisioned automatically.
- Others still emit `manual_only`, `manual_secrets`, and manual follow-up instructions.

**Why this is a real risk**:
The factory improves setup but still leaves sensitive or error-prone final wiring steps to operators.

**Human loop still required today**:
Users must manually complete secret wiring, provider setup, and some service onboarding.

**Recommended automation**:
Continue converting the service matrix from documentation-only guidance to provider-specific executable provisioning with explicit machine-readable completion status.

---

### AUTO-10 — Early ADRs Remain Legacy Pre-Register Records

**Severity**: LOW

**Current state**:
- ADRs 0001–0003 predate the current decision-register regime.
- They remain historically valid but do not link to DECISION_LOG rows.

**Why this matters**:
This is not an active defect, but it is a standing ambiguity unless deliberately classified.

**Recommended automation**:
Explicitly classify them as legacy pre-register ADRs in validation or documentation so they are not re-litigated later as “missing links.”

---

## 3. Recommended Implementation Order

### Quick wins

1. `AUTO-04` — decision-log reversal invariant validation
2. `AUTO-05` — prompt-registry completeness validation
3. `AUTO-07` — repo-wide placeholder-content check
4. `AUTO-10` — explicitly classify legacy pre-register ADRs

### Highest leverage

1. `AUTO-02` — executable governance close-out command
2. `AUTO-01` — structured, blocking Challenge Gate
3. `AUTO-03` — bidirectional drift enforcement for selected sync rules

### Larger architectural automations

1. `AUTO-06` — machine-readable prompt authority loading
2. `AUTO-08` — generated prompt families instead of manual prompt sync
3. `AUTO-09` — reduce manual service setup in generated repos

---

## 4. Save Strategy Recommendation

These findings should be treated as near-term backlog, not as accepted architecture decisions yet.

Recommended handling:

1. Keep this report as the detailed critical review record.
2. Queue the implementation work in `devlog/gameplans/hardeninggameplan.md` as a dedicated strategic follow-up phase.
3. Promote any adopted automation that changes durable workflow policy into DECISION_LOG and ADRs only when implementation begins or a policy decision is accepted.

This keeps the distinction clear between:
- observations and recommended changes
- scheduled implementation work
- accepted durable repo policy
