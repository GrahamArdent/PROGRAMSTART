"""Context provenance, relative outputs and conservative decision routing."""

import json
from typing import Any, cast

from scripts import programstart_context as context
from scripts import programstart_decision as decision
from scripts import programstart_impact as impact
from scripts.programstart_graph import DependencyGraph


def test_relative_context_build_and_query_preserve_actual_index(tmp_path, monkeypatch, capsys):
    original = context.workspace_path
    monkeypatch.setattr(
        context, "workspace_path", lambda relative: tmp_path / relative if relative == "index.json" else original(relative)
    )
    assert context.main(["build", "--output", "index.json"]) == 0
    index = json.loads((tmp_path / "index.json").read_text())
    assert index["documents"] and index["knowledge_base"]["stacks"]
    capsys.readouterr()
    assert context.main(["query", "--index", "index.json", "--file", "PROGRAMBUILD/ARCHITECTURE.md"]) == 0
    assert "ARCHITECTURE.md" in capsys.readouterr().out


def test_missing_journey_and_duplicate_route_do_not_manufacture_context(tmp_path, monkeypatch):
    source = tmp_path / "scripts/programstart_serve.py"
    source.parent.mkdir()
    source.write_text('def do_GET():\n    if parsed.path == "/": pass\ndef do_POST():\n    pass\ndef main(): pass\n')
    monkeypatch.setattr(context, "workspace_path", lambda relative: tmp_path / relative)
    assert context.extract_userjourney_concerns() == []
    routes = context.extract_dashboard_routes()
    assert sum(row["path"] == "/" for row in routes) == 1
    registry = {
        "workspace": {},
        "systems": {"programbuild": {"control_files": [], "output_files": ["data.json"]}, "userjourney": {"core_files": []}},
    }
    assert context.extract_documents(registry) == []


def test_nested_prompt_guidance_is_recovered_from_legacy_kb(tmp_path, monkeypatch):
    (tmp_path / "config").mkdir()
    (tmp_path / "config/knowledge-base.json").write_text(
        json.dumps(
            {
                "prompt_engineering_guidance": {},
                "retrieval_guidance": {"prompt_engineering_guidance": {"principles": ["evidence first"]}},
            }
        )
    )
    monkeypatch.setattr(context, "workspace_path", lambda relative: tmp_path / relative)
    context.load_knowledge_base.cache_clear()
    try:
        assert context.load_knowledge_base()["prompt_engineering_guidance"]["principles"] == ["evidence first"]
    finally:
        context.load_knowledge_base.cache_clear()


def test_sufficient_medium_uncertainty_reuses_evidence_and_unknown_stays_conservative():
    accepted = decision.route_decision(
        decision.DecisionContext(decision="Choose helper", uncertainty="medium", evidence_state="sufficient")
    )
    assert accepted.research_depth == "none"
    assert "research brief:" not in decision.render_text(accepted)
    unknown = decision.route_decision(
        decision.DecisionContext(decision="Unclassified API input", uncertainty=cast(Any, "unknown"), evidence_state="sufficient")
    )
    assert unknown.route == "investigate" and unknown.research_depth == "targeted"


def test_blank_impact_has_no_graph_seed_and_malformed_blast_radius_is_bounded(capsys):
    assert impact.resolve_blast_radius_starts(DependencyGraph(), " ", {}) == ()
    impact.print_impact_summary("fixture", {"blast_radius": []})
    assert "Impact summary for: fixture" in capsys.readouterr().out


def test_current_top_level_prompt_guidance_wins_over_legacy(tmp_path, monkeypatch):
    (tmp_path / "config").mkdir()
    (tmp_path / "config/knowledge-base.json").write_text(
        json.dumps(
            {
                "prompt_engineering_guidance": {"principles": ["current"]},
                "retrieval_guidance": {"prompt_engineering_guidance": {"principles": ["old"]}},
            }
        )
    )
    monkeypatch.setattr(context, "workspace_path", lambda relative: tmp_path / relative)
    context.load_knowledge_base.cache_clear()
    try:
        assert context.load_knowledge_base()["prompt_engineering_guidance"]["principles"] == ["current"]
    finally:
        context.load_knowledge_base.cache_clear()
