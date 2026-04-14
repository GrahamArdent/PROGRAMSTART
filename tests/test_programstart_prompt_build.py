"""Tests for scripts/programstart_prompt_build.py.

test_phase_l.py covers the core happy paths.  This file provides
dedicated coverage for uncovered branches and edge cases:
  - build_prompt() with an explicit pre-loaded registry
  - _render_body() for stages with no sync_rules (no rule_name branch)
  - _render_body() for stages with no script list
  - _render_body() for an early stage (id=0, no kill-criteria/shape-conditioning)
  - main() stdout path (no --output flag)
  - main() --list-stages without --json (tabular format)
  - main() Output Ordering "." branch (stage with no sync rule)
"""
from __future__ import annotations

import contextlib
import io
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.programstart_prompt_build import (
    AUTO_HEADER,
    _render_body,
    build_prompt,
    list_stages,
    main,
)
from scripts.programstart_common import load_registry


# ---------------------------------------------------------------------------
# build_prompt — explicit registry parameter (covers `if registry is None` False branch)
# ---------------------------------------------------------------------------

class TestBuildPromptWithExplicitRegistry:
    def test_explicit_registry_skips_reload(self) -> None:
        registry = load_registry()
        content = build_prompt("feasibility", registry=registry)
        assert AUTO_HEADER in content
        assert "Feasibility" in content

    def test_explicit_registry_same_output_as_implicit(self) -> None:
        registry = load_registry()
        via_explicit = build_prompt("feasibility", registry=registry)
        via_implicit = build_prompt("feasibility")
        assert via_explicit == via_implicit


# ---------------------------------------------------------------------------
# _render_body — stage with no sync_rules (covers else: lines.append(".\n"))
# ---------------------------------------------------------------------------

class TestRenderBodyNoSyncRules:
    def test_no_rule_name_outputs_period(self) -> None:
        """A stage dict with no matching sync_rules should produce '. ' in Output Ordering."""
        stage = {
            "name": "test_stage",
            "id": 0,
            "main_output": "PROGRAMBUILD/TEST.md",
            "description": "Test stage",
        }
        guidance: dict = {}
        sync_rules: list = []
        body = _render_body("test_stage", stage, guidance, sync_rules, stage_id=0)
        assert "Output Ordering" in body
        # The period-only output ordering branch
        assert "per `config/process-registry.json` `sync_rules`." in body


# ---------------------------------------------------------------------------
# _render_body — early stage (id=0): no kill criteria, no shape conditioning
# ---------------------------------------------------------------------------

class TestRenderBodyEarlyStage:
    def test_stage_0_has_no_kill_criteria(self) -> None:
        content = build_prompt("inputs_and_mode_selection")
        assert "Kill Criteria" not in content

    def test_stage_0_has_no_shape_conditioning(self) -> None:
        content = build_prompt("inputs_and_mode_selection")
        assert "PRODUCT_SHAPE Conditioning" not in content

    def test_stage_0_has_no_entry_criteria(self) -> None:
        content = build_prompt("inputs_and_mode_selection")
        assert "Entry Criteria Verification" not in content


# ---------------------------------------------------------------------------
# _render_body — stages with scripts listed
# ---------------------------------------------------------------------------

class TestRenderBodyWithScripts:
    def test_stage_with_scripts_lists_them(self) -> None:
        """_render_body with a crafted guidance dict that includes scripts."""
        stage = {
            "name": "feasibility",
            "id": 2,
            "main_output": "PROGRAMBUILD/FEASIBILITY.md",
            "description": "Feasibility",
        }
        guidance = {"scripts": ["uv run programstart validate", "uv run programstart drift"]}
        body = _render_body("feasibility", stage, guidance, sync_rules=[], stage_id=2)
        assert "Available scripts for this stage" in body
        assert "uv run programstart validate" in body


# ---------------------------------------------------------------------------
# main() — stdout output (no --output flag) and --list-stages tabular
# ---------------------------------------------------------------------------

class TestMainOutputPaths:
    def test_stdout_output_no_flag(self, capsys: pytest.CaptureFixture) -> None:
        """--stage without --output should print content to stdout."""
        rc = main(["--stage", "feasibility"])
        assert rc == 0
        captured = capsys.readouterr()
        assert AUTO_HEADER in captured.out
        assert "Feasibility" in captured.out

    def test_list_stages_tabular_format(self, capsys: pytest.CaptureFixture) -> None:
        """--list-stages without --json should print a tabular list."""
        rc = main(["--list-stages"])
        assert rc == 0
        captured = capsys.readouterr()
        # Tabular format has stage names without JSON brackets
        assert "feasibility" in captured.out
        assert "[" not in captured.out

    def test_no_stage_flag_exits(self) -> None:
        """Calling main without --stage or --list-stages should call parser.error."""
        with pytest.raises(SystemExit):
            main([])

    def test_output_to_file(self, tmp_path: Path) -> None:
        out = tmp_path / "out.prompt.md"
        rc = main(["--stage", "feasibility", "--output", str(out)])
        assert rc == 0
        assert out.exists()
        content = out.read_text(encoding="utf-8")
        assert AUTO_HEADER in content


# ---------------------------------------------------------------------------
# cross-stage-validation reference in all generated prompts
# ---------------------------------------------------------------------------

class TestCrossStageValidationReference:
    @pytest.mark.parametrize("stage_entry", [
        pytest.param(stage, id=stage["name"])
        for stage in load_registry().get("systems", {}).get("programbuild", {}).get("stage_order", [])
    ])
    def test_every_stage_references_cross_stage_validation(self, stage_entry: dict) -> None:
        content = build_prompt(stage_entry["name"])
        assert "programstart-cross-stage-validation" in content, (
            f"Stage '{stage_entry['name']}' is missing the cross-stage-validation reference"
        )
