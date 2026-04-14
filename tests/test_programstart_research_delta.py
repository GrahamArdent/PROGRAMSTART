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


def test_build_status_reports_tracks_and_domain_gaps() -> None:
    report = programstart_research_delta.build_status("2026-03-30")

    assert report.total_tracks >= 10
    assert any(track.track == "Python runtime and packaging" for track in report.tracks)
    assert any(track.track == "Desktop and local-first delivery" for track in report.tracks)
    assert any(track.track == "Developer tooling and monorepo delivery" for track in report.tracks)
    assert any(track.track == "Mobile and cross-platform delivery" for track in report.tracks)
    assert any(track.track == "Realtime and event-driven systems" for track in report.tracks)
    assert any(track.track == "Commerce and customer platforms" for track in report.tracks)
    assert any(domain.status in {"seed", "partial"} for domain in report.domains)
    assert any(
        domain.name == "Cloud, infrastructure, and platform operations" and domain.status == "strong" for domain in report.domains
    )
    assert any(
        domain.name == "Commerce, communication, and product integrations" and domain.status == "strong"
        for domain in report.domains
    )
    assert any(domain.name == "Data engineering and analytics" and domain.status == "strong" for domain in report.domains)
    assert any(
        domain.name == "Developer experience, quality, and supply chain" and domain.status == "strong"
        for domain in report.domains
    )
    assert any(
        domain.name == "Desktop, local-first, and offline-capable software" and domain.status == "partial"
        for domain in report.domains
    )
    assert any(
        domain.name == "Identity, security, and regulated delivery" and domain.status == "strong" for domain in report.domains
    )
    assert any(domain.name == "Mobile and cross-platform apps" and domain.status == "partial" for domain in report.domains)
    assert any(
        domain.name == "Realtime collaboration, messaging, and eventing" and domain.status == "strong"
        for domain in report.domains
    )


def test_main_status_json_emits_report(capsys) -> None:
    result = programstart_research_delta.main(["--status", "--date", "2026-03-30", "--json"])
    payload = json.loads(capsys.readouterr().out)

    assert result == 0
    assert payload["review_date"] == "2026-03-30"
    assert "tracks" in payload
    assert "domains" in payload


def test_main_status_fail_on_due_returns_one(capsys) -> None:
    result = programstart_research_delta.main(["--status", "--date", "2026-04-25", "--fail-on-due", "--json"])
    payload = json.loads(capsys.readouterr().out)

    assert result == 1
    assert payload["due_tracks"] >= 1


def test_mark_reviewed_updates_track_and_kb_version(tmp_path: Path, monkeypatch, capsys) -> None:
    kb_path = tmp_path / "config" / "knowledge-base.json"
    kb_path.parent.mkdir(parents=True)
    kb_path.write_text(
        json.dumps(
            {
                "version": "2026-03-30",
                "research_ledger": {
                    "tracks": [
                        {
                            "name": "Python runtime and packaging",
                            "freshness_days": 7,
                            "last_review_date": "2026-03-30",
                        }
                    ]
                },
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(programstart_research_delta, "workspace_path", lambda rel: tmp_path / rel)

    result = programstart_research_delta.main(
        [
            "--track",
            "Python runtime and packaging",
            "--date",
            "2026-04-12",
            "--mark-reviewed",
            "--json",
        ]
    )
    payload = json.loads(capsys.readouterr().out)
    updated = json.loads(kb_path.read_text(encoding="utf-8"))

    assert result == 0
    assert payload["track"] == "Python runtime and packaging"
    assert payload["review_date"] == "2026-04-12"
    assert updated["version"] == "2026-04-12"
    assert updated["research_ledger"]["tracks"][0]["last_review_date"] == "2026-04-12"


def test_mark_reviewed_requires_track() -> None:
    try:
        programstart_research_delta.main(["--mark-reviewed", "--date", "2026-04-12"])
    except SystemExit as exc:
        assert str(exc) == "--mark-reviewed requires --track"
    else:  # pragma: no cover - defensive guard
        raise AssertionError("Expected SystemExit")


def test_mark_reviewed_rejects_status_combo() -> None:
    try:
        programstart_research_delta.main(
            ["--track", "Python runtime and packaging", "--mark-reviewed", "--status", "--date", "2026-04-12"]
        )
    except SystemExit as exc:
        assert str(exc) == "--mark-reviewed cannot be combined with --status"
    else:  # pragma: no cover - defensive guard
        raise AssertionError("Expected SystemExit")
