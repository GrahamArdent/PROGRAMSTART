from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

import jsonschema
import pytest

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads(
    (ROOT / "schemas" / "decision-operationalization-manifest.schema.json").read_text(encoding="utf-8")
)
FIXTURE = ROOT / "tests" / "fixtures" / "decision_closure" / "operationalization_manifest_reference.json"


def _manifest() -> dict[str, Any]:
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def test_reference_and_active_manifest_validate() -> None:
    reference = _manifest()
    jsonschema.validate(reference, SCHEMA)
    active = copy.deepcopy(reference)
    active["projection_role"] = "ACTIVE_OPERATIONALIZATION"
    jsonschema.validate(active, SCHEMA)


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
