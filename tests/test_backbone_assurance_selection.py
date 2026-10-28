"""Keep audit protections selected by the repository's normal test command."""

import subprocess
import sys
from pathlib import Path

import pytest

from scripts.programstart_common import load_registry

ROOT = Path(__file__).resolve().parents[1]


def test_default_pytest_discovery_selects_audit_protections() -> None:
    if load_registry()["workspace"]["repo_role"] != "template_repo":
        pytest.skip("The populated backbone audit is maintained only by the template repository")
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "--collect-only", "-q"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    for case in ["test_baseline", "test_fake_case_pass", "test_committed_views_match_register", "test_altered_baseline"]:
        assert f"backbone-assurance/test_register.py::RegisterChecks::{case}" in result.stdout
