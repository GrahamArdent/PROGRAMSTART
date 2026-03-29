"""Tests for Pydantic models (programstart_models.py).

Covers validation, defaults, round-trip serialization, and edge cases.
"""

from __future__ import annotations

# ruff: noqa: I001

import json
from pathlib import Path

import pytest

from scripts.programstart_models import (
    CommandSet,
    ConcernRecord,
    ContextIndex,
    DocumentRecord,
    EmbeddingGuidance,
    IntegrationPattern,
    KnowledgeBase,
    RAGQueryResponse,
    RelationRecord,
    RetrievalGuidance,
    RouteRecord,
    RuntimeInfo,
    StackEntry,
)

ROOT = Path(__file__).resolve().parents[1]


# ---------------------------------------------------------------------------
# StackEntry
# ---------------------------------------------------------------------------


def test_stack_entry_minimal() -> None:
    entry = StackEntry(name="FastAPI")
    assert entry.name == "FastAPI"
    assert entry.aliases == []
    assert entry.best_for == []


def test_stack_entry_full() -> None:
    entry = StackEntry(
        name="React",
        category="frontend",
        aliases=["react"],
        best_for=["interactive UIs"],
        strengths=["component model"],
        capabilities=["spa"],
        risks=["state management"],
    )
    assert entry.category == "frontend"
    assert "react" in entry.aliases
    assert len(entry.risks) == 1


def test_stack_entry_round_trip() -> None:
    data = {"name": "Test", "category": "test", "aliases": ["t"], "best_for": [], "strengths": []}
    entry = StackEntry.model_validate(data)
    dumped = json.loads(entry.model_dump_json())
    assert dumped["name"] == "Test"


# ---------------------------------------------------------------------------
# IntegrationPattern
# ---------------------------------------------------------------------------


def test_integration_pattern_minimal() -> None:
    p = IntegrationPattern(name="Web Platform")
    assert p.name == "Web Platform"
    assert p.components == []


def test_integration_pattern_full() -> None:
    p = IntegrationPattern(
        name="Business Web",
        components=["Django", "PostgreSQL"],
        fit_for=["admin products"],
        notes=["keep monolithic"],
    )
    assert len(p.components) == 2


# ---------------------------------------------------------------------------
# RetrievalGuidance
# ---------------------------------------------------------------------------


def test_retrieval_guidance_defaults() -> None:
    g = RetrievalGuidance()
    assert g.principles == []
    assert isinstance(g.embedding_guidance, EmbeddingGuidance)


def test_retrieval_guidance_nested() -> None:
    g = RetrievalGuidance(
        principles=["Structured facts first"],
        embedding_guidance=EmbeddingGuidance(default_model="text-embedding-3-small"),
    )
    assert g.embedding_guidance.default_model == "text-embedding-3-small"


# ---------------------------------------------------------------------------
# KnowledgeBase
# ---------------------------------------------------------------------------


def test_knowledge_base_empty() -> None:
    kb = KnowledgeBase()
    assert kb.stacks == []
    assert kb.integration_patterns == []


def test_knowledge_base_with_stacks() -> None:
    kb = KnowledgeBase(
        version="2026-04-01",
        stacks=[StackEntry(name="FastAPI"), StackEntry(name="React")],
    )
    assert len(kb.stacks) == 2
    assert kb.version == "2026-04-01"


# ---------------------------------------------------------------------------
# DocumentRecord
# ---------------------------------------------------------------------------


def test_document_record_minimal() -> None:
    doc = DocumentRecord(path="README.md")
    assert doc.path == "README.md"
    assert doc.title == ""
    assert doc.headings == []


def test_document_record_full() -> None:
    doc = DocumentRecord(
        path="PROGRAMBUILD/ARCHITECTURE.md",
        title="Architecture",
        purpose="System boundaries",
        owner="PROGRAMBUILD",
        headings=["Components", "Data Flow"],
        depends_on=["REQUIREMENTS.md"],
    )
    assert len(doc.headings) == 2
    assert doc.depends_on == ["REQUIREMENTS.md"]


# ---------------------------------------------------------------------------
# ConcernRecord
# ---------------------------------------------------------------------------


def test_concern_record() -> None:
    c = ConcernRecord(concern="activation event", owner_file="STATES_AND_RULES.md", system="userjourney")
    assert c.concern == "activation event"
    assert c.system == "userjourney"


# ---------------------------------------------------------------------------
# RouteRecord
# ---------------------------------------------------------------------------


def test_route_record() -> None:
    r = RouteRecord(method="GET", path="/api/state", purpose="Dashboard state")
    assert r.method == "GET"


# ---------------------------------------------------------------------------
# RelationRecord
# ---------------------------------------------------------------------------


def test_relation_record_with_alias() -> None:
    r = RelationRecord.model_validate({"type": "depends_on", "from": "A.md", "to": "B.md", "source": "A.md"})
    assert r.from_ == "A.md"
    assert r.to == "B.md"


def test_relation_record_serialization() -> None:
    r = RelationRecord.model_validate({"type": "authority", "from": "X.md", "to": "Y.md"})
    dumped = r.model_dump(by_alias=True)
    assert "from" in dumped
    assert dumped["from"] == "X.md"


# ---------------------------------------------------------------------------
# CommandSet
# ---------------------------------------------------------------------------


def test_command_set() -> None:
    cs = CommandSet(cli=["status", "validate"], dashboard=["state.show"])
    assert len(cs.cli) == 2
    assert cs.dashboard[0] == "state.show"


# ---------------------------------------------------------------------------
# RuntimeInfo
# ---------------------------------------------------------------------------


def test_runtime_info_defaults() -> None:
    ri = RuntimeInfo()
    assert ri.programbuild is None
    assert ri.userjourney_attached is False


# ---------------------------------------------------------------------------
# ContextIndex — full model
# ---------------------------------------------------------------------------


def test_context_index_from_minimal_dict() -> None:
    data = {
        "version": "2026-03-28",
        "workspace": {"name": "PROGRAMSTART", "description": "test"},
        "documents": [{"path": "README.md", "title": "Readme"}],
        "knowledge_base": {"stacks": [{"name": "FastAPI"}]},
        "concerns": [],
        "commands": {"cli": ["status"], "dashboard": []},
        "routes": [{"method": "GET", "path": "/", "purpose": "root"}],
        "relations": [],
    }
    idx = ContextIndex.model_validate(data)
    assert idx.version == "2026-03-28"
    assert len(idx.documents) == 1
    assert idx.knowledge_base.stacks[0].name == "FastAPI"
    assert idx.workspace.name == "PROGRAMSTART"


def test_context_index_empty() -> None:
    idx = ContextIndex()
    assert idx.documents == []
    assert idx.knowledge_base.stacks == []


def test_context_index_round_trip() -> None:
    """Build from dict, dump back, and re-parse — data should survive."""
    data = {
        "version": "test",
        "documents": [{"path": "A.md", "title": "A", "headings": ["H1"]}],
        "knowledge_base": {
            "stacks": [{"name": "S1", "aliases": ["s1"]}],
            "integration_patterns": [{"name": "P1", "components": ["C1"]}],
        },
        "concerns": [{"concern": "auth", "owner_file": "AUTH.md"}],
        "routes": [{"method": "POST", "path": "/api/run", "purpose": "run"}],
        "relations": [{"type": "depends_on", "from": "A.md", "to": "B.md"}],
        "commands": {"cli": ["a"], "dashboard": ["b"]},
    }
    idx = ContextIndex.model_validate(data)
    serialized = json.loads(idx.model_dump_json(by_alias=True))
    idx2 = ContextIndex.model_validate(serialized)
    assert idx2.documents[0].path == "A.md"
    assert idx2.knowledge_base.stacks[0].aliases == ["s1"]
    assert idx2.relations[0].from_ == "A.md"


def test_context_index_loads_real_index_file() -> None:
    """Load the actual context-index.json from the workspace and validate it."""
    index_path = ROOT / "outputs" / "context" / "context-index.json"
    if not index_path.exists():
        pytest.skip("No context-index.json found — run 'programstart context build' first")

    raw = json.loads(index_path.read_text(encoding="utf-8"))
    idx = ContextIndex.model_validate(raw)
    assert idx.version
    assert len(idx.documents) > 0
    assert len(idx.knowledge_base.stacks) > 0


# ---------------------------------------------------------------------------
# RAGQueryResponse
# ---------------------------------------------------------------------------


def test_rag_query_response_minimal() -> None:
    r = RAGQueryResponse(answer="Test answer")
    assert r.answer == "Test answer"
    assert r.confidence == "medium"
    assert r.cited_sources == []


def test_rag_query_response_full() -> None:
    r = RAGQueryResponse(
        answer="The system uses BM25.",
        reasoning="Found in retrieval guidance.",
        confidence="high",
        cited_sources=["guidance:retrieval_guidance.principles[0]"],
    )
    assert r.confidence == "high"
    assert len(r.cited_sources) == 1


# ---------------------------------------------------------------------------
# Validation error cases
# ---------------------------------------------------------------------------


def test_stack_entry_missing_name_raises() -> None:
    with pytest.raises(Exception):
        StackEntry.model_validate({})


def test_concern_record_missing_concern_raises() -> None:
    with pytest.raises(Exception):
        ConcernRecord.model_validate({})


def test_route_record_missing_method_raises() -> None:
    with pytest.raises(Exception):
        RouteRecord.model_validate({"path": "/api/state"})
