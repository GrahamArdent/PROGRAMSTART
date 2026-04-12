"""Unit tests for scripts/programstart_markdown_parsers.py."""

from __future__ import annotations

from scripts.programstart_markdown_parsers import (
    clean_md,
    extract_bullets,
    extract_bullets_after_marker,
    extract_file_checklist_sections,
    extract_slice_sections,
    extract_startup_sections,
    extract_subagents,
    system_is_attached,
)


class TestCleanMd:
    def test_strips_backticks(self) -> None:
        assert clean_md("`hello`") == "hello"

    def test_strips_whitespace(self) -> None:
        assert clean_md("  hello  ") == "hello"

    def test_strips_combined(self) -> None:
        assert clean_md("  `value`  ") == "value"

    def test_empty_string(self) -> None:
        assert clean_md("") == ""


class TestExtractBullets:
    def test_extracts_items_under_heading(self) -> None:
        text = "## Fruits\n- apple\n- banana\n## Veggies\n- carrot\n"
        assert extract_bullets(text, "Fruits") == ["apple", "banana"]

    def test_returns_empty_for_missing_heading(self) -> None:
        text = "## Fruits\n- apple\n"
        assert extract_bullets(text, "Colors") == []

    def test_stops_at_next_heading(self) -> None:
        text = "## A\n- one\n## B\n- two\n"
        assert extract_bullets(text, "A") == ["one"]


class TestExtractBulletsAfterMarker:
    def test_extracts_after_marker(self) -> None:
        text = "Some intro\nBefore using this:\n- step one\n- step two\n---\nafter"
        assert extract_bullets_after_marker(text, "Before using this:") == ["step one", "step two"]

    def test_returns_empty_for_missing_marker(self) -> None:
        text = "Some intro\n- item\n"
        assert extract_bullets_after_marker(text, "No such marker") == []

    def test_stops_at_heading(self) -> None:
        text = "marker line\n- item1\n## Heading\n- item2\n"
        assert extract_bullets_after_marker(text, "marker line") == ["item1"]


class TestExtractSubagents:
    def test_parses_subagent_sections(self) -> None:
        text = (
            "Every subagent report should contain:\n"
            "- summary\n"
            "- findings\n"
            "---\n"
            "## 1. Discovery Agent\n"
            "Use for:\n"
            "- scoping\n"
            "- research\n"
            "Prompt:\n"
            "```\n"
            "Do discovery work.\n"
            "```\n"
        )
        agents, reqs = extract_subagents(text)
        assert reqs == ["summary", "findings"]
        assert len(agents) == 1
        assert agents[0]["name"] == "Discovery Agent"
        assert agents[0]["use_for"] == ["scoping", "research"]
        assert "discovery work" in agents[0]["prompt"].lower()

    def test_empty_text(self) -> None:
        agents, reqs = extract_subagents("")
        assert agents == []
        assert reqs == []


class TestExtractStartupSections:
    def test_parses_startup_checklist(self) -> None:
        text = (
            "## 3. Stage Startup Checklist\n"
            "### Pre-work\n"
            "- read docs\n"
            "- check state\n"
            "### Execution\n"
            "- run scripts\n"
            "## 4. Next Section\n"
        )
        sections = extract_startup_sections(text)
        assert len(sections) == 2
        assert sections[0]["title"] == "Pre-work"
        assert sections[0]["items"] == ["read docs", "check state"]
        assert sections[1]["title"] == "Execution"

    def test_returns_empty_when_no_matching_heading(self) -> None:
        text = "## Other Section\n### Sub\n- item\n"
        assert extract_startup_sections(text) == []


class TestExtractSliceSections:
    def test_parses_slice(self) -> None:
        text = (
            "## Slice 1: Auth\n"
            "### Outcome\n"
            "Users can log in.\n"
            "### Scope\n"
            "1. Build login page\n"
            "2. Add session handling\n"
            "### Test scope\n"
            "1. Unit tests for auth\n"
            "### Primary Risk\n"
            "Token expiry edge cases.\n"
        )
        sections = extract_slice_sections(text)
        assert len(sections) == 1
        assert sections[0]["title"] == "Slice 1: Auth"
        assert sections[0]["outcome"] == "Users can log in."
        assert len(sections[0]["scope"]) == 2
        assert sections[0]["risk"] == "Token expiry edge cases."

    def test_returns_empty_for_no_slices(self) -> None:
        assert extract_slice_sections("## Not a slice\nfoo\n") == []


class TestExtractFileChecklistSections:
    def test_parses_file_checklist(self) -> None:
        text = (
            "### `routes.py`\n"
            "Status: In Progress\n"
            "Checklist:\n"
            "1. Add health route\n"
            "2. Add auth middleware\n"
            "Critical warning:\n"
            "Must handle token refresh.\n"
        )
        sections = extract_file_checklist_sections(text)
        assert len(sections) == 1
        assert sections[0]["file"] == "routes.py"
        assert sections[0]["status"] == "In Progress"
        assert len(sections[0]["items"]) == 2
        assert sections[0]["warning"] == "Must handle token refresh."

    def test_returns_empty_for_no_backtick_headings(self) -> None:
        text = "### NoBackticks\nStatus: Done\n"
        assert extract_file_checklist_sections(text) == []


class TestSystemIsAttached:
    def test_returns_false_for_missing_system(self) -> None:
        registry: dict[str, object] = {"systems": {}}
        assert system_is_attached("nonexistent", registry) is False

    def test_returns_false_for_empty_root(self) -> None:
        registry = {"systems": {"test": {"root": ""}}}
        assert system_is_attached("test", registry) is False
