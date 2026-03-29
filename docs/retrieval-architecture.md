# Retrieval Architecture

PROGRAMSTART provides a 3-layer retrieval system that progressively adds retrieval sophistication on top of the structured context index.

## Design Principles

1. Each layer is independently useful and testable.
2. Layer 1 has zero external dependencies. Layers 2 and 3 require optional packages.
3. Structured authority always outranks similarity-based ranking.
4. All layers operate over the same context index built by `programstart context build`.

## Layer 1 — Lexical Search

**Dependencies:** None (pure Python, stdlib only).

Provides BM25-scored full-text search across every searchable surface in the context index:

- Document paths, titles, headings, purposes, and owners
- Concern names, owner files, and supporting files
- Knowledge base stack names, aliases, capabilities, strengths, risks, and best-for
- Integration pattern names, components, fit-for, and notes
- Retrieval guidance principles and recommendations
- Dashboard routes and their purposes
- CLI and dashboard command names

### How it works

1. **Corpus construction**: At init, the searcher walks the context index and creates one `Chunk` per searchable entity. Each chunk has a `source_type`, `source_id`, and `text` field.
2. **Tokenization**: Whitespace + punctuation split, lowercased, with simple stop-word removal.
3. **Inverted index**: Term → set of chunk IDs for fast lookup.
4. **BM25 scoring**: Standard Okapi BM25 with k1=1.5, b=0.75. Scores are computed per-query-term and summed.
5. **Result ranking**: Chunks are sorted by descending BM25 score and returned with metadata.

### CLI

```powershell
uv run programstart retrieval search "consent activation"
uv run programstart retrieval search "durable workflow" --top-k 5
```

## Layer 2 — Hybrid Lexical + Vector Search

**Dependencies:** `chromadb` (optional). Install with `pip install programstart-workflow[vector]`.

Adds embedding-based semantic search and blends it with BM25 scores using configurable alpha weighting.

### How it works

1. **Embedding store**: On first run, embeds all chunks using a sentence transformer (via ChromaDB's default embedder) and persists to `outputs/retrieval/chroma/`.
2. **Vector query**: The query string is embedded and the top-k nearest chunks are retrieved by cosine similarity.
3. **Score fusion**: Lexical and vector results are combined using reciprocal rank fusion (RRF) with a configurable alpha parameter (0.0 = lexical only, 1.0 = vector only, 0.5 = balanced).
4. **Deduplication**: Chunks appearing in both result sets are merged, keeping the higher fused score.

### CLI

```powershell
uv run programstart retrieval search "how does consent flow work" --method hybrid
uv run programstart retrieval search "workflow orchestration" --method hybrid --alpha 0.7
```

## Layer 3 — RAG Assistant

**Dependencies:** `litellm`, `instructor`, and optional provider credentials. Install with `pip install programstart-workflow[rag]`.

Adds LLM-powered question answering with retrieval-grounded context.

### How it works

1. **Retrieval**: Uses the hybrid searcher (Layer 2) or lexical searcher (Layer 1) to find the top-k most relevant chunks.
2. **Prompt composition**: Retrieval results are formatted as structured context and inserted into a system prompt that instructs the LLM to answer only from provided context.
3. **Generation**: LiteLLM routes the prompt to the configured provider/model.
4. **Structured validation**: Instructor can enforce the `RAGQueryResponse` schema for structured answers.
5. **Response**: The answer is returned alongside the source chunks used for grounding.

### CLI

```powershell
uv run programstart retrieval ask "who owns consent behavior?"
uv run programstart retrieval ask "what stage gates exist in PROGRAMBUILD?" --model gpt-4o-mini
uv run programstart retrieval ask "what changed downstream of ARCHITECTURE?" --structured
```

## Data Flow

```
context-index.json
       │
       ▼
┌─────────────────┐
│  Corpus Builder  │  ← Walks index, creates Chunk per entity
└────────┬────────┘
         │
         ▼
┌─────────────────┐     ┌──────────────────┐
│  BM25 Searcher  │────▶│  Lexical Results  │  Layer 1
└────────┬────────┘     └──────────────────┘
         │
         ▼
┌─────────────────┐     ┌──────────────────┐
│ Embedding Store │────▶│  Vector Results   │  Layer 2
└────────┬────────┘     └──────────────────┘
         │
         ▼
┌─────────────────┐     ┌──────────────────┐
│  Score Fusion   │────▶│  Hybrid Results   │  Layer 2
└────────┬────────┘     └──────────────────┘
         │
         ▼
┌─────────────────┐     ┌──────────────────┐
│  LLM Generator  │────▶│  Grounded Answer  │  Layer 3
└─────────────────┘     └──────────────────┘
```

## Configuration

| Setting | Environment Variable | Default |
| --- | --- | --- |
| Embedding store path | `PROGRAMSTART_CHROMA_PATH` | `outputs/retrieval/chroma/` |
| Provider credentials | provider-specific env vars via LiteLLM | (none) |
| Default LLM model | `PROGRAMSTART_LLM_MODEL` | `gpt-4o-mini` |
| Default search method | `PROGRAMSTART_SEARCH_METHOD` | `lexical` |
| Hybrid alpha | `PROGRAMSTART_HYBRID_ALPHA` | `0.5` |
| Top-k results | `PROGRAMSTART_TOP_K` | `10` |

## Integration With Existing Context Layer

The retrieval module imports and builds on top of `programstart_context.py`:

- Uses `build_context_index()` or loads a cached index from `outputs/context/context-index.json`
- All searchable content comes from the same authoritative sources (registry, documents, KB)
- Results link back to document paths, concern names, and stack entries from the context index

## File Layout

```
scripts/
  programstart_retrieval.py    ← retrieval engine (all 3 layers)
docs/
  retrieval-architecture.md    ← this document
config/
  knowledge-base.json          ← retrieval_guidance section informs behavior
```
