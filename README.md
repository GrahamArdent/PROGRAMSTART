# PROGRAMSTART

Purpose: A program that builds other programs — a workflow automation toolkit for structured product planning, execution tracking, and intelligent context retrieval.
Last updated: 2026-03-30

---

## What PROGRAMSTART Does

PROGRAMSTART is a CLI-driven planning and workflow automation system that guides the creation of new software products from kickoff through release. It replaces ad-hoc planning with a machine-readable, stage-gated process backed by validated templates, context indexing, and AI-powered retrieval.

**The core idea:** instead of starting every new project with blank documents and tribal knowledge, PROGRAMSTART gives you a validated scaffold, enforces completion gates, tracks drift from source-of-truth documents, and lets you query your own planning context intelligently.

PROGRAMSTART is the source template and orchestration repo. Product code and project infrastructure belong in separately generated repos, never inside this repository.

It also now includes a project-factory layer:

- `programstart create` turns product shape and capability needs into a stamped standalone repo, optional attachment decision, and generated kickoff/provisioning plans in one pass
- `programstart init` bootstraps and stamps a new standalone project repo in one pass
- `programstart attach userjourney --source <path>` adds the optional onboarding attachment later
- `programstart recommend` turns product shape and needs into workflow and stack guidance
- `programstart impact <target>` shows the likely downstream blast radius before you edit authority docs
- `programstart research --track <name>` generates a dated research-delta template from the KB maintenance ledger
- `programstart research --status` reports which weekly research lanes are due and which KB coverage domains are still only partial or seed-level

The knowledge base is also now more explicit about how it makes decisions:

- stack entries and archetypes capture baseline platform guidance
- CLI tool entries capture which developer CLIs should be installed and authenticated early
- third-party API entries capture reusable auth/env surfaces for common vendor integrations
- coverage domains make the KB honest about which product areas are strong, partial, or still seed-stage
- decision rules capture recurring architecture choices
- explicit KB relationships show complements, alternatives, and upgrade paths
- structured comparisons capture version deltas such as Python 3.13 vs 3.14
- a weekly research cadence plus CI-visible freshness status keeps recommendations current without turning the KB into an unbounded note dump

## How It Works — The Complete Workflow

### Phase 1: Bootstrap

A new project should usually start with `programstart create`. This compiles recommendation logic, stamps a new standalone repo, initializes local git, and writes generated kickoff and provisioning plans:

```
programstart create --dest ~/projects/new-product --project-name "MyProduct" --product-shape "API service"
```

If you want PROGRAMSTART to create the GitHub remote and provision supported project services as part of the factory run, opt in explicitly:

```
programstart create --dest ~/projects/new-product --project-name "MyProduct" --product-shape "web app" --github-repo my-org/my-product --create-github-repo --provision-services --supabase-org-id <org-id>
```

For Supabase provisioning, set `SUPABASE_ACCESS_TOKEN` in the environment before running the command. For Vercel provisioning, set `VERCEL_ACCESS_TOKEN`. For Neon provisioning, set `NEON_API_KEY` and optionally `NEON_ORG_ID`. The factory infers supported services from the recommended shape/stacks, writes machine-readable results to `outputs/factory/provisioning-state.json`, writes `outputs/factory/setup-surface.md` with recommended CLI installs and reusable API auth surfaces, emits starter `.env.example` files based on inferred services and third-party APIs, and hydrates non-secret provider IDs and URLs into those env templates after supported provisioning runs.

If you need the lower-level primitives, `programstart bootstrap` still scaffolds a clean project repo from validated templates:

```
programstart bootstrap --dest ~/projects/new-product --project-name "MyProduct" --variant product
```

This creates:
- A `PROGRAMBUILD/` directory with all required planning documents (FEASIBILITY, REQUIREMENTS, ARCHITECTURE, etc.)
- A `config/process-registry.json` defining stage order, required files, and sync rules
- Pre-configured tooling (`.pre-commit-config.yaml`, `noxfile.py`, test harness)
- A generated factory plan under `outputs/factory/create-plan.md`
- A generated provisioning plan under `outputs/factory/provisioning-plan.md`
- A standalone local git repository for the new project
- Optionally, a `USERJOURNEY/` attachment for interactive end-user products when the create flow is given an attachment source

For the faster path, use `programstart init` instead of raw bootstrap. It wraps bootstrap, stamps kickoff inputs, updates metadata owners and dates, and can attach `USERJOURNEY` during setup.

### Phase 2: Stage-Gated Execution

PROGRAMSTART enforces a strict stage order. Each stage has required outputs that must be completed before advancing:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        PROGRAMBUILD STAGE ORDER                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  0. INPUTS & MODE       → Variant, product shape, kickoff packet          │
│     └─ Output: kickoff inputs block                                        │
│                                                                             │
│  1. FEASIBILITY          → Go/no-go decision, kill criteria                │
│     └─ Output: FEASIBILITY.md                                              │
│                                                                             │
│  2. RESEARCH             → Market/tech research, stack validation           │
│     └─ Output: RESEARCH_SUMMARY.md                                         │
│                                                                             │
│  3. REQUIREMENTS & UX    → Scope, constraints, acceptance criteria          │
│     └─ Output: REQUIREMENTS.md                                             │
│                                                                             │
│  4. ARCHITECTURE & RISK  → System boundaries, contracts, risk spikes        │
│     └─ Output: ARCHITECTURE.md                                             │
│                                                                             │
│  5. SCAFFOLD & GATES     → Working skeleton and CI gates                    │
│     └─ Output: automation and skeleton state                               │
│                                                                             │
│  6. TEST_STRATEGY        → Test model, coverage plan, automation approach   │
│     └─ Output: TEST_STRATEGY.md                                            │
│                                                                             │
│  7. IMPLEMENTATION       → Feature code and tests                           │
│     └─ Output: working feature set                                         │
│                                                                             │
│  8. RELEASE_READINESS    → Launch gates, operational checks, rollback plan  │
│     └─ Output: RELEASE_READINESS.md                                        │
│                                                                             │
│  9. AUDIT                → Drift detection, risk findings                   │
│     └─ Output: AUDIT_REPORT.md                                             │
│                                                                             │
│ 10. POST_LAUNCH          → Outcomes, lessons, follow-up actions             │
│     └─ Output: POST_LAUNCH_REVIEW.md                                       │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

Advance through stages with:

```powershell
programstart state show                    # see current stage
programstart advance --system programbuild # approve and move forward
```

### Phase 3: Context Intelligence

PROGRAMSTART builds a structured context index from all planning documents, knowledge base entries, concerns, routes, and commands. This powers three layers of retrieval:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        RETRIEVAL ARCHITECTURE                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Layer 1: BM25 Lexical Search                                              │
│     ├─ Tokenization with stop-word removal                                 │
│     ├─ Inverted index with TF-IDF scoring                                  │
│     └─ Okapi BM25 ranking (k1=1.5, b=0.75)                                │
│                                                                             │
│  Layer 2: Hybrid Search (BM25 + Vector)                                    │
│     ├─ ChromaDB embedding store (optional)                                 │
│     ├─ Reciprocal Rank Fusion (RRF) merging                                │
│     └─ Alpha-weighted lexical/vector blending                              │
│                                                                             │
│  Layer 3: RAG Assistant (LiteLLM + Instructor)                             │
│     ├─ Multi-provider LLM gateway (OpenAI, Anthropic, etc.)               │
│     ├─ Pydantic-validated structured responses                             │
│     ├─ Source citation and confidence scoring                              │
│     └─ Instructor-powered schema enforcement with auto-retry               │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Phase 4: Continuous Validation

PROGRAMSTART continuously validates the planning workspace:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        VALIDATION PIPELINE                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  programstart validate                                                      │
│     ├─ required-files      → all stage outputs present                     │
│     ├─ metadata            → ownership and dating in every doc             │
│     ├─ authority-sync      → canonical docs match machine registry         │
│     ├─ repo-boundary       → cross-repo consent rule remains enforced      │
│     └─ planning-references → no broken cross-references                    │
│                                                                             │
│  programstart drift                                                         │
│     ├─ source-of-truth sync checking                                       │
│     ├─ future-stage edit rejection                                         │
│     └─ authority chain verification                                        │
│                                                                             │
│  pre-commit hooks                                                           │
│     ├─ ruff (lint + format)                                                │
│     ├─ pyright (type checking)                                             │
│     ├─ bandit (security)                                                   │
│     ├─ detect-secrets                                                      │
│     └─ yamllint                                                            │
│                                                                             │
│  pytest (factory + workflow coverage)                                       │
│     ├─ unit tests for all CLI commands                                     │
│     ├─ end-to-end project factory tests                                    │
│     ├─ Pydantic model validation tests                                     │
│     ├─ Hypothesis property-based tests (BM25, tokenizer, corpus)           │
│     ├─ RAG integration tests (mocked LLM layer)                            │
│     └─ Playwright golden screenshot tests (dashboard)                      │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Architecture — How the Components Fit Together

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        PROGRAMSTART SYSTEM MAP                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  config/                                                                    │
│     ├─ process-registry.json   ← machine-readable workflow rules           │
│     └─ knowledge-base.json     ← stacks, patterns, rules, relations, comparisons │
│                                                                             │
│  scripts/                                                                   │
│     ├─ programstart_cli.py     ← unified CLI entry point                   │
│     ├─ programstart_models.py  ← Pydantic typed models (ContextIndex, KB)  │
│     ├─ programstart_context.py ← context index builder                     │
│     ├─ programstart_retrieval.py ← BM25 + hybrid + RAG (LiteLLM/Instructor)│
│     ├─ programstart_validate.py  ← required files, metadata, sync checks  │
│     ├─ programstart_status.py    ← stage, blockers, next actions           │
│     ├─ programstart_workflow_state.py ← state inspection and advancement   │
│     ├─ programstart_drift_check.py    ← source-of-truth drift detection    │
│     ├─ programstart_bootstrap.py      ← low-level project scaffolding     │
│     ├─ programstart_create.py         ← one-shot factory orchestration    │
│     ├─ programstart_serve.py          ← dashboard HTTP server             │
│     └─ programstart_common.py         ← shared utilities                  │
│                                                                             │
│  PROGRAMBUILD/                                                              │
│     ├─ PROGRAMBUILD_CANONICAL.md  ← authority map (one concern, one owner) │
│     ├─ PROGRAMBUILD_FILE_INDEX.md ← file inventory and status             │
│     ├─ PROGRAMBUILD.md            ← stage order and base workflow         │
│     └─ [stage output templates]   ← FEASIBILITY, ARCHITECTURE, etc.       │
│                                                                             │
│  USERJOURNEY/ (optional attachment)                                         │
│     ├─ DELIVERY_GAMEPLAN.md    ← source-of-truth chain                    │
│     ├─ ROUTE_AND_STATE_FREEZE.md ← route/state design                     │
│     └─ [planning artifacts]    ← consent, analytics, UX, implementation    │
│                                                                             │
│  outputs/                                                                   │
│     ├─ context/context-index.json ← generated context index               │
│     ├─ STATUS_DASHBOARD.md        ← generated dashboard                   │
│     └─ retrieval/chroma/          ← vector store (when enabled)           │
│                                                                             │
│  tests/                                                                     │
│     ├─ test_programstart_models.py      ← Pydantic model tests            │
│     ├─ test_hypothesis_retrieval.py     ← property-based tests            │
│     ├─ test_rag_integration.py          ← RAG pipeline tests              │
│     ├─ test_programstart_retrieval.py   ← BM25/hybrid search tests        │
│     └─ [17 more test modules]           ← CLI, validation, workflow, etc.  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Data Flow — From Documents to Answers

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Planning   │     │   Context    │     │   Retrieval  │     │     RAG      │
│   Documents  │────▶│   Builder    │────▶│    Engine    │────▶│  Assistant   │
│              │     │              │     │              │     │              │
│ PROGRAMBUILD/│     │ Extracts:    │     │ BM25 index   │     │ LiteLLM      │
│ USERJOURNEY/ │     │ - documents  │     │ ChromaDB     │     │ + Instructor │
│ config/KB    │     │ - concerns   │     │ Hybrid RRF   │     │ → Pydantic   │
│ routes/cmds  │     │ - stacks     │     │              │     │   validated  │
│              │     │ - patterns   │     │              │     │   response   │
└──────────────┘     │ - routes     │     └──────────────┘     └──────────────┘
                     │ - relations  │
                     └──────────────┘
                            │
                            ▼
                     ┌──────────────┐
                     │ Pydantic     │
                     │ ContextIndex │
                     │ (validated)  │
                     └──────────────┘
```

## Why This Approach

### The Problem

Starting a new software product typically involves:
1. Blank documents filled inconsistently
2. No enforced completion gates — teams skip feasibility and jump to coding
3. Architecture decisions made without recorded rationale
4. Knowledge trapped in chat history or individual memory
5. No way to query "what did we decide about X?" after planning is done

### The Solution

PROGRAMSTART solves this by making the planning process itself a validated, queryable, machine-readable system:

1. **Templates with authority rules** — every concern has exactly one canonical owner document
2. **Stage gates** — you cannot advance to architecture before requirements are signed off
3. **Drift detection** — if someone changes a downstream doc without updating its authority source, the system flags it
4. **Context indexing** — all planning artifacts are indexed into a searchable corpus
5. **RAG retrieval** — ask natural language questions against your planning context and get source-cited answers
6. **Pydantic validation** — the context index and LLM responses are schema-validated, not loose JSON
7. **Knowledge base** — 49 verified technology stacks and 15 integration patterns inform stack selection decisions
8. **Bootstrapping** — scaffold new projects from a single command instead of copying and forgetting files

## Workflow Automation

This workspace now includes a durable workflow layer so the process is not kept only in chat context.

Key assets:

1. `config/process-registry.json` is the machine-readable registry for required files, stage order, metadata rules, source-of-truth sync rules, and optional attachment behavior
2. `.github/copilot-instructions.md` contains repo-wide Copilot guidance for using PROGRAMBUILD and USERJOURNEY correctly
3. `.github/instructions/` contains focused instructions for PROGRAMBUILD and USERJOURNEY work
4. `.github/agents/` contains the core PROGRAMBUILD specialist agents for discovery, architecture/security, and quality/release reviews
5. `.github/prompts/` contains reusable prompts for kickoff, next-slice planning, drift audit, and next-step summaries
6. `scripts/` contains helper scripts for bootstrap, status, validation, drift checks, and integrity refresh

`USERJOURNEY/` remains optional. It stays in this repository as a reference attachment and should only be attached to projects that truly need onboarding, consent, activation, or first-run routing planning.

## Tooling Stack

The repository includes a hardened development and automation stack:

### Core Dependencies

| Component | Purpose |
|---|---|
| Python 3.12+ | Runtime |
| Pydantic 2.x | Schema validation for context index, KB, and LLM responses |
| LiteLLM | Unified multi-provider LLM gateway (100+ providers) |
| Instructor | Pydantic-validated structured LLM output extraction |

### Development Toolchain

| Tool | Purpose |
|---|---|
| uv | Package and environment management |
| ruff | Linting and formatting (Rust speed) |
| pyright | Static type checking (basic mode) |
| pytest | Test framework (287 tests) |
| hypothesis | Property-based testing for BM25 and tokenization |
| coverage | Code coverage enforcement (≥80%) |
| pre-commit | Git hook quality gates (6 repos) |
| nox | Repeatable CI sessions |
| bandit | Security scanning |
| detect-secrets | Secret detection |
| yamllint | YAML linting |
| mkdocs-material | Documentation site |
| playwright | Browser verification and dashboard goldens |
| pip-audit | Dependency vulnerability scanning |

### Optional Components

| Extra | Packages | Purpose |
|---|---|---|
| `[rag]` | litellm, instructor, chromadb | RAG-powered context queries |
| `[vector]` | chromadb | Vector search over context index |

### Setup

```powershell
# Development setup (includes test tools, linting, hypothesis)
uv sync --extra dev
pre-commit install
python -m playwright install chromium

# Full setup with RAG capabilities
uv sync --extra dev --extra rag

# Run all quality checks
nox
nox -s ci
```

GitHub Actions mirrors the main repo checks in three layers:

1. `CI Guardrails` for PR and `main` validation
2. `Full CI Gate (Scheduled)` for nightly full-gate verification and manual dispatch
3. targeted docs, release, and weekly research workflows for the non-core lanes

Packaged install path for use outside a dev checkout:

```powershell
uv build
python -m pip install dist\programstart_workflow-*.whl
programstart help
```

The installed tool resolves the active planning workspace from the current directory. Run it from the target planning repo root, or set `PROGRAMSTART_ROOT` to point at that repo.

Unified Python CLI provides the primary entry point:

```powershell
# Planning workflow
uv run programstart init --dest <folder> --project-name <name> --product-shape "CLI tool"
uv run programstart status                          # current stage, blockers, next actions
uv run programstart validate                        # required files + metadata check
uv run programstart state show                      # inspect current workflow state
uv run programstart advance --system programbuild   # approve and advance stage
uv run programstart next                            # recommended next action
uv run programstart log                             # decision and change history
uv run programstart progress                        # checklist completion by section
uv run programstart guide --kickoff                 # files, scripts, prompts for kickoff
uv run programstart drift                           # source-of-truth drift detection
uv run programstart clean                           # remove temp artifacts
uv run programstart dashboard                       # generate STATUS_DASHBOARD.md
uv run programstart bootstrap --dest <folder> --project-name <name> --variant product
uv run programstart refresh --date 2026-03-29       # regenerate manifest + verification
uv run programstart serve                           # start dashboard HTTP server

# Context and retrieval
uv run programstart context build                   # generate context index
uv run programstart context query --concern activation
uv run programstart context query --stack fastapi
uv run programstart context query --impact USERJOURNEY/DELIVERY_GAMEPLAN.md

# Retrieval and RAG
uv run programstart-retrieval search "consent behavior"           # BM25 lexical search
uv run programstart-retrieval search "activation" --method hybrid  # hybrid BM25+vector
uv run programstart-retrieval search "release gates" --json        # JSON output
uv run programstart-retrieval validate                             # validate context index schema
uv run programstart-retrieval ask "What controls stage order?" --model gpt-4o-mini
uv run programstart-retrieval ask "What are the kill criteria?" --structured  # Pydantic-validated response

# Project factory helpers
uv run programstart recommend
uv run programstart recommend --product-shape "API service" --need rag --need durable-workflows
uv run programstart prompt-eval --json
uv run programstart impact PROGRAMBUILD/ARCHITECTURE.md
uv run programstart attach userjourney --source <path-to-userjourney-folder>

# Golden screenshot comparison
uv run python scripts/programstart_dashboard_golden.py
```

PowerShell wrapper (`scripts/pb.ps1`) remains as a thin Windows convenience layer and delegates to the unified CLI:

```powershell
pb status                          # current stage, blockers, next actions
pb validate                        # required files + metadata check
pb validate --system programbuild  # check only PROGRAMBUILD
pb state show                      # inspect current stage and phase state
pb state set --system programbuild --step feasibility --status completed --decision approved
pb advance --system programbuild   # approve the active stage and move forward
pb progress                        # checklist completion by section
pb guide --kickoff                 # files, scripts, and prompts for new-project kickoff
pb guide --system programbuild --stage feasibility
pb drift                           # source-of-truth sync check
pb clean                           # remove disposable local caches and temp artifacts
pb dashboard                       # regenerate outputs/STATUS_DASHBOARD.md
pb init --dest <folder> --project-name <name> --product-shape "CLI tool"
pb recommend
pb prompt-eval
pb impact PROGRAMBUILD/ARCHITECTURE.md
pb bootstrap --dest <folder> --project-name <name> --variant product
pb refresh --date 2026-03-29       # regenerate outputs/MANIFEST_* + VERIFICATION_REPORT_*
pb help                            # list all commands
```

Installed console script and module forms are also available:

1. `programstart status` — current stage, blockers, and next actions
2. `programstart validate --check required-files` — validate required planning files and metadata
3. `programstart state show` — inspect or update the active workflow state
4. `programstart advance --system programbuild` — approve the active step and advance
5. `programstart progress` — PROGRAMBUILD checklist completion by section
6. `programstart guide --kickoff` — authoritative files, scripts, and prompts for a step
7. `programstart drift` — source-of-truth drift detection and future-stage edit rejection
8. `programstart bootstrap --dest <folder> --project-name <name> --variant product` — scaffold a project
9. `programstart clean` — remove temp artifacts
10. `programstart refresh --date 2026-03-29` — regenerate manifest and verification report
11. `programstart dashboard` — generate `outputs/STATUS_DASHBOARD.md`
12. `programstart context build` — generate structured context index
13. `programstart context query --concern activation` — query concern ownership
14. `programstart-retrieval search "query"` — BM25 lexical search over context index
15. `programstart-retrieval search "query" --method hybrid` — hybrid BM25 + vector search
16. `programstart-retrieval validate` — validate context index against Pydantic schema
17. `programstart-retrieval ask "question"` — RAG-powered question answering via LiteLLM
18. `programstart-retrieval ask "question" --structured` — Pydantic-validated structured RAG response via Instructor
19. `programstart init --dest <folder> --project-name <name> --product-shape <shape>` — bootstrap and stamp a new planning repo
20. `programstart attach userjourney --source <path>` — attach the optional USERJOURNEY package later
21. `programstart recommend` — recommend the workflow variant and stack direction from project inputs
22. `programstart impact <target>` — inspect related documents, concerns, relations, commands, and routes
23. `programstart prompt-eval --json` — score generated prompts and factory plans against fixed scenarios

VS Code tasks are provided in `.vscode/tasks.json` so the default editor task runner can drive the hardened workflow without remembering commands.

Additional automated guardrails now check authority-doc sync and unresolved planning references:

1. `uv run programstart validate --check authority-sync` verifies the canonical docs, file index, sync rules, and workflow guidance still match the machine registry
2. `uv run programstart validate --check planning-references` scans USERJOURNEY planning docs for missing workspace paths and rejects non-allowlisted external implementation references

Integrity baselines are now registry-driven rather than hardcoded inside the script layer:

1. `uv run programstart refresh --date 2026-03-27` reads its snapshot and attachment manifest rules from `config/process-registry.json`
2. `USERJOURNEY/USERJOURNEY_INTEGRITY_REFERENCE.json` declares the attached package source plus the explicit external implementation paths the planning docs are allowed to mention
3. manifest collection is also scoped from the registry so temp, generated, and previously emitted integrity artifacts do not inflate the tracked file inventory
4. generated dashboards, manifests, and verification reports now default to `outputs/` instead of cluttering the repository root
5. Playwright screenshot goldens now cover the top dashboard shell in attached and PROGRAMBUILD-only modes, plus the attached signoff modal
6. `programstart create` now emits a runnable starter scaffold under `starter/` in addition to the planning package and factory plan
7. `programstart prompt-eval` provides a deterministic harness for generated prompt and factory-plan quality checks

## Safety Notes

1. the original flat exports were copied into `BACKUPS/2026-03-27_pre-structure_flat_export_snapshot/` before any moves were made
2. the full USERJOURNEY package was copied from the Resume Creator V6 source workspace into `USERJOURNEY/` as a project attachment, not as a reusable template
3. this workspace is organized non-destructively around preserved copies, not a single fragile export
