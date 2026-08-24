from __future__ import annotations

from pathlib import Path

from scripts import programstart_artifact_profiles as profiles


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


def test_artifact_has_body_ignores_metadata_only_stub(tmp_path: Path) -> None:
    path = tmp_path / "stub.md"
    path.write_text("Purpose: Test\nOwner: Dev\n---\n\n", encoding="utf-8")
    assert not profiles.artifact_has_body(path)

    path.write_text("Purpose: Test\nOwner: Dev\n---\n\n## Finding\nSomething changed.\n", encoding="utf-8")
    assert profiles.artifact_has_body(path)


def test_filter_stage_files_removes_only_dormant_conditional_outputs(tmp_path: Path, monkeypatch) -> None:
    registry = _registry()
    programbuild = tmp_path / "PROGRAMBUILD"
    programbuild.mkdir()
    (programbuild / "RISK.md").write_text("Purpose: Risk\n---\n\n", encoding="utf-8")
    (programbuild / "AUDIT.md").write_text("Purpose: Audit\n---\n\n## Findings\nOne finding.\n", encoding="utf-8")
    monkeypatch.setattr(profiles, "workspace_path", lambda relative: tmp_path / relative)

    filtered = profiles.filter_stage_files(
        registry,
        ["PROGRAMBUILD/A.md", "PROGRAMBUILD/RISK.md", "PROGRAMBUILD/AUDIT.md", "CONTROL.md"],
        variant="lite",
    )

    assert filtered == ["PROGRAMBUILD/A.md", "PROGRAMBUILD/AUDIT.md", "CONTROL.md"]


def test_conditional_stage_check_wakes_up_when_artifact_has_content(tmp_path: Path, monkeypatch) -> None:
    registry = _registry()
    programbuild = tmp_path / "PROGRAMBUILD"
    programbuild.mkdir()
    risk = programbuild / "RISK.md"
    risk.write_text("Purpose: Risk\n---\n\n", encoding="utf-8")
    monkeypatch.setattr(profiles, "workspace_path", lambda relative: tmp_path / relative)

    assert not profiles.stage_check_required(registry, "risk-spikes", variant="lite")
    assert profiles.stage_check_required(registry, "requirements-complete", variant="lite")

    risk.write_text("Purpose: Risk\n---\n\n## Spike Register\nReal spike.\n", encoding="utf-8")
    assert profiles.stage_check_required(registry, "risk-spikes", variant="lite")
