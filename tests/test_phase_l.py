"""Tests for Phase L: dashboard extraction, CSP headers, and prompt builder."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.programstart_command_registry import CLI_COMMANDS
from scripts.programstart_prompt_build import (
    AUTO_HEADER,
    build_prompt,
    eject_prompt,
    list_stages,
)
from scripts.programstart_prompt_build import (
    main as prompt_build_main,
)
from scripts.programstart_serve import _CSP, _STATIC_CONTENT_TYPES, _load_dashboard_html

# ---------------------------------------------------------------------------
# L-1: Dashboard static file extraction
# ---------------------------------------------------------------------------


class TestDashboardStaticFiles:
    """Verify the dashboard/ directory contains the extracted static files."""

    def test_dashboard_dir_exists(self) -> None:
        assert (ROOT / "dashboard").is_dir()

    def test_index_html_exists(self) -> None:
        html = (ROOT / "dashboard" / "index.html").read_text(encoding="utf-8")
        assert "<!DOCTYPE html>" in html
        assert "PROGRAMSTART" in html

    def test_style_css_exists(self) -> None:
        css = (ROOT / "dashboard" / "style.css").read_text(encoding="utf-8")
        assert ":root" in css
        assert "--bg:" in css

    def test_app_js_exists(self) -> None:
        js = (ROOT / "dashboard" / "app.js").read_text(encoding="utf-8")
        assert "document.body.dataset.root" in js
        assert "loadAll" in js

    def test_index_references_external_assets(self) -> None:
        html = (ROOT / "dashboard" / "index.html").read_text(encoding="utf-8")
        assert "/static/style.css" in html
        assert "/static/app.js" in html

    def test_index_has_data_root_attribute(self) -> None:
        html = (ROOT / "dashboard" / "index.html").read_text(encoding="utf-8")
        assert 'data-root="__ROOT__"' in html

    def test_no_inline_script_block_in_html(self) -> None:
        """The extracted HTML should not have a large inline <script> block."""
        html = (ROOT / "dashboard" / "index.html").read_text(encoding="utf-8")
        # The extracted HTML should reference external script, not inline it
        assert "<script>" not in html or html.count("<script>") == 0

    def test_serve_py_does_not_contain_html_string(self) -> None:
        """serve.py should no longer have the HTML = r triple-quote block."""
        source = (ROOT / "scripts" / "programstart_serve.py").read_text(encoding="utf-8")
        assert 'HTML = r"""' not in source


# ---------------------------------------------------------------------------
# L-1 continued: static file serving
# ---------------------------------------------------------------------------


class TestStaticFileServing:
    """Verify serve.py has static file serving infrastructure."""

    def test_dashboard_dir_constant(self) -> None:
        source = (ROOT / "scripts" / "programstart_serve.py").read_text(encoding="utf-8")
        assert "DASHBOARD_DIR" in source

    def test_serve_static_method(self) -> None:
        source = (ROOT / "scripts" / "programstart_serve.py").read_text(encoding="utf-8")
        assert "_serve_static" in source

    def test_static_route_in_do_get(self) -> None:
        source = (ROOT / "scripts" / "programstart_serve.py").read_text(encoding="utf-8")
        assert "/static/" in source

    def test_load_dashboard_html_function(self) -> None:
        html = _load_dashboard_html()
        assert "<!DOCTYPE html>" in html
        assert "__ROOT__" in html

    def test_content_type_map_exists(self) -> None:
        assert ".css" in _STATIC_CONTENT_TYPES
        assert ".js" in _STATIC_CONTENT_TYPES

    def test_serve_static_path_traversal_protection(self) -> None:
        """Verify _serve_static strips directory components."""
        source = (ROOT / "scripts" / "programstart_serve.py").read_text(encoding="utf-8")
        assert "Path(filename).name" in source


# ---------------------------------------------------------------------------
# L-2: CSP headers
# ---------------------------------------------------------------------------


class TestCSPHeaders:
    """Verify Content-Security-Policy is configured."""

    def test_csp_constant_exists(self) -> None:
        assert "default-src 'self'" in _CSP
        assert "script-src 'self'" in _CSP
        assert "style-src 'self' 'unsafe-inline'" in _CSP

    def test_csp_header_in_send_html(self) -> None:
        source = (ROOT / "scripts" / "programstart_serve.py").read_text(encoding="utf-8")
        assert "Content-Security-Policy" in source


# ---------------------------------------------------------------------------
# L-3: Prompt builder
# ---------------------------------------------------------------------------


class TestPromptBuilder:
    """Verify programstart_prompt_build.py generates valid prompts."""

    def test_list_stages_returns_all(self) -> None:
        stages = list_stages()
        assert len(stages) >= 11
        names = [s["name"] for s in stages]
        assert "feasibility" in names
        assert "implementation_loop" in names

    def test_build_prompt_feasibility(self) -> None:
        content = build_prompt("feasibility")
        assert "AUTO-GENERATED" in content
        assert "Data Grounding Rule" in content
        assert "Protocol Declaration" in content
        assert "Pre-flight" in content
        assert "Verification Gate" in content
        assert "FEASIBILITY.md" in content

    def test_build_prompt_includes_guidance_files(self) -> None:
        content = build_prompt("feasibility")
        assert "PROGRAMBUILD/FEASIBILITY.md" in content
        assert "PROGRAMBUILD/DECISION_LOG.md" in content

    def test_build_prompt_includes_sync_rule(self) -> None:
        content = build_prompt("feasibility")
        assert "sync_rule:" in content
        assert "programbuild_feasibility_cascade" in content

    def test_build_prompt_implementation_has_optional_sections(self) -> None:
        content = build_prompt("implementation_loop")
        assert "Kill Criteria Re-check" in content
        assert "PRODUCT_SHAPE Conditioning" in content
        assert "Entry Criteria Verification" in content

    def test_build_prompt_feasibility_no_entry_criteria(self) -> None:
        content = build_prompt("feasibility")
        assert "Entry Criteria Verification" not in content

    def test_build_prompt_unknown_stage_exits(self) -> None:
        with pytest.raises(SystemExit, match="Unknown stage"):
            build_prompt("nonexistent_stage")

    def test_eject_prompt(self, tmp_path: Path) -> None:
        test_file = tmp_path / "test.prompt.md"
        test_file.write_text(f"{AUTO_HEADER}\n---\nname: test\n---\n# Test\n", encoding="utf-8")
        result = eject_prompt(test_file)
        assert result == 0
        content = test_file.read_text(encoding="utf-8")
        assert AUTO_HEADER not in content
        assert "# Test" in content

    def test_eject_non_auto_prompt(self, tmp_path: Path) -> None:
        test_file = tmp_path / "manual.prompt.md"
        test_file.write_text("---\nname: manual\n---\n# Manual\n", encoding="utf-8")
        result = eject_prompt(test_file)
        assert result == 0

    def test_eject_missing_file(self, tmp_path: Path) -> None:
        result = eject_prompt(tmp_path / "missing.md")
        assert result == 1

    def test_main_list_stages_json(self) -> None:
        import contextlib
        import io

        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = prompt_build_main(["--list-stages", "--json"])
        assert rc == 0
        data = json.loads(buf.getvalue())
        assert isinstance(data, list)
        assert any(s["name"] == "feasibility" for s in data)

    def test_main_write_output(self, tmp_path: Path) -> None:
        out = tmp_path / "generated.prompt.md"
        rc = prompt_build_main(["--stage", "research", "--output", str(out)])
        assert rc == 0
        assert out.is_file()
        content = out.read_text(encoding="utf-8")
        assert "AUTO-GENERATED" in content
        assert "research" in content.lower()

    def test_prompt_build_in_cli_commands(self) -> None:
        assert "prompt-build" in CLI_COMMANDS
