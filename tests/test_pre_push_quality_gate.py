"""Regression tests for the PROGRAMSTART pre-push quality gate."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
HOOK = ROOT / "scripts" / "hooks" / "pre-push"


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
    env["PATH"] = f"{fake_bin}{os.pathsep}{env.get("PATH", "")}"
    env["PROGRAMSTART_TEST_GATE_LOG"] = str(gate_log)

    result = subprocess.run(
        ["/bin/sh", str(HOOK), "origin", "git@example.invalid:repo.git"],
        input=f"refs/heads/feature/test {'1' * 40} {remote_ref} {'2' * 40}\n",
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
