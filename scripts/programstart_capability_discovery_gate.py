"""Fail-closed gate for consequential capability conclusions."""

from __future__ import annotations

import hashlib
import json
from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, Field, model_validator


class CapabilityConclusion(StrEnum):
    HUMAN_REQUIRED = "human_required"
    UNAVAILABLE = "unavailable"
    AUTOMATION_GAP = "automation_gap"
    NEW_CAPABILITY_REQUIRED = "new_capability_required"
    PATH_SELECTED = "path_selected"


ABSENCE_CONCLUSIONS = {
    CapabilityConclusion.HUMAN_REQUIRED,
    CapabilityConclusion.UNAVAILABLE,
    CapabilityConclusion.AUTOMATION_GAP,
    CapabilityConclusion.NEW_CAPABILITY_REQUIRED,
}
USABLE_MACHINE_CLASSIFICATIONS = {
    "DIRECT_REALIZATION",
    "EQUIVALENT_REALIZATION",
    "PROVEN_COMPOSITION",
}


class PathsClassifierConstraints(BaseModel):
    require_current: bool = False
    require_proven: bool = False
    exclude_human_transport: bool = False
    max_privilege_boundary: str | None = None


class PathsClassifierInput(BaseModel):
    actor_ref: str = Field(min_length=1)
    effect_ref: str = Field(min_length=1)
    target_ref: str = Field(min_length=1)
    constraints: PathsClassifierConstraints = Field(default_factory=PathsClassifierConstraints)


class PathsClassifierResult(BaseModel):
    input: PathsClassifierInput
    ordered_candidate_refs: list[str] = Field(default_factory=list)
    constituent_refs: list[str] = Field(default_factory=list)
    missing_typed_edges: list[str] = Field(default_factory=list)
    owner_refs: list[str] = Field(default_factory=list)
    evidence_refs: list[str] = Field(default_factory=list)
    currentness_facts: list[str] = Field(default_factory=list)
    actor_admission_state: str = Field(min_length=1)
    activation_state: str = Field(min_length=1)
    proof_state: str = Field(min_length=1)
    privilege_boundary: str | None = None
    failure_domains: list[str] = Field(default_factory=list)
    authorization_inferred: Literal[False]
    classification: str = Field(min_length=1)
    reason_code: str = Field(min_length=1)

    @model_validator(mode="after")
    def normalized(self) -> PathsClassifierResult:
        refs = (
            self.ordered_candidate_refs,
            self.constituent_refs,
            self.missing_typed_edges,
            self.owner_refs,
            self.evidence_refs,
            self.currentness_facts,
            self.failure_domains,
        )
        for values in refs:
            if len(values) != len(set(values)):
                raise ValueError("Paths classifier receipt lists must not contain duplicates")
            if any(not value.strip() or value != value.strip() for value in values):
                raise ValueError("Paths classifier receipt values must be normalized")
        return self


class PathsDiscoveryDurability(BaseModel):
    status: Literal["proven"]
    source_repo: Literal["GrahamArdent/paths"]
    source_commit_sha: str = Field(pattern=r"^[0-9a-f]{40}$")
    mechanism_ref: Literal["scripts/find_capability_composition.py"]
    verification_ref: str = Field(min_length=1)
    result_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    invalidation_conditions: tuple[str, ...] = Field(min_length=1)

    @model_validator(mode="after")
    def normalized(self) -> PathsDiscoveryDurability:
        if self.verification_ref != self.verification_ref.strip():
            raise ValueError("verification_ref must be normalized")
        if any(not item.strip() or item != item.strip() for item in self.invalidation_conditions):
            raise ValueError("durability invalidation conditions must be normalized and non-empty")
        return self


def classifier_result_sha256(result: PathsClassifierResult) -> str:
    payload = json.dumps(
        result.model_dump(mode="json"),
        sort_keys=True,
        separators=(",", ":"),
    ).encode()
    return hashlib.sha256(payload).hexdigest()


class PathsDiscoveryEvidence(BaseModel):
    actor_ref: str = Field(min_length=1)
    effect_ref: str = Field(min_length=1)
    target_ref: str = Field(min_length=1)
    classifier_result: PathsClassifierResult
    durability: PathsDiscoveryDurability
    owner_native_verification_refs: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_receipt(self) -> PathsDiscoveryEvidence:
        if any(value != value.strip() for value in (self.actor_ref, self.effect_ref, self.target_ref)):
            raise ValueError("Paths discovery references must be normalized")
        expected = (self.actor_ref, self.effect_ref, self.target_ref)
        observed = (
            self.classifier_result.input.actor_ref,
            self.classifier_result.input.effect_ref,
            self.classifier_result.input.target_ref,
        )
        if observed != expected:
            raise ValueError("Paths classifier receipt input does not match discovery request")
        if classifier_result_sha256(self.classifier_result) != self.durability.result_sha256:
            raise ValueError("Paths classifier receipt hash does not match durable proof")
        if len(self.owner_native_verification_refs) != len(set(self.owner_native_verification_refs)):
            raise ValueError("owner-native verification references must be unique")
        if any(not value.strip() or value != value.strip() for value in self.owner_native_verification_refs):
            raise ValueError("owner-native verification references must be normalized")
        return self


class CapabilityDiscoveryDecision(BaseModel):
    conclusion: CapabilityConclusion
    discovery: PathsDiscoveryEvidence | None = None


def validate_capability_discovery(decision: CapabilityDiscoveryDecision) -> None:
    if decision.discovery is None:
        raise ValueError("consequential capability conclusion requires deterministic Paths discovery evidence")
    evidence = decision.discovery
    result = evidence.classifier_result
    constraints = result.input.constraints

    if decision.conclusion in ABSENCE_CONCLUSIONS:
        if not (constraints.require_current and constraints.require_proven and constraints.exclude_human_transport):
            raise ValueError(
                "capability-absence/escalation conclusion requires current, proven, machine-only Paths composition search"
            )
        if result.classification in USABLE_MACHINE_CLASSIFICATIONS:
            raise ValueError("capability-absence/escalation conclusion conflicts with discovered usable machine realization")

    if decision.conclusion == CapabilityConclusion.NEW_CAPABILITY_REQUIRED:
        if result.classification != "GENUINELY_NEW_PATH_REQUIRED":
            raise ValueError("new_capability_required requires Paths classification GENUINELY_NEW_PATH_REQUIRED")

    if decision.conclusion == CapabilityConclusion.HUMAN_REQUIRED:
        if not evidence.owner_native_verification_refs:
            raise ValueError("human_required requires owner-native verification of the irreducible human gate")

    if decision.conclusion == CapabilityConclusion.PATH_SELECTED:
        if result.classification not in USABLE_MACHINE_CLASSIFICATIONS:
            raise ValueError("selected path requires a usable Paths machine realization")
        if not result.ordered_candidate_refs:
            raise ValueError("selected path requires at least one Paths realization")
        if not evidence.owner_native_verification_refs:
            raise ValueError("discovered realization requires owner-native JIT verification before consequential selection")


class ContractDisposition(StrEnum):
    SATISFIED = "satisfied"
    CONTRADICTED = "contradicted"
    INSUFFICIENT = "insufficient"
    STALE_OR_UNKNOWN = "stale_or_unknown"
    SUPERSEDED = "superseded"


class FailureBoundaryKind(StrEnum):
    COMPONENT = "component"
    DISPATCHER = "dispatcher"
    ADAPTER = "adapter"
    COMPOSITION = "composition"
    INVOCATION = "invocation"
    CURRENTNESS = "currentness"
    EXTERNAL_DEPENDENCY = "external_dependency"
    TEST_ASSUMPTION = "test_assumption"


class FailureAction(StrEnum):
    REPAIR_COMPOSITION = "repair_composition"
    REVERIFY_CAPABILITY = "reverify_capability"
    ISOLATE_EXTERNAL_DEGRADATION = "isolate_external_degradation"
    CORRECT_TEST_ASSUMPTION = "correct_test_assumption"
    REPAIR_EXISTING_CAPABILITY = "repair_existing_capability"
    EXTEND_EXISTING_CAPABILITY = "extend_existing_capability"
    REPLACE_EXISTING_CAPABILITY = "replace_existing_capability"


COMPOSITION_BOUNDARIES = {
    FailureBoundaryKind.DISPATCHER,
    FailureBoundaryKind.ADAPTER,
    FailureBoundaryKind.COMPOSITION,
    FailureBoundaryKind.INVOCATION,
}


class FailureBoundaryEvidence(BaseModel):
    boundary_ref: str = Field(min_length=1)
    kind: FailureBoundaryKind
    evidence_refs: tuple[str, ...] = Field(min_length=1)

    @model_validator(mode="after")
    def normalized(self) -> FailureBoundaryEvidence:
        values = (self.boundary_ref, *self.evidence_refs)
        if any(not value.strip() or value != value.strip() for value in values):
            raise ValueError("failure-boundary references must be normalized and non-empty")
        if len(self.evidence_refs) != len(set(self.evidence_refs)):
            raise ValueError("failure-boundary evidence references must be unique")
        return self


class FailureLocalizationFacts(BaseModel):
    capability_ref: str = Field(min_length=1)
    contract_ref: str = Field(min_length=1)
    prior_proof_refs: tuple[str, ...] = Field(min_length=1)
    contract_evidence_refs: tuple[str, ...] = Field(min_length=1)
    contract_disposition: ContractDisposition
    first_failed_boundary: FailureBoundaryEvidence
    independent_degradation_refs: tuple[str, ...] = ()
    replacement_necessity_refs: tuple[str, ...] = ()

    @model_validator(mode="after")
    def normalized(self) -> FailureLocalizationFacts:
        values = (
            self.capability_ref,
            self.contract_ref,
            *self.prior_proof_refs,
            *self.contract_evidence_refs,
            *self.independent_degradation_refs,
            *self.replacement_necessity_refs,
        )
        if any(not value.strip() or value != value.strip() for value in values):
            raise ValueError("failure-localization references must be normalized and non-empty")
        for name, refs in (
            ("prior_proof_refs", self.prior_proof_refs),
            ("contract_evidence_refs", self.contract_evidence_refs),
            ("independent_degradation_refs", self.independent_degradation_refs),
            ("replacement_necessity_refs", self.replacement_necessity_refs),
        ):
            if len(refs) != len(set(refs)):
                raise ValueError(f"{name} must contain unique references")
        return self


def failure_localization_facts_sha256(facts: FailureLocalizationFacts) -> str:
    payload = json.dumps(
        facts.model_dump(mode="json"),
        sort_keys=True,
        separators=(",", ":"),
    ).encode()
    return hashlib.sha256(payload).hexdigest()


class FailureLocalizationDurability(BaseModel):
    status: Literal["proven"]
    mechanism: str = Field(min_length=1)
    verification_ref: str = Field(min_length=1)
    facts_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    invalidation_conditions: tuple[str, ...] = Field(min_length=1)

    @model_validator(mode="after")
    def normalized(self) -> FailureLocalizationDurability:
        values = (self.mechanism, self.verification_ref, *self.invalidation_conditions)
        if any(not value.strip() or value != value.strip() for value in values):
            raise ValueError("failure-localization durability references must be normalized and non-empty")
        return self


class FailureLocalizationEvidence(BaseModel):
    discovery: PathsDiscoveryEvidence
    facts: FailureLocalizationFacts
    durability: FailureLocalizationDurability

    @model_validator(mode="after")
    def validate_localization(self) -> FailureLocalizationEvidence:
        constraints = self.discovery.classifier_result.input.constraints
        if not (constraints.require_current and constraints.require_proven and constraints.exclude_human_transport):
            raise ValueError("failure localization requires current, proven, machine-only Paths discovery")
        if self.discovery.classifier_result.classification == "GENUINELY_NEW_PATH_REQUIRED":
            raise ValueError("existing-capability failure localization conflicts with GENUINELY_NEW_PATH_REQUIRED discovery")
        if failure_localization_facts_sha256(self.facts) != self.durability.facts_sha256:
            raise ValueError("failure-localization facts hash does not match durable proof")
        return self


class FailureLocalizationDecision(BaseModel):
    action: FailureAction
    evidence: FailureLocalizationEvidence | None = None


def validate_failure_localization(decision: FailureLocalizationDecision) -> None:
    if decision.evidence is None:
        raise ValueError("capability mutation conclusion requires durable failure-localization evidence")

    facts = decision.evidence.facts
    boundary = facts.first_failed_boundary
    action = decision.action

    if action == FailureAction.REPAIR_COMPOSITION:
        if boundary.kind not in COMPOSITION_BOUNDARIES or facts.contract_disposition != ContractDisposition.SATISFIED:
            raise ValueError("repair_composition requires a satisfied component contract and a localized composition boundary")
        return

    if action == FailureAction.REVERIFY_CAPABILITY:
        if facts.contract_disposition != ContractDisposition.STALE_OR_UNKNOWN:
            raise ValueError("reverify_capability requires stale_or_unknown component contract evidence")
        return

    if action == FailureAction.ISOLATE_EXTERNAL_DEGRADATION:
        if (
            boundary.kind != FailureBoundaryKind.EXTERNAL_DEPENDENCY
            or facts.contract_disposition != ContractDisposition.SATISFIED
            or not facts.independent_degradation_refs
        ):
            raise ValueError(
                "isolate_external_degradation requires a satisfied component contract "
                "and independently evidenced external degradation"
            )
        return

    if action == FailureAction.CORRECT_TEST_ASSUMPTION:
        if boundary.kind != FailureBoundaryKind.TEST_ASSUMPTION or facts.contract_disposition != ContractDisposition.SATISFIED:
            raise ValueError(
                "correct_test_assumption requires a satisfied component contract and localized test-assumption failure"
            )
        return

    if action == FailureAction.REPAIR_EXISTING_CAPABILITY:
        if boundary.kind != FailureBoundaryKind.COMPONENT or facts.contract_disposition != ContractDisposition.CONTRADICTED:
            raise ValueError("repair_existing_capability requires durable evidence contradicting the component's own contract")
        return

    if action == FailureAction.EXTEND_EXISTING_CAPABILITY:
        if boundary.kind != FailureBoundaryKind.COMPONENT or facts.contract_disposition != ContractDisposition.INSUFFICIENT:
            raise ValueError("extend_existing_capability requires durable evidence that the component contract is insufficient")
        return

    if action == FailureAction.REPLACE_EXISTING_CAPABILITY:
        if boundary.kind != FailureBoundaryKind.COMPONENT:
            raise ValueError("replacement requires the first proven failing boundary to be the component itself")
        if facts.contract_disposition not in {
            ContractDisposition.CONTRADICTED,
            ContractDisposition.INSUFFICIENT,
            ContractDisposition.SUPERSEDED,
        }:
            raise ValueError(
                "replacement requires the existing component contract to be contradicted, insufficient, or superseded"
            )
        if not facts.replacement_necessity_refs:
            raise ValueError(
                "replacement requires durable evidence that repair or extension is not the sufficient bounded remediation"
            )
        return

    raise ValueError(f"unsupported failure-localization action: {action}")
