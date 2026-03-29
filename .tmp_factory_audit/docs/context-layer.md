# Context Layer

PROGRAMSTART now includes a structured context layer for understanding the repository as a governed workflow system rather than as a bag of markdown files.

It also includes a research-backed stack knowledge base so future program work can start from reviewed platform patterns rather than generic stack recommendations.

## Why This Exists

This repo contains several different kinds of knowledge at once:

- machine-readable workflow structure in `config/process-registry.json`
- authority and source-of-truth rules in markdown docs
- executable command surfaces in the unified CLI
- internal dashboard routes and command actions
- live workflow state in state files

Vector search alone would help with semantic similarity, but it would not reliably answer which file is canonical, which concern depends on another file, or which routes and commands are actually implemented.

## Model

The context layer is intentionally hybrid.

### 1. Structured Facts First

The generated context index treats the registry, command surfaces, route inventory, and workflow state as hard facts.

### 2. Document Metadata Second

It then extracts titles, purpose fields, owners, authority fields, dependencies, and headings from key markdown documents.

### 3. Research-Backed Knowledge Base Third

The context index also includes a machine-readable knowledge base of stack choices, tradeoffs, integration patterns, and retrieval guidance.

### 4. Relations Across Everything

It records relations such as:

- canonical owner of a concern
- USERJOURNEY source-of-truth owner of a concern
- document dependency edges
- sync-rule authority dependencies

## CLI Surface

Build the current context index:

```powershell
uv run programstart context build
```

This writes a structured JSON bundle to:

```text
outputs/context/context-index.json
```

Query the current index or build one in memory if it does not exist yet:

```powershell
uv run programstart context query
uv run programstart context query --concern activation
uv run programstart context query --file USERJOURNEY/ROUTE_AND_STATE_FREEZE.md
uv run programstart context query --command guide
uv run programstart context query --route /api/workflow-advance
uv run programstart context query --stack fastapi
uv run programstart context query --capability durable-workflows
uv run programstart context query --impact USERJOURNEY/DELIVERY_GAMEPLAN.md
```

## What The Index Contains

The generated context index currently includes:

- workspace metadata
- system definitions from the process registry
- current runtime workflow state
- key document metadata from PROGRAMBUILD, USERJOURNEY, and docs pages
- stack and integration guidance from `config/knowledge-base.json`
- concern ownership extracted from authority tables
- CLI commands and dashboard command keys
- dashboard route inventory
- relation edges between documents, concerns, and sync rules

## Current Boundaries

This is a structured context index, not a full semantic knowledge engine.

It does not yet include:

- embeddings or vector retrieval
- graph database storage
- historical change lineage across git history
- section-level semantic ranking

## Current Recommendation

The current model is now strong enough to support practical stack guidance and impact lookup without a semantic layer.

Natural next steps after this phase are:

- add lexical retrieval over the generated index for section-level ranking
- add optional semantic retrieval only after authority ranking rules stay explicit
- surface stack and impact lookups in the dashboard if they prove useful in daily planning work
