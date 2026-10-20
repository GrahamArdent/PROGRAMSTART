from __future__ import annotations

from scripts import programstart_advance as advance


def _quiet_common_preflight(monkeypatch) -> None:
    monkeypatch.setattr(advance.programstart_validate_core, "validate_required_files", lambda *_args, **_kwargs: [])
    monkeypatch.setattr(advance.programstart_validate_core, "validate_metadata", lambda *_args, **_kwargs: [])
    monkeypatch.setattr(advance.programstart_validate_core, "validate_workflow_state", lambda *_args, **_kwargs: [])
    monkeypatch.setattr(advance.programstart_validate_core, "validate_authority_sync", lambda *_args, **_kwargs: [])
    monkeypatch.setattr(advance.programstart_drift_check, "load_changed_files", lambda *_args, **_kwargs: [])
    monkeypatch.setattr(advance, "load_workflow_state", lambda *_args, **_kwargs: {"variant": "lite"})


def test_architecture_preflight_skips_dormant_lite_risk_checks(monkeypatch) -> None:
    _quiet_common_preflight(monkeypatch)
    checks: list[str] = []
    monkeypatch.setattr(
        advance,
        "stage_check_required",
        lambda _registry, check_name, **_kwargs: not check_name.startswith("risk-spikes"),
    )
    monkeypatch.setattr(
        advance.programstart_validate_core,
        "run_stage_gate_check",
        lambda _registry, check_name: checks.append(check_name) or [],
    )

    problems = advance.variant_aware_preflight({}, active_step="architecture_and_risk_spikes")

    assert problems == []
    assert checks == ["architecture-contracts"]


def test_implementation_preflight_keeps_architecture_and_test_checks_when_risk_is_dormant(monkeypatch) -> None:
    _quiet_common_preflight(monkeypatch)
    checks: list[str] = []
    monkeypatch.setattr(
        advance,
        "stage_check_required",
        lambda _registry, check_name, **_kwargs: not check_name.startswith("risk-spikes"),
    )
    monkeypatch.setattr(
        advance.programstart_validate_core,
        "run_stage_gate_check",
        lambda _registry, check_name: checks.append(check_name) or [],
    )

    advance.variant_aware_preflight({}, active_step="implementation_loop")

    assert checks == ["architecture-contracts", "test-strategy-complete"]


def test_active_conditional_checks_are_not_suppressed(monkeypatch) -> None:
    _quiet_common_preflight(monkeypatch)
    checks: list[str] = []
    monkeypatch.setattr(advance, "stage_check_required", lambda *_args, **_kwargs: True)
    monkeypatch.setattr(
        advance.programstart_validate_core,
        "run_stage_gate_check",
        lambda _registry, check_name: checks.append(check_name) or [],
    )

    advance.variant_aware_preflight({}, active_step="architecture_and_risk_spikes")

    assert checks == ["architecture-contracts", "risk-spikes", "risk-spikes-resolved"]


def test_main_delegates_mutation_after_profile_aware_preflight(monkeypatch) -> None:
    monkeypatch.setattr(advance, "load_registry", lambda: {})
    monkeypatch.setattr(advance, "load_workflow_state", lambda *_args, **_kwargs: {"variant": "lite"})
    monkeypatch.setattr(advance, "workflow_active_step", lambda *_args, **_kwargs: "architecture_and_risk_spikes")
    monkeypatch.setattr(advance, "variant_aware_preflight", lambda *_args, **_kwargs: [])
    delegated: list[list[str]] = []
    monkeypatch.setattr(advance, "_delegate", lambda arguments: delegated.append(arguments) or 0)

    result = advance.main(["--system", "programbuild", "--gate-result", "clear"])

    assert result == 0
    assert delegated == [["--system", "programbuild", "--gate-result", "clear", "--skip-preflight"]]


def test_defer_preserves_state_engine_bypass_without_completion_preflight(monkeypatch) -> None:
    delegated: list[list[str]] = []
    monkeypatch.setattr(advance, "_delegate", lambda arguments: delegated.append(arguments) or 0)
    monkeypatch.setattr(
        advance,
        "variant_aware_preflight",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(AssertionError("completion preflight must not run for --defer")),
    )

    result = advance.main(["--system", "programbuild", "--defer", "--notes", "pause for external input"])

    assert result == 0
    assert delegated == [["--system", "programbuild", "--defer", "--notes", "pause for external input"]]


def test_real_invalid_workspace_preflight_prevents_delegate(tmp_path, monkeypatch, capsys):
    import copy

    from scripts import programstart_validate_core as core

    registry = copy.deepcopy(advance.load_registry())
    registry["systems"]["programbuild"]["control_files"] = ["missing.md"]
    registry["systems"]["programbuild"]["output_files"] = []
    (tmp_path / "state.json").write_text('{"current_stage":"research","variant":"product"}')
    original_path = core.workspace_path
    monkeypatch.setattr(core, "workspace_path", lambda p: tmp_path / p if p == "missing.md" else original_path(p))
    monkeypatch.setattr(advance, "load_registry", lambda: registry)
    monkeypatch.setattr(advance, "load_workflow_state", lambda *_: {"current_stage": "research"})
    monkeypatch.setattr(advance, "workflow_active_step", lambda *_: "research")
    monkeypatch.setattr(advance.programstart_drift_check, "git_changed_files", lambda: ["unrelated.md"])
    assert advance.main(["--system", "programbuild"]) == 1
    assert "Advance preflight failed" in capsys.readouterr().out
