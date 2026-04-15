from __future__ import annotations

import json

import pytest

from scripts import check_process_registry_schema


def test_main_validates_loaded_registry(monkeypatch: pytest.MonkeyPatch, tmp_path) -> None:
    schema_path = tmp_path / "schemas" / "process-registry.schema.json"
    schema_path.parent.mkdir(parents=True)
    schema_path.write_text(
        json.dumps(
            {
                "type": "object",
                "required": ["version"],
                "properties": {"version": {"type": "string"}},
            }
        ),
        encoding="utf-8",
    )

    monkeypatch.setattr(check_process_registry_schema, "load_registry_from_path", lambda _path: {"version": "2026-04-15"})
    monkeypatch.setattr(check_process_registry_schema, "workspace_path", lambda relative: tmp_path / relative)

    assert check_process_registry_schema.main() == 0