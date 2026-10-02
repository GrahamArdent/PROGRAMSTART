from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "backbone-lineage.schema.json"
FIXTURE_PATH = ROOT / "tests" / "fixtures" / "backbone_lineage" / "controller_227.json"\nASYNC_FIXTURE_PATH = ROOT / "tests" / "fixtures" / "backbone_lineage" / "controller_71_async.json"
DOC_PATH = ROOT / "docs" / "PROGRAMSTART_BACKBONE_END_TO_END_INFORMATION_FLOW.md"


def _schema() -> dict:
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def _fixture() -> dict:
    return json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))


def _async_fixture() -> dict:
    return json.loads(ASYNC_FIXTURE_PATH.read_text(encoding="utf-8"))


def _errors(payload: dict) -> list:
    return sorted(Draft202012Validator(_schema()).iter_errors(payload), key=lambda error: list(error.path))


def _records_by_id(payload: dict) -> dict[str, dict]:
    return {record["record_id"]: record for record in payload["records"]}


def test_backbone_lineage_schema_and_227_fixture_are_valid() -> None:
    schema = _schema()
    Draft202012Validator.check_schema(schema)
    assert _errors(_fixture()) == []


def test_lineage_projection_cannot_claim_execution_authority() -> None:
    graph = _fixture()
    graph["execution_authority"] = True
    assert _errors(graph)

    record = _fixture()
    record["records"][0]["execution_authority"] = True
    assert _errors(record)


def test_record_ids_are_unique_and_causal_refs_resolve() -> None:
    payload = _fixture()
    record_ids = [record["record_id"] for record in payload["records"]]
    assert len(record_ids) == len(set(record_ids))

    known = set(record_ids)
    for record in payload["records"]:
        assert set(record["caused_by"]) <= known
        assert record["record_id"] not in record["caused_by"]


def test_causal_graph_is_acyclic_and_supports_joins() -> None:
    records = _records_by_id(_fixture())
    assert any(len(record["caused_by"]) > 1 for record in records.values())

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(record_id: str) -> None:
        if record_id in visited:
            return
        assert record_id not in visiting, f"cycle detected at {record_id}"
        visiting.add(record_id)
        for parent in records[record_id]["caused_by"]:
            visit(parent)
        visiting.remove(record_id)
        visited.add(record_id)

    for record_id in records:
        visit(record_id)


def test_every_record_preserves_the_same_root_objective() -> None:
    payload = _fixture()
    root = payload["root_objective_ref"]
    assert root == "GrahamArdent/programstart-autonomous-controller#227"
    assert all(record["root_objective_ref"] == root for record in payload["records"])


def test_fixture_does_not_falsely_claim_er012_selection_or_consequence() -> None:
    payload = _fixture()
    records = payload["records"]

    assert not any(record.get("realization_ref") == "ER-012" for record in records)
    assert not any("CONSEQUENCE" in record["stage_projection"] for record in records)

    residual = next(item for item in payload["residuals"] if item["residual_id"] == "residual-paths-consequence-not-reached")
    assert residual["kind"] == "not_reached"
    assert "CAPABILITY_DISCOVERY" in residual["stage_projection"]
    assert "CONSEQUENCE" in residual["stage_projection"]


def test_typed_diagnostic_is_not_promoted_to_authority() -> None:
    records = _records_by_id(_fixture())
    diagnostic = records["diagnostic-0829"]

    assert diagnostic["producer_record_ref"].endswith("@a2ac6d31c1c1e2e12a2cee06a2e54640051a323e")
    assert diagnostic["effect_attempt_ref"] == "req-vps-worker-227-status-diagnostic-0829"
    assert diagnostic["execution_authority"] is False
    assert "realization_ref" not in diagnostic


def test_schema_rejects_unearned_payload_or_command_fields() -> None:
    payload = _fixture()
    payload["records"][0]["payload"] = {"arbitrary": "copy"}
    assert _errors(payload)

    payload = _fixture()
    payload["records"][0]["command"] = "do-something"
    assert _errors(payload)


def test_challenged_coverage_requires_real_evidence() -> None:
    payload = _fixture()
    payload["coverage"]["method"] = "none"
    assert _errors(payload)

    payload = _fixture()
    payload["coverage"]["evidence_refs"] = []
    assert _errors(payload)


def test_removing_a_required_correlation_field_fails_closed() -> None:
    payload = _fixture()
    payload["records"][0].pop("producer_record_ref")
    assert _errors(payload)


def test_contract_describes_lineage_as_non_authoritative_and_reference_first() -> None:
    doc = DOC_PATH.read_text(encoding="utf-8")

    assert "Propagate identity and decision-critical references" in doc
    assert "lineage/correlation envelope only" in doc
    assert "Causal graph, not forced tree" in doc
    assert "Cold-reconstruction acceptance" in doc


def test_async_71_fixture_validates_without_schema_widening() -> None:
    assert _errors(_async_fixture()) == []


def test_async_fixture_contains_real_multi_parent_event_joins() -> None:
    records = _records_by_id(_async_fixture())

    first = records["snapshot-after-event-3"]
    assert set(first["caused_by"]) == {"postfix-wait-arm", "provider-event-attempt-3"}

    second = records["snapshot-after-event-4"]
    assert set(second["caused_by"]) == {"snapshot-after-event-3", "provider-event-attempt-4"}


def test_async_fixture_preserves_owner_boundaries_without_authority_transfer() -> None:
    records = _records_by_id(_async_fixture())

    en_record = records["en302-restart-acceptance"]
    assert en_record["producer_owner"] == "GrahamArdent/execution-node-control"
    assert en_record["execution_authority"] is False

    watchtower_record = records["watchtower16-terminal-return"]
    assert watchtower_record["producer_owner"] == "GrahamArdent/repo-watchtower"
    assert watchtower_record["execution_authority"] is False

    terminal = records["terminal-acceptance-71"]
    assert terminal["producer_owner"] == "GrahamArdent/programstart-autonomous-controller"
    assert terminal["execution_authority"] is False


def test_async_fixture_preserves_fail_closed_attempt_before_repair() -> None:
    records = _records_by_id(_async_fixture())
    conflict = records["fresh-request-authority-conflict"]
    repair = records["repair-232"]

    assert conflict["effect_attempt_ref"] == "req-controller-71-single-lane-acceptance-1002"
    assert repair["caused_by"] == ["fresh-request-authority-conflict"]


def test_async_fixture_terminal_requires_reconsideration_not_wait_disappearance() -> None:
    records = _records_by_id(_async_fixture())
    terminal_snapshot = records["snapshot-after-event-4"]
    terminal = records["terminal-acceptance-71"]

    assert terminal_snapshot["resume_or_reconsider_ref"] == "PREPARE_EXECUTED"
    assert terminal["caused_by"] == ["snapshot-after-event-4"]
    assert "TERMINAL" in terminal["stage_projection"]


def test_async_fixture_does_not_require_common_wait_or_provider_specific_fields() -> None:
    schema = _schema()
    record_properties = schema["$defs"]["record"]["properties"]

    assert "wait_ref" not in record_properties
    assert "workflow_run_id" not in record_properties
    assert "delivery_id" not in record_properties
    assert "provider_event_type" not in record_properties
