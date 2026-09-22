"""Resolve owner-local PROGRAMSTART authority from an exact repository commit.

The committed declaration is owner-native machine-readable authority, not a PROGRAMSTART
registry or an operator/model assertion. Every permission remains explicit in the owning
repository and every referenced artifact is verified from the same Git tree before a
snapshot is produced.
"""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path, PurePosixPath
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, ValidationError, model_validator

from .programstart_intent_compile import AuthoritySnapshot, CompiledWorkPacket, ParallelWork, SurfaceRef
from .programstart_intent_ingress import (
    BoundedIntentEnvelope,
    ContextualIntentRequest,
    ContextualIntentResolution,
    ConversationHarvest,
    SemanticProducerRequest,
    SemanticProducerValidation,
    build_trusted_conversation_harvest,
    resolve_contextual_intent,
    validate_semantic_producer_response,
)

OWNER_AUTHORITY_PATHS = (
    ".programstart/authority.json",
    "PROGRAMSTART_AUTHORITY.json",
)


class AuthorityResolutionError(ValueError):
    """The observed repository cannot truthfully produce a current snapshot."""


class RepositoryAuthorityObservation(BaseModel):
    """Mechanical repository evidence supplied to the owner-local resolver."""

    model_config = ConfigDict(extra="forbid")

    repository_root: Path
    owning_repository: str
    observed_head: str
    methodology_commit: str

    @model_validator(mode="after")
    def evidence_must_be_explicit(self) -> RepositoryAuthorityObservation:
        if any(not value.strip() for value in (self.owning_repository, self.observed_head, self.methodology_commit)):
            raise ValueError("repository observation requires owner, observed head, and methodology commit")
        if any(re.fullmatch(r"[0-9a-f]{40,64}", value) is None for value in (self.observed_head, self.methodology_commit)):
            raise ValueError("repository observation commit evidence must be an exact hexadecimal object id")
        return self


class OwnerAuthorityDeclaration(BaseModel):
    """Strict owner-native declaration stored in the owning repository."""

    model_config = ConfigDict(extra="forbid")

    schema_version: Literal["programstart.owner-authority.v1"]
    project_name: str
    owning_repository: str
    execution_mode: str
    authority_paths: list[str] = Field(min_length=1, max_length=16)
    current_work_refs: list[str] = Field(default_factory=list, max_length=8)
    mutable_surfaces: list[SurfaceRef] = Field(default_factory=list)
    read_only_surfaces: list[SurfaceRef] = Field(default_factory=list)
    allowed_effects: list[str] = Field(default_factory=list)
    prohibited_effects: list[str] = Field(default_factory=list)
    human_gate_conditions: list[str] = Field(default_factory=list)
    automation_gap_conditions: list[str] = Field(default_factory=list)
    evidence_requirements: list[str] = Field(default_factory=list)
    acceptance_conditions: list[str] = Field(default_factory=list)
    challenge_required: bool = False
    invalidation_triggers: list[str] = Field(default_factory=list)
    stop_conditions: list[str] = Field(default_factory=list)
    parallel_work: list[ParallelWork] = Field(default_factory=list)

    @model_validator(mode="after")
    def declaration_must_be_unambiguous(self) -> OwnerAuthorityDeclaration:
        if any(not value.strip() for value in (self.project_name, self.owning_repository, self.execution_mode)):
            raise ValueError("owner authority requires project, repository, and execution mode")
        refs = [*self.authority_paths, *self.current_work_refs]
        refs.extend(work.evidence_ref for work in self.parallel_work)
        if any(not ref.strip() for ref in refs):
            raise ValueError("owner authority artifact references must not be empty")
        if len(refs) != len(set(refs)):
            raise ValueError("owner authority artifact references must be unique")
        if any(not work.name.strip() or not work.owner.strip() or not work.protected_surfaces for work in self.parallel_work):
            raise ValueError("parallel work requires an explicit owner and protected surface")
        text_lists = (
            self.allowed_effects,
            self.prohibited_effects,
            self.human_gate_conditions,
            self.automation_gap_conditions,
            self.evidence_requirements,
            self.acceptance_conditions,
            self.invalidation_triggers,
            self.stop_conditions,
        )
        if any(not value.strip() for values in text_lists for value in values):
            raise ValueError("owner authority declarations must not contain empty semantic values")
        return self


class OwnerLocalIntentResult(BaseModel):
    """Composition result; Controller admission is deliberately absent."""

    semantic_validation: SemanticProducerValidation
    authority: AuthoritySnapshot
    resolution: ContextualIntentResolution


def _git(root: Path, *args: str) -> str:
    completed = subprocess.run(
        ["git", "-C", str(root), *args],
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode:
        raise AuthorityResolutionError("repository evidence could not be read as a Git repository")
    return completed.stdout.strip()


def _safe_repo_path(value: str) -> str:
    if "\\" in value or any(ord(character) < 32 for character in value):
        raise AuthorityResolutionError(f"unsafe repository-relative authority path: {value!r}")
    path = PurePosixPath(value)
    if not value or path.is_absolute() or any(part in ("", ".", "..") for part in path.parts):
        raise AuthorityResolutionError(f"unsafe repository-relative authority path: {value!r}")
    return path.as_posix()


def _blob(root: Path, commit: str, path: str) -> str:
    safe = _safe_repo_path(path)
    entry = _git(root, "ls-tree", commit, "--", safe)
    fields = entry.split(None, 3)
    if len(fields) != 4 or fields[0] not in {"100644", "100755"} or fields[1] != "blob":
        raise AuthorityResolutionError(f"authority artifact is not a regular file at observed head: {safe}")
    return _git(root, "show", f"{commit}:{safe}")


def resolve_repository_authority(observation: RepositoryAuthorityObservation) -> AuthoritySnapshot:
    """Build an AuthoritySnapshot only from one exact owner repository tree."""

    root = observation.repository_root.resolve()
    if not root.is_dir():
        raise AuthorityResolutionError("owning repository root does not exist")
    head = _git(root, "rev-parse", "HEAD")
    observed = observation.observed_head.strip()
    if head != observed or _git(root, "rev-parse", observed) != observed:
        raise AuthorityResolutionError("observed repository head is stale or not an exact commit")
    methodology_root = Path(__file__).resolve().parents[1]
    methodology_head = _git(methodology_root, "rev-parse", "HEAD")
    if observation.methodology_commit != methodology_head:
        raise AuthorityResolutionError("observed PROGRAMSTART methodology head is stale")

    declarations: list[str] = []
    for candidate in OWNER_AUTHORITY_PATHS:
        completed = subprocess.run(
            ["git", "-C", str(root), "cat-file", "-e", f"{observed}:{candidate}"],
            check=False,
            capture_output=True,
        )
        if completed.returncode == 0:
            declarations.append(candidate)
    if len(declarations) != 1:
        raise AuthorityResolutionError("repository must expose exactly one owner-native PROGRAMSTART authority declaration")

    try:
        declaration = OwnerAuthorityDeclaration.model_validate_json(_blob(root, observed, declarations[0]))
    except (ValidationError, json.JSONDecodeError) as exc:
        raise AuthorityResolutionError("owner-native authority declaration is invalid") from exc
    if declaration.owning_repository != observation.owning_repository:
        raise AuthorityResolutionError("owner-native authority repository does not match the observed target")

    referenced = [*declaration.authority_paths, *declaration.current_work_refs]
    referenced.extend(work.evidence_ref for work in declaration.parallel_work)
    if declarations[0] in referenced:
        raise AuthorityResolutionError("owner authority declaration must not duplicate its own artifact reference")
    for path in referenced:
        _blob(root, observed, path)

    current_packet_entry = _git(root, "ls-tree", observed, "--", "CURRENT_WORK_PACKET.md")
    if current_packet_entry and "CURRENT_WORK_PACKET.md" not in declaration.current_work_refs:
        raise AuthorityResolutionError("current owner Work Packet exists but is not explicitly declared")

    return AuthoritySnapshot(
        **declaration.model_dump(exclude={"schema_version", "authority_paths"}),
        authority_paths=[declarations[0], *declaration.authority_paths],
        authority_commit=observed,
        methodology_commit=observation.methodology_commit,
    )


def compose_owner_local_intent(
    envelope: BoundedIntentEnvelope,
    raw_semantic_response: Any,
    observation: RepositoryAuthorityObservation,
    *,
    current_repository: str = "",
    existing_packet: CompiledWorkPacket | None = None,
) -> OwnerLocalIntentResult:
    """Validate semantics, resolve owner authority, then use the existing compiler path."""

    request = SemanticProducerRequest.from_envelope(envelope)
    semantic = validate_semantic_producer_response(request, raw_semantic_response)
    authority = resolve_repository_authority(observation)
    if semantic.accepted:
        candidate = semantic.candidate
        if candidate is None:  # pragma: no cover - enforced by the result model
            raise AssertionError("accepted semantic response has no candidate")
        harvest = build_trusted_conversation_harvest(envelope, candidate)
    else:
        harvest = ConversationHarvest(
            context_ref=envelope.context_ref,
            latest_operator_utterance=envelope.latest_operator_utterance,
            project_hint=envelope.project_hint,
            converged=False,
            existing_work_packet_ref=envelope.existing_work_packet_ref,
        )
    resolution = resolve_contextual_intent(
        ContextualIntentRequest(
            harvest=harvest,
            current_repository=current_repository,
            authority=authority,
            existing_packet=existing_packet,
        )
    )
    return OwnerLocalIntentResult(semantic_validation=semantic, authority=authority, resolution=resolution)
