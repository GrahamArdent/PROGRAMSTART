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
    def normalized(self) -> "PathsClassifierResult":
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
    def normalized(self) -> "PathsDiscoveryDurability":
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
    def validate_receipt(self) -> "PathsDiscoveryEvidence":
        if any(
            value != value.strip()
            for value in (self.actor_ref, self.effect_ref, self.target_ref)
        ):
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
        if any(
            not value.strip() or value != value.strip()
            for value in self.owner_native_verification_refs
        ):
            raise ValueError("owner-native verification references must be normalized")
        return self


class CapabilityDiscoveryDecision(BaseModel):
    conclusion: CapabilityConclusion
    discovery: PathsDiscoveryEvidence | None = None


def validate_capability_discovery(decision: CapabilityDiscoveryDecision) -> None:
    if decision.discovery is None:
        raise ValueError(
            "consequential capability conclusion requires deterministic Paths discovery evidence"
        )
    evidence = decision.discovery
    result = evidence.classifier_result
    constraints = result.input.constraints

    if decision.conclusion in ABSENCE_CONCLUSIONS:
        if not (
            constraints.require_current
            and constraints.require_proven
            and constraints.exclude_human_transport
        ):
            raise ValueError(
                "capability-absence/escalation conclusion requires current, proven, machine-only Paths composition search"
            )
        if result.classification in USABLE_MACHINE_CLASSIFICATIONS:
            raise ValueError(
                "capability-absence/escalation conclusion conflicts with discovered usable machine realization"
            )

    if decision.conclusion == CapabilityConclusion.NEW_CAPABILITY_REQUIRED:
        if result.classification != "GENUINELY_NEW_PATH_REQUIRED":
            raise ValueError(
                "new_capability_required requires Paths classification GENUINELY_NEW_PATH_REQUIRED"
            )

    if decision.conclusion == CapabilityConclusion.HUMAN_REQUIRED:
        if not evidence.owner_native_verification_refs:
            raise ValueError(
                "human_required requires owner-native verification of the irreducible human gate"
            )

    if decision.conclusion == CapabilityConclusion.PATH_SELECTED:
        if result.classification not in USABLE_MACHINE_CLASSIFICATIONS:
            raise ValueError("selected path requires a usable Paths machine realization")
        if not result.ordered_candidate_refs:
            raise ValueError("selected path requires at least one Paths realization")
        if not evidence.owner_native_verification_refs:
            raise ValueError(
                "discovered realization requires owner-native JIT verification before consequential selection"
            )
