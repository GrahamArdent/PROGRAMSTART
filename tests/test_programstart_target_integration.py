from __future__ import annotations

from pathlib import Path

from scripts.programstart_bootstrap_methodology import bootstrap_methodology_repository
from scripts.programstart_target import run_target_command


def test_lean_greenfield_repo_is_operable_from_central_runtime(tmp_path: Path) -> None:
    destination = tmp_path / "EmailBridgeLike"

    bootstrap_methodology_repository(
        destination,
        project_name="EmailBridgeLike",
        variant="product",
    )

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
