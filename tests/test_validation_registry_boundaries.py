"""Malformed registry and on-disk policy surfaces yield actionable diagnostics."""

import json
import runpy
from pathlib import Path

import pytest

from scripts import programstart_validate_core as core


@pytest.fixture
def workspace(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(core, "workspace_path", lambda relative: tmp_path / relative)
    return tmp_path


def put(root: Path, name: str, text: str = "content\n") -> Path:
    path = root / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    return path


@pytest.mark.parametrize(
    "class_name,path,reason",
    [
        ("workflow_prompt_files", "docs/not-a-prompt.md", "non-prompt path"),
        ("workflow_prompt_files", ".github/prompts/plain.md", "non-.prompt.md"),
        ("internal_prompt_files", ".github/prompts/public.prompt.md", "outside .github/prompts/internal"),
        ("operator_prompt_files", ".github/prompts/internal/private.prompt.md", "public prompt class"),
        ("operator_prompt_files", ".github/prompts/missing.prompt.md", "missing prompt file"),
    ],
)
def test_prompt_class_registration_is_not_interchangeable(workspace, class_name, path, reason):
    errors = core.validate_prompt_registry_completeness({"prompt_registry": {class_name: [path]}})
    assert any(reason in error for error in errors)


def test_duplicate_and_unregistered_prompts_are_reported(workspace):
    put(workspace, ".github/prompts/internal/nested/new.prompt.md")
    name = ".github/prompts/duplicate.prompt.md"
    registry = {"prompt_registry": {"workflow_prompt_files": [name], "operator_prompt_files": [name]}}
    errors = core.validate_prompt_registry_completeness(registry)
    assert any("duplicates prompt" in error for error in errors)
    assert any("missing on-disk" in error and "nested/new" in error for error in errors)


@pytest.mark.parametrize(
    "change,reason",
    [
        ("foreign", "outside public"),
        ("missing", "missing prompt file"),
        ("empty", "no authority_files"),
        ("duplicates", "duplicate authority_files"),
        ("no-section", "without '## Authority Loading'"),
        ("missing-authority", "missing authority file"),
        ("unmentioned", "text is missing it"),
        ("unregistered", "missing metadata"),
    ],
)
def test_prompt_authority_metadata_requires_real_matching_files(workspace, change, reason):
    name = ".github/prompts/operator.prompt.md"
    put(workspace, name, "## Authority Loading\n\n`authority.md`\n")
    put(workspace, "authority.md")
    registry = {
        "prompt_registry": {"operator_prompt_files": [name]},
        "prompt_authority": {name: {"authority_files": ["authority.md"]}},
    }
    if change == "foreign":
        registry["prompt_registry"] = {}
    elif change == "missing":
        (workspace / name).unlink()
    elif change == "empty":
        registry["prompt_authority"][name]["authority_files"] = []
    elif change == "duplicates":
        registry["prompt_authority"][name]["authority_files"] *= 2
    elif change == "no-section":
        put(workspace, name, "# no authority section\n")
    elif change == "missing-authority":
        (workspace / "authority.md").unlink()
    elif change == "unmentioned":
        put(workspace, name, "## Authority Loading\n\nDifferent authority\n")
    else:
        registry["prompt_authority"] = {}
    assert any(reason in error for error in core.validate_prompt_authority_metadata(registry))


def test_managed_prompt_boundary_rejects_ambiguous_mapping(workspace):
    name = ".github/prompts/operator.prompt.md"
    registry = {
        "prompt_registry": {"operator_prompt_files": [name]},
        "prompt_generation": {
            "artifact_root": "generated",
            "managed_stage_prompts": [
                {"stage": "", "path": ""},
                {"stage": "scope", "path": name},
                {"stage": "scope", "path": name},
            ],
        },
    }
    errors = core.validate_prompt_generation_boundary(registry)
    for reason in [
        "non-empty stage",
        "duplicates managed stage",
        "duplicates managed prompt",
        "outside artifact_root",
        "must not appear",
    ]:
        assert any(reason in error for error in errors)


@pytest.mark.parametrize(
    "entry,reason",
    [
        ({"status": "paired"}, "has no prompt"),
        ({"status": "paired", "prompt": "missing.prompt.md"}, "prompt file missing"),
        ({"status": "paired", "prompt": "present.prompt.md"}, "not registered"),
        ({"status": "other"}, "unrecognized status"),
    ],
)
def test_gameplan_pairing_requires_registered_prompt(workspace, entry, reason):
    put(workspace, "plan.md")
    put(workspace, "present.prompt.md")
    registry = {"gameplan_prompt_policy": {"operator_gameplans": {"plan.md": entry}}}
    assert any(reason in error for error in core.validate_gameplan_prompt_pairing(registry))


def test_boundary_policy_and_bootstrap_references_must_exist(workspace):
    errors = core.validate_repo_boundary_policy({"repo_boundary_policy": {"enabled": True, "docs": [{"path": "missing.md"}]}})
    assert any("missing file" in error for error in errors)
    errors = core.validate_bootstrap_assets(
        {"workspace": {"bootstrap_assets": ["missing.md"]}, "systems": {"userjourney": {"optional": False}}}
    )
    assert any("references missing" in error for error in errors)
    assert core._relative_workspace_path(workspace.parent / "outside.md") == (workspace.parent / "outside.md").as_posix()


def test_malformed_frontmatter_and_readme_rows_are_not_parsed_as_authority():
    assert core._parse_markdown_frontmatter("---\nmissing closing delimiter") == {}
    assert core._parse_markdown_frontmatter("---\ncomment\nstatus: accepted\n---\n") == {"status": "accepted"}
    text = "## Index\n\n| ID | Title | Status | Date |\n|---|---|---|---|\n| plain | bad | accepted | today |\n"
    assert core._adr_readme_entries(text) == {}


def test_adr_index_metadata_and_unknown_decision_are_reported(workspace):
    put(
        workspace,
        "PROGRAMBUILD/DECISION_LOG.md",
        "## Decision Register\n\n| ID | Decision | Status | Related file |\n|---|---|---|---|\n"
        "| DEC-001 | current | ACTIVE | none |\n",
    )
    put(
        workspace,
        "docs/decisions/README.md",
        "## Index\n\n| ID | Title | Status | Date |\n|---|---|---|---|\n| [0001](wrong.md) | Wrong | accepted | yesterday |\n",
    )
    put(
        workspace,
        "docs/decisions/0001-test.md",
        "---\nstatus: accepted\ndate: today\n---\n# 0001. Right title\n<!-- DEC-999 -->\n",
    )
    errors = core.validate_adr_coherence({})
    for reason in ["unknown DECISION_LOG", "target mismatch", "title mismatch", "date mismatch", "points to missing"]:
        assert any(reason in error for error in errors)
    put(workspace, "docs/decisions/0001-test.md", "unstructured")
    errors = core.validate_adr_coherence({})
    assert any("missing YAML" in error for error in errors)
    assert any("missing MADR" in error for error in errors)


@pytest.mark.parametrize(
    "rows,reasons",
    [
        (["DEC-001 | REVERSED | —"], ["REVERSED but Replaces is empty"]),
        (["DEC-001 | REVERSED | DEC-001"], ["cannot reverse itself"]),
        (["DEC-001 | SUPERSEDED | —"], ["SUPERSEDED but Replaces is empty"]),
        (["DEC-001 | SUPERSEDED | DEC-001"], ["cannot supersede itself"]),
        (["DEC-001 | SUPERSEDED | DEC-999"], ["SUPERSEDED by missing"]),
        (["DEC-001 | SUPERSEDED | DEC-002", "DEC-002 | ACTIVE | —"], ["instead of REVERSED", "must point back"]),
        (["DEC-001 | REVERSED | DEC-003", "DEC-002 | REVERSED | DEC-003", "DEC-003 | ACTIVE | —"], ["reversed more than once"]),
        (
            ["DEC-001 | SUPERSEDED | DEC-003", "DEC-002 | SUPERSEDED | DEC-003", "DEC-003 | ACTIVE | —"],
            ["supersedes more than one"],
        ),
    ],
)
def test_decision_reversal_graph_cannot_contradict_itself(workspace, rows, reasons):
    table = "## Decision Register\n\n| ID | Status | Replaces |\n|---|---|---|\n" + "\n".join("| " + row + " |" for row in rows)
    put(workspace, "PROGRAMBUILD/DECISION_LOG.md", table)
    errors = core.validate_decision_log_reversal_invariants({})
    for reason in reasons:
        assert any(reason in error for error in errors)


def test_missing_stage_sections_produce_specific_diagnostics(workspace):
    put(workspace, "PROGRAMBUILD/PROGRAMBUILD_KICKOFF_PACKET.md", "# no fields\n")
    assert any("field not found" in error for error in core.validate_intake_complete({}))
    put(workspace, "PROGRAMBUILD/FEASIBILITY.md", "# no kill criteria\n")
    assert any("no '## Kill Criteria'" in error for error in core.validate_feasibility_criteria({}))
    put(workspace, "PROGRAMBUILD/ARCHITECTURE.md", "# no topology\n")
    assert any("no System Topology" in error for error in core.validate_architecture_contracts({}))
    put(workspace, "PROGRAMBUILD/RELEASE_READINESS.md", "# no decision\n")
    assert any("no '## Go / No-Go" in error for error in core.validate_release_ready({}))


def test_optional_absent_metadata_and_assets_do_not_become_obligations(workspace):
    registry = {
        "systems": {
            "programbuild": {"root": "PROGRAMBUILD", "output_files": []},
            "userjourney": {"root": "unattached-fixture", "optional": True},
        },
        "workspace": {"userjourney_bootstrap_assets": ["unattached-fixture/optional.md"]},
        "metadata_rules": {"required_prefixes": []},
    }
    assert core.validate_metadata(registry, "userjourney") == []
    assert core.metadata_warnings(registry, "userjourney") == []
    assert not any("optional.md" in problem for problem in core.validate_bootstrap_assets(registry))
    assert core.validate_repo_boundary_policy({}) == []
    assert core.validate_gameplan_prompt_pairing({"workspace": {"repo_role": "project_repo"}}) == []


def test_absent_inventory_and_decision_roots_have_empty_results(workspace):
    assert core.validate_test_coverage({}) == []
    assert core.validate_coverage_source_completeness({}) == []
    (workspace / "scripts").mkdir()
    assert core.validate_coverage_source_completeness({}) == []
    assert core.validate_adr_coherence({}) == []
    assert core.validate_decision_log_reversal_invariants({}) == []
    put(workspace, "PROGRAMBUILD/DECISION_LOG.md", "# no register\n")
    assert core.validate_decision_log_reversal_invariants({}) == []


def test_unwired_governance_and_missing_sync_authority_are_reported(workspace):
    registry = {
        "workspace": {"bootstrap_assets": ["scripts/check_new.py"]},
        "systems": {"userjourney": {"optional": True, "root": "unattached-fixture"}},
        "sync_rules": [
            {"name": "required", "authority_files": ["missing-owner.md"], "dependent_files": ["missing-view.md"]},
            {"name": "optional", "system": "userjourney", "authority_files": ["skip.md"], "dependent_files": []},
        ],
    }
    put(workspace, ".github/copilot-instructions.md", "# missing required references\n")
    errors = core.validate_rule_enforcement(registry)
    for reason in ["authority file missing", "dependent file missing", "governance file not covered", "missing rule reference"]:
        assert any(reason in error for error in errors)
    assert not any("skip.md" in error for error in errors)
    assert any(
        "missing gameplan" in error
        for error in core.validate_gameplan_prompt_pairing(
            {"gameplan_prompt_policy": {"operator_gameplans": {"missing.md": {"status": "paired"}}}}
        )
    )


def test_blank_authority_map_row_and_foreign_missing_path(workspace):
    from tests.test_programstart_validate import build_registry, write_programbuild_authority_docs

    registry = build_registry()
    write_programbuild_authority_docs(workspace, [], [])
    path = workspace / "PROGRAMBUILD/PROGRAMBUILD_CANONICAL.md"
    with path.open("a") as handle:
        handle.write(
            "\n## 3. Authority Map\n\n| Concern | Canonical file |\n|---|---|\n| blank | |\n| foreign | `docs/missing.md` |\n"
        )
    errors = core.validate_authority_sync(registry)
    assert any("references missing file: docs/missing.md" in error for error in errors)


def test_planning_allowlist_missing_and_wildcard_entries(workspace):
    registry = {"planning_reference_rules": {"docs": ["plan.md"], "allowlist_manifest": "USERJOURNEY/allow.json"}}
    put(workspace, "plan.md", "`foreign/path.py`\n")
    (workspace / "USERJOURNEY").mkdir()
    assert any("allowlist manifest is missing" in error for error in core.validate_planning_references(registry)[0])
    put(workspace, "USERJOURNEY/allow.json", json.dumps({"allowed_external_paths": ["foreign/*.py"]}))
    assert core.validate_planning_references(registry) == ([], [])
    assert core.load_external_reference_allowlist({}) == set()


def test_standalone_validation_imports_preserve_objective_rejection(workspace, monkeypatch):
    put(workspace, "PROGRAMBUILD/OBJECTIVES.json", "{")
    raw = runpy.run_path(str(Path(core.__file__)), run_name="validation_probe")
    for name in ["validate_implementation_entry_criteria", "validate_prompt_generation_boundary"]:
        function = raw[name]
        monkeypatch.setitem(function.__globals__, "workspace_path", lambda relative: workspace / relative)
        registry = {"prompt_generation": {"artifact_root": "generated", "managed_stage_prompts": []}}
        result = function(registry)
        if name == "validate_implementation_entry_criteria":
            assert result, "invalid objective enrollment must remain a blocker"


@pytest.mark.parametrize(
    "check",
    [
        "workflow-state",
        "authority-sync",
        "repo-boundary",
        "rule-enforcement",
        "adr-coherence",
        "feasibility-criteria",
        "architecture-contracts",
        "risk-spikes",
        "scaffold-complete",
        "implementation-entry",
        "release-ready",
        "audit-complete",
        "post-launch-review",
        "objective-proof",
        "research-admission",
    ],
)
def test_public_validation_selector_reports_named_gate(check, capsys):
    from scripts import programstart_validate as cli

    result = cli.main(["--check", check])
    output = capsys.readouterr().out
    assert result in {0, 1}
    assert output.startswith(("Validation failed", f"Validation passed for check: {check}"))


def test_registry_missing_policy_path_is_reported():
    assert any(
        "missing path" in item
        for item in core.validate_registry(
            {"systems": {}, "sync_rules": [], "repo_boundary_policy": {"enabled": True, "docs": [{}]}}
        )
    )


def test_blank_active_decision_id_is_not_an_adr_requirement(workspace):
    put(
        workspace,
        "PROGRAMBUILD/DECISION_LOG.md",
        "## Decision Register\n\n| ID | Decision | Status |\n|---|---|---|\n"
        "| | unnamed | ACTIVE |\n| DEC-001 | named | ACTIVE |\n",
    )
    warnings = core.validate_adr_coverage({})
    assert len(warnings) == 1 and "DEC-001" in warnings[0]


def test_non_markdown_output_is_not_scanned_as_placeholder_content():
    result = core.placeholder_content_targets({"systems": {"programbuild": {"output_files": ["state.json"]}}})
    assert "state.json" not in result


def test_unindexed_adr_is_reported(workspace):
    put(workspace, "docs/decisions/README.md", "# Index\n")
    put(workspace, "PROGRAMBUILD/DECISION_LOG.md", "# Log\n")
    put(
        workspace,
        "docs/decisions/0001-test.md",
        "---\nstatus: accepted\ndate: 2026-10-20\n---\n# 0001. Test\n\n<!-- DEC-001 -->\n",
    )
    errors = core.validate_adr_coherence({})
    assert any("missing from docs/decisions/README.md index" in error for error in errors)


@pytest.mark.parametrize(
    "check", ["planning-references", "adr-coverage", "prompt-generation", "coverage-source", "file-hygiene", "engineering-ready"]
)
def test_remaining_public_validation_selectors_keep_diagnostics(check, capsys):
    from scripts import programstart_validate as cli

    assert cli.main(["--check", check]) in {0, 1}
    assert capsys.readouterr().out.startswith("Validation")


def test_research_admission_uses_actual_enrollment_file(tmp_path, monkeypatch, capsys):
    from scripts import programstart_validate as cli

    path = tmp_path / "PROGRAMBUILD/RESEARCH_EVIDENCE.json"
    path.parent.mkdir()
    path.write_text("{}")
    monkeypatch.setattr(cli, "workspace_path", lambda relative: tmp_path / relative)
    assert cli.main(["--check", "research-admission"]) == 1
    assert "Objective proof gate blocked" in capsys.readouterr().out


@pytest.mark.parametrize("state_mode", ["unavailable", "research", "journey"])
def test_full_validation_classifies_current_state_failure_and_system_scope(tmp_path, monkeypatch, capsys, state_mode):
    from scripts import programstart_common as common
    from scripts import programstart_validate as cli

    registry = common.load_registry()
    if state_mode == "unavailable":
        original_load = core.load_workflow_state
        reads = []

        def intermittent(*args):
            reads.append(1)
            if len(reads) == 1:
                raise OSError("transient state read failure")
            return original_load(*args)

        monkeypatch.setattr(core, "load_workflow_state", intermittent)
    elif state_mode == "research":
        current = common.load_workflow_state(registry, "programbuild")
        current[registry["workflow_state"]["programbuild"]["active_key"]] = "research"
        path = tmp_path / "state.json"
        path.write_text(json.dumps(current))
        registry["workflow_state"]["programbuild"]["state_file"] = str(path)
    monkeypatch.setattr(cli, "load_registry", lambda: registry)
    result = cli.main(["--check", "all", *(["--system", "userjourney"] if state_mode == "journey" else [])])
    assert result in {0, 1}
    text = capsys.readouterr().out
    if state_mode == "unavailable":
        assert "Objective workflow state unavailable" in text
    else:
        assert text.startswith("Validation")


def test_empty_acceptance_criteria_and_prose_bullets_remain_empty(workspace):
    put(
        workspace,
        "PROGRAMBUILD/REQUIREMENTS.md",
        "## Functional Requirements\n\n| ID | Requirement | Priority |\n|---|---|---|\n"
        "| REQ-001 | Real requirement | P0 |\n\n### Story 1\nAcceptance criteria:",
    )
    assert any("empty acceptance criteria" in x for x in core.validate_requirements_complete({}))
    assert core.extract_bullets_after_marker("Marker\nprose\n- item\n", "Marker") == ["item"]


def test_reference_validation_without_allowlist_manifest_is_supported(workspace):
    assert core.validate_planning_references(
        {"planning_references": {"allowlist_manifest": ""}, "systems": {}, "workspace": {}}
    ) == ([], [])


@pytest.mark.parametrize("check", ["bootstrap-assets", "gameplan-prompt-pairing", "intake-complete"])
def test_named_content_selector_executes_actual_registry_validation(check, capsys):
    from scripts import programstart_validate as cli

    assert cli.main(["--check", check]) in {0, 1}
    assert capsys.readouterr().out.startswith("Validation")


def test_story_without_acceptance_marker_still_validates_requirement_rows(workspace):
    put(workspace, "PROGRAMBUILD/USER_FLOWS.md", "## Main flow\nREQ-001 follows this flow.\n")
    put(
        workspace,
        "PROGRAMBUILD/REQUIREMENTS.md",
        "## Functional Requirements\n\n| ID | Requirement | Priority |\n|---|---|---|\n"
        "| REQ-001 | Real requirement | P0 |\n\n### Story 1\nDescription without acceptance marker.\n",
    )
    assert core.validate_requirements_complete({}) == []
