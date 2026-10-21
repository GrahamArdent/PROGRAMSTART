"""Static discovery regressions; not live mailbox or independent-chat acceptance."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROUTE = json.loads((ROOT / "config/repository-creation-routing.json").read_text(encoding="utf-8"))


def test_startup_resolves_instruction_and_discovery_reference() -> None:
    entry = (ROOT / ROUTE["entrypoint"]).read_text(encoding="utf-8")
    assert ROUTE["instruction"] in entry
    assert "config/repository-creation-routing.json" in entry
    assert (ROOT / ROUTE["instruction"]).is_file()
    assert ".github/copilot-instructions.md" in entry


def test_instruction_is_available_to_repository_agents() -> None:
    text = (ROOT / ROUTE["instruction"]).read_text(encoding="utf-8")
    assert text.startswith("---\n")
    assert 'applyTo: "**"' in text
    assert "Repository creation is an existing PROGRAMSTART" in text


def test_discovery_does_not_grant_execution_or_arbitrary_target_authority() -> None:
    assert ROUTE["kind"] == "derived_agent_discovery_reference"
    assert ROUTE["execution_authority"] is False
    assert ROUTE["arbitrary_target_admission"] is False
    assert ROUTE["owner_contract"]["refresh_before_use"] is True


def test_existing_factory_remains_an_explicit_opt_in() -> None:
    factory = ROUTE["local_factory"]
    assert factory["command"] == "programstart create"
    assert factory["opt_in_flags"] == ["--github-repo", "--create-github-repo"]
    assert factory["requires_current_authorized_execution_surface"] is True


def test_mailbox_has_actual_invocation_and_result_locations() -> None:
    mailbox = ROUTE["native_mailbox"]
    assert mailbox["repository"] == ROUTE["owner_contract"]["repository"]
    assert mailbox["branch"] == "main"
    assert mailbox["request_path_template"] == "requests/<request_id>.json"
    assert mailbox["result_path_template"] == "results/<request_id>/result.json"
    assert mailbox["action"] == "github_private_repository_create_v1"
    assert mailbox["entry_tools"] == ["GitHub.create_file", "GitHub.fetch_file", "GitHub.get_repo"]
    assert mailbox["repository_evidence_path"] == "dispatcher.evidence.repository_creation"


def test_mailbox_does_not_inherit_unrelated_transport_dependencies() -> None:
    mailbox = ROUTE["native_mailbox"]
    assert mailbox["requires_hosted_desktop_commander"] is False
    assert mailbox["requires_windows"] is False
    assert mailbox["requires_controller_compute"] is False


def test_live_admission_and_release_cannot_be_replaced_by_cached_values() -> None:
    mailbox = ROUTE["native_mailbox"]
    assert mailbox["requires_current_owner_admission"] is True
    assert mailbox["requires_verified_installed_release"] is True
    assert mailbox["copy_historical_runtime_values"] is False
    for field in ("request_id", "created_at", "expires_at", "expected_installed_commit", "arguments"):
        assert field not in mailbox


def test_recovery_does_not_default_to_another_create() -> None:
    mailbox = ROUTE["native_mailbox"]
    assert mailbox["completed_effect_route"] == "read_only_status_or_reconciliation"
    assert mailbox["unknown_effect_route"] == "recover_existing_effect_without_provider_retry"
    assert mailbox["new_target_route"] == "existing_owner_review_release_admission"


def test_success_requires_independent_target_readback() -> None:
    assert ROUTE["native_mailbox"]["requires_independent_target_readback"] is True
    text = (ROOT / ROUTE["instruction"]).read_text(encoding="utf-8")
    assert "Creation and content publication are separate effects" in text
    assert "not permission to retry creation" in text


def test_static_checks_cannot_be_reported_as_fresh_chat_acceptance() -> None:
    acceptance = ROUTE["acceptance"]
    assert acceptance["static_contract_tests"] == "tests/test_repository_creation_discovery.py"
    assert acceptance["independent_fresh_chat_test_required"] is True
    assert acceptance["static_tests_prove_live_execution"] is False

def test_project_owned_agent_entry_is_not_bootstrapped() -> None:
    workspace = json.loads((ROOT / "config/registry/workspace.json").read_text(encoding="utf-8"))
    assets = workspace["workspace"]["bootstrap_assets"]
    assert "AGENTS.md" not in assets
    assert "config/repository-creation-routing.json" in assets
    assert ROUTE["instruction"] in assets
    assert "tests/test_repository_creation_discovery.py" in assets
    source_entry = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    assert "uv run programstart status" in source_entry
    assert "project-owned file" in source_entry
