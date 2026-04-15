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


# ---------------------------------------------------------------------------
# D-3: Schema version contract
# ---------------------------------------------------------------------------


def test_registry_has_version_key() -> None:
    """D-3: config/process-registry.json must have a top-level 'version' key."""
    registry = json.loads((ROOT / "config" / "process-registry.json").read_text(encoding="utf-8"))
    assert "version" in registry, "process-registry.json is missing the 'version' key"
    assert isinstance(registry["version"], str) and registry["version"]


def test_load_registry_warns_when_version_missing(monkeypatch, tmp_path: Path) -> None:
    """D-3: load_registry() emits a warning when the registry lacks 'version'."""
    import sys
    import warnings

    ROOT_TESTS = Path(__file__).resolve().parents[1]
    if str(ROOT_TESTS) not in sys.path:
        sys.path.insert(0, str(ROOT_TESTS))

    from scripts import programstart_common

    registry_without_version = {"systems": {}, "sync_rules": []}
    reg_path = tmp_path / "config" / "process-registry.json"
    reg_path.parent.mkdir(parents=True)
    reg_path.write_text(json.dumps(registry_without_version), encoding="utf-8")

    monkeypatch.setattr(programstart_common, "workspace_path", lambda rel: tmp_path / rel)

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        programstart_common.load_registry()

    assert any("version" in str(w.message).lower() for w in caught)


# ---------------------------------------------------------------------------
# D-5: pyproject.toml → requirements.txt sync enforcement
# ---------------------------------------------------------------------------


def test_pyproject_direct_deps_present_in_requirements_txt() -> None:
    """D-5: every direct dependency in pyproject.toml appears in requirements.txt."""
    import re

    pyproject_text = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    requirements_text = (ROOT / "requirements.txt").read_text(encoding="utf-8")

    # Extract package names from [project.dependencies]
    dep_section = re.search(r"\[project\]\s.*?dependencies\s*=\s*\[(.*?)\]", pyproject_text, re.DOTALL)
    assert dep_section, "Could not parse [project] dependencies from pyproject.toml"

    req_lower = requirements_text.lower()
    missing = []
    for dep_line in dep_section.group(1).splitlines():
        dep_line = dep_line.strip().strip('",')
        if not dep_line or dep_line.startswith("#"):
            continue
        # Extract bare package name (before any version specifier)
        pkg_name = re.split(r"[>=<!;]", dep_line)[0].strip().lower().replace("-", "_")
        # Accept either hyphenated or underscored package name in requirements.txt
        pkg_hyphen = pkg_name.replace("_", "-")
        if pkg_name not in req_lower and pkg_hyphen not in req_lower:
            missing.append(dep_line)

    assert not missing, f"pyproject.toml deps missing from requirements.txt: {missing}"


def test_registry_pyproject_requirements_sync_rule_exists() -> None:
    """D-5: process-registry.json must document pyproject.toml as authority over requirements.txt."""
    registry = json.loads((ROOT / "config" / "process-registry.json").read_text(encoding="utf-8"))
    sync_names = {rule["name"] for rule in registry.get("sync_rules", [])}
    assert "pyproject_requirements_sync" in sync_names, (
        "sync_rules must include 'pyproject_requirements_sync' documenting pyproject.toml authority"
    )


def test_commit_enforcement_alignment_excludes_entire_pre_commit_file() -> None:
    """Conventional Commits authority must not claim unrelated pre-commit hook edits."""
    registry = json.loads((ROOT / "config" / "process-registry.json").read_text(encoding="utf-8"))
    rule = next(rule for rule in registry.get("sync_rules", []) if rule["name"] == "commit_enforcement_alignment")
    assert ".pre-commit-config.yaml" not in rule["dependent_files"]


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
