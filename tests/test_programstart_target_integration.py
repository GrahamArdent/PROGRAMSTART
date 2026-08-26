from __future__ import annotations

from pathlib import Path

from scripts.programstart_bootstrap_methodology import bootstrap_methodology_repository
from scripts.programstart_target import run_target_command


def _bootstrap_email_bridge_like(destination: Path) -> None:
    bootstrap_methodology_repository(
        destination,
        project_name="EmailBridgeLike",
        variant="product",
    )


def test_lean_greenfield_repo_is_operable_from_central_runtime(tmp_path: Path) -> None:
    destination = tmp_path / "EmailBridgeLike"
    _bootstrap_email_bridge_like(destination)

    assert (destination / "PROGRAMBUILD" / "PROGRAMBUILD_STATE.json").exists()
    assert (destination / "config" / "process-registry.json").exists()
    assert (destination / ".programstart-manifest.json").exists()
    assert (destination / ".github" / "prompts" / "shape-idea.prompt.md").exists()

    # The product remains lean: PROGRAMSTART's executable runtime/test/dashboard tree is not vendored.
    assert not (destination / "scripts").exists()
    assert not (destination / "tests").exists()
    assert not (destination / "dashboard").exists()

    assert run_target_command(destination, ["status", "--system", "programbuild"]) == 0
    assert run_target_command(destination, ["guide", "--system", "programbuild"]) == 0
    assert run_target_command(
        destination,
        ["validate", "--check", "required-files", "--system", "programbuild"],
    ) == 0
    assert run_target_command(
        destination,
        [
            "decide",
            "--decision",
            "Choose the next bounded implementation slice",
            "--mode",
            "c",
            "--impact",
            "medium",
            "--uncertainty",
            "low",
            "--evidence",
            "sufficient",
        ],
    ) == 0


def test_target_project_cannot_shadow_central_programstart_package(tmp_path: Path) -> None:
    destination = tmp_path / "ProjectWithScriptsPackage"
    _bootstrap_email_bridge_like(destination)

    target_scripts = destination / "scripts"
    target_scripts.mkdir()
    (target_scripts / "__init__.py").write_text("# product-owned package\n", encoding="utf-8")
    (target_scripts / "programstart_cli.py").write_text(
        "raise RuntimeError('target scripts package must not shadow central PROGRAMSTART')\n",
        encoding="utf-8",
    )

    assert run_target_command(destination, ["status", "--system", "programbuild"]) == 0
