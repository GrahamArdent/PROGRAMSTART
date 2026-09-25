from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "decision-closure.schema.json"
FIXTURE_PATH = ROOT / "tests" / "fixtures" / "decision_closure" / "current_conversation.json"
DOC_PATH = ROOT / "docs" / "PROGRAMSTART_DECISION_CLOSURE.md"


def _schema() -> dict:
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def _fixture() -> dict:
    return json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))


def _errors(payload: dict) -> list:
    return sorted(Draft202012Validator(_schema()).iter_errors(payload), key=lambda error: list(error.path))


def test_decision_closure_schema_and_natural_fixture_are_valid() -> None:
    schema = _schema()
    Draft202012Validator.check_schema(schema)
    assert _errors(_fixture()) == []


def test_receipt_and_outcomes_cannot_claim_execution_authority() -> None:
    receipt = _fixture()
    receipt["execution_authority"] = True
    assert _errors(receipt)

    outcome = _fixture()
    outcome["outcomes"][0]["execution_authority"] = True
    assert _errors(outcome)


def test_accepted_outcome_requires_acceptance_evidence() -> None:
    payload = _fixture()
    payload["outcomes"][0].pop("acceptance_evidence_refs")
    assert _errors(payload)


def test_durable_or_routed_outcome_requires_owner_reference() -> None:
    durable = _fixture()
    durable["outcomes"][0].pop("owner_ref")
    assert _errors(durable)

    routed = _fixture()
    routed["outcomes"][4].pop("owner_ref")
    assert _errors(routed)


def test_superseded_outcome_requires_superseding_reference() -> None:
    payload = _fixture()
    payload["outcomes"][3].pop("superseded_by_ref")
    assert _errors(payload)


def test_challenged_coverage_requires_independent_or_adjudicated_evidence() -> None:
    payload = _fixture()
    payload["coverage"]["method"] = "none"
    assert _errors(payload)

    payload = _fixture()
    payload["coverage"]["evidence_refs"] = []
    assert _errors(payload)


def test_fixture_represents_required_natural_conversation_states() -> None:
    outcomes = _fixture()["outcomes"]

    assert any(item["acceptance_state"] == "accepted" and item["currentness_state"] == "current" for item in outcomes)
    assert any(item["disposition"] == "CANDIDATE_PRESERVED" and item["acceptance_state"] == "not_accepted" for item in outcomes)
    assert any(item["disposition"] == "UNRESOLVED" for item in outcomes)
    assert any(item["currentness_state"] == "superseded" for item in outcomes)
    assert any(item["disposition"] == "ROUTED_REFERENCE" and item["authority_state"] == "not_authority" for item in outcomes)


def test_contract_document_preserves_owner_boundaries() -> None:
    doc = DOC_PATH.read_text(encoding="utf-8")

    assert "PROGRAMSTART owns the reusable Decision-Closure semantics" in doc
    assert "Portfolio Operations" in doc
    assert "Owning project repositories" in doc
    assert "Evidence Spine" in doc
    assert "Controller/runtime" in doc
    assert "Matrix/read models" in doc
    assert "Capture != acceptance != authority != execution" in doc
    assert "Distribution/materialization into generated repos is a separate concern" in doc
