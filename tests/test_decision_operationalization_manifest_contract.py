from __future__ import annotations

import json
from pathlib import Path

import jsonschema
import pytest

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((ROOT / "schemas" / "decision-operationalization-manifest.schema.json").read_text(encoding="utf-8"))


def _manifest(role: str = "REFERENCE_PLAN") -> dict[str, Any]:
    return {
        "contract_version": "1.0",
        "record_type": "decision_operationalization_manifest",
        "owner": "GrahamArdent/programstart-compute-spine#135",
        "source_ref": "GrahamArdent/programstart-compute-spine#135",
        "source_version": "issuecomment-6003659425",
        "decision_refs": ["GrahamArdent/programstart-compute-spine#135"],
        "convergence_source": {
            "packet_ref": "disposable_execution_isolation_programstart_convergence_packet.md",
            "packet_hash": "4" * 64,
            "coverage_status": "challenged",
            "evidence_refs": ["PROGRAMSTART Challenge"],
        },
        "projection_role": role,
        "protected_outcome": "A disposable hostile-code boundary is reconstructable without chat.",
        "obligations": [{
            "id": "ISO-01", "outcome": "Host feasibility is proven.", "owner_ref": "GrahamArdent/execution-node-control#335",
            "acceptance_refs": ["fixture:iso-01"], "terminal_refs": ["fixture:terminal"], "invalidation_triggers": []
        }],
        "planned_steps": [{
            "id": "GATE-01", "title": "Prove feasibility", "outcome_supported": ["ISO-01"],
            "owner_ref": "GrahamArdent/execution-node-control#335", "depends_on": [], "gate_refs": [],
            "execution_class": "read_only", "expected_effect_surface": ["execution-node"],
            "acceptance_conditions": ["feasibility evidence exists"], "stop_conditions": ["falsifier fires"]
        }],
        "impact_scope": [{
            "object_id": "GrahamArdent/execution-node-control#335", "object_type": "issue",
            "owner_ref": "GrahamArdent/execution-node-control", "source_ref": "GrahamArdent/programstart-compute-spine#135",
            "impact_type": "host_isolation"
        }],
        "associations": [{
            "source": "ISO-01", "target": "GrahamArdent/execution-node-control#335", "relation": "OWNED_BY",
            "basis_ref": "GrahamArdent/programstart-compute-spine#135", "currentness": "CURRENT"
        }],
        "gates": [{
            "id": "GATE-01", "type": "feasibility", "condition": "candidate is evaluated",
            "pass_condition": "requirements satisfied", "fail_disposition": "reconsider", "owner_ref": "GrahamArdent/programstart-compute-spine#135"
        }],
        "falsifiers": [{"id": "F-01", "condition": "boundary cannot contain hostile code", "consequence": "evaluate stronger isolation"}],
        "exclusions": ["generic shell"], "non_goals": ["second Controller"], "constraints": ["execution_authority=false"],
        "residuals": [], "acceptance_conditions": ["cold reconstruction succeeds"],
        "terminal_condition": "protected outcome is independently proven",
        "invalidation_conditions": ["owner supersedes the plan"], "reconsideration_triggers": ["candidate falsified"],
        "coverage": {"status": "challenged", "method": "independent fixture challenge", "evidence_refs": ["fixture:coverage"], "residuals": []},
        "execution_authority": False,
    }


def test_reference_and_active_manifest_validate() -> None:
    jsonschema.validate(_manifest("REFERENCE_PLAN"), SCHEMA)
    jsonschema.validate(_manifest("ACTIVE_OPERATIONALIZATION"), SCHEMA)


def test_manifest_cannot_grant_execution_authority() -> None:
    data = _manifest()
    data["execution_authority"] = True
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(data, SCHEMA)


def test_challenged_manifest_requires_explicit_reconstruction_fields() -> None:
    data = _manifest()
    data.pop("falsifiers")
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(data, SCHEMA)


def test_association_relation_is_bounded_to_existing_matrix_vocabulary() -> None:
    data = _manifest()
    data["associations"][0]["relation"] = "INVENTED_RELATION"
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(data, SCHEMA)


def test_methodology_requires_owner_reconstruction_before_cold_resumption() -> None:
    planning = (ROOT / "PROGRAMBUILD" / "PROGRAMBUILD_PLANNING_OPERATING_MODEL.md").read_text(encoding="utf-8")
    closure = (ROOT / "docs" / "PROGRAMSTART_DECISION_CLOSURE.md").read_text(encoding="utf-8")
    prompt = (ROOT / ".github" / "prompts" / "programstart-convergence-packet.prompt.md").read_text(encoding="utf-8")
    assert "downloadable delivery alone is not reconstructable durability" in planning
    assert "REFERENCE_PLAN" in planning and "ACTIVE_OPERATIONALIZATION" in planning
    assert "REFERENCE_PLAN" in closure and "ACTIVE_OPERATIONALIZATION" in closure
    assert "durable owner reconstruction reference" in prompt
