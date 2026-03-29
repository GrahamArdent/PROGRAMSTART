"""Pydantic models for the PROGRAMSTART context index and knowledge base.

These models replace raw dict[str, Any] access with validated, typed data structures.
They are used by the context builder, retrieval engine, and RAG assistant.
"""

from __future__ import annotations

# ruff: noqa: I001

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Knowledge Base models
# ---------------------------------------------------------------------------


class StackEntry(BaseModel):
    """A single technology stack entry in the knowledge base."""

    name: str
    category: str = ""
    aliases: list[str] = Field(default_factory=list)
    layer: str = ""
    primary_languages: list[str] = Field(default_factory=list)
    delivery_models: list[str] = Field(default_factory=list)
    strengths: list[str] = Field(default_factory=list)
    tradeoffs: list[str] = Field(default_factory=list)
    best_for: list[str] = Field(default_factory=list)
    avoid_when: list[str] = Field(default_factory=list)
    pairs_with: list[str] = Field(default_factory=list)
    capabilities: list[str] = Field(default_factory=list)
    risks: list[str] = Field(default_factory=list)
    best_practices: list[str] = Field(default_factory=list)
    sources: list[str] = Field(default_factory=list)


class IntegrationPattern(BaseModel):
    """A recommended integration pattern combining multiple stacks."""

    name: str
    components: list[str] = Field(default_factory=list)
    fit_for: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)


class EmbeddingGuidance(BaseModel):
    """Guidance for embedding configuration."""

    default_model: str = ""
    best_practices: list[str] = Field(default_factory=list)


class RetrievalGuidance(BaseModel):
    """Retrieval strategy guidance from the knowledge base."""

    principles: list[str] = Field(default_factory=list)
    recommended_layers: list[str] = Field(default_factory=list)
    avoid: list[str] = Field(default_factory=list)
    embedding_guidance: EmbeddingGuidance = Field(default_factory=EmbeddingGuidance)
    vector_index_guidance: dict[str, str] = Field(default_factory=dict)
    search_type_guidance: dict[str, str] = Field(default_factory=dict)


class PromptEngineeringGuidance(BaseModel):
    """Prompt engineering guidance from the knowledge base."""

    principles: list[str] = Field(default_factory=list)
    patterns: list[str] = Field(default_factory=list)
    anti_patterns: list[str] = Field(default_factory=list)


class KnowledgeRelation(BaseModel):
    """An explicit relationship between KB entries or concepts."""

    subject: str
    relation: str
    object: str
    rationale: str = ""
    evidence: list[str] = Field(default_factory=list)
    confidence: str = "medium"
    tags: list[str] = Field(default_factory=list)


class DecisionRule(BaseModel):
    """A recommendation rule derived from the KB."""

    title: str
    when: str = ""
    prefer: str = ""
    because: str = ""
    avoid: list[str] = Field(default_factory=list)
    related_items: list[str] = Field(default_factory=list)
    confidence: str = "medium"


class ComparisonFinding(BaseModel):
    """A single comparison finding for two versions or options."""

    area: str
    summary: str = ""
    option_a: str = ""
    option_b: str = ""
    recommendation: str = ""
    migration_risk: str = ""


class VersionComparison(BaseModel):
    """A structured comparison between versions or closely related options."""

    name: str
    scope: list[str] = Field(default_factory=list)
    compared_versions: list[str] = Field(default_factory=list)
    status: str = ""
    summary: str = ""
    related_items: list[str] = Field(default_factory=list)
    findings: list[ComparisonFinding] = Field(default_factory=list)
    decision: str = ""
    sources: list[str] = Field(default_factory=list)


class ResearchTrack(BaseModel):
    """A recurring research lane used to keep the KB current."""

    name: str
    cadence: str = ""
    owner: str = ""
    scope: list[str] = Field(default_factory=list)
    trigger_signals: list[str] = Field(default_factory=list)
    required_outputs: list[str] = Field(default_factory=list)


class ResearchLedger(BaseModel):
    """Operating guidance for recurring KB maintenance."""

    operating_model: str = ""
    weekly_review_day: str = ""
    update_policy: list[str] = Field(default_factory=list)
    tracks: list[ResearchTrack] = Field(default_factory=list)


class KnowledgeBase(BaseModel):
    """The full knowledge base with stacks, patterns, and guidance."""

    version: str = ""
    method: str = ""
    stacks: list[StackEntry] = Field(default_factory=list)
    integration_patterns: list[IntegrationPattern] = Field(default_factory=list)
    decision_rules: list[DecisionRule] = Field(default_factory=list)
    relationships: list[KnowledgeRelation] = Field(default_factory=list)
    comparisons: list[VersionComparison] = Field(default_factory=list)
    retrieval_guidance: RetrievalGuidance = Field(default_factory=RetrievalGuidance)
    prompt_engineering_guidance: PromptEngineeringGuidance = Field(default_factory=PromptEngineeringGuidance)
    research_ledger: ResearchLedger = Field(default_factory=ResearchLedger)


# ---------------------------------------------------------------------------
# Context Index models
# ---------------------------------------------------------------------------


class DocumentRecord(BaseModel):
    """A document entry in the context index."""

    path: str
    title: str = ""
    purpose: str | None = None
    owner: str | None = None
    last_updated: str | None = None
    depends_on: list[str] = Field(default_factory=list)
    authority: str | None = None
    headings: list[str] = Field(default_factory=list)


class ConcernRecord(BaseModel):
    """A concern entry mapping ownership in the context index."""

    concern: str
    owner_file: str = ""
    supporting_files: list[str] = Field(default_factory=list)
    system: str = ""
    source: str = ""
    relation: str = ""


class RouteRecord(BaseModel):
    """An API route entry in the context index."""

    method: str
    path: str
    purpose: str = ""


class CommandSet(BaseModel):
    """CLI and dashboard command inventories."""

    cli: list[str] = Field(default_factory=list)
    dashboard: list[str] = Field(default_factory=list)


class RelationRecord(BaseModel):
    """A dependency or authority relation between documents."""

    type: str
    from_: str = Field(alias="from", default="")
    to: str = ""
    source: str = ""

    model_config = {"populate_by_name": True}


class WorkspaceInfo(BaseModel):
    """Workspace metadata from the context index."""

    name: str = ""
    description: str = ""
    root_readme: str = ""
    generated_outputs_root: str = "outputs"


class RuntimeInfo(BaseModel):
    """Runtime state snapshot embedded in the context index."""

    programbuild: dict[str, object] | None = None
    userjourney_attached: bool = False
    userjourney: dict[str, object] | None = None


class SystemConfig(BaseModel):
    """Configuration for a workflow system (programbuild or userjourney)."""

    root: str = ""
    control_files: list[str] = Field(default_factory=list)
    output_files: list[str] = Field(default_factory=list)
    core_files: list[str] = Field(default_factory=list)

    model_config = {"extra": "allow"}


class ContextIndex(BaseModel):
    """The full context index produced by the context builder.

    This is the central data structure that ties together all workspace
    metadata, documents, concerns, knowledge base, routes, commands,
    and relations into a single validated object.
    """

    version: str = ""
    workspace: WorkspaceInfo = Field(default_factory=WorkspaceInfo)
    systems: dict[str, SystemConfig] = Field(default_factory=dict)
    runtime: RuntimeInfo = Field(default_factory=RuntimeInfo)
    documents: list[DocumentRecord] = Field(default_factory=list)
    knowledge_base: KnowledgeBase = Field(default_factory=KnowledgeBase)
    concerns: list[ConcernRecord] = Field(default_factory=list)
    commands: CommandSet = Field(default_factory=CommandSet)
    routes: list[RouteRecord] = Field(default_factory=list)
    relations: list[RelationRecord] = Field(default_factory=list)

    # ---------------------------------------------------------------------------
    # Stage order convenience (present in registry but not always in context index)
    # ---------------------------------------------------------------------------
    stage_order: list[str] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# RAG response model (replaces the frozen dataclass for LLM responses)
# ---------------------------------------------------------------------------


class RAGQueryResponse(BaseModel):
    """Structured LLM response for a RAG query, used with Instructor."""

    answer: str = Field(description="The answer to the user's question based on the retrieved context.")
    reasoning: str = Field(
        default="",
        description="Brief explanation of how the answer was derived from the context.",
    )
    confidence: str = Field(
        default="medium",
        description="Confidence level: high, medium, or low.",
    )
    cited_sources: list[str] = Field(
        default_factory=list,
        description="List of source_type:source_id strings that were used to form the answer.",
    )
