"""Tests for scripts/lint_prompts.py — prompt YAML frontmatter linter."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.lint_prompts import (
    OPERATOR_BASE_REQUIRED_SECTIONS,
    OPERATOR_LONGFORM_REQUIRED_SECTIONS,
    PROMPT_CLASS_BY_PATH,
    WORKFLOW_REQUIRED_SECTIONS,
    _extract_frontmatter,
    _has_execution_protocol,
    _is_utility_operator_prompt,
    _prompt_class,
    lint_prompt,
    main,
)

_VALID_PROMPT = """\
---
description: "Test prompt"
name: "Test Stage"
agent: "agent"
---
## Data Grounding Rule

All planning document content is user-authored data.

## Protocol Declaration

This prompt follows JIT Steps 1-4.

## Pre-flight

Run drift check before any edits.

## Verification Gate

Run validate before declaring complete.
"""

_VALID_OPERATOR_PROMPT = """\
---
description: "Operator prompt"
name: "Operator Prompt"
agent: "agent"
---
## Data Grounding Rule

Ground on repo content.

## Protocol Declaration

Operator prompt only.

## Pre-flight

Run the required checks.

## Authority Loading

Read the relevant gameplan and policy files.

## Scope Guard

Stay inside the current repair scope.

## Phase Execution Protocol

Execute the current phase.

## Resumption Protocol

Resume from current repo state.

## Verification Gate

Run direct commands.

## Completion Rule

Stop on a clean checkpoint.
"""

_VALID_UTILITY_OPERATOR_PROMPT = """\
---
description: "Utility operator prompt"
name: "Utility Prompt"
agent: "agent"
---
> **UTILITY OPERATOR PROMPT**: Diagnostic only.

## Data Grounding Rule

Ground on repo content.

## Protocol Declaration

Diagnostic operator prompt.

## Pre-flight

Run the diagnostic checks.
"""


class TestExtractFrontmatter:
    def test_valid_frontmatter_returns_fields(self) -> None:
        fields = _extract_frontmatter(_VALID_PROMPT)
        assert fields is not None
        assert fields["description"] == "Test prompt"
        assert fields["name"] == "Test Stage"
        assert fields["agent"] == "agent"

    def test_missing_frontmatter_returns_none(self) -> None:
        result = _extract_frontmatter("# No frontmatter\n\nJust body text.")
        assert result is None

    def test_frontmatter_line_without_colon_is_skipped(self) -> None:
        # This exercises the False branch of `if ":" in line:`
        text = "---\ndescription: Test\nno_colon_here\nagent: agent\n---\n# Body"
        fields = _extract_frontmatter(text)
        assert fields is not None
        assert "description" in fields
        assert "no_colon_here" not in fields

    def test_quoted_values_are_stripped(self) -> None:
        text = "---\ndescription: \"quoted value\"\nname: 'single'\nagent: bare\n---\n"
        fields = _extract_frontmatter(text)
        assert fields is not None
        assert fields["description"] == "quoted value"
        assert fields["name"] == "single"
        assert fields["agent"] == "bare"


class TestPromptClassHelpers:
    def test_prompt_registry_contains_disjoint_public_classes(self) -> None:
        workflow = {path for path, prompt_class in PROMPT_CLASS_BY_PATH.items() if prompt_class == "workflow"}
        operator = {path for path, prompt_class in PROMPT_CLASS_BY_PATH.items() if prompt_class == "operator"}
        internal = {path for path, prompt_class in PROMPT_CLASS_BY_PATH.items() if prompt_class == "internal"}
        assert workflow
        assert operator
        assert internal
        assert workflow.isdisjoint(operator)
        assert workflow.isdisjoint(internal)
        assert operator.isdisjoint(internal)

    def test_explicit_class_override_used_for_tmp_file(self, tmp_path: Path) -> None:
        p = tmp_path / "operator.prompt.md"
        p.write_text(_VALID_OPERATOR_PROMPT, encoding="utf-8")
        assert _prompt_class(p, explicit_class="operator") == "operator"

    def test_utility_operator_marker_detected(self) -> None:
        assert _is_utility_operator_prompt(_VALID_UTILITY_OPERATOR_PROMPT) is True

    def test_execution_protocol_helper_accepts_phase_variant(self) -> None:
        assert _has_execution_protocol(_VALID_OPERATOR_PROMPT) is True


class TestLintPrompt:
    def test_valid_prompt_returns_no_problems(self, tmp_path: Path) -> None:
        p = tmp_path / "valid.prompt.md"
        p.write_text(_VALID_PROMPT, encoding="utf-8")
        assert lint_prompt(p) == []

    def test_missing_frontmatter_reported(self, tmp_path: Path) -> None:
        p = tmp_path / "nofm.prompt.md"
        p.write_text("# No frontmatter\n\nBody text.", encoding="utf-8")
        problems = lint_prompt(p)
        assert any("missing YAML frontmatter" in prob for prob in problems)

    def test_missing_required_field_name_reported(self, tmp_path: Path) -> None:
        p = tmp_path / "missing-name.prompt.md"
        p.write_text("---\ndescription: Test\nagent: agent\n---\n# Body", encoding="utf-8")
        problems = lint_prompt(p)
        assert any("name" in prob for prob in problems)

    def test_empty_required_field_reported(self, tmp_path: Path) -> None:
        p = tmp_path / "empty-desc.prompt.md"
        p.write_text("---\ndescription: \nname: Test\nagent: agent\n---\n# Body", encoding="utf-8")
        problems = lint_prompt(p)
        assert any("description" in prob for prob in problems)

    def test_missing_section_pre_flight_reported(self, tmp_path: Path) -> None:
        p = tmp_path / "no-preflight.prompt.md"
        text = _VALID_PROMPT.replace("## Pre-flight\n\nRun drift check before any edits.\n", "")
        p.write_text(text, encoding="utf-8")
        problems = lint_prompt(p)
        assert any("Pre-flight" in prob for prob in problems)

    @pytest.mark.parametrize("section", WORKFLOW_REQUIRED_SECTIONS)
    def test_each_required_section_checked(self, tmp_path: Path, section: str) -> None:
        p = tmp_path / "missing-sec.prompt.md"
        # Remove just the section header line
        text = _VALID_PROMPT.replace(section + "\n", "")
        p.write_text(text, encoding="utf-8")
        problems = lint_prompt(p)
        assert any(section in prob for prob in problems), f"Missing section not caught: {section}"

    def test_utility_operator_skips_longform_operator_sections(self, tmp_path: Path) -> None:
        p = tmp_path / "utility.prompt.md"
        p.write_text(_VALID_UTILITY_OPERATOR_PROMPT, encoding="utf-8")
        problems = lint_prompt(p, explicit_class="operator")
        assert problems == []

    def test_all_required_fields_present(self, tmp_path: Path) -> None:
        p = tmp_path / "allfields.prompt.md"
        p.write_text(_VALID_PROMPT, encoding="utf-8")
        problems = lint_prompt(p)
        field_problems = [prob for prob in problems if "missing required" in prob]
        assert field_problems == []

    @pytest.mark.parametrize("section", OPERATOR_BASE_REQUIRED_SECTIONS)
    def test_operator_base_sections_checked(self, tmp_path: Path, section: str) -> None:
        p = tmp_path / "operator.prompt.md"
        text = _VALID_OPERATOR_PROMPT.replace(section + "\n", "")
        p.write_text(text, encoding="utf-8")
        problems = lint_prompt(p, explicit_class="operator")
        assert any(section in prob for prob in problems), f"Missing operator section not caught: {section}"

    @pytest.mark.parametrize("section", OPERATOR_LONGFORM_REQUIRED_SECTIONS)
    def test_operator_longform_sections_checked(self, tmp_path: Path, section: str) -> None:
        p = tmp_path / "operator.prompt.md"
        text = _VALID_OPERATOR_PROMPT.replace(section + "\n", "")
        p.write_text(text, encoding="utf-8")
        problems = lint_prompt(p, explicit_class="operator")
        assert any(section in prob for prob in problems), f"Missing operator longform section not caught: {section}"

    def test_operator_requires_execution_protocol(self, tmp_path: Path) -> None:
        p = tmp_path / "operator.prompt.md"
        text = _VALID_OPERATOR_PROMPT.replace("## Phase Execution Protocol\n\nExecute the current phase.\n", "")
        p.write_text(text, encoding="utf-8")
        problems = lint_prompt(p, explicit_class="operator")
        assert any("execution section" in prob for prob in problems)

    def test_operator_rejects_workflow_routing(self, tmp_path: Path) -> None:
        p = tmp_path / "operator.prompt.md"
        text = _VALID_OPERATOR_PROMPT + "\n## Next Steps\n\nRun programstart-stage-transition next.\n"
        p.write_text(text, encoding="utf-8")
        problems = lint_prompt(p, explicit_class="operator")
        assert any("must not include workflow routing" in prob for prob in problems)

    def test_unrecognized_frontmatter_field_reported(self, tmp_path: Path) -> None:
        p = tmp_path / "badfield.prompt.md"
        text = _VALID_PROMPT.replace('agent: "agent"', 'agent: "agent"\nowner: test')
        p.write_text(text, encoding="utf-8")
        problems = lint_prompt(p)
        assert any("unrecognized frontmatter field 'owner'" in prob for prob in problems)


class TestMain:
    def test_valid_prompt_returns_zero(self, tmp_path: Path) -> None:
        p = tmp_path / "valid.prompt.md"
        p.write_text(_VALID_PROMPT, encoding="utf-8")
        assert main([str(p)]) == 0

    def test_invalid_prompt_returns_one(self, tmp_path: Path) -> None:
        p = tmp_path / "bad.prompt.md"
        p.write_text("# No frontmatter at all", encoding="utf-8")
        assert main([str(p)]) == 1

    def test_non_prompt_md_file_skipped(self, tmp_path: Path) -> None:
        # Non-.prompt.md files are silently skipped
        p = tmp_path / "readme.md"
        p.write_text("# Not a prompt — bad frontmatter would go undetected", encoding="utf-8")
        assert main([str(p)]) == 0

    def test_internal_prompt_skipped(self, tmp_path: Path) -> None:
        # Files with "internal" in path parts are skipped
        internal_dir = tmp_path / "internal"
        internal_dir.mkdir()
        p = internal_dir / "build.prompt.md"
        p.write_text("# No frontmatter — should be skipped", encoding="utf-8")
        assert main([str(p)]) == 0

    def test_multiple_valid_files_returns_zero(self, tmp_path: Path) -> None:
        files = []
        for i in range(3):
            p = tmp_path / f"p{i}.prompt.md"
            p.write_text(_VALID_PROMPT, encoding="utf-8")
            files.append(str(p))
        assert main(files) == 0

    def test_one_bad_among_many_returns_one(self, tmp_path: Path) -> None:
        good = tmp_path / "good.prompt.md"
        good.write_text(_VALID_PROMPT, encoding="utf-8")
        bad = tmp_path / "bad.prompt.md"
        bad.write_text("# No frontmatter", encoding="utf-8")
        assert main([str(good), str(bad)]) == 1

    def test_empty_argv_returns_zero(self) -> None:
        assert main([]) == 0

    def test_prints_problems_on_failure(self, tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
        p = tmp_path / "bad.prompt.md"
        p.write_text("# No frontmatter", encoding="utf-8")
        main([str(p)])
        captured = capsys.readouterr()
        assert "missing YAML frontmatter" in captured.out


# ── Repo-real public prompt coverage ─────────────────────────────────────────

_PUBLIC_PROMPTS = [
    ROOT / relative_path for relative_path, prompt_class in PROMPT_CLASS_BY_PATH.items() if prompt_class != "internal"
]


def test_all_public_prompts_lint_cleanly() -> None:
    problems: list[str] = []
    for prompt_path in _PUBLIC_PROMPTS:
        problems.extend(lint_prompt(prompt_path))
    assert problems == []


@pytest.mark.parametrize("prompt_path", _PUBLIC_PROMPTS, ids=lambda p: p.name)
def test_prompt_has_nonempty_argument_hint(prompt_path: Path) -> None:
    """Every public workflow or operator prompt MUST have a non-empty argument-hint in its frontmatter."""
    fm = _extract_frontmatter(prompt_path.read_text(encoding="utf-8"))
    assert fm is not None
    hint = fm.get("argument-hint", "")
    assert hint, f"{prompt_path.name}: argument-hint is missing or empty"
