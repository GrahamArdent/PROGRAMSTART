from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts import programstart_research_delta


def test_build_template_defaults_to_first_track() -> None:
    template = programstart_research_delta.build_template("2026-03-29", None, None)
    assert template.track == "Python runtime and packaging"
    assert template.review_date == "2026-03-29"
    assert template.output_path.endswith("2026-03-29_python-runtime-and-packaging_delta.md")


def test_main_json_emits_template_metadata(tmp_path: Path, capsys) -> None:
    output_path = tmp_path / "runtime-delta.md"
    result = programstart_research_delta.main(
        [
            "--track",
            "Python runtime and packaging",
            "--date",
            "2026-03-29",
            "--output",
            str(output_path),
            "--json",
        ]
    )
    payload = json.loads(capsys.readouterr().out)
    assert result == 0
    assert payload["track"] == "Python runtime and packaging"
    assert Path(payload["output_path"]).exists()


def test_render_markdown_contains_required_sections(tmp_path: Path) -> None:
    template = programstart_research_delta.build_template(
        "2026-03-29",
        "LLM, retrieval, and agent tooling",
        str(tmp_path / "agent-delta.md"),
    )
    markdown = programstart_research_delta.render_markdown(template)
    assert "## Source Changes" in markdown
    assert "## Recommendation Decision" in markdown
    assert "## KB Update Surface" in markdown
