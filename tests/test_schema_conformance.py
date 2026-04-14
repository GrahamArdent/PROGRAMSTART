"""Validate JSON data files against their schemas."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

try:
    import jsonschema
except ImportError:
    pytest.skip("jsonschema not installed", allow_module_level=True)

ROOT = Path(__file__).resolve().parent.parent


@pytest.mark.parametrize(
    "data_file, schema_file",
    [
        ("PROGRAMBUILD/PROGRAMBUILD_STATE.json", "schemas/programbuild-state.schema.json"),
        ("USERJOURNEY/USERJOURNEY_STATE.json", "schemas/userjourney-state.schema.json"),
        ("config/process-registry.json", "schemas/process-registry.schema.json"),
        ("config/knowledge-base.json", "schemas/knowledge-base.schema.json"),
        ("config/prompt-eval-scenarios.json", "schemas/prompt-eval-scenarios.schema.json"),
    ],
)
def test_data_conforms_to_schema(data_file: str, schema_file: str) -> None:
    data_path = ROOT / data_file
    if not data_path.exists():
        pytest.skip(f"{data_file} not present")
    data = json.loads(data_path.read_text(encoding="utf-8"))
    schema = json.loads((ROOT / schema_file).read_text(encoding="utf-8"))
    jsonschema.validate(instance=data, schema=schema)


@pytest.mark.parametrize(
    "schema_file",
    [
        "schemas/programbuild-state.schema.json",
        "schemas/userjourney-state.schema.json",
        "schemas/process-registry.schema.json",
        "schemas/knowledge-base.schema.json",
        "schemas/prompt-eval-scenarios.schema.json",
    ],
)
def test_schema_is_valid_json_schema(schema_file: str) -> None:
    schema = json.loads((ROOT / schema_file).read_text(encoding="utf-8"))
    jsonschema.Draft202012Validator.check_schema(schema)


def test_programbuild_state_keys_subset_of_registry_stages() -> None:
    """Stage keys in the state file must be a subset of registry stage_order names."""
    state_path = ROOT / "PROGRAMBUILD" / "PROGRAMBUILD_STATE.json"
    if not state_path.exists():
        pytest.skip("PROGRAMBUILD_STATE.json not present")
    registry = json.loads((ROOT / "config" / "process-registry.json").read_text(encoding="utf-8"))
    state = json.loads(state_path.read_text(encoding="utf-8"))
    valid_stages = {s["name"] for s in registry["systems"]["programbuild"]["stage_order"]}
    actual_stages = set(state.get("stages", {}).keys())
    assert actual_stages <= valid_stages, f"Unknown stages: {actual_stages - valid_stages}"
    assert state.get("active_stage") in valid_stages


def test_userjourney_state_keys_subset_of_registry_phases() -> None:
    """Phase keys in the state file must be a subset of registry step_order names."""
    state_path = ROOT / "USERJOURNEY" / "USERJOURNEY_STATE.json"
    if not state_path.exists():
        pytest.skip("USERJOURNEY_STATE.json not present")
    registry = json.loads((ROOT / "config" / "process-registry.json").read_text(encoding="utf-8"))
    state = json.loads(state_path.read_text(encoding="utf-8"))
    valid_phases = set(registry["workflow_state"]["userjourney"]["step_order"])
    actual_phases = set(state.get("phases", {}).keys())
    assert actual_phases <= valid_phases, f"Unknown phases: {actual_phases - valid_phases}"
    assert state.get("active_phase") in valid_phases
