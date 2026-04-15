from __future__ import annotations

import sys
from pathlib import Path
from time import perf_counter
from unittest.mock import patch

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts import programstart_context, programstart_recommend, programstart_retrieval


def _minimal_registry() -> dict:
    return {
        "workflow_guidance": {
            "kickoff": {
                "files": ["PROGRAMBUILD/PROGRAMBUILD_KICKOFF_PACKET.md"],
            },
        },
    }


def _minimal_knowledge_base() -> dict:
    return {
        "stacks": [],
        "provisioning_services": [],
        "third_party_apis": [],
        "cli_tools": [],
        "coverage_domains": [],
        "comparisons": [],
        "relationships": [],
        "integration_patterns": [],
        "decision_rules": [],
        "prompt_engineering_guidance": {},
    }


@pytest.mark.slow
def test_build_recommendation_under_threshold() -> None:
    with (
        patch.object(programstart_recommend, "load_registry", return_value=_minimal_registry()),
        patch.object(programstart_recommend, "load_knowledge_base", return_value=_minimal_knowledge_base()),
    ):
        started = perf_counter()
        recommendation = programstart_recommend.build_recommendation(
            product_shape="web app",
            needs={"dashboard", "auth"},
            regulated=False,
            attach_userjourney=None,
        )
        duration = perf_counter() - started

    assert recommendation.product_shape == "web app"
    assert duration < 2.0


@pytest.mark.slow
def test_lexical_search_under_threshold() -> None:
    chunks = [
        programstart_retrieval.Chunk(
            source_type="document",
            source_id="PROGRAMBUILD/ARCHITECTURE.md",
            text="Architecture contracts define API boundaries and system data flow.",
            metadata={"path": "PROGRAMBUILD/ARCHITECTURE.md"},
        ),
        programstart_retrieval.Chunk(
            source_type="document",
            source_id="PROGRAMBUILD/TEST_STRATEGY.md",
            text="Test strategy covers quality gates, smoke coverage, and regression controls.",
            metadata={"path": "PROGRAMBUILD/TEST_STRATEGY.md"},
        ),
        programstart_retrieval.Chunk(
            source_type="document",
            source_id="docs/retrieval-architecture.md",
            text="Retrieval architecture uses lexical ranking before optional vector search.",
            metadata={"path": "docs/retrieval-architecture.md"},
        ),
    ]
    searcher = programstart_retrieval.LexicalSearcher(chunks)

    started = perf_counter()
    results = searcher.search("architecture", top_k=2)
    duration = perf_counter() - started

    assert results
    assert duration <= 0.5


@pytest.mark.slow
def test_build_context_index_under_threshold() -> None:
    registry = {
        "workspace": {
            "name": "PROGRAMSTART",
            "description": "Workflow tooling",
            "root_readme": "README.md",
            "generated_outputs_root": "outputs",
        },
        "systems": {
            "programbuild": {"root": "PROGRAMBUILD"},
            "userjourney": {"root": "USERJOURNEY"},
        },
    }

    with (
        patch.object(programstart_context, "load_registry", return_value=registry),
        patch.object(programstart_context, "extract_documents", return_value=[{"path": "README.md", "title": "README"}]),
        patch.object(programstart_context, "extract_programbuild_concerns", return_value=[]),
        patch.object(programstart_context, "extract_userjourney_concerns", return_value=[]),
        patch.object(programstart_context, "dashboard_allowed_commands", return_value={"state.show": ["python", "state"]}),
        patch.object(
            programstart_context, "load_knowledge_base", return_value={"stacks": [], "decision_rules": [], "relationships": []}
        ),
        patch.object(programstart_context, "load_workflow_state", return_value={"active": "inputs_and_mode_selection"}),
        patch.object(programstart_context, "extract_dashboard_routes", return_value=[]),
        patch.object(programstart_context, "build_relations", return_value=[]),
    ):
        started = perf_counter()
        index = programstart_context.build_context_index()
        duration = perf_counter() - started

    assert index["workspace"]["name"] == "PROGRAMSTART"
    assert duration < 3.0
