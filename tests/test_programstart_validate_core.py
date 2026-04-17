"""Tests for programstart_validate_core.

The bulk of validate-core testing is exercised through
tests/test_programstart_validate.py, which calls the core functions via
the thin ``programstart_validate`` facade.  This file covers import
smoke-testing and any core-only implementation details.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts import programstart_validate_core as validate_core


def test_core_module_exposes_validate_functions() -> None:
    """Smoke-test that the core module exports the expected public API."""
    expected = [
        "validate_intake_complete",
        "validate_authority_sync",
        "validate_required_files",
        "validate_metadata",
        "validate_workflow_state",
        "validate_bootstrap_assets",
        "validate_engineering_ready",
        "run_stage_gate_check",
    ]
    for name in expected:
        assert hasattr(validate_core, name), f"validate_core missing expected name: {name}"
        assert callable(getattr(validate_core, name))
