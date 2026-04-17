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
  - build_context_prompt() Mode B (context-driven prompt generation)
  - main() --mode context CLI routing
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.programstart_common import load_registry
from scripts.programstart_prompt_build import (
    AUTO_HEADER,
    _render_body,
    build_context_prompt,
    build_prompt,
    main,
    managed_stage_prompts,
    sync_managed_prompts,
)

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

    def test_sync_managed_writes_registry_configured_artifacts(self, tmp_path: Path, monkeypatch) -> None:
        registry = {
            "prompt_generation": {
                "artifact_root": "outputs/generated-prompts",
                "managed_stage_prompts": [
                    {"stage": "feasibility", "path": str((tmp_path / "generated" / "feasibility.prompt.md").as_posix())}
                ],
            },
            "systems": load_registry().get("systems", {}),
            "workflow_guidance": load_registry().get("workflow_guidance", {}),
            "sync_rules": load_registry().get("sync_rules", []),
        }
        monkeypatch.setattr("scripts.programstart_prompt_build.ROOT", tmp_path)

        written = sync_managed_prompts(registry=registry)

        assert len(written) == 1
        assert written[0].exists()
        assert AUTO_HEADER in written[0].read_text(encoding="utf-8")

    def test_managed_stage_prompts_returns_registry_entries(self) -> None:
        registry = {
            "prompt_generation": {
                "artifact_root": "outputs/generated-prompts",
                "managed_stage_prompts": [{"stage": "feasibility", "path": "outputs/generated-prompts/feasibility.prompt.md"}],
            }
        }

        result = managed_stage_prompts(registry=registry)

        assert result == [{"stage": "feasibility", "path": "outputs/generated-prompts/feasibility.prompt.md"}]


# ---------------------------------------------------------------------------
# cross-stage-validation reference in all generated prompts
# ---------------------------------------------------------------------------


class TestCrossStageValidationReference:
    @pytest.mark.parametrize(
        "stage_entry",
        [
            pytest.param(stage, id=stage["name"])
            for stage in load_registry().get("systems", {}).get("programbuild", {}).get("stage_order", [])
        ],
    )
    def test_every_stage_references_cross_stage_validation(self, stage_entry: dict) -> None:
        content = build_prompt(stage_entry["name"])
        assert "programstart-cross-stage-validation" in content, (
            f"Stage '{stage_entry['name']}' is missing the cross-stage-validation reference"
        )


# ---------------------------------------------------------------------------
# Mode B — build_context_prompt()
# ---------------------------------------------------------------------------


class TestBuildContextPrompt:
    def test_minimal_context_with_goal_only(self) -> None:
        content = build_context_prompt({"goal": "Build a receipt reader"})
        assert AUTO_HEADER in content
        assert "Build a receipt reader" in content
        assert "Data Grounding Rule" in content
        assert "Protocol" in content
        assert "Verification" in content

    def test_all_well_known_keys(self) -> None:
        ctx = {
            "project": "ReceiptReader",
            "goal": "OCR pipeline for receipts",
            "stage": "architecture",
            "stack": "Python, FastAPI, Supabase",
            "shape": "web-app",
        }
        content = build_context_prompt(ctx)
        assert "ReceiptReader" in content
        assert "OCR pipeline for receipts" in content
        assert "Architecture" in content
        assert "Python, FastAPI, Supabase" in content
        assert "web-app" in content

    def test_extra_custom_keys_in_context(self) -> None:
        ctx = {
            "goal": "Build an API",
            "team_size": "3",
            "deadline": "2026-06-01",
        }
        content = build_context_prompt(ctx)
        assert "Team Size" in content
        assert "3" in content
        assert "Deadline" in content
        assert "2026-06-01" in content

    def test_missing_goal_raises_system_exit(self) -> None:
        with pytest.raises(SystemExit, match="goal"):
            build_context_prompt({})

    def test_empty_goal_raises_system_exit(self) -> None:
        with pytest.raises(SystemExit, match="goal"):
            build_context_prompt({"goal": ""})

    def test_frontmatter_present(self) -> None:
        content = build_context_prompt({"goal": "Test frontmatter"})
        assert "---" in content
        assert "description:" in content
        assert "version:" in content

    def test_defaults_for_missing_optional_keys(self) -> None:
        content = build_context_prompt({"goal": "Test defaults"})
        # Default project name used
        assert "the project" in content
        # Default stage used
        assert "planning" in content.lower()


# ---------------------------------------------------------------------------
# Mode B — CLI routing via main()
# ---------------------------------------------------------------------------


class TestMainModeContext:
    def test_mode_context_stdout(self, capsys: pytest.CaptureFixture) -> None:
        rc = main(["--mode", "context", "--context", "goal=Build a CLI tool"])
        assert rc == 0
        captured = capsys.readouterr()
        assert AUTO_HEADER in captured.out
        assert "Build a CLI tool" in captured.out

    def test_mode_context_to_file(self, tmp_path: Path) -> None:
        out = tmp_path / "ctx.prompt.md"
        rc = main(["--mode", "context", "--context", "goal=Ship it", "--output", str(out)])
        assert rc == 0
        assert out.exists()
        content = out.read_text(encoding="utf-8")
        assert AUTO_HEADER in content
        assert "Ship it" in content

    def test_mode_context_multiple_fields(self, capsys: pytest.CaptureFixture) -> None:
        rc = main(
            [
                "--mode",
                "context",
                "--context",
                "project=Foo",
                "--context",
                "goal=Build Foo",
                "--context",
                "stack=Rust",
            ]
        )
        assert rc == 0
        captured = capsys.readouterr()
        assert "Foo" in captured.out
        assert "Rust" in captured.out

    def test_mode_context_missing_goal_exits(self) -> None:
        with pytest.raises(SystemExit):
            main(["--mode", "context"])

    def test_mode_context_bad_format_exits(self) -> None:
        with pytest.raises(SystemExit):
            main(["--mode", "context", "--context", "no-equals-sign"])

    def test_mode_registry_still_requires_stage(self) -> None:
        with pytest.raises(SystemExit):
            main(["--mode", "registry"])
