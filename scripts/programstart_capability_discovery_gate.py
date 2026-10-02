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


class FailureLocalizationClass(StrEnum):
    COMPOSITION_OR_WIRING_GAP = "composition_or_wiring_gap"
    COMPONENT_CONTRACT_FAILURE = "component_contract_failure"
    COMPONENT_CONTRACT_INSUFFICIENT = "component_contract_insufficient"
    CURRENTNESS_OR_ACTIVATION_FAILURE = "currentness_or_activation_failure"
    INDEPENDENT_DEGRADATION = "independent_degradation"
    TEST_OR_ASSUMPTION_FAILURE = "test_or_assumption_failure"
    UNKNOWN = "unknown"


class FailureLocalizationConclusion(StrEnum):
    PRESERVE_COMPONENT_AND_REPAIR_BOUNDARY = "preserve_component_and_repair_boundary"
    COMPONENT_DEFECTIVE = "component_defective"
    COMPONENT_REPLACEMENT_REQUIRED = "component_replacement_required"
    CURRENTNESS_RECHECK_REQUIRED = "currentness_recheck_required"
    INDEPENDENT_DEGRADATION = "independent_degradation"
    TEST_ASSUMPTION_CORRECTION_REQUIRED = "test_assumption_correction_required"
    FURTHER_LOCALIZATION_REQUIRED = "further_localization_required"


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


class FailureLocalizationEvidence(BaseModel):
    observed_failure_ref: str = Field(min_length=1)
    component_ref: str = Field(min_length=1)
    component_contract_ref: str = Field(min_length=1)
    classification: FailureLocalizationClass
    first_failed_boundary_ref: str = Field(min_length=1)
    preserved_evidence_refs: list[str] = Field(default_factory=list)
    contradictory_component_evidence_refs: list[str] = Field(default_factory=list)
    invalidated_component_evidence_refs: list[str] = Field(default_factory=list)
    independent_degradation_refs: list[str] = Field(default_factory=list)
    requirement_gap_refs: list[str] = Field(default_factory=list)
    authorization_inferred: Literal[False] = False

    @model_validator(mode="after")
    def normalized(self) -> FailureLocalizationEvidence:
        scalar_refs = (
            self.observed_failure_ref,
            self.component_ref,
            self.component_contract_ref,
            self.first_failed_boundary_ref,
        )
        if any(not value.strip() or value != value.strip() for value in scalar_refs):
            raise ValueError("failure-localization references must be normalized and non-empty")
        ref_lists = (
            self.preserved_evidence_refs,
            self.contradictory_component_evidence_refs,
            self.invalidated_component_evidence_refs,
            self.independent_degradation_refs,
            self.requirement_gap_refs,
        )
        for values in ref_lists:
            if len(values) != len(set(values)):
                raise ValueError("failure-localization evidence lists must not contain duplicates")
            if any(not value.strip() or value != value.strip() for value in values):
                raise ValueError("failure-localization evidence references must be normalized")
        return self


class FailureLocalizationDecision(BaseModel):
    conclusion: FailureLocalizationConclusion
    discovery: PathsDiscoveryEvidence
    localization: FailureLocalizationEvidence


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


def validate_failure_localization(decision: FailureLocalizationDecision) -> None:
    result = decision.discovery.classifier_result
    constraints = result.input.constraints
    evidence = decision.localization

    if not (constraints.require_current and constraints.require_proven):
        raise ValueError("failure localization requires current and proven Paths discovery context")

    if decision.conclusion == FailureLocalizationConclusion.PRESERVE_COMPONENT_AND_REPAIR_BOUNDARY:
        if evidence.classification != FailureLocalizationClass.COMPOSITION_OR_WIRING_GAP:
            raise ValueError("boundary repair conclusion requires a composition/wiring gap classification")
        if not evidence.preserved_evidence_refs:
            raise ValueError("boundary repair must preserve prior component evidence explicitly")
        if evidence.contradictory_component_evidence_refs:
            raise ValueError("boundary repair cannot ignore contradictory component evidence")
        return

    if decision.conclusion == FailureLocalizationConclusion.COMPONENT_DEFECTIVE:
        if evidence.classification != FailureLocalizationClass.COMPONENT_CONTRACT_FAILURE:
            raise ValueError("component_defective requires component contract failure evidence")
        if not evidence.contradictory_component_evidence_refs or not evidence.invalidated_component_evidence_refs:
            raise ValueError("component_defective requires contradictory evidence and explicit component-proof invalidation")
        return

    if decision.conclusion == FailureLocalizationConclusion.COMPONENT_REPLACEMENT_REQUIRED:
        if evidence.classification == FailureLocalizationClass.COMPONENT_CONTRACT_FAILURE:
            if not evidence.contradictory_component_evidence_refs or not evidence.invalidated_component_evidence_refs:
                raise ValueError("replacement after contract failure requires contradictory evidence and proof invalidation")
            return
        if evidence.classification == FailureLocalizationClass.COMPONENT_CONTRACT_INSUFFICIENT:
            if not evidence.requirement_gap_refs:
                raise ValueError("replacement after contract insufficiency requires an evidenced requirement gap")
            return
        raise ValueError("replacement requires component contract failure or evidenced contract insufficiency")

    if decision.conclusion == FailureLocalizationConclusion.CURRENTNESS_RECHECK_REQUIRED:
        if evidence.classification != FailureLocalizationClass.CURRENTNESS_OR_ACTIVATION_FAILURE:
            raise ValueError("currentness recheck conclusion requires a currentness/activation failure")
        return

    if decision.conclusion == FailureLocalizationConclusion.INDEPENDENT_DEGRADATION:
        if evidence.classification != FailureLocalizationClass.INDEPENDENT_DEGRADATION:
            raise ValueError("independent degradation conclusion requires independent degradation classification")
        if not evidence.independent_degradation_refs:
            raise ValueError("independent degradation requires durable degradation evidence")
        return

    if decision.conclusion == FailureLocalizationConclusion.TEST_ASSUMPTION_CORRECTION_REQUIRED:
        if evidence.classification != FailureLocalizationClass.TEST_OR_ASSUMPTION_FAILURE:
            raise ValueError("test-assumption correction requires a test/assumption failure classification")
        return

    if decision.conclusion == FailureLocalizationConclusion.FURTHER_LOCALIZATION_REQUIRED:
        if evidence.classification != FailureLocalizationClass.UNKNOWN:
            raise ValueError("further localization is reserved for an unresolved failure boundary")
        return

    raise ValueError(f"unsupported failure-localization conclusion: {decision.conclusion}")
