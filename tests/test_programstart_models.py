"""Tests for Pydantic models (programstart_models.py).

Covers validation, defaults, round-trip serialization, and edge cases.
"""

from __future__ import annotations

# ruff: noqa: I001

import json
from pathlib import Path

import pytest

from scripts.programstart_models import (
    CliToolEntry,
    ComparisonFinding,
    CommandSet,
    ConcernRecord,
    ContextIndex,
    CoverageDomain,
    DecisionRule,
    DocumentRecord,
    EmbeddingGuidance,
    IntegrationPattern,
    KnowledgeBase,
    KnowledgeRelation,
    ProvisioningServiceEntry,
    RAGQueryResponse,
    RelationRecord,
    ResearchLedger,
    ResearchTrack,
    RetrievalGuidance,
    RouteRecord,
    RuntimeInfo,
    StackEntry,
    ThirdPartyAPIEntry,
    VersionComparison,
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
        best_practices=["define rendering boundaries early"],
    )
    assert entry.category == "frontend"
    assert "react" in entry.aliases
    assert len(entry.risks) == 1
    assert entry.best_practices == ["define rendering boundaries early"]


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


def test_provisioning_service_entry_minimal() -> None:
    entry = ProvisioningServiceEntry(name="Supabase")
    assert entry.name == "Supabase"
    assert entry.automation_supported is False


def test_cli_tool_entry_minimal() -> None:
    entry = CliToolEntry(name="GitHub CLI")
    assert entry.name == "GitHub CLI"
    assert entry.install_methods == []


def test_third_party_api_entry_minimal() -> None:
    entry = ThirdPartyAPIEntry(name="OpenAI")
    assert entry.name == "OpenAI"
    assert entry.server_env_vars == []


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
        provisioning_services=[ProvisioningServiceEntry(name="Supabase", provider="Supabase")],
        cli_tools=[CliToolEntry(name="GitHub CLI", provider="GitHub")],
        third_party_apis=[ThirdPartyAPIEntry(name="OpenAI", provider="OpenAI")],
        coverage_domains=[CoverageDomain(name="Mobile apps", status="seed", priority="high")],
    )
    assert len(kb.stacks) == 2
    assert kb.version == "2026-04-01"
    assert kb.provisioning_services[0].provider == "Supabase"
    assert kb.cli_tools[0].provider == "GitHub"
    assert kb.third_party_apis[0].provider == "OpenAI"
    assert kb.coverage_domains[0].status == "seed"


def test_knowledge_base_extended_sections() -> None:
    kb = KnowledgeBase(
        decision_rules=[
            DecisionRule(
                title="Prefer durable workflows",
                when="work spans retries and waits",
                prefer="Temporal",
                because="state needs to be replayable",
                related_items=["Temporal", "Celery"],
            )
        ],
        relationships=[KnowledgeRelation(subject="Temporal", relation="alternative_to", object="Celery")],
        comparisons=[
            VersionComparison(
                name="Python 3.13 vs 3.14",
                compared_versions=["3.13", "3.14"],
                findings=[ComparisonFinding(area="concurrency", option_a="experimental", option_b="supported")],
            )
        ],
        research_ledger=ResearchLedger(
            operating_model="weekly delta review",
            tracks=[
                ResearchTrack(
                    name="Python runtime",
                    cadence="weekly",
                    freshness_days=7,
                    last_review_date="2026-03-29",
                    linked_domains=["Developer experience"],
                )
            ],
        ),
    )
    assert kb.decision_rules[0].title == "Prefer durable workflows"
    assert kb.relationships[0].relation == "alternative_to"
    assert kb.comparisons[0].findings[0].area == "concurrency"
    assert kb.research_ledger.tracks[0].name == "Python runtime"
    assert kb.research_ledger.tracks[0].freshness_days == 7


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
            "decision_rules": [{"title": "R1", "prefer": "P1"}],
            "relationships": [{"subject": "S1", "relation": "complements", "object": "P1"}],
            "comparisons": [{"name": "C1", "compared_versions": ["a", "b"]}],
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
    assert idx2.knowledge_base.decision_rules[0].title == "R1"
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


# ---------------------------------------------------------------------------
# Registry Pydantic Models (G-2)
# ---------------------------------------------------------------------------

from scripts.programstart_models import (
    BaselineEntry,
    ExemptGameplanEntry,
    ManifestCollectionConfig,
    ManagedStagePrompt,
    OperatorGameplanEntry,
    ProcessRegistry,
    RepoBoundaryDoc,
    StageOrderEntry,
    SyncRule,
    SystemDefinition,
    WorkspaceConfig,
)


class TestRegistryModelsUnit:
    """Unit tests for individual registry model classes."""

    def test_stage_order_entry_minimal(self) -> None:
        entry = StageOrderEntry(id=0, name="inputs")
        assert entry.id == 0
        assert entry.name == "inputs"
        assert entry.main_output == ""

    def test_stage_order_entry_full(self) -> None:
        entry = StageOrderEntry(id=3, name="requirements", main_output="REQUIREMENTS.md")
        assert entry.main_output == "REQUIREMENTS.md"

    def test_stage_order_entry_extra_fields_allowed(self) -> None:
        entry = StageOrderEntry.model_validate({"id": 1, "name": "feasibility", "future_field": True})
        assert entry.name == "feasibility"

    def test_repo_boundary_doc(self) -> None:
        doc = RepoBoundaryDoc(path="README.md", must_contain=["boundary rule"])
        assert doc.path == "README.md"
        assert len(doc.must_contain) == 1

    def test_managed_stage_prompt(self) -> None:
        p = ManagedStagePrompt(stage="feasibility", path="prompts/feasibility.prompt.md")
        assert p.stage == "feasibility"

    def test_operator_gameplan_entry(self) -> None:
        g = OperatorGameplanEntry(status="paired", prompt="execute.prompt.md")
        assert g.status == "paired"

    def test_exempt_gameplan_entry(self) -> None:
        g = ExemptGameplanEntry(reason="infrastructure-repair", note="gates broken")
        assert g.reason == "infrastructure-repair"

    def test_manifest_collection_config_defaults(self) -> None:
        m = ManifestCollectionConfig()
        assert m.include_workspace_readme is False
        assert m.exclude_prefixes == []

    def test_baseline_entry(self) -> None:
        b = BaselineEntry(name="pb_snap", system="programbuild", kind="snapshot", root="BACKUPS/snap")
        assert b.kind == "snapshot"

    def test_sync_rule_minimal(self) -> None:
        r = SyncRule(name="canonical_authority")
        assert r.authority_files == []
        assert r.require_authority_when_dependents_change is False

    def test_system_definition_stage_order_takes_entries(self) -> None:
        sd = SystemDefinition(
            root="PB",
            stage_order=[StageOrderEntry(id=0, name="inputs", main_output="block")],
        )
        assert isinstance(sd.stage_order[0], StageOrderEntry)
        assert sd.stage_order[0].name == "inputs"

    def test_workspace_config_defaults(self) -> None:
        w = WorkspaceConfig()
        assert w.generated_outputs_root == "outputs"
        assert w.bootstrap_assets == []


class TestProcessRegistryIntegration:
    """Integration tests loading the real registry."""

    def test_load_validated_registry_succeeds(self) -> None:
        from scripts.programstart_common import load_validated_registry

        reg = load_validated_registry()
        assert isinstance(reg, ProcessRegistry)

    def test_registry_version_nonempty(self) -> None:
        from scripts.programstart_common import load_validated_registry

        reg = load_validated_registry()
        assert reg.version != ""

    def test_registry_systems_keys(self) -> None:
        from scripts.programstart_common import load_validated_registry

        reg = load_validated_registry()
        assert "programbuild" in reg.systems
        assert reg.systems["programbuild"].root == "PROGRAMBUILD"

    def test_registry_stage_order_typed(self) -> None:
        from scripts.programstart_common import load_validated_registry

        reg = load_validated_registry()
        stages = reg.systems["programbuild"].stage_order
        assert len(stages) > 0
        assert isinstance(stages[0], StageOrderEntry)
        assert stages[0].id == 0

    def test_registry_sync_rules_nonempty(self) -> None:
        from scripts.programstart_common import load_validated_registry

        reg = load_validated_registry()
        assert len(reg.sync_rules) > 0
        assert isinstance(reg.sync_rules[0], SyncRule)
        assert reg.sync_rules[0].name != ""

    def test_registry_workspace_bootstrap_assets(self) -> None:
        from scripts.programstart_common import load_validated_registry

        reg = load_validated_registry()
        assert len(reg.workspace.bootstrap_assets) > 0

    def test_registry_round_trip(self) -> None:
        from scripts.programstart_common import load_validated_registry

        reg = load_validated_registry()
        dumped = reg.model_dump()
        assert isinstance(dumped, dict)
        assert "systems" in dumped
        re_validated = ProcessRegistry.model_validate(dumped)
        assert re_validated.version == reg.version

    def test_registry_integrity_manifest_collection(self) -> None:
        from scripts.programstart_common import load_validated_registry

        reg = load_validated_registry()
        mc = reg.integrity.manifest_collection
        assert isinstance(mc, ManifestCollectionConfig)
        assert mc.include_workspace_readme is True
        assert len(mc.exclude_prefixes) > 0

    def test_registry_baselines(self) -> None:
        from scripts.programstart_common import load_validated_registry

        reg = load_validated_registry()
        assert len(reg.integrity.baselines) > 0
        assert isinstance(reg.integrity.baselines[0], BaselineEntry)
