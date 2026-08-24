from __future__ import annotations

import json
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

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


def _relation(relation_type: str, dependent: str, prerequisite: str, source: str = "registry") -> dict:
    return {
        "type": relation_type,
        "from": dependent,
        "to": prerequisite,
        "source": source,
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


def test_print_impact_summary_lists_blast_radius_paths(capsys) -> None:
    result = _empty_result()
    result["blast_radius"] = {
        "start_nodes": ["ARCHITECTURE.md"],
        "affected": [
            {
                "node": "TEST_STRATEGY.md",
                "depth": 1,
                "path": ["ARCHITECTURE.md", "TEST_STRATEGY.md"],
                "edges": [],
            }
        ],
    }
    impact.print_impact_summary("ARCHITECTURE.md", result)
    captured = capsys.readouterr()
    assert "dependency blast radius: 1" in captured.out
    assert "ARCHITECTURE.md -> TEST_STRATEGY.md" in captured.out


# ── blast-radius graph integration ─────────────────────────────────────────────


def test_build_blast_radius_walks_downstream_dependencies() -> None:
    index = _minimal_index()
    index["relations"] = [
        _relation("depends_on", "TEST_STRATEGY.md", "ARCHITECTURE.md", "sync-rule"),
        _relation("depends_on", "RELEASE_READINESS.md", "TEST_STRATEGY.md", "sync-rule"),
    ]
    related = _empty_result()
    related["documents"] = [{"path": "ARCHITECTURE.md"}]

    result = impact.build_blast_radius(index, "ARCHITECTURE.md", related)

    assert result["start_nodes"] == ["ARCHITECTURE.md"]
    assert [item["node"] for item in result["affected"]] == ["TEST_STRATEGY.md", "RELEASE_READINESS.md"]
    assert result["affected"][1]["path"] == [
        "ARCHITECTURE.md",
        "TEST_STRATEGY.md",
        "RELEASE_READINESS.md",
    ]
    assert result["affected"][0]["edges"][0] == {
        "type": "depends_on",
        "from": "TEST_STRATEGY.md",
        "to": "ARCHITECTURE.md",
        "source": "sync-rule",
    }


def test_build_blast_radius_includes_authority_dependency() -> None:
    index = _minimal_index()
    index["relations"] = [
        _relation("authority_dependency", "PROGRAMBUILD_PRODUCT.md", "PROGRAMBUILD.md", "authority-map"),
    ]
    related = _empty_result()

    result = impact.build_blast_radius(index, "PROGRAMBUILD.md", related)

    assert [item["node"] for item in result["affected"]] == ["PROGRAMBUILD_PRODUCT.md"]
    assert result["affected"][0]["edges"][0]["type"] == "authority_dependency"


def test_build_blast_radius_ignores_non_dependency_relations() -> None:
    index = _minimal_index()
    index["relations"] = [
        _relation("semantic_related", "B.md", "A.md"),
        _relation("depends_on", "C.md", "A.md"),
    ]
    related = _empty_result()

    result = impact.build_blast_radius(index, "A.md", related)

    assert [item["node"] for item in result["affected"]] == ["C.md"]


def test_build_blast_radius_respects_max_depth() -> None:
    index = _minimal_index()
    index["relations"] = [
        _relation("depends_on", "B.md", "A.md"),
        _relation("depends_on", "C.md", "B.md"),
    ]
    related = _empty_result()

    result = impact.build_blast_radius(index, "A.md", related, max_depth=1)

    assert [item["node"] for item in result["affected"]] == ["B.md"]
    assert result["max_depth"] == 1


def test_build_blast_radius_uses_shortest_path_across_multiple_starts() -> None:
    index = _minimal_index()
    index["relations"] = [
        _relation("depends_on", "B.md", "A.md"),
        _relation("depends_on", "C.md", "A.md"),
        _relation("depends_on", "D.md", "B.md"),
        _relation("depends_on", "D.md", "C.md"),
    ]
    related = _empty_result()
    related["documents"] = [{"path": "A.md"}, {"path": "C.md"}]

    result = impact.build_blast_radius(index, "md", related)
    d = next(item for item in result["affected"] if item["node"] == "D.md")

    assert d["depth"] == 1
    assert d["path"] == ["C.md", "D.md"]


def test_build_blast_radius_no_matching_graph_node_is_empty() -> None:
    index = _minimal_index()
    index["relations"] = [_relation("depends_on", "B.md", "A.md")]

    result = impact.build_blast_radius(index, "not-present", _empty_result())

    assert result["start_nodes"] == []
    assert result["affected"] == []


def test_resolve_blast_radius_starts_prefers_exact_match() -> None:
    index = _minimal_index()
    index["relations"] = [
        _relation("depends_on", "ARCHITECTURE_NOTES.md", "ARCHITECTURE.md"),
    ]
    graph = impact.DependencyGraph(index["relations"], relation_types=impact.DEFAULT_IMPACT_TYPES)
    related = _empty_result()
    related["documents"] = [{"path": "ARCHITECTURE_NOTES.md"}]

    starts = impact.resolve_blast_radius_starts(graph, "ARCHITECTURE.md", related)

    assert starts == ("ARCHITECTURE.md",)


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
    assert parsed["blast_radius"]["affected"] == []


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


def test_main_passes_max_depth_to_blast_radius() -> None:
    index = _minimal_index()
    captured_depths: list[int | None] = []

    def fake_blast(idx, target, related, *, max_depth=None):
        captured_depths.append(max_depth)
        return {"start_nodes": [], "relation_types": [], "max_depth": max_depth, "affected": []}

    with (
        patch.object(impact, "load_index", return_value=index),
        patch.object(impact, "query_context_index", return_value=_empty_result()),
        patch.object(impact, "build_blast_radius", side_effect=fake_blast),
    ):
        impact.main(["target", "--max-depth", "2"])

    assert captured_depths == [2]


def test_main_rejects_negative_max_depth() -> None:
    with pytest.raises(SystemExit):
        impact.main(["target", "--max-depth", "-1"])


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


# ── load_index ─────────────────────────────────────────────────────────────────


def test_load_index_compatible_cached(tmp_path) -> None:
    index = _minimal_index()
    index_path = tmp_path / "index.json"
    index_path.write_text(json.dumps(index), encoding="utf-8")
    with patch.object(impact, "cached_index_is_compatible", return_value=True):
        result = impact.load_index(str(index_path))
    assert result == index


def test_load_index_incompatible_rebuilds(tmp_path) -> None:
    index = _minimal_index()
    index_path = tmp_path / "index.json"
    index_path.write_text(json.dumps(index), encoding="utf-8")
    rebuilt = _minimal_index()
    rebuilt["version"] = 99
    with (
        patch.object(impact, "cached_index_is_compatible", return_value=False),
        patch.object(impact, "build_context_index", return_value=rebuilt),
    ):
        result = impact.load_index(str(index_path))
    assert result["version"] == 99


def test_load_index_missing_file_rebuilds(tmp_path) -> None:
    rebuilt = _minimal_index()
    rebuilt["version"] = 42
    with patch.object(impact, "build_context_index", return_value=rebuilt):
        result = impact.load_index(str(tmp_path / "nonexistent.json"))
    assert result["version"] == 42


def test_load_index_relative_path(tmp_path) -> None:
    rebuilt = _minimal_index()
    with (
        patch.object(impact, "workspace_path", return_value=tmp_path / "rel.json"),
        patch.object(impact, "build_context_index", return_value=rebuilt),
    ):
        result = impact.load_index("rel.json")
    assert result == rebuilt


def test_load_index_none_uses_default() -> None:
    rebuilt = _minimal_index()
    with (
        patch.object(impact, "default_index_path", return_value=Path("/fake/index.json")),
        patch.object(impact, "build_context_index", return_value=rebuilt),
    ):
        result = impact.load_index(None)
    assert result == rebuilt


# ── print_impact_summary detail sections ───────────────────────────────────────


def test_print_impact_summary_lists_relations(capsys) -> None:
    result = _empty_result()
    result["relations"] = [{"type": "sync", "from": "A.md", "to": "B.md"}]
    impact.print_impact_summary("sync", result)
    captured = capsys.readouterr()
    assert "A.md" in captured.out and "B.md" in captured.out


def test_print_impact_summary_lists_decision_rules(capsys) -> None:
    result = _empty_result()
    result["decision_rules"] = [{"title": "Use JWT for auth"}]
    impact.print_impact_summary("auth", result)
    captured = capsys.readouterr()
    assert "Use JWT for auth" in captured.out


def test_print_impact_summary_lists_relationships(capsys) -> None:
    result = _empty_result()
    result["relationships"] = [{"subject": "User", "relation": "has", "object": "Session"}]
    impact.print_impact_summary("user", result)
    captured = capsys.readouterr()
    assert "User" in captured.out and "Session" in captured.out


def test_print_impact_summary_lists_comparisons(capsys) -> None:
    result = _empty_result()
    result["comparisons"] = [{"name": "Supabase vs Firebase"}]
    impact.print_impact_summary("stack", result)
    captured = capsys.readouterr()
    assert "Supabase" in captured.out and "Firebase" in captured.out
