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
    ],
)
def test_schema_is_valid_json_schema(schema_file: str) -> None:
    schema = json.loads((ROOT / schema_file).read_text(encoding="utf-8"))
    jsonschema.Draft202012Validator.check_schema(schema)
