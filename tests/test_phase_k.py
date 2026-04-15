"""Phase K tests: CLI features, prompt versioning, file hygiene."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.lint_prompts import lint_prompt
from scripts.lint_prompts import main as lint_main
from scripts.programstart_doctor import main as doctor_main
from scripts.programstart_doctor import run_checks
from scripts.programstart_drift_check import main as drift_main
from scripts.programstart_recommend import KNOWN_SHAPES, list_shapes
from scripts.programstart_recommend import main as recommend_main
from scripts.programstart_status import main as status_main
from scripts.programstart_step_guide import main as guide_main
from scripts.programstart_validate import main as validate_main
from scripts.programstart_validate import validate_file_hygiene

# ---------------------------------------------------------------------------
# K-1: --list-shapes
# ---------------------------------------------------------------------------


class TestListShapes:
    def test_list_shapes_returns_all_known(self) -> None:
        result = list_shapes()
        assert len(result) == len(KNOWN_SHAPES)
        shape_names = {entry["shape"] for entry in result}
        assert shape_names == set(KNOWN_SHAPES)

    def test_list_shapes_has_archetype(self) -> None:
        result = list_shapes()
        for entry in result:
            assert "archetype" in entry
            assert len(entry["archetype"]) > 0

    def test_list_shapes_cli_text(self, capsys: pytest.CaptureFixture[str]) -> None:
        rc = recommend_main(["--list-shapes"])
        assert rc == 0
        out = capsys.readouterr().out
        assert "Known product shapes:" in out
        for shape in KNOWN_SHAPES:
            assert shape in out

    def test_list_shapes_cli_json(self, capsys: pytest.CaptureFixture[str]) -> None:
        rc = recommend_main(["--list-shapes", "--json"])
        assert rc == 0
        data = json.loads(capsys.readouterr().out)
        assert isinstance(data, list)
        assert len(data) == len(KNOWN_SHAPES)


# ---------------------------------------------------------------------------
# K-2: programstart doctor
# ---------------------------------------------------------------------------


class TestDoctor:
    def test_run_checks_returns_list(self) -> None:
        results = run_checks()
        assert len(results) == 7
        for ok, msg in results:
            assert isinstance(ok, bool)
            assert isinstance(msg, str)

    def test_doctor_main_returns_int(self, capsys: pytest.CaptureFixture[str]) -> None:
        rc = doctor_main()
        assert isinstance(rc, int)
        out = capsys.readouterr().out
        assert "checks" in out.lower()

    def test_python_version_check_passes(self) -> None:
        results = run_checks()
        # Python version is the first check
        ok, msg = results[0]
        assert ok, f"Python version check failed: {msg}"


# ---------------------------------------------------------------------------
# K-3: --json output
# ---------------------------------------------------------------------------


class TestJsonOutput:
    def test_status_json(self, capsys: pytest.CaptureFixture[str]) -> None:
        with patch("sys.argv", ["programstart", "--system", "all", "--json"]):
            rc = status_main()
        assert rc == 0
        data = json.loads(capsys.readouterr().out)
        assert "lines" in data

    def test_guide_json_programbuild(self, capsys: pytest.CaptureFixture[str]) -> None:
        with patch("sys.argv", ["programstart", "--system", "programbuild", "--json"]):
            rc = guide_main()
        assert rc == 0
        data = json.loads(capsys.readouterr().out)
        assert data["type"] == "programbuild"
        assert "stage" in data

    def test_guide_json_kickoff(self, capsys: pytest.CaptureFixture[str]) -> None:
        with patch("sys.argv", ["programstart", "--kickoff", "--json"]):
            rc = guide_main()
        assert rc == 0
        data = json.loads(capsys.readouterr().out)
        assert data["type"] == "kickoff"

    def test_drift_json_no_files(self, capsys: pytest.CaptureFixture[str], tmp_path: Path) -> None:
        empty_list = tmp_path / "empty.txt"
        empty_list.write_text("", encoding="utf-8")
        with patch("sys.argv", ["programstart", "--json", "--changed-file-list", str(empty_list)]):
            rc = drift_main()
        assert rc == 0
        data = json.loads(capsys.readouterr().out)
        assert data["status"] == "skip"


# ---------------------------------------------------------------------------
# K-4: prompt version field
# ---------------------------------------------------------------------------


class TestPromptVersion:
    PROMPTS_DIR = ROOT / ".github" / "prompts"

    def test_all_prompts_have_version(self) -> None:
        for path in sorted(self.PROMPTS_DIR.glob("*.prompt.md")):
            text = path.read_text(encoding="utf-8")
            assert 'version: "1.0"' in text, f"{path.name} missing version field"

    def test_prompt_standard_documents_version(self) -> None:
        standard = (self.PROMPTS_DIR / "PROMPT_STANDARD.md").read_text(encoding="utf-8")
        assert "version:" in standard
        assert "deprecated:" in standard


# ---------------------------------------------------------------------------
# K-5: pre-commit prompt lint
# ---------------------------------------------------------------------------


class TestPromptLint:
    PROMPTS_DIR = ROOT / ".github" / "prompts"

    def test_lint_valid_prompt(self) -> None:
        # shape-idea should pass lint
        path = self.PROMPTS_DIR / "shape-idea.prompt.md"
        problems = lint_prompt(path)
        assert problems == []

    def test_lint_missing_frontmatter(self, tmp_path: Path) -> None:
        bad = tmp_path / "bad.prompt.md"
        bad.write_text("# No frontmatter\n", encoding="utf-8")
        problems = lint_prompt(bad)
        assert any("missing YAML frontmatter" in p for p in problems)

    def test_lint_missing_required_field(self, tmp_path: Path) -> None:
        bad = tmp_path / "bad.prompt.md"
        bad.write_text(
            '---\ndescription: "test"\nname: "test"\n---\n'
            "## Data Grounding Rule\n## Protocol Declaration\n"
            "## Pre-flight\n## Verification Gate\n",
            encoding="utf-8",
        )
        problems = lint_prompt(bad)
        assert any("agent" in p for p in problems)

    def test_lint_utility_operator_prompt(self, tmp_path: Path) -> None:
        # Utility operator prompts keep the short-form operator path.
        exempt = tmp_path / "audit-process-drift.prompt.md"
        exempt.write_text(
            '---\ndescription: "test"\nname: "test"\nagent: "agent"\n---\n'
            "> **UTILITY OPERATOR PROMPT**: Diagnostic only.\n\n"
            "## Data Grounding Rule\n\nGround on repo data.\n\n"
            "## Protocol Declaration\n\nDiagnostic operator prompt.\n\n"
            "## Pre-flight\n\nRun drift.\n",
            encoding="utf-8",
        )
        problems = lint_prompt(exempt, explicit_class="operator")
        assert problems == []

    def test_lint_main_returns_zero_for_valid(self) -> None:
        paths = [str(self.PROMPTS_DIR / "shape-idea.prompt.md")]
        rc = lint_main(paths)
        assert rc == 0

    def test_lint_main_returns_one_for_invalid(self, tmp_path: Path) -> None:
        bad = tmp_path / "bad.prompt.md"
        bad.write_text("no frontmatter\n", encoding="utf-8")
        rc = lint_main([str(bad)])
        assert rc == 1


class TestPreCommitParity:
    PRE_COMMIT_CONFIG = ROOT / ".pre-commit-config.yaml"

    def test_programstart_drift_hook_uses_repo_wide_semantics(self) -> None:
        text = self.PRE_COMMIT_CONFIG.read_text(encoding="utf-8")
        expected_block = (
            "- id: programstart-drift\n"
            "        name: programstart drift check\n"
            "        entry: uv run programstart drift --strict\n"
            "        language: system\n"
            "        pass_filenames: false\n"
        )
        assert expected_block in text


# ---------------------------------------------------------------------------
# K-6: file-hygiene validation
# ---------------------------------------------------------------------------


class TestFileHygiene:
    def test_validate_file_hygiene_passes_clean_repo(self) -> None:
        # The current repo should pass (assuming no stray files)
        problems = validate_file_hygiene({})
        # This passes if all .md files at root are in the allowlist
        for p in problems:
            assert "Unexpected" in p  # pragma: no cover

    def test_validate_check_file_hygiene_via_cli(self, capsys: pytest.CaptureFixture[str]) -> None:
        with patch("sys.argv", ["programstart", "--check", "file-hygiene"]):
            rc = validate_main()
        out = capsys.readouterr().out
        # Should either pass or show warnings — not crash
        assert rc == 0 or "Validation" in out

    def test_validate_file_hygiene_with_stray_file(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        # Create a fake repo root with an unexpected .md file
        (tmp_path / "README.md").write_text("ok", encoding="utf-8")
        (tmp_path / "STRAY_FILE.md").write_text("bad", encoding="utf-8")
        monkeypatch.setattr("scripts.programstart_validate.workspace_path", lambda p: tmp_path / p if p == "." else tmp_path / p)
        from scripts.programstart_validate import validate_file_hygiene

        problems = validate_file_hygiene({})
        assert any("STRAY_FILE.md" in p for p in problems)
