from __future__ import annotations

from scripts import programstart_context, programstart_retrieval


def _current_searcher() -> programstart_retrieval.LexicalSearcher:
    index = programstart_context.build_context_index()
    return programstart_retrieval.LexicalSearcher(programstart_retrieval.build_corpus(index))


def _source_ids(results: list[programstart_retrieval.SearchResult]) -> set[str]:
    return {result.source_id for result in results}


def test_search_recovers_contextual_proceed_from_operator_language() -> None:
    searcher = _current_searcher()

    results = searcher.search("contextual proceed intent ingress", top_k=10)

    assert "docs/experiments/CONTEXTUAL_PROCEED_RESOLUTION_V0_2.md" in _source_ids(results)


def test_search_recovers_gate_semantics_from_short_proceed_question() -> None:
    searcher = _current_searcher()

    results = searcher.search("proceed genuine human gate", top_k=10)
    sources = _source_ids(results)

    assert "docs/experiments/CONTEXTUAL_PROCEED_RESOLUTION_V0_2.md" in sources
    assert "docs/PROGRAMSTART_EFFECTIVE_AUTONOMY.md" in sources


def test_search_recovers_effective_autonomy_alternative_actuation() -> None:
    searcher = _current_searcher()

    results = searcher.search("alternative actuation temporary automation gap", top_k=10)

    assert "docs/PROGRAMSTART_EFFECTIVE_AUTONOMY.md" in _source_ids(results)


def test_search_indexes_required_downstream_support_protocols() -> None:
    searcher = _current_searcher()

    authority_gap = searcher.search("authority gap reconciliation", top_k=10)
    effective_autonomy = searcher.search("effective autonomy posture", top_k=10)

    assert "docs/PROGRAMSTART_AUTHORITY_GAP_RECONCILIATION.md" in _source_ids(authority_gap)
    assert "docs/PROGRAMSTART_EFFECTIVE_AUTONOMY.md" in _source_ids(effective_autonomy)
