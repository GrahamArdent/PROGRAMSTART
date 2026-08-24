from __future__ import annotations

from pathlib import Path

from scripts import programstart_artifact_profiles as profiles
from scripts.programstart_bootstrap import bootstrap_programbuild, bootstrap_shared_assets
from scripts.programstart_common import load_registry

ROOT = Path(__file__).resolve().parents[1]


def _registry() -> dict:
    return {
        "systems": {
            "programbuild": {
                "output_files": ["PROGRAMBUILD/A.md", "PROGRAMBUILD/RISK.md", "PROGRAMBUILD/AUDIT.md"],
                "artifact_profiles": {
                    "lite": {
                        "core_output_files": ["PROGRAMBUILD/A.md"],
                        "conditional_output_files": ["PROGRAMBUILD/RISK.md", "PROGRAMBUILD/AUDIT.md"],
                        "conditional_stage_checks": {
                            "risk-spikes": "PROGRAMBUILD/RISK.md",
                            "audit-complete": "PROGRAMBUILD/AUDIT.md",
                        },
                    }
                },
            }
        }
    }


def test_product_falls_back_to_full_output_set() -> None:
    registry = _registry()
    assert profiles.core_output_files(registry, variant="product") == (
        "PROGRAMBUILD/A.md",
        "PROGRAMBUILD/RISK.md",
        "PROGRAMBUILD/AUDIT.md",
    )
    assert profiles.conditional_output_files(registry, variant="product") == ()


def test_lite_exposes_core_and_conditional_outputs() -> None:
    registry = _registry()
    assert profiles.core_output_files(registry, variant="lite") == ("PROGRAMBUILD/A.md",)
    assert profiles.conditional_output_files(registry, variant="lite") == (
        "PROGRAMBUILD/RISK.md",
        "PROGRAMBUILD/AUDIT.md",
    )


def test_artifact_has_body_uses_explicit_activation_marker(tmp_path: Path) -> None:
    path = tmp_path / "conditional.md"
    path.write_text(
        "Purpose: Test\nActivation: dormant\n---\n\n## Template Heading\n- placeholder\n",
        encoding="utf-8",
    )
    assert not profiles.artifact_has_body(path)

    path.write_text(
        "Purpose: Test\nActivation: active\n---\n\n## Template Heading\n- placeholder\n",
        encoding="utf-8",
    )
    assert profiles.artifact_has_body(path)


def test_artifact_has_body_preserves_legacy_body_fallback(tmp_path: Path) -> None:
    path = tmp_path / "legacy.md"
    path.write_text("Purpose: Test\nOwner: Dev\n---\n\n", encoding="utf-8")
    assert not profiles.artifact_has_body(path)

    path.write_text("Purpose: Test\nOwner: Dev\n---\n\n## Finding\nSomething changed.\n", encoding="utf-8")
    assert profiles.artifact_has_body(path)


def test_real_conditional_templates_are_dormant() -> None:
    assert not profiles.artifact_has_body(ROOT / "PROGRAMBUILD" / "RISK_SPIKES.md")
    assert not profiles.artifact_has_body(ROOT / "PROGRAMBUILD" / "AUDIT_REPORT.md")


def test_lite_bootstrap_preserves_dormancy_until_activation(tmp_path: Path, monkeypatch) -> None:
    registry = load_registry()
    destination = tmp_path / "lite-bootstrap"
    bootstrap_shared_assets(destination, registry, dry_run=False)
    bootstrap_programbuild(destination, registry, "lite", dry_run=False)

    risk = destination / "PROGRAMBUILD" / "RISK_SPIKES.md"
    audit = destination / "PROGRAMBUILD" / "AUDIT_REPORT.md"
    assert "Activation: dormant" in risk.read_text(encoding="utf-8")
    assert "Activation: dormant" in audit.read_text(encoding="utf-8")

    monkeypatch.setattr(profiles, "workspace_path", lambda relative: destination / relative)
    assert profiles.active_conditional_outputs(registry, variant="lite") == ()

    risk.write_text(risk.read_text(encoding="utf-8").replace("Activation: dormant", "Activation: active"), encoding="utf-8")
    assert profiles.active_conditional_outputs(registry, variant="lite") == ("PROGRAMBUILD/RISK_SPIKES.md",)


def test_filter_stage_files_removes_only_dormant_conditional_outputs(tmp_path: Path, monkeypatch) -> None:
    registry = _registry()
    programbuild = tmp_path / "PROGRAMBUILD"
    programbuild.mkdir()
    (programbuild / "RISK.md").write_text(
        "Purpose: Risk\nActivation: dormant\n---\n\n## Spike Register\n| Spike | Result |\n|---|---|\n| | |\n",
        encoding="utf-8",
    )
    (programbuild / "AUDIT.md").write_text(
        "Purpose: Audit\nActivation: active\n---\n\n## Findings\nOne finding.\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(profiles, "workspace_path", lambda relative: tmp_path / relative)

    filtered = profiles.filter_stage_files(
        registry,
        ["PROGRAMBUILD/A.md", "PROGRAMBUILD/RISK.md", "PROGRAMBUILD/AUDIT.md", "CONTROL.md"],
        variant="lite",
    )

    assert filtered == ["PROGRAMBUILD/A.md", "PROGRAMBUILD/AUDIT.md", "CONTROL.md"]


def test_conditional_stage_check_wakes_up_when_activation_changes(tmp_path: Path, monkeypatch) -> None:
    registry = _registry()
    programbuild = tmp_path / "PROGRAMBUILD"
    programbuild.mkdir()
    risk = programbuild / "RISK.md"
    risk.write_text(
        "Purpose: Risk\nActivation: dormant\n---\n\n## Spike Register\n| Spike | Result |\n|---|---|\n| | |\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(profiles, "workspace_path", lambda relative: tmp_path / relative)

    assert not profiles.stage_check_required(registry, "risk-spikes", variant="lite")
    assert profiles.stage_check_required(registry, "requirements-complete", variant="lite")

    risk.write_text(
        "Purpose: Risk\nActivation: active\n---\n\n## Spike Register\nReal spike.\n",
        encoding="utf-8",
    )
    assert profiles.stage_check_required(registry, "risk-spikes", variant="lite")
