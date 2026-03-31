from __future__ import annotations

# ruff: noqa: I001

import argparse
import json
import math
import os
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, cast

try:
    from .programstart_common import (
        generated_outputs_root,
        warn_direct_script_invocation,
        workspace_path,
    )
    from .programstart_context import build_context_index, default_index_path
    from .programstart_models import ContextIndex, RAGQueryResponse
except ImportError:  # pragma: no cover - standalone script execution fallback
    from programstart_common import (
        generated_outputs_root,
        warn_direct_script_invocation,
        workspace_path,
    )
    from programstart_context import build_context_index, default_index_path
    from programstart_models import ContextIndex, RAGQueryResponse


# ---------------------------------------------------------------------------
# Stop words — minimal set to improve BM25 precision
# ---------------------------------------------------------------------------

_STOP_WORDS: frozenset[str] = frozenset("a an and are as at be by for from has have in is it of on or the to was with".split())

_TOKEN_RE = re.compile(r"[a-z0-9_]+")


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Chunk:
    """A searchable unit extracted from the context index."""

    source_type: str  # document, concern, stack, pattern, guidance, route, command
    source_id: str  # unique within source_type
    text: str  # searchable content
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class SearchResult:
    """A scored search result."""

    source_type: str
    source_id: str
    text: str
    score: float
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class RAGResponse:
    """A retrieval-augmented generation response."""

    answer: str
    sources: list[SearchResult]
    model: str
    retrieval_method: str


# ---------------------------------------------------------------------------
# Corpus builder — walks context index to create chunks
# ---------------------------------------------------------------------------


def build_corpus(index: dict[str, Any]) -> list[Chunk]:
    """Extract searchable chunks from a context index."""
    chunks: list[Chunk] = []

    # Documents
    for doc in index.get("documents", []):
        parts = [doc.get("path", ""), doc.get("title", ""), doc.get("purpose", "") or ""]
        if doc.get("owner"):
            parts.append(doc["owner"])
        parts.extend(doc.get("headings", []))
        chunks.append(
            Chunk(
                source_type="document",
                source_id=doc["path"],
                text=" ".join(parts),
                metadata={"path": doc["path"], "title": doc.get("title", ""), "owner": doc.get("owner")},
            )
        )

    # Concerns
    for concern in index.get("concerns", []):
        parts = [concern.get("concern", ""), concern.get("owner_file", "")]
        parts.extend(concern.get("supporting_files", []))
        chunks.append(
            Chunk(
                source_type="concern",
                source_id=concern["concern"],
                text=" ".join(parts),
                metadata={
                    "concern": concern["concern"],
                    "owner_file": concern["owner_file"],
                    "system": concern.get("system", ""),
                },
            )
        )

    # KB stacks
    kb = index.get("knowledge_base", {})
    for stack_entry in kb.get("stacks", []):
        parts = [stack_entry.get("name", "")]
        parts.extend(stack_entry.get("aliases", []))
        parts.extend(stack_entry.get("best_for", []))
        parts.extend(stack_entry.get("strengths", []))
        parts.extend(stack_entry.get("tradeoffs", []))
        parts.extend(stack_entry.get("capabilities", []))
        parts.extend(stack_entry.get("risks", []))
        parts.extend(stack_entry.get("best_practices", []))
        chunks.append(
            Chunk(
                source_type="stack",
                source_id=stack_entry["name"],
                text=" ".join(parts),
                metadata={"name": stack_entry["name"], "category": stack_entry.get("category", "")},
            )
        )

    # KB integration patterns
    for pattern in kb.get("integration_patterns", []):
        parts = [pattern.get("name", "")]
        parts.extend(pattern.get("components", []))
        parts.extend(pattern.get("fit_for", []))
        parts.extend(pattern.get("notes", []))
        chunks.append(
            Chunk(
                source_type="pattern",
                source_id=pattern["name"],
                text=" ".join(parts),
                metadata={"name": pattern["name"], "components": pattern.get("components", [])},
            )
        )

    # KB CLI tools
    for cli_tool in kb.get("cli_tools", []):
        parts = [cli_tool.get("name", ""), cli_tool.get("provider", ""), cli_tool.get("category", "")]
        parts.extend(cli_tool.get("aliases", []))
        parts.extend(cli_tool.get("install_methods", []))
        parts.extend(cli_tool.get("recommended_commands", []))
        parts.extend(cli_tool.get("required_config", []))
        parts.extend(cli_tool.get("notes", []))
        chunks.append(
            Chunk(
                source_type="cli_tool",
                source_id=cli_tool["name"],
                text=" ".join(parts),
                metadata={"name": cli_tool["name"], "provider": cli_tool.get("provider", "")},
            )
        )

    # KB third-party APIs
    for api_entry in kb.get("third_party_apis", []):
        parts = [api_entry.get("name", ""), api_entry.get("provider", ""), api_entry.get("category", "")]
        parts.extend(api_entry.get("aliases", []))
        parts.extend(api_entry.get("server_env_vars", []))
        parts.extend(api_entry.get("public_env_vars", []))
        if api_entry.get("base_url"):
            parts.append(api_entry["base_url"])
        if api_entry.get("docs_url"):
            parts.append(api_entry["docs_url"])
        parts.extend(api_entry.get("notes", []))
        chunks.append(
            Chunk(
                source_type="third_party_api",
                source_id=api_entry["name"],
                text=" ".join(parts),
                metadata={"name": api_entry["name"], "provider": api_entry.get("provider", "")},
            )
        )

    # KB coverage domains
    for domain in kb.get("coverage_domains", []):
        parts = [
            domain.get("name", ""),
            domain.get("status", ""),
            domain.get("priority", ""),
            domain.get("summary", ""),
        ]
        parts.extend(domain.get("key_capabilities", []))
        parts.extend(domain.get("representative_tools", []))
        parts.extend(domain.get("current_gaps", []))
        parts.extend(domain.get("linked_tracks", []))
        chunks.append(
            Chunk(
                source_type="coverage_domain",
                source_id=domain["name"],
                text=" ".join(parts),
                metadata={
                    "name": domain["name"],
                    "status": domain.get("status", ""),
                    "priority": domain.get("priority", ""),
                },
            )
        )

    # KB decision rules
    for rule in kb.get("decision_rules", []):
        parts = [rule.get("title", ""), rule.get("when", ""), rule.get("prefer", ""), rule.get("because", "")]
        parts.extend(rule.get("avoid", []))
        parts.extend(rule.get("related_items", []))
        chunks.append(
            Chunk(
                source_type="decision_rule",
                source_id=rule["title"],
                text=" ".join(parts),
                metadata={"title": rule["title"], "confidence": rule.get("confidence", "")},
            )
        )

    # KB explicit relationships
    for relation in kb.get("relationships", []):
        parts = [
            relation.get("subject", ""),
            relation.get("relation", ""),
            relation.get("object", ""),
            relation.get("rationale", ""),
        ]
        parts.extend(relation.get("evidence", []))
        parts.extend(relation.get("tags", []))
        chunks.append(
            Chunk(
                source_type="kb_relation",
                source_id=f"{relation.get('subject', '')}:{relation.get('relation', '')}:{relation.get('object', '')}",
                text=" ".join(parts),
                metadata={
                    "subject": relation.get("subject", ""),
                    "relation": relation.get("relation", ""),
                    "object": relation.get("object", ""),
                },
            )
        )

    # KB comparisons
    for comparison in kb.get("comparisons", []):
        parts = [comparison.get("name", ""), comparison.get("summary", ""), comparison.get("decision", "")]
        parts.extend(comparison.get("scope", []))
        parts.extend(comparison.get("compared_versions", []))
        parts.extend(comparison.get("related_items", []))
        for finding in comparison.get("findings", []):
            parts.extend(
                [
                    finding.get("area", ""),
                    finding.get("summary", ""),
                    finding.get("option_a", ""),
                    finding.get("option_b", ""),
                    finding.get("recommendation", ""),
                    finding.get("migration_risk", ""),
                ]
            )
        chunks.append(
            Chunk(
                source_type="comparison",
                source_id=comparison["name"],
                text=" ".join(parts),
                metadata={"name": comparison["name"], "status": comparison.get("status", "")},
            )
        )

    # KB retrieval guidance
    guidance = kb.get("retrieval_guidance", {})
    for section_key in ("principles", "recommended_layers", "avoid"):
        items = guidance.get(section_key, [])
        if isinstance(items, list):
            for i, item in enumerate(items):
                chunks.append(
                    Chunk(
                        source_type="guidance",
                        source_id=f"retrieval_guidance.{section_key}[{i}]",
                        text=item,
                        metadata={"section": section_key},
                    )
                )

    # Nested guidance subsections (embedding_guidance, vector_index_guidance, search_type_guidance)
    for sub_key in ("embedding_guidance", "vector_index_guidance", "search_type_guidance"):
        sub = guidance.get(sub_key, {})
        if isinstance(sub, dict):
            for entry_key, entry_val in sub.items():
                if isinstance(entry_val, str):
                    chunks.append(
                        Chunk(
                            source_type="guidance",
                            source_id=f"retrieval_guidance.{sub_key}.{entry_key}",
                            text=f"{entry_key}: {entry_val}",
                            metadata={"section": sub_key, "key": entry_key},
                        )
                    )
                elif isinstance(entry_val, list):
                    for i, item in enumerate(entry_val):
                        chunks.append(
                            Chunk(
                                source_type="guidance",
                                source_id=f"retrieval_guidance.{sub_key}.{entry_key}[{i}]",
                                text=f"{entry_key}: {item}",
                                metadata={"section": sub_key, "key": entry_key},
                            )
                        )

    # KB research operations
    research_ledger = kb.get("research_ledger", {})
    for track in research_ledger.get("tracks", []):
        parts = [
            track.get("name", ""),
            track.get("cadence", ""),
            track.get("owner", ""),
            research_ledger.get("operating_model", ""),
            research_ledger.get("weekly_review_day", ""),
        ]
        parts.extend(track.get("scope", []))
        parts.extend(track.get("trigger_signals", []))
        parts.extend(track.get("required_outputs", []))
        chunks.append(
            Chunk(
                source_type="research_track",
                source_id=track["name"],
                text=" ".join(parts),
                metadata={"name": track["name"], "cadence": track.get("cadence", "")},
            )
        )

    # Routes
    for route in index.get("routes", []):
        chunks.append(
            Chunk(
                source_type="route",
                source_id=f"{route['method']} {route['path']}",
                text=f"{route['method']} {route['path']} {route.get('purpose', '')}",
                metadata=route,
            )
        )

    # Commands
    for cmd in index.get("commands", {}).get("cli", []):
        chunks.append(Chunk(source_type="command", source_id=f"cli:{cmd}", text=f"cli command {cmd}", metadata={"kind": "cli"}))
    for cmd in index.get("commands", {}).get("dashboard", []):
        chunks.append(
            Chunk(
                source_type="command",
                source_id=f"dashboard:{cmd}",
                text=f"dashboard command {cmd}",
                metadata={"kind": "dashboard"},
            )
        )

    return chunks


# ---------------------------------------------------------------------------
# Tokenizer
# ---------------------------------------------------------------------------


def tokenize(text: str) -> list[str]:
    """Lowercase tokenization with stop-word removal."""
    return [tok for tok in _TOKEN_RE.findall(text.lower()) if tok not in _STOP_WORDS]


# ---------------------------------------------------------------------------
# Layer 1 — BM25 Lexical Search
# ---------------------------------------------------------------------------


class LexicalSearcher:
    """Okapi BM25 search over context index chunks."""

    def __init__(self, chunks: list[Chunk], *, k1: float = 1.5, b: float = 0.75) -> None:
        self.chunks = chunks
        self.k1 = k1
        self.b = b

        # Tokenize all chunks
        self._doc_tokens: list[list[str]] = [tokenize(chunk.text) for chunk in chunks]
        self._doc_lengths: list[int] = [len(tokens) for tokens in self._doc_tokens]
        self._avg_dl = sum(self._doc_lengths) / max(len(self._doc_lengths), 1)
        self._n_docs = len(chunks)

        # Build inverted index: term -> set of doc indices
        self._inverted: dict[str, set[int]] = {}
        for doc_idx, tokens in enumerate(self._doc_tokens):
            for token in set(tokens):
                self._inverted.setdefault(token, set()).add(doc_idx)

        # Pre-compute term frequencies per document
        self._tf: list[dict[str, int]] = []
        for tokens in self._doc_tokens:
            freq: dict[str, int] = {}
            for tok in tokens:
                freq[tok] = freq.get(tok, 0) + 1
            self._tf.append(freq)

    def _idf(self, term: str) -> float:
        df = len(self._inverted.get(term, set()))
        return math.log((self._n_docs - df + 0.5) / (df + 0.5) + 1.0)

    def search(self, query: str, top_k: int = 10) -> list[SearchResult]:
        """Score all chunks against the query and return top-k results."""
        query_tokens = tokenize(query)
        if not query_tokens:
            return []

        scores: list[float] = [0.0] * self._n_docs

        for token in query_tokens:
            idf = self._idf(token)
            candidate_docs = self._inverted.get(token, set())
            for doc_idx in candidate_docs:
                tf = self._tf[doc_idx].get(token, 0)
                dl = self._doc_lengths[doc_idx]
                numerator = tf * (self.k1 + 1)
                denominator = tf + self.k1 * (1 - self.b + self.b * (dl / self._avg_dl))
                scores[doc_idx] += idf * (numerator / denominator)

        # Rank and collect top-k
        ranked = sorted(
            ((score, idx) for idx, score in enumerate(scores) if score > 0),
            key=lambda x: x[0],
            reverse=True,
        )

        results: list[SearchResult] = []
        for score, idx in ranked[:top_k]:
            chunk = self.chunks[idx]
            results.append(
                SearchResult(
                    source_type=chunk.source_type,
                    source_id=chunk.source_id,
                    text=chunk.text,
                    score=score,
                    metadata=dict(chunk.metadata),
                )
            )
        return results


# ---------------------------------------------------------------------------
# Layer 2 — Hybrid Lexical + Vector Search
# ---------------------------------------------------------------------------


class EmbeddingStore:
    """ChromaDB-backed embedding store for vector search over chunks."""

    def __init__(self, chunks: list[Chunk], persist_path: Path | None = None) -> None:
        try:
            import chromadb  # type: ignore[import-untyped]
        except ImportError:
            raise ImportError("ChromaDB is required for vector search. Install with: pip install chromadb") from None

        self.chunks = chunks
        if persist_path:
            persist_path.mkdir(parents=True, exist_ok=True)
            self._client = chromadb.PersistentClient(path=str(persist_path))
        else:
            self._client = chromadb.Client()

        self._collection = self._client.get_or_create_collection(
            name="programstart_context",
            metadata={"hnsw:space": "cosine"},
        )

        # Add chunks if collection is empty or size mismatch
        if self._collection.count() != len(chunks):
            self._collection.delete(where={"source_type": {"$ne": ""}})
            ids = [f"{c.source_type}:{c.source_id}" for c in chunks]
            documents = [c.text for c in chunks]
            metadatas = [{"source_type": c.source_type, "source_id": c.source_id} for c in chunks]

            # ChromaDB has a batch size limit; add in batches of 500
            batch_size = 500
            for start in range(0, len(ids), batch_size):
                end = start + batch_size
                self._collection.add(
                    ids=ids[start:end],
                    documents=documents[start:end],
                    metadatas=cast(Any, metadatas[start:end]),
                )

    def query(self, query_text: str, top_k: int = 10) -> list[SearchResult]:
        """Return top-k results by embedding similarity."""
        results = self._collection.query(
            query_texts=[query_text],
            n_results=min(top_k, self._collection.count()),
        )
        search_results: list[SearchResult] = []
        raw_ids = cast(list[list[str]] | None, results.get("ids"))
        if raw_ids:
            ids = raw_ids[0]
            raw_distances = cast(list[list[float]] | None, results.get("distances"))
            raw_documents = cast(list[list[str]] | None, results.get("documents"))
            raw_metadatas = cast(list[list[dict[str, Any]]] | None, results.get("metadatas"))
            distances = raw_distances[0] if raw_distances else []
            documents = raw_documents[0] if raw_documents else []
            metadatas = raw_metadatas[0] if raw_metadatas else []
            for i, _doc_id in enumerate(ids):
                # ChromaDB returns distances (lower = closer for cosine); convert to similarity
                similarity = 1.0 - distances[i] if distances else 0.0
                meta = metadatas[i] if metadatas else {}
                search_results.append(
                    SearchResult(
                        source_type=str(meta.get("source_type", "")),
                        source_id=str(meta.get("source_id", "")),
                        text=documents[i] if documents else "",
                        score=similarity,
                        metadata=dict(meta),
                    )
                )
        return search_results


class HybridSearcher:
    """Combines BM25 lexical search with vector search using reciprocal rank fusion."""

    def __init__(
        self,
        lexical: LexicalSearcher,
        embedding_store: EmbeddingStore | None = None,
    ) -> None:
        self.lexical = lexical
        self.embedding_store = embedding_store

    def search(self, query: str, top_k: int = 10, alpha: float = 0.5, method: str = "lexical") -> list[SearchResult]:
        """Search with the specified method.

        Args:
            query: Search query string.
            top_k: Maximum number of results.
            alpha: Weight for vector vs lexical (0.0 = lexical only, 1.0 = vector only).
            method: One of 'lexical', 'vector', 'hybrid'.
        """
        if method == "lexical" or (method == "hybrid" and self.embedding_store is None):
            return self.lexical.search(query, top_k=top_k)

        if method == "vector":
            if self.embedding_store is None:
                raise ValueError("Vector search requires an embedding store. Install chromadb.")
            return self.embedding_store.query(query, top_k=top_k)

        # Hybrid: reciprocal rank fusion
        lexical_k = max(top_k * 2, 20)
        lexical_results = self.lexical.search(query, top_k=lexical_k)
        vector_results = self.embedding_store.query(query, top_k=lexical_k) if self.embedding_store else []

        return self._reciprocal_rank_fusion(lexical_results, vector_results, alpha=alpha, top_k=top_k)

    @staticmethod
    def _reciprocal_rank_fusion(
        lexical_results: list[SearchResult],
        vector_results: list[SearchResult],
        alpha: float,
        top_k: int,
        rrf_k: int = 60,
    ) -> list[SearchResult]:
        """Merge two ranked lists using reciprocal rank fusion."""
        fused_scores: dict[str, float] = {}
        result_map: dict[str, SearchResult] = {}

        for rank, result in enumerate(lexical_results):
            key = f"{result.source_type}:{result.source_id}"
            rrf_score = (1.0 - alpha) / (rrf_k + rank + 1)
            fused_scores[key] = fused_scores.get(key, 0.0) + rrf_score
            result_map[key] = result

        for rank, result in enumerate(vector_results):
            key = f"{result.source_type}:{result.source_id}"
            rrf_score = alpha / (rrf_k + rank + 1)
            fused_scores[key] = fused_scores.get(key, 0.0) + rrf_score
            if key not in result_map:
                result_map[key] = result

        ranked = sorted(fused_scores.items(), key=lambda x: x[1], reverse=True)
        results: list[SearchResult] = []
        for key, score in ranked[:top_k]:
            r = result_map[key]
            results.append(
                SearchResult(
                    source_type=r.source_type,
                    source_id=r.source_id,
                    text=r.text,
                    score=score,
                    metadata=dict(r.metadata),
                )
            )
        return results


# ---------------------------------------------------------------------------
# Layer 3 — RAG Assistant
# ---------------------------------------------------------------------------


_SYSTEM_PROMPT = """\
You are a PROGRAMSTART assistant. Answer questions using ONLY the context provided below.
If the context does not contain enough information to answer, say so explicitly.
Cite your sources by referencing the source_type and source_id of the chunks you used.

Context:
{context}
"""


class RAGAssistant:
    """Retrieval-augmented generation over the context index."""

    def __init__(self, searcher: HybridSearcher, *, model: str | None = None) -> None:
        self.searcher = searcher
        self.model = model or os.environ.get("PROGRAMSTART_LLM_MODEL", "gpt-4o-mini")

    def _format_context(self, results: list[SearchResult]) -> str:
        parts: list[str] = []
        for i, r in enumerate(results, 1):
            parts.append(f"[{i}] ({r.source_type}: {r.source_id})\n{r.text}")
        return "\n\n".join(parts)

    def ask(
        self,
        question: str,
        *,
        top_k: int = 10,
        method: str = "lexical",
        alpha: float = 0.5,
    ) -> RAGResponse:
        """Retrieve context and generate an answer."""
        results = self.searcher.search(question, top_k=top_k, method=method, alpha=alpha)
        context = self._format_context(results)
        system_message = _SYSTEM_PROMPT.format(context=context)

        answer = self._generate(system_message, question)
        return RAGResponse(
            answer=answer.answer if isinstance(answer, RAGQueryResponse) else answer,
            sources=results,
            model=self.model,
            retrieval_method=method,
        )

    def ask_structured(
        self,
        question: str,
        *,
        top_k: int = 10,
        method: str = "lexical",
        alpha: float = 0.5,
    ) -> RAGQueryResponse:
        """Retrieve context and generate a validated, structured response via Instructor."""
        results = self.searcher.search(question, top_k=top_k, method=method, alpha=alpha)
        context = self._format_context(results)
        system_message = _SYSTEM_PROMPT.format(context=context)

        return self._generate_structured(system_message, question)

    def _generate(self, system_message: str, user_message: str) -> str | RAGQueryResponse:
        """Call the configured LLM via LiteLLM (unified multi-provider interface)."""
        try:
            return self._generate_structured(system_message, user_message)
        except Exception:
            return self._generate_litellm(system_message, user_message)

    def _generate_litellm(self, system_message: str, user_message: str) -> str:
        """Call the configured LLM via LiteLLM's unified API."""
        try:
            import litellm  # type: ignore[import-untyped]
        except ImportError:
            raise ImportError("LiteLLM is required for RAG. Install with: pip install 'programstart-workflow[rag]'") from None

        response = cast(
            Any,
            litellm.completion(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message},
                ],
                temperature=0.1,
                max_tokens=2048,
            ),
        )
        return response.choices[0].message.content or ""

    def _generate_structured(self, system_message: str, user_message: str) -> RAGQueryResponse:
        """Call the configured LLM via Instructor for validated, structured output."""
        try:
            import instructor  # type: ignore[import-untyped]
            import litellm  # type: ignore[import-untyped]
        except ImportError:
            raise ImportError(
                "Instructor + LiteLLM are required for structured RAG. Install with: pip install 'programstart-workflow[rag]'"
            ) from None

        client = instructor.from_litellm(litellm.completion)
        return client.chat.completions.create(
            model=self.model,
            response_model=RAGQueryResponse,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message},
            ],
            temperature=0.1,
            max_tokens=2048,
        )


# ---------------------------------------------------------------------------
# Factory — build the retrieval stack from a context index
# ---------------------------------------------------------------------------


def default_chroma_path() -> Path:
    env_path = os.environ.get("PROGRAMSTART_CHROMA_PATH")
    if env_path:
        return Path(env_path)
    return generated_outputs_root() / "retrieval" / "chroma"


def build_retrieval_stack(
    index: dict[str, Any],
    *,
    method: str = "lexical",
    chroma_path: Path | None = None,
    model: str | None = None,
) -> tuple[HybridSearcher, RAGAssistant | None]:
    """Build the retrieval stack from a context index.

    Returns a (searcher, rag_assistant) tuple. rag_assistant is None if method is not 'ask'.
    """
    chunks = build_corpus(index)
    lexical = LexicalSearcher(chunks)

    embedding_store = None
    if method in ("hybrid", "vector", "ask"):
        try:
            persist_path = chroma_path or default_chroma_path()
            embedding_store = EmbeddingStore(chunks, persist_path=persist_path)
        except ImportError:
            pass  # Fall back to lexical-only

    searcher = HybridSearcher(lexical, embedding_store)
    rag = RAGAssistant(searcher, model=model) if method == "ask" else None
    return searcher, rag


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _load_or_build_index(index_path: str | None) -> dict[str, Any]:
    path = Path(index_path) if index_path else default_index_path()
    if not path.is_absolute():
        path = workspace_path(str(path))
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return build_context_index()


def load_validated_index(index_path: str | None = None) -> ContextIndex:
    """Load and validate the context index through Pydantic models.

    Returns a fully validated ContextIndex instance. Raises ValidationError
    if the index data does not match the expected schema.
    """
    raw = _load_or_build_index(index_path)
    return ContextIndex.model_validate(raw)


def _print_search_results(results: list[SearchResult]) -> None:
    if not results:
        print("No results found.")
        return
    for i, r in enumerate(results, 1):
        print(f"\n--- Result {i} (score: {r.score:.4f}) ---")
        print(f"  Type: {r.source_type}")
        print(f"  ID:   {r.source_id}")
        preview = r.text[:200] + "..." if len(r.text) > 200 else r.text
        print(f"  Text: {preview}")


def _print_rag_response(response: RAGResponse) -> None:
    print(f"\n{'=' * 60}")
    print(f"Model: {response.model} | Method: {response.retrieval_method}")
    print(f"{'=' * 60}")
    print(f"\n{response.answer}\n")
    print(f"--- Sources ({len(response.sources)}) ---")
    for i, s in enumerate(response.sources, 1):
        print(f"  [{i}] {s.source_type}: {s.source_id} (score: {s.score:.4f})")


def _print_structured_response(response: RAGQueryResponse) -> None:
    print(f"\n{'=' * 60}")
    print(f"Confidence: {response.confidence}")
    print(f"{'=' * 60}")
    print(f"\n{response.answer}\n")
    if response.reasoning:
        print(f"Reasoning: {response.reasoning}\n")
    if response.cited_sources:
        print(f"--- Cited Sources ({len(response.cited_sources)}) ---")
        for i, src in enumerate(response.cited_sources, 1):
            print(f"  [{i}] {src}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Search and RAG over the PROGRAMSTART context index.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # search subcommand
    search_parser = subparsers.add_parser("search", help="Search the context index.")
    search_parser.add_argument("query", help="Search query.")
    search_parser.add_argument("--index", default=None, help="Context index path.")
    search_parser.add_argument("--method", choices=["lexical", "hybrid", "vector"], default="lexical")
    search_parser.add_argument("--alpha", type=float, default=0.5, help="Hybrid alpha (0=lexical, 1=vector).")
    search_parser.add_argument("--top-k", type=int, default=10, help="Number of results.")
    search_parser.add_argument("--json", action="store_true", help="Output as JSON.")

    # ask subcommand
    ask_parser = subparsers.add_parser("ask", help="Ask a question using RAG.")
    ask_parser.add_argument("question", help="Question to answer.")
    ask_parser.add_argument("--index", default=None, help="Context index path.")
    ask_parser.add_argument("--method", choices=["lexical", "hybrid", "vector"], default="lexical")
    ask_parser.add_argument("--alpha", type=float, default=0.5, help="Hybrid alpha (0=lexical, 1=vector).")
    ask_parser.add_argument("--top-k", type=int, default=10, help="Number of context chunks.")
    ask_parser.add_argument("--model", default=None, help="LLM model name.")
    ask_parser.add_argument("--structured", action="store_true", help="Use Instructor for structured output.")

    # validate subcommand
    validate_parser = subparsers.add_parser("validate", help="Validate the context index against Pydantic models.")
    validate_parser.add_argument("--index", default=None, help="Context index path.")

    args = parser.parse_args(argv)
    index = _load_or_build_index(args.index)

    if args.command == "search":
        searcher, _ = build_retrieval_stack(index, method=args.method)
        results = searcher.search(args.query, top_k=args.top_k, method=args.method, alpha=args.alpha)
        if args.json:
            print(json.dumps([asdict(r) for r in results], indent=2))
        else:
            _print_search_results(results)
        return 0

    if args.command == "ask":
        need_vector = args.method in ("hybrid", "vector")
        searcher, rag = build_retrieval_stack(index, method="ask" if not need_vector else args.method, model=args.model)
        if rag is None:
            rag = RAGAssistant(searcher, model=args.model)
        if args.structured:
            response = rag.ask_structured(args.question, top_k=args.top_k, method=args.method, alpha=args.alpha)
            _print_structured_response(response)
        else:
            response = rag.ask(args.question, top_k=args.top_k, method=args.method, alpha=args.alpha)
            _print_rag_response(response)
        return 0

    if args.command == "validate":
        try:
            validated = load_validated_index(args.index)
            print("Context index validated successfully.")
            print(f"  Version:    {validated.version}")
            print(f"  Documents:  {len(validated.documents)}")
            print(f"  Concerns:   {len(validated.concerns)}")
            print(f"  KB stacks:  {len(validated.knowledge_base.stacks)}")
            print(f"  KB patterns:{len(validated.knowledge_base.integration_patterns)}")
            print(f"  Routes:     {len(validated.routes)}")
            print(f"  Relations:  {len(validated.relations)}")
            return 0
        except Exception as e:
            print(f"Validation failed: {e}")
            return 1

    return 1


if __name__ == "__main__":  # pragma: no cover
    warn_direct_script_invocation("'uv run programstart retrieval <subcommand>' or 'pb retrieval <subcommand>'")
    raise SystemExit(main())
