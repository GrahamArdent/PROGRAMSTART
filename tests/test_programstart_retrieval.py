from __future__ import annotations

# ruff: noqa: I001

import contextlib
import io
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts import programstart_retrieval


# ---------------------------------------------------------------------------
# Fixtures — minimal context index for isolated testing
# ---------------------------------------------------------------------------


def _minimal_index() -> dict[str, object]:
    return {
        "documents": [
            {
                "path": "USERJOURNEY/DELIVERY_GAMEPLAN.md",
                "title": "Delivery Gameplan",
                "purpose": "Defines execution order and synchronization rules",
                "owner": "USERJOURNEY",
                "headings": ["Source Of Truth Matrix", "Phase Sequence"],
                "depends_on": [],
            },
            {
                "path": "PROGRAMBUILD/ARCHITECTURE.md",
                "title": "Architecture Overview",
                "purpose": "System architecture and component diagram",
                "owner": "PROGRAMBUILD",
                "headings": ["Components", "Data Flow"],
                "depends_on": [],
            },
        ],
        "concerns": [
            {
                "concern": "consent behavior",
                "owner_file": "LEGAL_AND_CONSENT.md",
                "supporting_files": ["PRIVACY_POLICY_DRAFT.md"],
                "system": "userjourney",
                "source": "USERJOURNEY/DELIVERY_GAMEPLAN.md",
                "relation": "source_of_truth",
            },
            {
                "concern": "activation event",
                "owner_file": "STATES_AND_RULES.md",
                "supporting_files": ["ANALYTICS_AND_OUTCOMES.md"],
                "system": "userjourney",
                "source": "USERJOURNEY/DELIVERY_GAMEPLAN.md",
                "relation": "source_of_truth",
            },
        ],
        "knowledge_base": {
            "stacks": [
                {
                    "name": "FastAPI",
                    "category": "backend",
                    "aliases": ["fastapi"],
                    "best_for": ["typed Python APIs"],
                    "strengths": ["validation plus OpenAPI"],
                    "capabilities": ["async request handling"],
                    "risks": ["missing batteries"],
                    "best_practices": ["use typed response models"],
                },
                {
                    "name": "PostgreSQL",
                    "category": "data",
                    "aliases": ["postgres", "pg"],
                    "best_for": ["primary transactional system"],
                    "strengths": ["relational integrity"],
                    "capabilities": ["ACID transactions"],
                    "risks": ["misuse as universal storage"],
                },
            ],
            "integration_patterns": [
                {
                    "name": "Business web platform",
                    "components": ["Django", "PostgreSQL", "Redis"],
                    "fit_for": ["workflow-heavy admin products"],
                    "notes": ["keep monolithic until deployment boundaries require splitting"],
                },
            ],
            "cli_tools": [
                {
                    "name": "GitHub CLI",
                    "provider": "GitHub",
                    "install_methods": ["gh auth login"],
                    "recommended_commands": ["gh repo create"],
                    "notes": ["use GH_TOKEN in automation"],
                }
            ],
            "third_party_apis": [
                {
                    "name": "OpenAI",
                    "provider": "OpenAI",
                    "server_env_vars": ["OPENAI_API_KEY"],
                    "base_url": "https://api.openai.com/v1",
                    "notes": ["keep keys server-side"],
                }
            ],
            "coverage_domains": [
                {
                    "name": "Mobile and cross-platform apps",
                    "status": "seed",
                    "priority": "high",
                    "summary": "Native and cross-platform mobile guidance is still thin.",
                    "current_gaps": ["No React Native guidance"],
                    "linked_tracks": ["Web and platform delivery"],
                }
            ],
            "decision_rules": [
                {
                    "title": "Prefer durable workflows",
                    "when": "retries and waits matter",
                    "prefer": "Temporal",
                    "because": "state should be explicit",
                    "related_items": ["Temporal", "Celery"],
                }
            ],
            "relationships": [
                {
                    "subject": "FastAPI",
                    "relation": "complements",
                    "object": "Pydantic",
                    "rationale": "typed models strengthen API contracts",
                    "tags": ["validation"],
                }
            ],
            "comparisons": [
                {
                    "name": "Python 3.13 vs 3.14",
                    "summary": "3.14 is the stronger default when dependencies are green.",
                    "decision": "Prefer 3.14 for new services after validation.",
                    "compared_versions": ["3.13", "3.14"],
                    "findings": [
                        {
                            "area": "concurrency",
                            "option_a": "experimental free-threaded mode",
                            "option_b": "supported free-threaded mode",
                            "recommendation": "Prefer 3.14 for new concurrency-heavy services.",
                        }
                    ],
                }
            ],
            "retrieval_guidance": {
                "principles": [
                    "Structured facts should remain authoritative.",
                    "Hybrid retrieval is preferable to vector-only retrieval.",
                ],
                "recommended_layers": [
                    "Registry and state facts",
                    "Lexical retrieval",
                ],
                "avoid": [
                    "Treating embeddings as the only context layer",
                ],
                "embedding_guidance": {
                    "default_model": "text-embedding-3-small",
                    "best_practices": [
                        "Pre-clean text before embedding.",
                        "Use cosine similarity.",
                    ],
                },
                "vector_index_guidance": {
                    "hnsw": "Default for most workloads. Logarithmic search time.",
                },
                "search_type_guidance": {
                    "keyword_bm25": "Use when exact term matching matters.",
                    "hybrid": "Combine BM25 and vector search.",
                },
            },
            "research_ledger": {
                "operating_model": "weekly delta review",
                "weekly_review_day": "Friday",
                "tracks": [
                    {
                        "name": "Python runtime",
                        "cadence": "weekly",
                        "freshness_days": 7,
                        "last_review_date": "2026-03-29",
                        "scope": ["CPython releases"],
                        "required_outputs": ["comparison delta"],
                    }
                ],
            },
        },
        "routes": [
            {"method": "GET", "path": "/api/state", "purpose": "Dashboard state payload"},
            {"method": "POST", "path": "/api/run", "purpose": "Run whitelisted command"},
        ],
        "commands": {
            "cli": ["status", "validate", "context", "retrieval"],
            "dashboard": ["context.summary", "state.show"],
        },
        "relations": [],
    }


# ---------------------------------------------------------------------------
# Corpus builder tests
# ---------------------------------------------------------------------------


def test_build_corpus_creates_chunks_for_all_source_types() -> None:
    index = _minimal_index()
    chunks = programstart_retrieval.build_corpus(index)

    source_types = {c.source_type for c in chunks}
    assert "document" in source_types
    assert "concern" in source_types
    assert "stack" in source_types
    assert "pattern" in source_types
    assert "cli_tool" in source_types
    assert "third_party_api" in source_types
    assert "coverage_domain" in source_types
    assert "decision_rule" in source_types
    assert "kb_relation" in source_types
    assert "comparison" in source_types
    assert "guidance" in source_types
    assert "research_track" in source_types
    assert "route" in source_types
    assert "command" in source_types


def test_build_corpus_document_chunks_contain_headings() -> None:
    index = _minimal_index()
    chunks = programstart_retrieval.build_corpus(index)
    doc_chunks = [c for c in chunks if c.source_type == "document"]

    gameplan = next(c for c in doc_chunks if "DELIVERY_GAMEPLAN" in c.source_id)
    assert "Source Of Truth Matrix" in gameplan.text
    assert "Phase Sequence" in gameplan.text


def test_build_corpus_guidance_chunks_include_subsections() -> None:
    index = _minimal_index()
    chunks = programstart_retrieval.build_corpus(index)
    guidance_chunks = [c for c in chunks if c.source_type == "guidance"]

    source_ids = {c.source_id for c in guidance_chunks}
    assert any("embedding_guidance" in sid for sid in source_ids)
    assert any("vector_index_guidance" in sid for sid in source_ids)
    assert any("search_type_guidance" in sid for sid in source_ids)


def test_build_corpus_includes_comparison_and_relationship_text() -> None:
    index = _minimal_index()
    chunks = programstart_retrieval.build_corpus(index)

    assert any(c.source_type == "comparison" and "3.14" in c.text for c in chunks)
    assert any(c.source_type == "kb_relation" and c.metadata["object"] == "Pydantic" for c in chunks)


def test_lexical_search_finds_runtime_comparison() -> None:
    index = _minimal_index()
    chunks = programstart_retrieval.build_corpus(index)
    searcher = programstart_retrieval.LexicalSearcher(chunks)

    results = searcher.search("Python 3.14 free-threaded")
    assert any(r.source_type == "comparison" for r in results)


# ---------------------------------------------------------------------------
# Tokenizer tests
# ---------------------------------------------------------------------------


def test_tokenize_lowercases_and_removes_stop_words() -> None:
    tokens = programstart_retrieval.tokenize("The FastAPI is a great framework for APIs")
    assert "the" not in tokens
    assert "is" not in tokens
    assert "a" not in tokens
    assert "fastapi" in tokens
    assert "great" in tokens
    assert "framework" in tokens
    assert "apis" in tokens


def test_tokenize_handles_punctuation() -> None:
    tokens = programstart_retrieval.tokenize("consent-behavior, activation_event!")
    assert "consent" in tokens
    assert "behavior" in tokens
    assert "activation_event" in tokens


# ---------------------------------------------------------------------------
# Layer 1 — Lexical search tests
# ---------------------------------------------------------------------------


def test_lexical_search_finds_relevant_documents() -> None:
    index = _minimal_index()
    chunks = programstart_retrieval.build_corpus(index)
    searcher = programstart_retrieval.LexicalSearcher(chunks)

    results = searcher.search("consent behavior")
    assert len(results) > 0
    assert results[0].source_id == "consent behavior"
    assert results[0].source_type == "concern"


def test_lexical_search_finds_stacks_by_name() -> None:
    index = _minimal_index()
    chunks = programstart_retrieval.build_corpus(index)
    searcher = programstart_retrieval.LexicalSearcher(chunks)

    results = searcher.search("FastAPI")
    assert len(results) > 0
    assert any(r.source_id == "FastAPI" for r in results)


def test_lexical_search_finds_stacks_by_capability() -> None:
    index = _minimal_index()
    chunks = programstart_retrieval.build_corpus(index)
    searcher = programstart_retrieval.LexicalSearcher(chunks)

    results = searcher.search("async request handling")
    assert len(results) > 0
    assert any(r.source_type == "stack" for r in results)


def test_lexical_search_respects_top_k() -> None:
    index = _minimal_index()
    chunks = programstart_retrieval.build_corpus(index)
    searcher = programstart_retrieval.LexicalSearcher(chunks)

    results = searcher.search("retrieval", top_k=3)
    assert len(results) <= 3


def test_lexical_search_empty_query_returns_empty() -> None:
    index = _minimal_index()
    chunks = programstart_retrieval.build_corpus(index)
    searcher = programstart_retrieval.LexicalSearcher(chunks)

    results = searcher.search("")
    assert results == []


def test_lexical_search_scores_are_descending() -> None:
    index = _minimal_index()
    chunks = programstart_retrieval.build_corpus(index)
    searcher = programstart_retrieval.LexicalSearcher(chunks)

    results = searcher.search("retrieval guidance")
    scores = [r.score for r in results]
    assert scores == sorted(scores, reverse=True)


def test_lexical_search_finds_routes() -> None:
    index = _minimal_index()
    chunks = programstart_retrieval.build_corpus(index)
    searcher = programstart_retrieval.LexicalSearcher(chunks)

    results = searcher.search("dashboard state")
    assert any(r.source_type == "route" for r in results)


def test_lexical_search_finds_commands() -> None:
    index = _minimal_index()
    chunks = programstart_retrieval.build_corpus(index)
    searcher = programstart_retrieval.LexicalSearcher(chunks)

    results = searcher.search("validate")
    assert any(r.source_type == "command" for r in results)


# ---------------------------------------------------------------------------
# Hybrid search tests (lexical-only fallback)
# ---------------------------------------------------------------------------


def test_hybrid_searcher_lexical_fallback() -> None:
    index = _minimal_index()
    chunks = programstart_retrieval.build_corpus(index)
    lexical = programstart_retrieval.LexicalSearcher(chunks)
    searcher = programstart_retrieval.HybridSearcher(lexical, embedding_store=None)

    results = searcher.search("consent", method="lexical")
    assert len(results) > 0


def test_hybrid_searcher_hybrid_without_embeddings_falls_back() -> None:
    index = _minimal_index()
    chunks = programstart_retrieval.build_corpus(index)
    lexical = programstart_retrieval.LexicalSearcher(chunks)
    searcher = programstart_retrieval.HybridSearcher(lexical, embedding_store=None)

    # When embedding_store is None, hybrid should fall back to lexical
    results = searcher.search("consent", method="hybrid")
    assert len(results) > 0


def test_hybrid_searcher_vector_without_embeddings_raises() -> None:
    index = _minimal_index()
    chunks = programstart_retrieval.build_corpus(index)
    lexical = programstart_retrieval.LexicalSearcher(chunks)
    searcher = programstart_retrieval.HybridSearcher(lexical, embedding_store=None)

    try:
        searcher.search("consent", method="vector")
        assert False, "Should have raised ValueError"
    except ValueError:
        pass


# ---------------------------------------------------------------------------
# Reciprocal rank fusion tests
# ---------------------------------------------------------------------------


def test_rrf_merges_two_result_lists() -> None:
    r1 = programstart_retrieval.SearchResult("doc", "a", "text a", 1.0)
    r2 = programstart_retrieval.SearchResult("doc", "b", "text b", 0.8)
    r3 = programstart_retrieval.SearchResult("doc", "c", "text c", 0.6)
    r4 = programstart_retrieval.SearchResult("doc", "a", "text a", 0.9)  # overlap with r1

    fused = programstart_retrieval.HybridSearcher._reciprocal_rank_fusion(
        lexical_results=[r1, r2],
        vector_results=[r3, r4],
        alpha=0.5,
        top_k=5,
    )
    assert len(fused) == 3  # a, b, c — a appears in both
    # 'a' should be ranked highest since it appears in both lists
    assert fused[0].source_id == "a"


def test_rrf_alpha_zero_favors_lexical() -> None:
    r1 = programstart_retrieval.SearchResult("doc", "lex_top", "lexical winner", 1.0)
    r2 = programstart_retrieval.SearchResult("doc", "vec_top", "vector winner", 1.0)

    fused = programstart_retrieval.HybridSearcher._reciprocal_rank_fusion(
        lexical_results=[r1],
        vector_results=[r2],
        alpha=0.0,
        top_k=5,
    )
    assert fused[0].source_id == "lex_top"


def test_rrf_alpha_one_favors_vector() -> None:
    r1 = programstart_retrieval.SearchResult("doc", "lex_top", "lexical winner", 1.0)
    r2 = programstart_retrieval.SearchResult("doc", "vec_top", "vector winner", 1.0)

    fused = programstart_retrieval.HybridSearcher._reciprocal_rank_fusion(
        lexical_results=[r1],
        vector_results=[r2],
        alpha=1.0,
        top_k=5,
    )
    assert fused[0].source_id == "vec_top"


# ---------------------------------------------------------------------------
# RAG context formatting tests
# ---------------------------------------------------------------------------


def test_rag_format_context() -> None:
    index = _minimal_index()
    chunks = programstart_retrieval.build_corpus(index)
    lexical = programstart_retrieval.LexicalSearcher(chunks)
    searcher = programstart_retrieval.HybridSearcher(lexical)
    rag = programstart_retrieval.RAGAssistant(searcher, model="test-model")

    results = [
        programstart_retrieval.SearchResult("concern", "consent behavior", "consent text", 1.0),
        programstart_retrieval.SearchResult("document", "doc.md", "doc text", 0.9),
    ]
    context = rag._format_context(results)
    assert "[1] (concern: consent behavior)" in context
    assert "[2] (document: doc.md)" in context
    assert "consent text" in context


# ---------------------------------------------------------------------------
# CLI integration tests (lexical only — no external deps)
# ---------------------------------------------------------------------------


def test_cli_search_returns_zero() -> None:
    result = programstart_retrieval.main(["search", "consent"])
    assert result == 0


def test_cli_search_json_output_is_valid() -> None:
    f = io.StringIO()
    with contextlib.redirect_stdout(f):
        result = programstart_retrieval.main(["search", "consent", "--json", "--top-k", "3"])
    assert result == 0
    output = f.getvalue()
    parsed = json.loads(output)
    assert isinstance(parsed, list)


def test_cli_search_top_k() -> None:
    f = io.StringIO()
    with contextlib.redirect_stdout(f):
        result = programstart_retrieval.main(["search", "retrieval", "--json", "--top-k", "2"])
    assert result == 0
    parsed = json.loads(f.getvalue())
    assert len(parsed) <= 2


# ---------------------------------------------------------------------------
# Full context index integration test
# ---------------------------------------------------------------------------


def test_lexical_search_over_full_index() -> None:
    from scripts import programstart_context

    index = programstart_context.build_context_index()
    chunks = programstart_retrieval.build_corpus(index)
    searcher = programstart_retrieval.LexicalSearcher(chunks)

    results = searcher.search("consent activation")
    assert len(results) > 0
    # Should find concrete concern or document entries
    assert any(r.source_type in ("concern", "document") for r in results)


def test_build_retrieval_stack_lexical() -> None:
    from scripts import programstart_context

    index = programstart_context.build_context_index()
    searcher, rag = programstart_retrieval.build_retrieval_stack(index, method="lexical")
    assert rag is None
    results = searcher.search("FastAPI", method="lexical")
    assert any(r.source_id == "FastAPI" for r in results)


def test_corpus_chunk_count_matches_index_scope() -> None:
    index = _minimal_index()
    chunks = programstart_retrieval.build_corpus(index)

    # 2 docs + 2 concerns + 2 stacks + 1 pattern + guidance chunks + 2 routes + 4 commands
    # Guidance: 2 principles + 2 layers + 1 avoid + 1 default_model + 2 best_practices + 1 hnsw + 1 bm25 + 1 hybrid = 11
    expected_min = 2 + 2 + 2 + 1 + 2 + 4  # = 13 minimum
    assert len(chunks) >= expected_min
