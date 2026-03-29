# ARCHITECTURE.md

Purpose: System boundaries, contracts, data ownership, auth model, and technical decisions.
Owner: Audit Owner
Last updated: 2026-03-29
Depends on: REQUIREMENTS.md, USER_FLOWS.md, RESEARCH_SUMMARY.md
Authority: Canonical for technical architecture

---

## System Topology

PROGRAMSTART is a CLI-driven planning automation tool. It has no server, no deployed service, and no end-user auth. It runs locally on the operator's machine and works on local filesystem planning repositories.

```
┌───────────────────────────────────────────────────────────────────────┐
│                     OPERATOR'S LOCAL MACHINE                         │
├───────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ┌─────────────────┐   ┌──────────────────┐   ┌────────────────────┐ │
│  │  CLI Entry Point│──▶│  Script Modules  │──▶│  Planning Docs     │ │
│  │  programstart   │   │  (scripts/*.py)  │   │  (PROGRAMBUILD/,   │ │
│  │                 │   │                  │   │   USERJOURNEY/,     │ │
│  └─────────────────┘   │  ┌────────────┐  │   │   config/)         │ │
│                        │  │ Models     │  │   └────────────────────┘ │
│                        │  │ (Pydantic) │  │                          │
│  ┌─────────────────┐   │  └────────────┘  │   ┌────────────────────┐ │
│  │  Dashboard      │──▶│  ┌────────────┐  │──▶│  Generated Outputs │ │
│  │  HTTP Server    │   │  │ Retrieval  │  │   │  (outputs/)        │ │
│  │  (localhost)    │   │  │ BM25+RAG   │  │   │  context-index.json│ │
│  └─────────────────┘   │  └────────────┘  │   │  STATUS_DASHBOARD  │ │
│                        └──────────────────┘   └────────────────────┘ │
│                                                                       │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │  Optional External: LLM API (OpenAI/Anthropic/etc via LiteLLM)│  │
│  │  Only used when 'programstart-retrieval ask' is invoked        │  │
│  └─────────────────────────────────────────────────────────────────┘  │
│                                                                       │
└───────────────────────────────────────────────────────────────────────┘
```

## PRODUCT_SHAPE Checklist

| PRODUCT_SHAPE | Architecture focus |
|---|---|
| CLI tool | command surface, config/loading order, exit codes, local file/system effects, non-interactive invocation |

## Technology Decision Table

| Tier | Choice | Alternatives | Reason |
|---|---|---|---|
| Language | Python 3.12+ | N/A | Rich ecosystem for CLI, text processing, and ML integrations |
| Package management | uv | pip, poetry | 10-100x faster, replaces pip+virtualenv+pyenv |
| Data validation | Pydantic 2.x | dataclasses, attrs | Validated context index and LLM response schemas at runtime |
| LLM gateway | LiteLLM | direct OpenAI/Anthropic SDKs | Single interface for 100+ providers with fallback routing |
| Structured extraction | Instructor | manual JSON parsing | Pydantic-validated LLM outputs with auto-retry |
| Lexical search | BM25 (built-in) | Whoosh, Elasticsearch | Zero-dependency, appropriate for planning corpus size |
| Vector search | ChromaDB (optional) | pgvector, Weaviate | Simple persistent client for local use |
| Testing | pytest + Hypothesis | unittest | Property-based testing catches edge cases in BM25 math |
| Linting | Ruff | flake8, pylint | Rust-speed, single tool for lint + format |
| Type checking | pyright | mypy | Faster, VS Code native integration |
| Build | setuptools | flit, hatch | Standard, stable packaging backend |

## Data Model And Ownership

| Entity | Owner | Key fields | Access notes |
|---|---|---|---|
| process-registry.json | config/ | systems, stage_order, sync_rules | Machine-readable workflow rules |
| knowledge-base.json | config/ | stacks, integration_patterns, retrieval_guidance | 49 stacks, 15 patterns |
| context-index.json | outputs/context/ | documents, concerns, knowledge_base, routes, relations | Generated, validated via Pydantic ContextIndex |
| workflow state files | outputs/state/ | active_stage, steps, decisions | Per-system stage tracking |
| ContextIndex (Pydantic) | scripts/programstart_models.py | All fields from context-index.json | Typed validation layer |
| RAGQueryResponse (Pydantic) | scripts/programstart_models.py | answer, reasoning, confidence, cited_sources | Structured LLM response model |
| Chunk (dataclass) | scripts/programstart_retrieval.py | source_type, source_id, text, metadata | Searchable unit in BM25 index |
| SearchResult (dataclass) | scripts/programstart_retrieval.py | source_type, source_id, text, score, metadata | Scored search result |

## Command Surface

| Command | Module | Purpose |
|---|---|---|
| programstart | programstart_cli | Unified CLI with subcommands |
| programstart-retrieval search | programstart_retrieval | BM25/hybrid/vector search |
| programstart-retrieval ask | programstart_retrieval | RAG question answering |
| programstart-retrieval validate | programstart_retrieval | Pydantic schema validation |
| programstart-context | programstart_context | Context index build |
| programstart-bootstrap | programstart_bootstrap | Project scaffolding |
| programstart-validate | programstart_validate | Planning file checks |
| programstart-status | programstart_status | Stage and blocker summary |
| programstart-workflow | programstart_workflow_state | State inspection/advancement |
| programstart-drift | programstart_drift_check | Source-of-truth drift detection |

## Retrieval Pipeline Architecture

```
  Query
    │
    ▼
┌──────────┐    ┌──────────────┐    ┌──────────────┐    ┌─────────────────┐
│ Tokenize │───▶│ BM25 Scoring │───▶│ Top-K Ranked │───▶│  Format Context │
│ + Filter │    │ (IDF * BM25) │    │   Results    │    │  [1] source:id  │
│ StopWords│    │              │    │              │    │  [2] source:id  │
└──────────┘    └──────────────┘    └──────────────┘    └─────────────────┘
                                                               │
                                          ┌────────────────────┤
                                          │ (if --method ask)  │ (if search only)
                                          ▼                    ▼
                                   ┌──────────────┐    ┌──────────────┐
                                   │  LiteLLM     │    │  Print/JSON  │
                                   │  Completion   │    │  Output      │
                                   │              │    └──────────────┘
                                   │  ┌────────┐  │
                                   │  │Instruc-│  │
                                   │  │tor     │  │
                                   │  │(Pydant)│  │
                                   │  └────────┘  │
                                   └──────────────┘
                                          │
                                          ▼
                                   ┌──────────────┐
                                   │ RAGQuery     │
                                   │ Response     │
                                   │ (validated)  │
                                   └──────────────┘
```

## External Dependencies

| Dependency | Purpose | SLA or expectation | Fallback | Owner |
|---|---|---|---|---|
| LLM API (via LiteLLM) | RAG question answering | Optional, only for `ask` | Lexical search works without it | Operator manages API keys |
| ChromaDB | Vector search | Optional, for hybrid/vector modes | BM25 lexical-only fallback | Local installation |

## Environment Strategy

- **local**: Primary execution environment. All features work locally with `uv sync --extra dev`.
- **CI**: `nox -s ci` runs lint, typecheck, tests, validate. No LLM keys needed.
- **RAG mode**: Requires `uv sync --extra rag` and `OPENAI_API_KEY` or `ANTHROPIC_API_KEY` env var.

- logs
- metrics
- alerts
---
