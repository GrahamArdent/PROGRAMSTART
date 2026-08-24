from __future__ import annotations

import pytest

from scripts.programstart_evidence import (
    EvidenceRecord,
    assess_evidence,
    evaluate_evidence,
    impact_causes,
)
from scripts.programstart_graph import DependencyGraph


def _relation(dependent: str, prerequisite: str) -> dict:
    return {
        "type": "depends_on",
        "from": dependent,
        "to": prerequisite,
        "source": "test",
    }


def test_evidence_id_is_required() -> None:
    with pytest.raises(ValueError, match="evidence_id"):
        EvidenceRecord(evidence_id="  ")


def test_unrelated_change_does_not_invalidate_evidence() -> None:
    record = EvidenceRecord(
        evidence_id="api-contract-test",
        scopes=("api",),
        depends_on=("openapi-contract",),
        observed_at="2026-01-01",
    )

    assessment = assess_evidence(record, changed_surfaces={"marketing-copy"})

    assert assessment.valid
    assert assessment.invalidated_surfaces == ()


def test_direct_scope_change_invalidates_evidence() -> None:
    record = EvidenceRecord(evidence_id="api-smoke", scopes=("api",))

    assessment = assess_evidence(record, changed_surfaces={"api"})

    assert not assessment.valid
    assert assessment.invalidated_surfaces == ("api",)
    assert assessment.causes[0].path == ("api",)
    assert not assessment.causes[0].propagated


def test_direct_dependency_change_invalidates_evidence() -> None:
    record = EvidenceRecord(evidence_id="ui-contract", scopes=("ui",), depends_on=("api-contract",))

    assessment = assess_evidence(record, changed_surfaces={"api-contract"})

    assert not assessment.valid
    assert assessment.invalidated_surfaces == ("api-contract",)


def test_dependency_graph_propagates_change_to_downstream_evidence_scope() -> None:
    graph = DependencyGraph(
        [
            _relation("architecture", "requirements"),
            _relation("implementation", "architecture"),
        ]
    )
    record = EvidenceRecord(evidence_id="implementation-tests", scopes=("implementation",))

    assessment = assess_evidence(
        record,
        changed_surfaces={"requirements"},
        graph=graph,
    )

    assert not assessment.valid
    assert assessment.invalidated_surfaces == ("implementation",)
    cause = assessment.causes[0]
    assert cause.trigger == "requirements"
    assert cause.path == ("requirements", "architecture", "implementation")
    assert cause.propagated


def test_bounded_invalidation_can_limit_propagation_depth() -> None:
    graph = DependencyGraph(
        [
            _relation("architecture", "requirements"),
            _relation("implementation", "architecture"),
        ]
    )
    record = EvidenceRecord(evidence_id="implementation-tests", scopes=("implementation",))

    assessment = assess_evidence(
        record,
        changed_surfaces={"requirements"},
        graph=graph,
        max_depth=1,
    )

    assert assessment.valid


def test_age_is_metadata_not_an_invalidation_trigger() -> None:
    record = EvidenceRecord(
        evidence_id="old-but-current",
        scopes=("stable-contract",),
        observed_at="2020-01-01",
    )

    assessment = assess_evidence(record, changed_surfaces=set())

    assert assessment.valid


def test_batch_evaluation_partitions_valid_and_invalidated_evidence() -> None:
    records = [
        EvidenceRecord(evidence_id="api", scopes=("api",)),
        EvidenceRecord(evidence_id="database", scopes=("database",)),
        EvidenceRecord(evidence_id="ui", scopes=("ui",), depends_on=("api",)),
    ]

    evaluation = evaluate_evidence(records, changed_surfaces={"api"})

    assert [record.evidence_id for record in evaluation.valid_evidence] == ["database"]
    assert [record.evidence_id for record in evaluation.invalidated_evidence] == ["api", "ui"]
    assert evaluation.changed_surfaces == ("api",)
    assert evaluation.impacted_surfaces == ("api",)


def test_batch_evaluation_reports_transitive_impacted_surfaces() -> None:
    graph = DependencyGraph(
        [
            _relation("architecture", "requirements"),
            _relation("implementation", "architecture"),
        ]
    )

    evaluation = evaluate_evidence(
        [EvidenceRecord(evidence_id="impl", scopes=("implementation",))],
        changed_surfaces={"requirements"},
        graph=graph,
    )

    assert evaluation.impacted_surfaces == ("architecture", "implementation", "requirements")


def test_multiple_change_triggers_preserve_each_invalidation_path() -> None:
    graph = DependencyGraph(
        [
            _relation("implementation", "architecture"),
            _relation("implementation", "database"),
        ]
    )
    record = EvidenceRecord(evidence_id="implementation-tests", scopes=("implementation",))

    assessment = assess_evidence(
        record,
        changed_surfaces={"architecture", "database"},
        graph=graph,
    )

    assert [cause.trigger for cause in assessment.causes] == ["architecture", "database"]
    assert {cause.path for cause in assessment.causes} == {
        ("architecture", "implementation"),
        ("database", "implementation"),
    }


def test_impact_causes_without_graph_contains_only_direct_changes() -> None:
    causes = impact_causes({"b", "a"})

    assert tuple(causes) == ("a", "b")
    assert causes["a"][0].path == ("a",)
    assert causes["b"][0].path == ("b",)
