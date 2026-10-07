"""Bounded resource preparation; no model routing or execution authority."""

from __future__ import annotations

import re
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class ResourceStep(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    task: str = Field(min_length=1, max_length=300)
    task_kind: Literal["mechanical", "bounded_reasoning", "unresolved_decision", "independent_review"]
    execution_class: Literal["deterministic", "approved_default", "approved_stronger", "approved_review"]
    approved_profile_ref: str | None = Field(default=None, min_length=1, max_length=512)
    escalation_reason: (
        Literal[
            "novel_inference",
            "conflicting_evidence",
            "consequential_design",
            "authority_security_uncertainty",
            "cheaper_path_insufficient",
        ]
        | None
    ) = None
    escalation_evidence: str | None = Field(default=None, min_length=1, max_length=512)
    step_down_condition: str | None = Field(default=None, min_length=1, max_length=300)

    @model_validator(mode="after")
    def policy_boundary(self) -> ResourceStep:
        if self.task_kind == "mechanical" and self.execution_class != "deterministic":
            raise ValueError("mechanical steps must use deterministic tooling")
        if self.execution_class == "deterministic":
            if any((self.approved_profile_ref, self.escalation_reason, self.escalation_evidence, self.step_down_condition)):
                raise ValueError("deterministic work cannot claim a model or escalation")
        elif not self.approved_profile_ref:
            raise ValueError("reasoning requires an existing approved profile reference")
        if self.execution_class in {"approved_stronger", "approved_review"}:
            if not all((self.escalation_reason, self.escalation_evidence, self.step_down_condition)):
                raise ValueError("stronger reasoning requires evidence and an explicit step-down condition")
        elif any((self.escalation_reason, self.escalation_evidence, self.step_down_condition)):
            raise ValueError("default work cannot carry premium escalation state")
        if self.task_kind == "independent_review" and self.execution_class != "approved_review":
            raise ValueError("independent review requires a separate approved review profile")
        return self


class ResourcePreflight(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    schema_version: Literal["programstart.resource-preflight.v1"]
    work_ref: str = Field(min_length=1, max_length=512)
    work_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    policy_ref: str = Field(min_length=1, max_length=512)
    working_set: list[str] = Field(min_length=1, max_length=32)
    reusable_evidence: list[str] = Field(default_factory=list, max_length=32)
    invalidation_triggers: list[str] = Field(min_length=1, max_length=16)
    steps: list[ResourceStep] = Field(min_length=1, max_length=16)
    no_progress_disposition: Literal["stop_and_reorient"]
    capability_gap_disposition: Literal["return_capability_gap"]
    telemetry_sink_ref: str = Field(min_length=1, max_length=512)
    missing_telemetry: Literal["unknown"]
    preserves_required_verification: Literal[True]
    execution_authority: Literal[False]

    @model_validator(mode="after")
    def bounded_references(self) -> ResourcePreflight:
        for values in (self.working_set, self.reusable_evidence, self.invalidation_triggers):
            if any(not value.strip() or len(value) > 512 or any(ord(c) < 32 for c in value) for value in values):
                raise ValueError("resource preflight requires bounded non-empty references")
            if len(values) != len(set(values)):
                raise ValueError("resource preflight references must be unique")
        if not re.fullmatch(
            r"GrahamArdent/PROGRAMSTART@[0-9a-f]{40}:docs/PROGRAMSTART_COST_GOVERNANCE.md",
            self.policy_ref,
        ):
            raise ValueError("resource policy must reference exact PROGRAMSTART Cost Governance")
        return self
