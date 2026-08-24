# PROGRAMSTART — Quick Start Guide

> Use this workspace to start a product, convert research into an executable project, or apply PROGRAMBUILD discipline to an existing project without creating duplicate planning authority.

---

## Workflow Modes

| System | Use it when... | Key state file |
|---|---|---|
| **PROGRAMBUILD** | Project intake, scope, architecture, testing, implementation, release, audit, learning | `PROGRAMBUILD/PROGRAMBUILD_STATE.json` |
| **USERJOURNEY** | Signup, consent, onboarding, activation, analytics, first-run routing | `USERJOURNEY/USERJOURNEY_STATE.json` when attached |

PROGRAMBUILD is the default workflow. USERJOURNEY is optional and should be attached only when real onboarding, consent, activation, or first-run routing work exists.

Repo boundary rule: PROGRAMSTART work stays inside this repo unless the user explicitly names another repo and asks you to work there.

PROGRAMBUILD tracks 11 stages from inputs/mode selection through post-launch review.

---

## 1. Select The Planning Entry Mode

Read `PROGRAMBUILD/PROGRAMBUILD_PLANNING_OPERATING_MODEL.md` first.

- **Raw idea** — little reliable planning/evidence exists.
- **Research-backed project** — substantial research exists and should be converted into durable project structure.
- **Existing / in-flight project** — current repository/product authority already exists. Identify its execution spine and propose explicit deltas instead of creating another Master Game Plan.

Then run Idea Intake in the matching mode. Research and audits are evidence until their recommendations are adopted into canonical project authority.

---

## 2. Orient Yourself

From the workspace root:

```bash
uv run programstart next
```

Windows shortcut:

```powershell
.\scripts\pb.ps1 next
```

`programstart next` reports current strategic state, blockers, and the registry-backed baseline files/prompts for the active step. The guide output is the **allowed stage context**, not an instruction to read every file in full for every task.

Useful orientation commands:

```powershell
.\scripts\pb.ps1 state show
.\scripts\pb.ps1 guide --system programbuild
.\scripts\pb.ps1 status
# USERJOURNEY only if attached:
.\scripts\pb.ps1 guide --system userjourney
```

---

## 3. Day-To-Day Execution Loop

```text
pb next / pb guide
      ↓
strategic stage + next convergence milestone
      ↓
derive/refresh CURRENT_WORK_PACKET.md for non-trivial work
      ↓
load exact authority sections + specialist context needed now
      ↓
identify reusable evidence + invalidation triggers
      ↓
perform one bounded slice
      ↓
run targeted verification for changed/at-risk surfaces
      ↓
reconcile material decisions/state into canonical authority
      ↓
next packet OR wider stage/release convergence gate
```

### Stage baseline vs current slice

Use `pb guide --system programbuild` to establish the stage baseline.

For non-trivial implementation, derive `CURRENT_WORK_PACKET.md` from `PROGRAMBUILD/PROGRAMBUILD_WORK_PACKET.md`. The packet should name:

- strategic execution spine/current stage
- one bounded objective
- explicit non-goals
- requirement IDs and exact authority sections needed now
- expected changed surfaces
- specialist references needed only for this slice
- trusted existing verification evidence
- invalidation triggers
- acceptance criteria
- targeted verification

`CURRENT_WORK_PACKET.md` is derived execution state and canonical for nothing. Replace/close it as work advances rather than accumulating a second planning hierarchy.

For trivial work, state the same fields briefly without creating unnecessary ceremony.

---

## 4. JIT, Drift, And Verification

### JIT authority baseline

```powershell
.\scripts\pb.ps1 jit-check --system programbuild
```

`jit-check` runs guide + drift + sync-rule summary. Use it especially before/after planning-authority or registry changes and at meaningful convergence points.

Do **not** run it around every code-only slice purely for ceremony. During bounded implementation, use the task-scoped `product-jit-check.prompt.md` protocol.

### Drift

```powershell
.\scripts\pb.ps1 drift
```

Run drift before changing planning authority/registry policy, after those changes, or when source-of-truth drift is suspected.

### Targeted slice verification

Ask:

1. What changed?
2. Which contracts, requirements, decisions, flows, environments, or operational behaviors could it invalidate?
3. Which prior evidence is still trustworthy because its invalidation trigger did not occur?
4. What is the smallest verification set that proves the changed/at-risk surface?

Examples:

- contract/auth change → relevant contract/auth/integration/alignment checks
- isolated internal refactor with unchanged contracts → focused unit/regression checks
- planning/registry authority change → full validation + drift
- stage transition/release → wider Challenge Gate/convergence suite

For planning-authority or registry changes:

```powershell
.\scripts\pb.ps1 validate
.\scripts\pb.ps1 validate --check repo-boundary # cross-repo consent rule still enforced
.\scripts\pb.ps1 drift
```

Narrow verification is appropriate during slices. Broader verification returns at stage transitions, periodic convergence reviews, and release readiness.

---

## 5. Close A Work Packet

Before deriving the next slice:

1. record verification evidence actually produced;
2. reconcile material scope/architecture/decision changes into canonical authority and `DECISION_LOG.md`;
3. confirm reused evidence remains within scope;
4. close/replace the current packet;
5. derive the next packet from updated authority.

Do not let packet history become a second roadmap.

---

## 6. Advance Only At A Real Stage Gate

A completed packet does not automatically mean the PROGRAMBUILD stage is complete.

Preview:

```powershell
.\scripts\pb.ps1 advance --system programbuild --dry-run
```

Advance only when the stage’s Challenge Gate is actually satisfied:

```powershell
.\scripts\pb.ps1 advance --system programbuild --decision "approved" --notes "Stage criteria confirmed"
```

USERJOURNEY, when attached:

```powershell
.\scripts\pb.ps1 advance --system userjourney --dry-run
.\scripts\pb.ps1 advance --system userjourney
```

Commit completed stage work before advancing so the drift/gate machinery evaluates the intended baseline.

---

## 7. Starting A New Project

Recommended factory path:

```powershell
programstart create `
  --dest "C:\Projects\MyNewApp" `
  --project-name "MyNewApp" `
  --product-shape "API service" `
  --owner "Your Name"
```

The generated project lives outside PROGRAMSTART and gets its own planning state, scaffold, setup surface, and git repository.

To also create/provision supported remote services:

```powershell
programstart create `
  --dest "C:\Projects\MyNewApp" `
  --project-name "MyNewApp" `
  --product-shape "web app" `
  --github-repo "your-org/MyNewApp" `
  --create-github-repo `
  --provision-services `
  --supabase-org-id "your-supabase-org-id"
```

Set relevant provider tokens before provisioning. Project-scoped services belong to the generated project, not the PROGRAMSTART template.

Lower-level bootstrap:

```powershell
.\scripts\pb.ps1 bootstrap `
  --dest "C:\Projects\MyNewApp" `
  --project-name "MyNewApp" `
  --variant product
```

Variants:
- `lite` — lean, low-risk
- `product` — standard production default
- `enterprise` — high-consequence, regulated, audit-heavy

Variant changes ceremony/evidence strength, not the one-spine or canonical-authority rules.

---

## 8. Applying PROGRAMBUILD To An Existing Project

Do **not** bootstrap a second planning hierarchy into an in-flight repository.

1. Identify the current canonical roadmap/Master Game Plan/execution spine.
2. Use **existing / in-flight project** mode.
3. Run Idea Intake as a delta audit, reusing current evidence rather than re-asking settled questions.
4. Convert research/audits into explicit recommended deltas.
5. Adopt accepted deltas through the existing project’s authority process.
6. During implementation, derive bounded work packets from that existing spine.

PROGRAMBUILD owns reusable methodology. The real project owns its live plan and state.

---

## 9. Toolchain Setup

Recommended local setup:

```powershell
uv sync --extra dev
pre-commit install
python -m playwright install chromium
uv run programstart validate --check bootstrap-assets
uv run --extra dev pyright
```

Useful confidence tiers:

```powershell
nox -s quick       # fast lint + type feedback
nox -s gate_safe   # local pre-merge convergence gate
nox -s ci          # full CI-equivalent gate
```

Use the narrowest truthful check during iteration and the broader required gate at convergence.

---

## 10. Emergency Reference Card

| Command | Purpose |
|---|---|
| `pb next` | Strategic orientation: status + active-step guides |
| `pb status` | Blockers and next strategic actions |
| `pb state show` | Stage/phase and sign-off history |
| `pb guide --system <s>` | Baseline files/prompts for active step |
| `pb jit-check --system <s>` | Authority baseline: guide + drift + sync rules |
| `pb drift` | Source-of-truth/order drift |
| `pb validate` | Full workspace validation; use at authority/convergence gates |
| `pb progress` | PROGRAMBUILD checklist progress |
| `pb advance --system <s> --dry-run` | Preview stage/phase advance |
| `pb advance --system <s>` | Advance after gate approval |
| `pb recommend` | Variant/stack recommendation |
| `pb impact <target>` | Downstream impact analysis |
| `pb research` | Knowledge/research delta operations |
| `pb create` | One-shot standalone project factory |
| `pb bootstrap` | Lower-level project bootstrap |
| `pb clean` | Remove disposable caches/temp artifacts |
| `pb dashboard` | Refresh status dashboard |

---

## 11. Authority Model

```text
PROGRAMBUILD_CANONICAL.md
       │
       ├── one concern → one canonical owner
       ├── one real project → one strategic execution spine
       └── research/audits/work packets do not silently replace authority

config/process-registry.json
       │
       ├── workflow_state
       ├── workflow_guidance
       ├── required/control files
       └── sync_rules

strategic execution spine
       │
       └── CURRENT_WORK_PACKET.md (optional, derived, replaceable)
```

The core discipline is:

**Narrow while executing. Widen while converging. Preserve one authority chain throughout.**
