from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts import programstart_context


def test_build_context_index_contains_core_sections() -> None:
    index = programstart_context.build_context_index()

    assert index["workspace"]["name"] == "PROGRAMSTART"
    assert "programbuild" in index["systems"]
    assert "userjourney" in index["systems"]
    assert any(item["name"] == "FastAPI" for item in index["knowledge_base"]["stacks"])
    assert index["knowledge_base"]["decision_rules"]
    assert index["knowledge_base"]["relationships"]
    assert index["knowledge_base"]["comparisons"]
    assert index["commands"]["cli"]
    assert index["commands"]["dashboard"]
    assert any(route["path"] == "/api/state" for route in index["routes"])
    assert any(item["concern"] == "overall process and stage order" for item in index["concerns"])


def test_query_context_index_by_concern_returns_owner() -> None:
    index = programstart_context.build_context_index()

    result = programstart_context.query_context_index(
        index,
        concern="activation",
        file_path=None,
        command=None,
        route=None,
        stack=None,
        capability=None,
        impact=None,
    )

    assert result["concerns"]
    assert any(item["owner_file"] in {"STATES_AND_RULES.md", "ANALYTICS_AND_OUTCOMES.md"} for item in result["concerns"])


def test_query_context_index_by_file_returns_document_and_relations() -> None:
    index = programstart_context.build_context_index()

    result = programstart_context.query_context_index(
        index,
        concern=None,
        file_path="USERJOURNEY/ROUTE_AND_STATE_FREEZE.md",
        command=None,
        route=None,
        stack=None,
        capability=None,
        impact=None,
    )

    assert any(doc["path"] == "USERJOURNEY/ROUTE_AND_STATE_FREEZE.md" for doc in result["documents"])
    assert result["relations"]


def test_query_context_index_by_command_returns_matches() -> None:
    index = programstart_context.build_context_index()

    result = programstart_context.query_context_index(
        index,
        concern=None,
        file_path=None,
        command="context",
        route=None,
        stack=None,
        capability=None,
        impact=None,
    )

    assert "context" in result["cli"]
    assert any(item == "context.summary" for item in result["dashboard"])


def test_query_context_index_by_route_returns_matches() -> None:
    index = programstart_context.build_context_index()

    result = programstart_context.query_context_index(
        index,
        concern=None,
        file_path=None,
        command=None,
        route="workflow",
        stack=None,
        capability=None,
        impact=None,
    )

    assert any(route["path"] == "/api/workflow-advance" for route in result["routes"])


def test_query_context_index_by_stack_returns_kb_matches() -> None:
    index = programstart_context.build_context_index()

    result = programstart_context.query_context_index(
        index,
        concern=None,
        file_path=None,
        command=None,
        route=None,
        stack="fastapi",
        capability=None,
        impact=None,
    )

    assert any(item["name"] == "FastAPI" for item in result["stacks"])
    assert result["integration_patterns"]
    assert any(item["object"] == "Pydantic" for item in result["relationships"])


def test_query_context_index_by_capability_returns_relevant_guidance() -> None:
    index = programstart_context.build_context_index()

    result = programstart_context.query_context_index(
        index,
        concern=None,
        file_path=None,
        command=None,
        route=None,
        stack=None,
        capability="durable-workflows",
        impact=None,
    )

    assert any(item["name"] == "Temporal" for item in result["stacks"])
    assert any("durable workflows" in item["title"].lower() for item in result["decision_rules"])


def test_query_context_index_returns_python_runtime_comparison() -> None:
    index = programstart_context.build_context_index()

    result = programstart_context.query_context_index(
        index,
        concern=None,
        file_path=None,
        command=None,
        route=None,
        stack=None,
        capability="3.14",
        impact=None,
    )

    assert any("Python 3.13 vs 3.14" in item["name"] for item in result["comparisons"])


def test_query_context_index_by_impact_returns_related_context() -> None:
    index = programstart_context.build_context_index()

    result = programstart_context.query_context_index(
        index,
        concern=None,
        file_path=None,
        command=None,
        route=None,
        stack=None,
        capability=None,
        impact="workflow",
    )

    assert result["relations"]
    assert any(route["path"] == "/api/workflow-advance" for route in result["routes"])


def test_query_context_index_by_impact_includes_kb_comparisons() -> None:
    index = programstart_context.build_context_index()

    result = programstart_context.query_context_index(
        index,
        concern=None,
        file_path=None,
        command=None,
        route=None,
        stack=None,
        capability=None,
        impact="python 3.14",
    )

    assert any("Python 3.13 vs 3.14" in item["name"] for item in result["comparisons"])


def test_context_build_writes_output_file(tmp_path: Path) -> None:
    output_path = tmp_path / "context-index.json"

    exit_code = programstart_context.main(["build", "--output", str(output_path)])

    assert exit_code == 0
    payload = json.loads(output_path.read_text(encoding="utf-8"))
    assert payload["workspace"]["name"] == "PROGRAMSTART"
