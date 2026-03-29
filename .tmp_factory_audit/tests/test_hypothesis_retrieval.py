"""Property-based tests for BM25 scoring, tokenization, and build_corpus.

Uses Hypothesis to generate arbitrary inputs and verify invariants that must
always hold regardless of input data.
"""

from __future__ import annotations

# ruff: noqa: I001

from hypothesis import given, settings
from hypothesis import strategies as st

from scripts import programstart_retrieval


# ---------------------------------------------------------------------------
# Tokenizer properties
# ---------------------------------------------------------------------------


@given(text=st.text(min_size=0, max_size=500))
@settings(max_examples=200)
def test_tokenize_always_returns_list(text: str) -> None:
    """Tokenize must always return a list, never raise."""
    result = programstart_retrieval.tokenize(text)
    assert isinstance(result, list)


@given(text=st.text(min_size=0, max_size=500))
@settings(max_examples=200)
def test_tokenize_tokens_are_lowercase(text: str) -> None:
    """Every token returned must be lowercase."""
    for token in programstart_retrieval.tokenize(text):
        assert token == token.lower()


@given(text=st.text(min_size=0, max_size=500))
@settings(max_examples=200)
def test_tokenize_no_stop_words(text: str) -> None:
    """No token should be a stop word."""
    tokens = programstart_retrieval.tokenize(text)
    for token in tokens:
        assert token not in programstart_retrieval._STOP_WORDS


@given(text=st.text(alphabet=st.characters(whitelist_categories=("Lu", "Ll", "Nd")), min_size=1, max_size=100))
@settings(max_examples=100)
def test_tokenize_nonempty_alphanums_produce_tokens(text: str) -> None:
    """A string with alphanumeric characters produces at least one token (unless all stop words)."""
    tokens = programstart_retrieval.tokenize(text)
    # At minimum, the text has alphanumerics, so tokens should be non-empty
    # unless every token is a stop word
    all_raw_tokens = programstart_retrieval._TOKEN_RE.findall(text.lower())
    non_stop = [t for t in all_raw_tokens if t not in programstart_retrieval._STOP_WORDS]
    assert len(tokens) == len(non_stop)


# ---------------------------------------------------------------------------
# BM25 scoring properties
# ---------------------------------------------------------------------------

_SIMPLE_INDEX = {
    "documents": [
        {"path": f"doc{i}.md", "title": f"Document {i}", "purpose": f"purpose {i}", "headings": []}
        for i in range(5)
    ],
    "concerns": [],
    "knowledge_base": {"stacks": [], "integration_patterns": [], "retrieval_guidance": {}},
    "routes": [],
    "commands": {"cli": [], "dashboard": []},
}


def _make_searcher() -> programstart_retrieval.LexicalSearcher:
    chunks = programstart_retrieval.build_corpus(_SIMPLE_INDEX)
    return programstart_retrieval.LexicalSearcher(chunks)


@given(query=st.text(min_size=0, max_size=200))
@settings(max_examples=200)
def test_bm25_search_never_raises(query: str) -> None:
    """BM25 search must never raise on any query string."""
    searcher = _make_searcher()
    results = searcher.search(query)
    assert isinstance(results, list)


@given(query=st.text(min_size=0, max_size=200))
@settings(max_examples=200)
def test_bm25_scores_are_non_negative(query: str) -> None:
    """All BM25 scores must be non-negative."""
    searcher = _make_searcher()
    results = searcher.search(query)
    for r in results:
        assert r.score >= 0.0, f"Negative score: {r.score}"


@given(query=st.text(min_size=0, max_size=200))
@settings(max_examples=200)
def test_bm25_results_are_sorted_descending(query: str) -> None:
    """Results must always be sorted by score descending."""
    searcher = _make_searcher()
    results = searcher.search(query)
    scores = [r.score for r in results]
    assert scores == sorted(scores, reverse=True)


@given(top_k=st.integers(min_value=1, max_value=100))
@settings(max_examples=50)
def test_bm25_respects_top_k(top_k: int) -> None:
    """Result count must never exceed top_k."""
    searcher = _make_searcher()
    results = searcher.search("document purpose", top_k=top_k)
    assert len(results) <= top_k


@given(query=st.text(min_size=0, max_size=200))
@settings(max_examples=100)
def test_bm25_empty_query_tokens_return_empty(query: str) -> None:
    """If all tokens are stop words or non-alphanumeric, result is empty."""
    tokens = programstart_retrieval.tokenize(query)
    if not tokens:
        searcher = _make_searcher()
        results = searcher.search(query)
        assert results == []


# ---------------------------------------------------------------------------
# build_corpus properties
# ---------------------------------------------------------------------------


_STACK_NAMES = st.text(
    alphabet=st.characters(whitelist_categories=("Lu", "Ll", "Nd")),
    min_size=1,
    max_size=30,
)


@given(
    n_docs=st.integers(min_value=0, max_value=20),
    n_stacks=st.integers(min_value=0, max_value=20),
    n_concerns=st.integers(min_value=0, max_value=20),
)
@settings(max_examples=100)
def test_build_corpus_chunk_count_matches_inputs(n_docs: int, n_stacks: int, n_concerns: int) -> None:
    """Number of document/stack/concern chunks should match input counts."""
    index = {
        "documents": [
            {"path": f"d{i}.md", "title": f"D{i}", "headings": []}
            for i in range(n_docs)
        ],
        "concerns": [
            {"concern": f"c{i}", "owner_file": f"o{i}.md", "supporting_files": [], "system": "test"}
            for i in range(n_concerns)
        ],
        "knowledge_base": {
            "stacks": [
                {"name": f"S{i}", "aliases": [], "best_for": [], "strengths": [], "capabilities": [], "risks": []}
                for i in range(n_stacks)
            ],
            "integration_patterns": [],
            "retrieval_guidance": {},
        },
        "routes": [],
        "commands": {"cli": [], "dashboard": []},
    }
    chunks = programstart_retrieval.build_corpus(index)
    doc_chunks = [c for c in chunks if c.source_type == "document"]
    stack_chunks = [c for c in chunks if c.source_type == "stack"]
    concern_chunks = [c for c in chunks if c.source_type == "concern"]
    assert len(doc_chunks) == n_docs
    assert len(stack_chunks) == n_stacks
    assert len(concern_chunks) == n_concerns


def test_build_corpus_empty_index() -> None:
    """An empty index should produce an empty corpus."""
    index = {
        "documents": [],
        "concerns": [],
        "knowledge_base": {"stacks": [], "integration_patterns": [], "retrieval_guidance": {}},
        "routes": [],
        "commands": {"cli": [], "dashboard": []},
    }
    assert programstart_retrieval.build_corpus(index) == []


def test_build_corpus_completely_empty_dict() -> None:
    """An entirely empty dict should produce an empty corpus without raising."""
    assert programstart_retrieval.build_corpus({}) == []


# ---------------------------------------------------------------------------
# LexicalSearcher with empty corpus
# ---------------------------------------------------------------------------


def test_lexical_searcher_empty_corpus_returns_empty() -> None:
    """Searching an empty corpus must return empty results."""
    searcher = programstart_retrieval.LexicalSearcher([])
    results = searcher.search("anything")
    assert results == []


@given(
    k1=st.floats(min_value=0.1, max_value=5.0, allow_nan=False, allow_infinity=False),
    b=st.floats(min_value=0.0, max_value=1.0, allow_nan=False, allow_infinity=False),
)
@settings(max_examples=50)
def test_bm25_params_do_not_crash(k1: float, b: float) -> None:
    """BM25 should handle a wide range of k1 and b parameters without crashing."""
    chunks = programstart_retrieval.build_corpus(_SIMPLE_INDEX)
    searcher = programstart_retrieval.LexicalSearcher(chunks, k1=k1, b=b)
    results = searcher.search("document")
    assert isinstance(results, list)


# ---------------------------------------------------------------------------
# HybridSearcher reciprocal rank fusion properties
# ---------------------------------------------------------------------------


@given(
    alpha=st.floats(min_value=0.0, max_value=1.0, allow_nan=False, allow_infinity=False),
    top_k=st.integers(min_value=1, max_value=50),
)
@settings(max_examples=50)
def test_rrf_respects_top_k_and_alpha(alpha: float, top_k: int) -> None:
    """RRF must always respect top_k limit regardless of alpha."""
    r1 = programstart_retrieval.SearchResult("doc", "a", "text", 1.0)
    r2 = programstart_retrieval.SearchResult("doc", "b", "text", 0.8)
    r3 = programstart_retrieval.SearchResult("doc", "c", "text", 0.6)

    fused = programstart_retrieval.HybridSearcher._reciprocal_rank_fusion(
        lexical_results=[r1, r2],
        vector_results=[r2, r3],
        alpha=alpha,
        top_k=top_k,
    )
    assert len(fused) <= top_k
    # All fused scores must be non-negative
    for r in fused:
        assert r.score >= 0


@given(alpha=st.floats(min_value=0.0, max_value=1.0, allow_nan=False, allow_infinity=False))
@settings(max_examples=50)
def test_rrf_empty_inputs_return_empty(alpha: float) -> None:
    """RRF with no inputs returns empty."""
    fused = programstart_retrieval.HybridSearcher._reciprocal_rank_fusion(
        lexical_results=[],
        vector_results=[],
        alpha=alpha,
        top_k=10,
    )
    assert fused == []
