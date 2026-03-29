# Knowledge Base

PROGRAMSTART includes a research-backed stack knowledge base so new program plans can start from verified platform patterns instead of generic stack folklore.

## What This Adds

The knowledge base is intentionally opinionated.

It does not try to list every framework. It captures a practical working set of stacks, platform layers, and integration patterns that repeatedly matter when scoping new products:

- frontend delivery choices
- backend API and web framework choices
- data ownership and ORM strategy
- background work and durable workflow orchestration
- container and platform operations
- observability and browser verification
- retrieval and hybrid knowledge system patterns
- LLM integration, embeddings, and function calling
- agentic frameworks and stateful multi-step workflows
- ML model inference and fine-tuning
- vector databases and hybrid search architecture
- data processing and analytical query engines
- infrastructure as code and BaaS platforms
- data validation and schema enforcement
- code quality tooling and CI/CD automation
- API security threat modeling

The machine-readable source lives in `config/knowledge-base.json` and is indexed into the context layer.

The KB now stores five distinct kinds of decision material instead of flattening everything into stack blurbs:

- stacks and integration patterns for baseline platform selection
- decision rules for recurring architecture choices
- explicit relationships such as `complements`, `alternative_to`, and `supersedes_for_new_work`
- structured comparisons for version deltas and migration decisions
- a research ledger that defines how weekly deep-research updates should be run and recorded

## How PROGRAMSTART Uses the Knowledge Base

The KB is not just reference material — it is an active part of the PROGRAMSTART retrieval pipeline:

1. **Context Indexing**: `programstart context build` includes KB stacks and integration patterns in the context index, making them searchable alongside planning documents
2. **BM25 Search**: `programstart-retrieval search "async Python API"` finds relevant stacks by name, alias, capability, or best-for description
3. **RAG Queries**: `programstart-retrieval ask "What stack should I use for durable workflows?"` retrieves KB entries as context and generates source-cited answers via LiteLLM + Instructor
4. **Schema Validation**: `programstart-retrieval validate` verifies the KB conforms to the Pydantic `KnowledgeBase` model with typed submodels for stacks, rules, relations, comparisons, and retrieval guidance

## Knowledge Layers

Use the KB in this order:

1. facts and stack baselines
2. decision rules
3. explicit associations and alternatives
4. version or platform comparisons
5. weekly research deltas

That separation matters. Facts answer what something is. Rules answer when to choose it. Relations answer what it complements or replaces. Comparisons answer what changed. Research deltas answer whether the recommendation should move.

### Active Integrations in PROGRAMSTART

| Integration | How it's used | Module |
|---|---|---|
| **Pydantic** | `ContextIndex`, `KnowledgeBase`, `StackEntry`, `RAGQueryResponse` models validate all structured data | `scripts/programstart_models.py` |
| **LiteLLM** | Unified LLM gateway for RAG `ask` command — supports OpenAI, Anthropic, and 100+ other providers | `scripts/programstart_retrieval.py` |
| **Instructor** | Pydantic-validated structured extraction from LLM responses with auto-retry | `scripts/programstart_retrieval.py` |
| **Hypothesis** | Property-based testing for BM25 scoring, tokenization, and corpus building | `tests/test_hypothesis_retrieval.py` |
| **ChromaDB** | Optional vector store for hybrid BM25+embedding search | `scripts/programstart_retrieval.py` |

## Research Method

The entries were synthesized from official documentation rather than community rankings or tutorial blogs. That keeps the KB closer to each tool's actual operating model and constraints.

The synthesis is still critical rather than promotional. Official docs are useful for capabilities, but they understate migration cost, operational overhead, and architectural misuse. This KB adds those tradeoffs explicitly.

Weekly deep-research is the right follow-on only if it stays delta-oriented. The KB now includes a `research_ledger` section so each recurring review produces a bounded output: what changed, whether the recommendation changed, what evidence supports that, and what confidence level applies.

## Decision Rules

Use these heuristics before picking a stack:

1. Choose the system of record first.
2. Choose the workflow durability model second.
3. Choose the frontend delivery model third.
4. Only then choose build tools, ORM flavor, and deployment substrate.

That ordering avoids a common failure mode where teams pick a frontend framework first and then distort backend, data, and workflow architecture around it.

## Stack Matrix

| Stack | Best fit | Strongest advantage | Main risk if misused |
| --- | --- | --- | --- |
| React | rich interactive UI | stable component model | not a full architecture by itself |
| Vite | SPA and frontend-heavy apps | fast local iteration | no backend or routing opinion |
| Next.js | SSR/BFF web products | route-level full-stack integration | complexity if rendering and data boundaries blur |
| Django | admin-heavy business systems | batteries-included platform | too heavy for narrow API-only services |
| FastAPI | typed Python APIs and automations | validation plus OpenAPI contract | missing batteries can become architecture drift |
| NestJS | large TypeScript services | modular structure and DI | excessive ceremony for simple apps |
| PostgreSQL | primary transactional system of record | relational integrity and mature indexing | misuse as the answer to every storage problem |
| SQLAlchemy | Python relational access | precise query and transaction control | inconsistent session/query patterns |
| Prisma | TypeScript schema-first data access | generated type-safe client | abstraction can hide query cost |
| Redis | cache and broker-adjacent workloads | low-latency data structures | storing canonical truth in ephemeral patterns |
| Celery | conventional Python background jobs | simple async job scaling | long workflows become opaque task chains |
| Temporal | durable business workflows | explicit replayable workflow state | higher conceptual and operational overhead |
| Docker | portable packaging | environment parity and deploy artifact standardization | packaging without platform discipline |
| Kubernetes | platform-scale orchestration | resilient rollout and scaling substrate | overbuilding for small products |
| OpenTelemetry | cross-system observability | vendor-neutral telemetry model | noisy telemetry without naming discipline |
| Playwright | browser verification and goldens | realistic end-to-end UI coverage | brittle tests if used for everything |
| pgvector | relational plus vector retrieval | keep vectors near authoritative data | vector-only thinking replacing structure |
| LangChain | retrieval orchestration and chains | composable retrieval pipelines | over-abstraction hiding simple operations |
| OpenAI API | embeddings, completions, function calling | mature ecosystem and strict function calling mode | cost scales with token volume; vendor lock-in |
| Anthropic Claude API | long-context analysis and tool use | 200k+ context window; structured tool use | client-side tool execution responsibility |
| MCP | standardized LLM-tool integration | vendor-neutral JSON-RPC 2.0 protocol for tools, resources, prompts | protocol overhead for simple integrations |
| ChromaDB | prototyping and small-scale vector search | zero-config in-memory or persistent client | not designed for production-scale multi-tenant workloads |
| Weaviate | production vector and hybrid search | HNSW indexing, hybrid BM25+vector, reranking, multi-tenancy | operational complexity for small projects |
| LlamaIndex | RAG pipeline orchestration | 5-stage RAG framework with evaluation | abstraction layers can hide retrieval quality issues |
| Pydantic | runtime data validation and serialization | typed model validation with rich error messages | over-modeling simple data structures |
| pytest | Python test framework | fixtures, parametrize, conftest composition | fixture scope misuse can create hidden test coupling |
| Ruff | Python linting and formatting | Rust-speed linter with 800+ rules and formatter | rule churn if not pinned; opinionated defaults |
| GitHub Actions | CI/CD workflow automation | deep GitHub integration and matrix builds | script injection risk if inputs are not sanitized |
| OWASP API Security | API threat modeling reference | canonical risk taxonomy for API design reviews | checklist compliance without contextual threat modeling |
| Python Asyncio | concurrent I/O-bound services | TaskGroup structured concurrency (3.11+) | callback-style code if structured patterns aren't adopted |
| Python Typing | large Python codebases | Protocol structural subtyping, TypeGuard narrowing | over-annotating simple code; annotation creep |
| Python Dataclasses | structured domain objects | frozen/slots/kw_only for safe, fast data objects | mutable defaults and inheritance fragility |
| Python Logging | production service diagnostics | hierarchical logger with handlers, formatters, filters | print-based debugging leaking into production |
| Hypothesis | property-based testing | automatic shrinking and counterexample discovery | slow test suites if strategies aren't bounded |
| uv | Python package and project management | 10-100x faster than pip; replaces pip+virtualenv+pyenv+pipx | ecosystem newness; some edge-case compatibility gaps |
| Prompt Engineering | LLM output quality and reliability | output contracts, verification loops, structured reasoning | prompt complexity becoming unmaintainable without version control |
| OWASP Authentication | identity and credential security | password policy, MFA (99.9% attack reduction), JWT validation | checklist compliance without threat-model context |
| OWASP REST Security | REST API hardening | HTTP method restriction, CORS, security headers, input validation | over-restricting legitimate use while missing actual threats |
| LangGraph | stateful multi-step agents | durable execution with checkpointing and human-in-the-loop gates | graph topology complexity without observability tooling |
| Instructor | structured LLM output extraction | Pydantic-validated extraction with auto-retry across 15+ providers | debugging multi-retry loops when schema violations are systematic |
| LiteLLM | unified LLM gateway | single interface for 100+ providers with fallback Router and cost tracking | proxy server maintenance complexity for teams without DevOps capacity |
| Google Gemini API | long-context and multimodal LLM tasks | million-token context, built-in Search/URL/Code tools, OpenAI-compatible | Google infrastructure dependency; long-context cost needs upfront modeling |
| Hugging Face Transformers | open-weight model loading and fine-tuning | 1M+ Hub checkpoints, Pipeline class, Trainer for fine-tuning | GPU memory and license management complexity |
| Qdrant | production vector search at scale | HNSW with quantization, multi-tenancy, named vectors, distributed deployment | HNSW memory requirements; self-hosting maintenance |
| Polars | high-throughput DataFrame processing | Rust-speed with lazy evaluation, streaming, and Arrow-native zero-copy | pandas ecosystem incompatibility; lazy API debugging overhead |
| DuckDB | embedded SQL analytics over files | in-process columnar OLAP; reads Parquet/CSV/Arrow without a server | single-writer model; not for OLTP or shared multi-service access |
| Terraform | multi-cloud infrastructure as code | Write/Plan/Apply with drift detection; thousands of providers via Registry | state file sensitivity; declarative model resists imperative logic |
| Supabase | full-stack BaaS with PostgreSQL core | Auth + Realtime + Storage + pgvector + Queues + Cron in one service | vendor lock-in on Auth/Storage APIs; self-hosting complexity |
| pre-commit | automated git hook quality gates | multi-language hook runner with revision-pinned .pre-commit-config.yaml | per-commit latency if slow hooks are not moved to pre-push |
| mypy | Python static type checking | --strict mode, Protocol, TypeGuard, incremental mode, mypy daemon | annotation investment on untyped codebases; some dynamic patterns resist analysis |

## Recommended Archetypes

### 1. Business Web Platform

Use when the product is workflow-heavy, admin-heavy, and data-governed.

- default stack: Django + PostgreSQL + Redis + Celery + Playwright
- reason: the product benefits from coherent ownership of data, admin, auth, forms, and operational tasks
- warning: do not split into services early unless deployment or team boundaries truly require it

### 2. API And Automation Platform

Use when the main product value lives in APIs, automations, or typed service contracts.

- default stack: FastAPI + PostgreSQL + SQLAlchemy + Redis + Celery + OpenTelemetry
- reason: it gives strong contracts without forcing server-rendered assumptions
- warning: move durable or human-waiting processes to Temporal instead of stretching task queues too far

### 3. TypeScript Full-Stack Web Product

Use when SSR, route-level rendering, and backend-for-frontend behavior are product-critical.

- default stack: Next.js + PostgreSQL + Prisma + Playwright + OpenTelemetry
- reason: rendering, auth, and route-bound data loading can be designed together
- warning: define cache, mutation, and service boundaries early or the stack becomes hard to reason about

### 4. Durable Workflow Product

Use when the process itself is the product surface.

- default stack: FastAPI or NestJS + Temporal + PostgreSQL + OpenTelemetry
- reason: workflow state, retries, timers, and human waits become explicit and operable
- warning: do not hide long-running state transitions in conventional background queues

### 5. Hybrid Knowledge System

Use when the product needs authoritative knowledge retrieval rather than only semantic similarity.

- default stack: PostgreSQL + pgvector + structured metadata and relations + optional LangChain-style retrieval orchestration
- reason: structured ownership and dependency edges stay authoritative while lexical and vector layers rank results
- warning: embeddings should rank and augment; they should not decide authority

### 6. LLM-Powered Agent Platform

Use when the product surface requires tool-calling LLM agents, function execution, or conversational automation.

- default stack: FastAPI + OpenAI API or Anthropic Claude API + MCP + Pydantic + PostgreSQL + OpenTelemetry
- reason: typed function calling with strict mode gives deterministic tool dispatch; MCP standardizes tool integration; Pydantic validates all LLM outputs before execution
- warning: always validate LLM-generated arguments through schemas; never execute unvalidated tool calls; instrument every agent step for observability

### 7. RAG Pipeline With Evaluation

Use when the product needs grounded answers from a curated knowledge corpus rather than raw LLM generation.

- default stack: LlamaIndex or LangChain + ChromaDB or Weaviate or pgvector + OpenAI API embeddings + Pydantic + pytest
- reason: separates the five RAG stages (loading, indexing, storing, querying, evaluation) so each can be measured and tuned independently
- warning: measure retrieval quality (recall@k, precision@k) separately from generation quality (faithfulness, relevance); do not skip evaluation

### 8. Python CI/CD Quality Pipeline

Use when the project needs automated linting, formatting, type checking, and test enforcement on every commit.

- default stack: Ruff + pytest + GitHub Actions + Pydantic (for config validation)
- reason: Ruff replaces multiple linters with a single Rust-speed tool; GitHub Actions matrix builds catch cross-version issues; pytest fixtures provide clean test composition
- warning: pin Ruff version and rule set to avoid churn; use conftest.py for shared fixtures to prevent duplication

### 9. Security-Hardened API Service

Use when the API handles sensitive data, financial transactions, or regulated workloads.

- default stack: FastAPI + PostgreSQL + SQLAlchemy + Pydantic + OWASP API Security checklist + OWASP Authentication + OWASP REST Security + OpenTelemetry + GitHub Actions (with OIDC and Dependabot)
- reason: Pydantic validates all input boundaries; OWASP provides structured threat review; OIDC eliminates long-lived secrets; Dependabot automates vulnerability patching; OWASP Authentication enforces MFA and credential hygiene; OWASP REST Security hardens transport and headers
- warning: OWASP is a checklist, not a security guarantee; contextual threat modeling is still required
- authentication: use Argon2id or bcrypt for password hashing; enforce MFA for admin and sensitive operations; validate JWT claims (iss, aud, exp, nbf, algorithm whitelist)
- headers: Strict-Transport-Security, X-Content-Type-Options, X-Frame-Options, Content-Security-Policy; restrict CORS origins to known domains

### 10. Async Python Microservice

Use when the service is I/O-bound, handles concurrent external calls, or uses event-driven patterns.

- default stack: FastAPI + Python Asyncio + PostgreSQL + Python Logging + Python Typing + OpenTelemetry
- reason: TaskGroup structured concurrency prevents orphaned tasks; asyncio.to_thread bridges blocking libraries without thread-pool sprawl; typed interfaces enforce contract stability
- warning: do not mix raw create_task with TaskGroup; handle CancelledError as BaseException; avoid blocking the event loop with synchronous I/O
- key patterns: use asyncio.TaskGroup for fan-out/fan-in; use asyncio.timeout for deadline enforcement; use asyncio.to_thread for CPU-bound or blocking library calls

### 11. Type-Safe Python Application

Use when the codebase is large, has multiple contributors, or requires strict domain modeling.

- default stack: Python Typing + Python Dataclasses + Pydantic + Hypothesis + pytest + Ruff
- reason: Protocol gives structural subtyping without inheritance hierarchies; frozen dataclasses enforce immutability; Hypothesis catches edge cases that example-based tests miss; Ruff enforces consistent style
- warning: do not over-annotate; use Protocol for public interfaces, not internal helpers; prefer dataclasses for internal domain models and Pydantic for external boundaries

### 12. AI Agent With Prompt Discipline

Use when the product involves LLM agents, multi-step tool calling, or autonomous decision-making.

- default stack: OpenAI API or Anthropic Claude API + Pydantic + Prompt Engineering practices + MCP + PostgreSQL + OpenTelemetry
- reason: output contracts and verification loops prevent hallucinated or incomplete outputs; structured outputs guarantee schema conformance; tool persistence rules prevent premature termination
- warning: always apply verification loops (correctness, grounding, formatting, safety) before executing high-impact actions; use reasoning effort tuning to balance quality vs cost; track tool call success rates for continuous improvement

### 13. Stateful Multi-Agent System

Use when agents must coordinate across steps, resume after failures, require human review gates, or maintain conversation state across sessions.

- default stack: LangGraph + LiteLLM + Instructor + MCP + Pydantic + PostgreSQL + OpenTelemetry
- reason: LangGraph StateGraph provides durable checkpointing and human-in-the-loop without redesigning topology; LiteLLM abstracts provider routing and cost; Instructor handles schema-validated extraction with retry; MCP standardizes tool dispatch
- warning: define state schema (TypedDict/Pydantic) and checkpointing strategy before building graphs; use subgraphs for modularity; instrument with LangSmith or OpenTelemetry before production rollout

### 14. ML Inference and Data Pipeline

Use when the product loads open-weight models, processes large datasets, or serves ML predictions alongside structured data.

- default stack: Hugging Face Transformers + Polars + DuckDB + FastAPI + OpenTelemetry
- reason: Transformers handles model loading and inference; Polars provides Rust-speed preprocessing; DuckDB enables SQL analytics over Parquet/CSV without a separate server; FastAPI serves predictions with typed contracts
- warning: pin model revision hashes in production; review Hub licenses per model; profile GPU memory before choosing quantization strategy

### 15. Full-Stack BaaS Product

Use when rapid product delivery is the priority and the team can accept PostgreSQL-as-a-service constraints.

- default stack: Supabase + Next.js or React + Pydantic + Playwright
- reason: Supabase collapses Auth + Database + Storage + Realtime + pgvector into one managed service; RLS enforces per-row access at the database layer; REST and GraphQL APIs are auto-generated
- warning: enable RLS on every table from day one; never expose service_role key to client code; define migrations in supabase/migrations/ for reproducibility

## Interaction Guidance

## Highlighted Comparison: Python 3.13 vs 3.14

The KB now tracks Python runtime deltas as a structured comparison instead of burying them in narrative notes.

- **3.13** is the lower-risk target if your environment is already green there and you want to avoid runtime annotation and ecosystem surprises while still getting recent typing improvements.
- **3.14** is the stronger default for new async and tooling-heavy services once dependencies are validated, because it upgrades concurrency and operational tooling in ways that matter to platform decisions.

The practical split is:

- choose **3.13** when stability of current images, wheels, and runtime reflection behavior matters more than newer platform surfaces
- choose **3.14** when you want supported free-threaded builds, stdlib subinterpreter tooling, improved runtime observability, and you can afford an explicit compatibility pass

The comparison entry is intentionally decision-oriented. It does not just list features. It records concurrency impact, typing/runtime impact, tooling/ops implications, and migration risk so PROGRAMSTART can keep making a recommendation rather than only archiving notes.

### Frontend with backend

- Use SPA plus API when frontend and backend should deploy independently.
- Use SSR/BFF when route rendering, auth, and data composition belong in one surface.
- Avoid mixing both models accidentally inside one codebase without explicit boundaries.

### API with jobs and workflows

- Use task queues for finite background work.
- Use durable workflows for long-running, retry-heavy, stateful business processes.
- Keep request handlers thin even when async frameworks are available.

### Data with retrieval

- Keep canonical truth in relational structures first.
- Add full-text and vector search as retrieval layers, not as replacements for authority and schema.
- Prefer hybrid search over vector-only search when the system must respect ownership, compliance, or execution order.

### Packaging with orchestration

- Docker is the packaging boundary.
- Kubernetes is the operations substrate.
- Do not adopt the second just because the first exists.

### Testing with observability

- Use Playwright to prove critical user flows and UI contracts.
- Use OpenTelemetry to explain failures across services, jobs, and workflows.
- Browser tests tell you that something failed; telemetry helps tell you why.

### LLM integration with validation

- Use strict function calling (OpenAI) or strict tool use (Anthropic) to constrain LLM outputs to valid schemas.
- Validate all LLM-generated arguments through Pydantic models before executing tool calls.
- Use MCP when integrating multiple tool providers; it standardizes discovery, invocation, and error handling.
- Optimize in order: prompt engineering first, then evaluation harness, then RAG retrieval tuning, then fine-tuning only if needed.
- Apply output contracts (exact sections, order, length, format) to control LLM response structure.
- Use verification loops (correctness, grounding, formatting, safety) before finalizing high-impact LLM actions.
- For function calling: keep under 20 tools per turn; use namespaces to group related tools; use tool search for large surfaces.
- Handle the agentic loop: check stop_reason for tool_use (Anthropic) or tool_calls (OpenAI), execute, return result, repeat until complete.

### Prompt engineering with structured outputs

- Use structured outputs (response_format with JSON Schema) when the output must conform to a known schema.
- Prefer Pydantic model definitions as the source of truth for response schemas.
- Use completeness contracts: track deliverables internally, mark blocked items with reason, confirm full coverage before finishing.
- Apply reasoning effort tuning: use low effort for execution-heavy tasks, high effort for research-heavy tasks; add prompt structure before raising effort.
- For empty results: do not conclude immediately; retry with alternate query wording, broader filters, prerequisite lookup, or alternate source.
- Only cite retrieved sources; never fabricate citations, URLs, or IDs.

### Async Python with structured concurrency

- Use asyncio.TaskGroup (Python 3.11+) for fan-out/fan-in; it automatically cancels siblings on first failure.
- Use asyncio.to_thread for blocking I/O (file ops, sync libraries) to avoid blocking the event loop.
- Use asyncio.timeout (Python 3.11+) for deadline enforcement instead of manual timer patterns.
- Handle CancelledError as BaseException, not Exception; catching Exception will not catch it.
- Use eager_task_factory (Python 3.12+) for latency-critical synchronous-looking coroutines.
- Use logger = logging.getLogger(__name__) per module; never use the root logger in library code.

### Type safety with Python typing

- Use Protocol for structural subtyping at public interfaces; prefer over ABC when implementation inheritance isn't needed.
- Use TypeGuard (3.10+) or TypeIs (3.12+) for type narrowing in conditional checks.
- Use frozen=True and slots=True on dataclasses for immutable, memory-efficient domain objects.
- Use NewType for domain-specific string/int wrappers (UserId, EmailAddress) to prevent type confusion.
- Use Pydantic for external boundary validation; use dataclasses for internal domain models.

### Vector search with structured authority

- Use ChromaDB for prototyping and small-scale experiments with automatic embedding.
- Use pgvector when vectors must live alongside relational data in PostgreSQL.
- Use Weaviate for production-scale hybrid search with HNSW indexing, reranking, and multi-tenancy.
- Always pair vector search with structured metadata filtering; pure semantic similarity is insufficient for authority-sensitive workloads.
- Prefer hybrid search (BM25 + vector) over vector-only when exact terms matter (code, config keys, error messages).

### Code quality with automation

- Use Ruff as the single linter and formatter; pin the version and rule set in pyproject.toml.
- Use pre-commit to enforce Ruff, trailing-whitespace, check-yaml, and detect-secrets on every commit.
- Use mypy with per-module strictness config; add to pre-commit at stages: [pre-push] to avoid per-commit latency.
- Use pytest fixtures with appropriate scopes (function, class, module, session) to avoid hidden test coupling.
- Use conftest.py at each test directory level for shared fixtures.
- Use GitHub Actions with OIDC for secret-free CI; enable Dependabot for dependency vulnerability monitoring.
- Sanitize all GitHub Actions inputs used in run blocks to prevent script injection.

### Agentic systems with LangGraph

- Use LangGraph StateGraph for any workflow with loops, conditional branching, or durable state.
- Define state as TypedDict or Pydantic model; use message reducers for accumulation patterns.
- Use interrupt_before/interrupt_after for human review gates; do not redesign graph topology for oversight.
- Use MemorySaver in development; switch to PostgreSQL or Redis checkpointer for production persistence.
- Use LiteLLM as the model-agnostic backend; swap providers without touching graph logic.
- Instrument with LangSmith or OpenTelemetry before production; agent graph traversal is hard to debug from logs alone.

### Multi-provider LLM with LiteLLM

- Use litellm.Router with retry and fallback policies instead of direct provider SDK calls in multi-provider setups.
- Set consistent model strings: 'provider/model-name' (e.g., 'openai/gpt-4o', 'anthropic/claude-3-5-sonnet-20241022').
- Use virtual keys in the Proxy Server for team isolation and per-team budget enforcement.
- Hook success_callback and failure_callback into Langfuse or OpenTelemetry for cost and latency observability.
- Combine LiteLLM with Instructor for schema-validated structured extraction across all providers.

### Data processing with Polars and DuckDB

- Use Polars lazy API (scan_csv, scan_parquet) for large DataFrame pipelines; defer .collect() to the end.
- Use DuckDB for SQL-first analytics over files and DataFrames; avoids setting up a separate database server.
- Combine both: use Polars for DataFrame transformations, DuckDB for complex SQL aggregations and joins.
- Use streaming=True in Polars .collect() for datasets that exceed available RAM.
- Use duckdb.sql('SELECT * FROM df') to query Polars DataFrames directly by Python variable name.

## KB And The Context Layer

The KB is not a separate knowledge silo. It is folded into the context layer so stack guidance can be queried next to authority docs, routes, commands, and workflow relations.

Current useful queries:

```powershell
uv run programstart context query --stack fastapi
uv run programstart context query --capability durable-workflows
uv run programstart context query --impact USERJOURNEY/DELIVERY_GAMEPLAN.md
```

## Source Anchors

- https://react.dev/learn
- https://vite.dev/guide/
- https://nextjs.org/docs/app/getting-started/project-structure
- https://fastapi.tiangolo.com/
- https://docs.djangoproject.com/en/stable/
- https://docs.nestjs.com/
- https://www.postgresql.org/docs/current/
- https://docs.sqlalchemy.org/en/20/orm/quickstart.html
- https://www.prisma.io/docs/orm/overview/introduction/what-is-prisma
- https://docs.celeryq.dev/en/stable/getting-started/introduction.html
- https://redis.io/docs/latest/
- https://docs.temporal.io/workflow-execution
- https://docs.docker.com/get-started/docker-overview/
- https://kubernetes.io/docs/concepts/overview/
- https://opentelemetry.io/docs/what-is-opentelemetry/
- https://playwright.dev/python/docs/intro
- https://github.com/pgvector/pgvector
- https://docs.langchain.com/oss/python/langchain/retrieval
- https://platform.openai.com/docs/guides/embeddings
- https://platform.openai.com/docs/guides/function-calling
- https://platform.openai.com/docs/guides/prompt-engineering
- https://docs.anthropic.com/en/docs/build-with-claude/tool-use
- https://modelcontextprotocol.io/docs/concepts/architecture
- https://docs.trychroma.com/docs/overview/getting-started
- https://docs.weaviate.io/weaviate/concepts/search
- https://docs.llamaindex.ai/en/stable/understanding/rag/
- https://docs.pydantic.dev/latest/concepts/models/
- https://docs.pytest.org/en/stable/how-to/fixtures.html
- https://docs.astral.sh/ruff/configuration/
- https://docs.github.com/en/actions/security-for-github-actions/security-hardening-for-github-actions
- https://owasp.org/API-Security/editions/2023/en/0x11-t10/
- https://docs.python.org/3/library/asyncio.html
- https://docs.python.org/3/library/typing.html
- https://docs.python.org/3/library/dataclasses.html
- https://docs.python.org/3/library/logging.html
- https://hypothesis.readthedocs.io/en/latest/quickstart.html
- https://docs.astral.sh/uv/
- https://developers.openai.com/docs/guides/function-calling
- https://developers.openai.com/docs/guides/structured-outputs
- https://developers.openai.com/docs/guides/prompt-guidance
- https://platform.claude.com/docs/en/docs/build-with-claude/tool-use
- https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html
- https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html
- https://raw.githubusercontent.com/langchain-ai/langgraph/refs/heads/main/README.md
- https://docs.langchain.com/oss/python/langgraph/overview
- https://python.useinstructor.com/
- https://docs.litellm.ai/docs/
- https://ai.google.dev/gemini-api/docs
- https://huggingface.co/docs/transformers/index
- https://qdrant.tech/documentation/
- https://qdrant.tech/documentation/quickstart/
- https://docs.pola.rs/
- https://duckdb.org/docs/
- https://developer.hashicorp.com/terraform/intro
- https://supabase.com/docs
- https://pre-commit.com/
- https://mypy.readthedocs.io/en/stable/