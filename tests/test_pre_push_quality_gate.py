"""Regression tests for the PROGRAMSTART pre-push quality gate."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
HOOK = ROOT / "scripts" / "hooks" / "pre-push"
SOURCE_JIT = ROOT / ".github" / "instructions" / "source-of-truth.instructions.md"
COPILOT_INSTRUCTIONS = ROOT / ".github" / "copilot-instructions.md"
QUICKSTART = ROOT / "QUICKSTART.md"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _run_hook(
    tmp_path: Path,
    gate_exit_code: int,
    remote_ref: str = "refs/heads/feature/test",
) -> tuple[subprocess.CompletedProcess[str], Path]:
    if os.name == "nt":
        pytest.skip("Shell hook execution is covered on the Linux CI runner")

    fake_bin = tmp_path / "bin"
    fake_bin.mkdir()
    gate_log = tmp_path / "gate.log"
    fake_uv = fake_bin / "uv"
    fake_uv.write_text(
        "#!/bin/sh\n"
        "printf '%s\\n' \"$*\" > \"$PROGRAMSTART_TEST_GATE_LOG\"\n"
        f"exit {gate_exit_code}\n",
        encoding="utf-8",
    )
    fake_uv.chmod(0o755)

    env = os.environ.copy()
    current_path = env.get("PATH", "")
    env["PATH"] = f"{fake_bin}{os.pathsep}{current_path}"
    env["PROGRAMSTART_TEST_GATE_LOG"] = str(gate_log)

    local_oid = "1" * 40
    remote_oid = "2" * 40
    result = subprocess.run(
        ["/bin/sh", str(HOOK), "origin", "git@example.invalid:repo.git"],
        input=f"refs/heads/feature/test {local_oid} {remote_ref} {remote_oid}\n",
        text=True,
        capture_output=True,
        cwd=ROOT,
        env=env,
        check=False,
    )
    return result, gate_log


def test_pre_push_runs_repo_owned_gate_before_feature_publish(tmp_path: Path) -> None:
    result, gate_log = _run_hook(tmp_path, gate_exit_code=0)

    assert result.returncode == 0
    assert gate_log.read_text(encoding="utf-8").strip() == "run nox -s gate_safe"
    assert "local confidence gate" in result.stderr


def test_pre_push_blocks_feature_publish_when_local_gate_fails(tmp_path: Path) -> None:
    result, gate_log = _run_hook(tmp_path, gate_exit_code=1)

    assert result.returncode == 1
    assert gate_log.read_text(encoding="utf-8").strip() == "run nox -s gate_safe"
    assert "fix the failure before pushing" in result.stderr


def test_main_branch_policy_blocks_before_quality_gate(tmp_path: Path) -> None:
    result, gate_log = _run_hook(tmp_path, gate_exit_code=0, remote_ref="refs/heads/main")

    assert result.returncode == 1
    assert not gate_log.exists()
    assert "direct push to 'main' is blocked" in result.stderr


def test_main_override_still_requires_quality_gate(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("PROGRAMSTART_ALLOW_MAIN_PUSH", "1")
    result, gate_log = _run_hook(tmp_path, gate_exit_code=1, remote_ref="refs/heads/main")

    assert result.returncode == 1
    assert gate_log.read_text(encoding="utf-8").strip() == "run nox -s gate_safe"
    assert "local confidence gate failed" in result.stderr


def test_worker_instructions_cover_hook_bypassing_publication_paths() -> None:
    source_jit = _read(SOURCE_JIT)
    copilot = _read(COPILOT_INSTRUCTIONS)
    quickstart = _read(QUICKSTART)

    sequence = (
        "edit -> deterministic fix -> local validation -> commit -> "
        "pre-push validation -> GitHub authoritative verification"
    )

    assert sequence in source_jit
    assert sequence in quickstart
    assert "Direct GitHub/API/connector writes bypass local hooks" in source_jit
    assert "API/connector publication paths bypass Git hooks" in copilot
    assert "Autonomous auto-fix is bounded to two mutation passes" in copilot
    assert "GitHub Actions remains the independent authoritative verification layer" in quickstart
