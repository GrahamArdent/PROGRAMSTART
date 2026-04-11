from __future__ import annotations

import json
import sys
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts import programstart_impact as impact

# ── helpers ────────────────────────────────────────────────────────────────────


def _empty_result() -> dict:
    return {
        "documents": [],
        "concerns": [],
        "relations": [],
        "routes": [],
        "cli": [],
        "dashboard": [],
        "stacks": [],
        "integration_patterns": [],
        "decision_rules": [],
        "relationships": [],
        "comparisons": [],
    }


def _minimal_index() -> dict:
    return {
        "version": 1,
        "schema_version": 1,
        "documents": [],
        "concerns": [],
        "relations": [],
        "routes": [],
        "cli": [],
        "dashboard": [],
        "stacks": [],
        "integration_patterns": [],
        "decision_rules": [],
        "relationships": [],
        "comparisons": [],
    }


# ── print_impact_summary ───────────────────────────────────────────────────────


def test_print_impact_summary_shows_target(capsys) -> None:
    result = _empty_result()
    impact.print_impact_summary("consent.md", result)
    captured = capsys.readouterr()
    assert "consent.md" in captured.out


def test_print_impact_summary_shows_counts(capsys) -> None:
    result = _empty_result()
    result["documents"] = [{"path": "USERJOURNEY/DELIVERY_GAMEPLAN.md"}]
    result["concerns"] = [{"concern": "auth", "owner_file": "USERJOURNEY/LEGAL.md"}]
    impact.print_impact_summary("auth", result)
    captured = capsys.readouterr()
    assert "documents: 1" in captured.out
    assert "concerns: 1" in captured.out


def test_print_impact_summary_lists_related_documents(capsys) -> None:
    result = _empty_result()
    result["documents"] = [{"path": "USERJOURNEY/ROUTE_AND_STATE_FREEZE.md"}]
    impact.print_impact_summary("route", result)
    captured = capsys.readouterr()
    assert "USERJOURNEY/ROUTE_AND_STATE_FREEZE.md" in captured.out


def test_print_impact_summary_lists_concerns(capsys) -> None:
    result = _empty_result()
    result["concerns"] = [{"concern": "GDPR consent", "owner_file": "USERJOURNEY/LEGAL_AND_CONSENT.md"}]
    impact.print_impact_summary("consent", result)
    captured = capsys.readouterr()
    assert "GDPR consent" in captured.out


# ── main ───────────────────────────────────────────────────────────────────────


def test_main_text_mode_returns_zero(tmp_path) -> None:
    index = _minimal_index()
    index_path = tmp_path / "index.json"
    index_path.write_text(json.dumps(index), encoding="utf-8")
    with (
        patch.object(impact, "load_index", return_value=index),
        patch.object(impact, "query_context_index", return_value=_empty_result()),
    ):
        result = impact.main(["consent.md"])
    assert result == 0


def test_main_json_mode_emits_json(capsys, tmp_path) -> None:
    index = _minimal_index()
    expected_result = _empty_result()
    expected_result["documents"] = [{"path": "USERJOURNEY/FILE.md"}]
    with (
        patch.object(impact, "load_index", return_value=index),
        patch.object(impact, "query_context_index", return_value=expected_result),
    ):
        result = impact.main(["consent.md", "--json"])
    assert result == 0
    captured = capsys.readouterr()
    parsed = json.loads(captured.out)
    assert parsed["documents"] == [{"path": "USERJOURNEY/FILE.md"}]


def test_main_passes_target_to_query_context_index() -> None:
    index = _minimal_index()
    captured_kwargs: list[dict] = []

    def fake_query(idx, **kwargs):
        captured_kwargs.append(kwargs)
        return _empty_result()

    with (
        patch.object(impact, "load_index", return_value=index),
        patch.object(impact, "query_context_index", side_effect=fake_query),
    ):
        impact.main(["activation-event"])

    assert len(captured_kwargs) == 1
    assert captured_kwargs[0]["impact"] == "activation-event"


def test_main_uses_provided_index_path(tmp_path) -> None:
    index = _minimal_index()
    index_path = tmp_path / "custom_index.json"
    index_path.write_text(json.dumps(index), encoding="utf-8")
    loaded: list[str] = []

    def fake_load(index_path_arg):
        loaded.append(str(index_path_arg))
        return index

    with (
        patch.object(impact, "load_index", side_effect=fake_load),
        patch.object(impact, "query_context_index", return_value=_empty_result()),
    ):
        impact.main(["target", "--index", str(index_path)])

    assert str(index_path) in loaded[0]
