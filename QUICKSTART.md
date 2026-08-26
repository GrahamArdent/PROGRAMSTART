# PROGRAMSTART — Quick Start Guide

> Start, resume, or improve a project without loading the whole methodology or creating duplicate planning authority.

Repo boundary rule: PROGRAMSTART work stays inside this repo unless the user explicitly names another repo and asks you to work there.

---

## 1. Start With Live Orientation

Do **not** begin by reading the documentation tree.

From the workspace root:

```powershell
.\scripts\pb.ps1 status
.\scripts\pb.ps1 guide --system programbuild
```

Or:

```bash
uv run programstart status
uv run programstart guide --system programbuild
```

`status` tells you where the project is.
`guide` tells you the allowed baseline authority for the active stage.

The guide is **not a reading list**. Load only the exact authority/evidence needed for the current task.

USERJOURNEY is optional. Use its guide only when that workflow is actually attached/relevant.

---

## 2. Know The Authority Model

```text
PROGRAMBUILD methodology
        ↓
real project's one strategic execution spine
        ↓
current logical work packet (derived, replaceable)
        ↓
JIT authority + evidence for this slice
```

Rules:

- PROGRAMBUILD owns reusable methodology, not every project's live plan.
- Existing projects keep their current Master Game Plan/roadmap unless explicitly replaced.
- Research, audits, checklists, adaptive-router outputs, and packets are evidence/derived aids.
- A newer document does not automatically outrank established authority.

---

## 3. Select Entry Mode When Starting/Reshaping A Project

Use `PROGRAMBUILD/PROGRAMBUILD_PLANNING_OPERATING_MODEL.md` when entry-mode decisions are actually needed:

- **Raw idea** — little reliable planning exists.
- **Research-backed** — substantial evidence exists but needs conversion into decisions/scope.
- **Existing / in-flight** — code/plans/state already exist; produce deltas to current authority instead of another master plan.

Run Idea Intake using existing evidence to prefill settled questions.

### Adaptive decision routing

Do not research merely because more knowledge might be useful.

If current evidence already makes a low-risk, reversible decision safe, execute it. When missing knowledge could materially change the next important decision, route that decision to the smallest justified scrutiny:

```powershell
.\scripts\pb.ps1 decide `
  --decision "Choose the provider integration contract" `
  --mode c `
  --impact medium `
  --uncertainty high `
  --reversibility costly `
  --evidence partial `
  --concern contract `
  --concern runtime
```

Research depth is qualitative:

- `none` — current evidence is sufficient;
- `targeted` — fill/refresh a bounded decision-relevant gap;
- `deep` — reserve for high-impact, high-uncertainty decisions where evidence is absent/conflicting and focused checking cannot safely bound the decision.

`decide` is advisory. It does not create a new lifecycle or execution spine. In Mode C, resolve any bounded evidence gap and return to the existing project's next executable slice.

---

## 4. Day-To-Day Execution Loop

```text
status + guide
    ↓
define one compact logical work packet
    ↓
load exact task authority/evidence
    ↓
reuse still-valid evidence
    ↓
execute one bounded slice
    ↓
targeted verification
    ↓
reconcile durable decisions/state
    ↓
next slice OR meaningful convergence gate
```

### Compact work packet — default

Use `PROGRAMBUILD/PROGRAMBUILD_WORK_PACKET.md` and state:

```text
OBJECTIVE:
WHY_NOW / AUTHORITY:
IN_SCOPE:
OUT_OF_SCOPE:
REQUIRED_CONTEXT:
REUSABLE_EVIDENCE:
INVALIDATION_TRIGGERS:
ACCEPTANCE_CRITERIA:
TARGETED_VERIFICATION:
DURABLE_UPDATES_IF_NEEDED:
```

This may live in the task/issue/PR/current session.

Persist `CURRENT_WORK_PACKET.md` only when multi-session/multi-agent coordination, risk, dependencies/blockers, or resumability makes a file genuinely useful.

A packet is canonical for nothing.

---

## 5. Verification Economy

For each slice ask:

1. What changed?
2. What can that change invalidate?
3. Which prior evidence remains trustworthy?
4. What is the smallest check that restores confidence?
5. Is this a convergence boundary requiring wider verification?

Examples:

- contract/auth change → relevant contract/auth/integration checks;
- isolated internal refactor → focused unit/regression checks;
- planning/registry authority change → required validation + drift;
- release readiness → full Product/Enterprise convergence as applicable.

Useful commands:

```powershell
.\scripts\pb.ps1 drift
.\scripts\pb.ps1 validate
.\scripts\pb.ps1 validate --check repo-boundary # cross-repo consent rule still enforced
```

Do not run broad checks because a session changed.
Do not use a fixed feature/time counter as proof that convergence is due.

---

## 6. Challenge Gates

A completed slice does not automatically finish a stage.

Use `PROGRAMBUILD/PROGRAMBUILD_CHALLENGE_GATE.md` at stage transitions.

- Lite: A/C/F minimum + risk-relevant parts.
- Product: A/C/F baseline + stage/risk-relevant B/D/E/G/H.
- Product full A–H: release readiness and other genuinely whole-system convergence.
- Enterprise: full A–H with retained evidence/sign-off appropriate to risk.

Do not rerun adaptive-router analysis at a Challenge Gate if its evidence is still current; reuse it and run only the gate parts that the transition/convergence actually requires.

Preview stage advancement:

```powershell
.\scripts\pb.ps1 advance --system programbuild --dry-run
```

Advance after the actual gate is satisfied:

```powershell
.\scripts\pb.ps1 advance --system programbuild --decision "approved" --notes "Stage criteria confirmed"
```

---

## 7. Full Convergence — Manual, Not A Heartbeat

During iteration, use targeted checks.

Local confidence tiers:

```powershell
nox -s quick
nox -s gate_safe
nox -s ci
```

PROGRAMSTART also has `.github/workflows/manual-convergence.yml`, intentionally `workflow_dispatch`-only. Use it when a meaningful full-repository convergence gate is warranted.

Generated projects receive a manual-only Full CI Gate template by default. Add automatic PR/push/schedule triggers only when that project's actual operating needs justify the cost/noise.

---

## 8. Starting A New Project

Recommended factory path:

```powershell
programstart create `
  --dest "C:\Projects\MyNewApp" `
  --project-name "MyNewApp" `
  --product-shape "API service" `
  --owner "Your Name"
```

Lower-level full bootstrap:

```powershell
.\scripts\pb.ps1 bootstrap `
  --dest "C:\Projects\MyNewApp" `
  --project-name "MyNewApp" `
  --variant product
```

For a project that needs PROGRAMBUILD governance but **not** PROGRAMSTART's dashboard/scripts/tests/toolchain, use the methodology-only bootstrap. It now creates a lightweight external-control surface: PROGRAMBUILD files, a flat project registry, managed workflow prompts, and a sync manifest. The executable PROGRAMSTART runtime stays in this repository.

Once the target checkout exists, operate it from the central runtime:

```powershell
uv run programstart target --repo "C:\Projects\MyNewApp" status
uv run programstart target --repo "C:\Projects\MyNewApp" guide --system programbuild
uv run programstart target --repo "C:\Projects\MyNewApp" decide --decision "Choose the next slice" --mode c --evidence sufficient --uncertainty low
```

A methodology-only repo created before this control surface existed can be linked without replacing its PROGRAMBUILD state or project files:

```powershell
uv run programstart target --repo "C:\Projects\ExistingLeanRepo" --prepare
```

`--prepare` adds only the process registry, managed workflow prompts, and sync manifest. It refuses conflicting project-owned prompt files and does not copy PROGRAMSTART's runtime, dashboard, tests, CI, or development toolchain.

Variants:

- `lite` — lean/low-risk;
- `product` — normal production default;
- `enterprise` — high-consequence/regulated/audit-heavy.

Variant controls rigor, not the number of documents for its own sake.

---

## 9. Applying PROGRAMBUILD To An Existing Project

Do **not** bootstrap a second planning hierarchy.

1. Identify the existing strategic execution spine.
2. Use existing/in-flight mode.
3. Reuse current evidence.
4. Convert new research/audits into explicit deltas.
5. Adopt accepted deltas through existing project authority.
6. Execute bounded logical packets derived from that spine.

`programstart-adopt` remains the non-destructive first-time overlay for an established repository that has no PROGRAMBUILD surface yet. After adoption, the same central target command can drive it without requiring the project to own a copy of PROGRAMSTART's runtime:

```powershell
uv run programstart target --repo "C:\Projects\ExistingApp" next
```

---

## 10. Toolchain Setup

```powershell
uv sync --extra dev
pre-commit install
python -m playwright install chromium
uv run programstart validate --check bootstrap-assets
uv run --extra dev pyright
```

---

## 11. Emergency Reference

| Command | Purpose |
|---|---|
| `pb status` | current stage/blockers |
| `pb next` | strategic orientation bundle |
| `pb guide --system <s>` | allowed stage baseline |
| `pb state show` | workflow state/history |
| `pb drift` | source-of-truth drift when relevant |
| `pb validate` | structural/convergence validation |
| `pb advance --system <s> --dry-run` | preview transition |
| `pb advance --system <s>` | advance after gate |
| `pb recommend` | shape/stack guidance |
| `pb impact <target>` | impact analysis |
| `pb decide --decision <d>` | minimum justified decision scrutiny/research depth |
| `pb target --repo <path> <command>` | run central PROGRAMSTART machinery against a lean/external project checkout |
| `pb research` | research/KB operations |
| `pb create` | standalone project factory |
| `pb bootstrap` | lower-level full bootstrap |

---

## Success Rule

**Narrow while executing. Widen while converging. Investigate only uncertainty that can change a decision. Preserve one authority chain.**

If the process makes you read, write, research, or rerun more than is needed to answer “what matters now and how do we prove it?”, simplify it.
