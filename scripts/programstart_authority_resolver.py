"""Resolve owner-local PROGRAMSTART authority from an exact repository commit.

The committed declaration is owner-native machine-readable authority, not a PROGRAMSTART
registry or an operator/model assertion. Every permission remains explicit in the owning
repository and every referenced artifact is verified from the same Git tree before a
snapshot is produced.
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path, PurePosixPath
from typing import Any, Literal

import jsonschema
from pydantic import BaseModel, ConfigDict, Field, ValidationError, model_validator

from .programstart_intent_compile import (
    AuthoritySnapshot,
    CompiledWorkPacket,
    DecisionOperationalizationBinding,
    MatrixProjectionBinding,
    OperationalizationEvidence,
    ParallelWork,
    SurfaceRef,
    _digest,
)
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
from .programstart_resource_preflight import ResourcePreflight

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
    decision_operationalization_path: str | None = None
    resource_preflight_required: bool = False
    resource_preflight_path: str | None = None
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
        if self.resource_preflight_path and not self.resource_preflight_required:
            raise ValueError("resource preflight path requires an active owner gate")
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

    resource_plan = None
    if declaration.resource_preflight_required:
        if not declaration.resource_preflight_path:
            raise AuthorityResolutionError("required reasoning/token resource preflight is missing")
        raw_plan = _blob(root, observed, declaration.resource_preflight_path)
        if len(raw_plan.encode("utf-8")) > 16384:
            raise AuthorityResolutionError("resource preflight exceeds bounded size")
        try:
            resource_plan = ResourcePreflight.model_validate_json(raw_plan)
        except (ValidationError, json.JSONDecodeError) as exc:
            raise AuthorityResolutionError("resource preflight is invalid") from exc
        if resource_plan.work_ref not in declaration.current_work_refs:
            raise AuthorityResolutionError("resource preflight must bind declared current work")
        _blob(root, observed, resource_plan.work_ref)  # validate regular, safe owner artifact
        work_bytes = subprocess.run(
            ["git", "-C", str(root), "show", f"{observed}:{resource_plan.work_ref}"],
            check=True,
            capture_output=True,
        ).stdout
        if hashlib.sha256(work_bytes).hexdigest() != resource_plan.work_sha256:
            raise AuthorityResolutionError("resource preflight work digest is stale")
        policy_ref = f"GrahamArdent/PROGRAMSTART@{observation.methodology_commit}:docs/PROGRAMSTART_COST_GOVERNANCE.md"
        if resource_plan.policy_ref != policy_ref:
            raise AuthorityResolutionError("resource preflight methodology is stale")

    snapshot = AuthoritySnapshot(
        owner_repository_root=str(root) if declaration.decision_operationalization_path else None,
        resource_preflight=resource_plan,
        **declaration.model_dump(exclude={"schema_version", "authority_paths", "decision_operationalization_path"}),
        authority_paths=[declarations[0], *declaration.authority_paths],
        authority_commit=observed,
        methodology_commit=observation.methodology_commit,
    )

    # Projection acquisition needs an explicit separately supplied trusted Matrix checkout.
    # Keep the snapshot nonready until the caller binds that evidence through the adapter.
    return snapshot


def compose_decision_operationalization_currentness(
    authority: AuthoritySnapshot,
    binding: DecisionOperationalizationBinding | None,
) -> AuthoritySnapshot:
    """Bind decision-derived Matrix currentness after owner-native authority resolution."""

    if binding is None:
        raise AuthorityResolutionError(
            "decision-derived currentness composition requires an explicit decision operationalization binding"
        )
    if not isinstance(binding, DecisionOperationalizationBinding):
        raise AuthorityResolutionError("decision operationalization currentness binding is not typed/validated")
    try:
        binding = DecisionOperationalizationBinding.model_validate(binding.model_dump(mode="python"))
    except ValidationError as exc:
        raise AuthorityResolutionError("decision operationalization currentness binding is no longer valid") from exc
    if authority.decision_operationalization is not None and authority.decision_operationalization != binding:
        raise AuthorityResolutionError("resolved authority already carries a different decision operationalization binding")
    return authority.model_copy(update={"decision_operationalization": binding})


def _json_artifact(root: Path, commit: str, path: str) -> dict[str, Any]:
    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise AuthorityResolutionError("duplicate JSON key in owner evidence")
            result[key] = value
        return result

    text = _blob(root, commit, path)
    if len(text.encode()) > 1_048_576:
        raise AuthorityResolutionError("operationalization evidence exceeds bounded size")
    result = json.loads(text, object_pairs_hook=unique)
    if not isinstance(result, dict):
        raise AuthorityResolutionError("operationalization artifact must be an object")
    return result


def _owner_selection(root: Path, repository: str, commit: str) -> str | None:
    if _git(root, "rev-parse", "HEAD") != commit:
        raise AuthorityResolutionError("operationalization owner head is stale")
    paths = [path for path in OWNER_AUTHORITY_PATHS if _git(root, "ls-tree", commit, "--", path)]
    if len(paths) != 1:
        raise AuthorityResolutionError("exact owner authority declaration required")
    declaration = OwnerAuthorityDeclaration.model_validate(_json_artifact(root, commit, paths[0]))
    if declaration.owning_repository != repository:
        raise AuthorityResolutionError("operationalization owner repository mismatch")
    return declaration.decision_operationalization_path


def resolve_operationalization_binding(
    authority: AuthoritySnapshot,
    matrix_repository_root: Path,
) -> DecisionOperationalizationBinding:
    """Reconstruct evidence from an explicitly selected current owner Git contract.

    Repositories must be obtained through the caller's authenticated acquisition
    path, as for RepositoryAuthorityObservation. A local path is not provenance.
    """
    if not authority.owner_repository_root:
        raise AuthorityResolutionError("owner-resolved repository evidence required")
    root = Path(authority.owner_repository_root)
    selected = _owner_selection(root, authority.owning_repository, authority.authority_commit)
    if not selected:
        raise AuthorityResolutionError("owner has not selected a decision operationalization")
    evidence = OperationalizationEvidence(
        owner_repository_root=str(root.resolve()),
        owner_repository=authority.owning_repository,
        owner_commit=authority.authority_commit,
        descriptor_path=selected,
        matrix_repository_root=str(matrix_repository_root.resolve()),
    )
    return _reconstruct_binding(evidence)


def _reconstruct_binding(evidence: OperationalizationEvidence) -> DecisionOperationalizationBinding:
    from .matrix_projection_dependency.operationalization import (
        project_operationalization,
        reconstruct_operationalization,
        validate_manifest,
    )
    from .matrix_projection_dependency.root_frontier import root_frontier

    root = Path(evidence.owner_repository_root)
    selected = _owner_selection(root, evidence.owner_repository, evidence.owner_commit)
    if not selected or selected != evidence.descriptor_path:
        raise AuthorityResolutionError("owner-selected operationalization descriptor mismatch")
    descriptor = _json_artifact(root, evidence.owner_commit, selected)
    if descriptor.get("contract_version") != "programstart.accepted-operationalization.v1":
        raise AuthorityResolutionError("unsupported owner operationalization contract")
    manifest = _json_artifact(root, evidence.owner_commit, descriptor["manifest_path"])
    validate_manifest(manifest)
    if (
        manifest["contract_version"] != "1.0"
        or manifest["projection_role"] != "ACTIVE_OPERATIONALIZATION"
        or descriptor["accepted_manifest_sha256"] != _digest(manifest)
        or descriptor["owner_decision_ref"] not in manifest["decision_refs"]
    ):
        raise AuthorityResolutionError("accepted ACTIVE full owner manifest required")
    if manifest["source_ref"] != f"{evidence.owner_repository}:{descriptor['manifest_path']}":
        raise AuthorityResolutionError("operationalization source must bind the exact current owner manifest file")
    for ref in (manifest["owner"], manifest["source_ref"]):
        if ref.split("@", 1)[0].split("#", 1)[0].split(":", 1)[0] != evidence.owner_repository:
            raise AuthorityResolutionError("manifest owner/source repository mismatch")
    repository_version, path = descriptor["projection_ref"].split(":", 1)
    repository, commit = repository_version.rsplit("@", 1)
    if repository != "GrahamArdent/ecosystem-matrix" or re.fullmatch(r"[0-9a-f]{40}", commit) is None:
        raise AuthorityResolutionError("immutable Matrix-owned projection required")
    artifact = _json_artifact(Path(evidence.matrix_repository_root), commit, path)
    recovered = reconstruct_operationalization(artifact)
    graph = _json_artifact(root, evidence.owner_commit, descriptor["readiness_path"])
    receipt = _json_artifact(root, evidence.owner_commit, descriptor["reconstruction_path"])
    source = artifact["source_binding"]
    if (
        artifact.get("artifact_version") != "2.0"
        or artifact.get("artifact_type") != "ecosystem_matrix.operationalization_projection"
        or artifact.get("execution_authority") is not False
        or source
        != {
            "owner": evidence.owner_repository,
            "ref": manifest["source_ref"],
            "version": manifest["source_version"],
            "currentness": "CURRENT",
        }
        or recovered != manifest
        or artifact.get("root_task_id") != descriptor["root_task_id"]
    ):
        raise AuthorityResolutionError("projection is thin or mismatches current full owner semantics")
    bookkeeping = artifact["matrix_bookkeeping"]
    if bookkeeping != {
        "projection_currentness": "CURRENT",
        "ingestion_reconciliation_state": "RECONCILED",
        "reconsideration_required": False,
    }:
        raise AuthorityResolutionError("projection is not reconciled/current")
    expected_artifact = project_operationalization(
        manifest,
        source_owner=evidence.owner_repository,
        source_ref=manifest["source_ref"],
        source_version=manifest["source_version"],
        readiness_graph=graph,
        root_task_id=descriptor["root_task_id"],
        projection_identity=artifact["projection_identity"],
    )
    if expected_artifact != artifact:
        raise AuthorityResolutionError("projection differs from current native owner reconstruction")
    frontier = root_frontier(graph, descriptor["root_task_id"])
    if frontier != artifact["frontier"] or frontier["selected_task_id"] is None or frontier["readiness_blocker_ids"]:
        raise AuthorityResolutionError("material owner graph is not ready")
    semantic = _digest({key: artifact[key] for key in ("owner_manifest", "readiness_graph", "root_task_id")})
    if artifact["semantic_hash"] != semantic:
        raise AuthorityResolutionError("comprehensive semantic hash mismatch")
    if receipt != {
        "record_type": "matrix.operationalization_reconstruction.v1",
        "execution_authority": False,
        "projection_sha256": _digest(artifact),
        "reconstructed_manifest": manifest,
        "reconstructed_manifest_sha256": _digest(manifest),
    }:
        raise AuthorityResolutionError("actual full reconstruction evidence mismatch")
    if _owner_selection(root, evidence.owner_repository, evidence.owner_commit) != selected:
        raise AuthorityResolutionError("owner operationalization changed during reconstruction")
    projection = MatrixProjectionBinding(
        artifact_version="2.0",
        projection_role="ACTIVE_OPERATIONALIZATION",
        artifact_ref=descriptor["projection_ref"],
        projection_identity=artifact["projection_identity"],
        decision_ref=descriptor["owner_decision_ref"],
        source_ref=manifest["source_ref"],
        source_version=manifest["source_version"],
        semantic_hash=semantic,
        source_fingerprint=_digest({"owner": source["owner"], "ref": source["ref"], "version": source["version"]}),
        source_currentness="CURRENT",
        projection_currentness="CURRENT",
        ingestion_reconciliation_state="RECONCILED",
        reconsideration_required=False,
        execution_authority=False,
    )
    return DecisionOperationalizationBinding(
        owner_decision_ref=descriptor["owner_decision_ref"],
        operationalization_source_ref=manifest["source_ref"],
        operationalization_source_version=manifest["source_version"],
        projection_identity=artifact["projection_identity"],
        matrix_projection=projection,
        reconstruction_evidence=evidence,
    )


def verify_bound_operationalization(binding: DecisionOperationalizationBinding) -> bool:
    try:
        evidence = binding.reconstruction_evidence
        return evidence is not None and _reconstruct_binding(evidence).model_dump() == binding.model_dump()
    except (ValueError, KeyError, TypeError, OSError, AttributeError, jsonschema.ValidationError):
        return False


def verify_authority_operationalization(authority: AuthoritySnapshot) -> bool:
    binding = authority.decision_operationalization
    try:
        if authority.owner_repository_root:
            selected = _owner_selection(
                Path(authority.owner_repository_root), authority.owning_repository, authority.authority_commit
            )
            if selected and (binding is None or binding.reconstruction_evidence is None):
                return False
        if binding is not None:
            evidence = binding.reconstruction_evidence
            return bool(
                evidence is not None
                and evidence.owner_repository == authority.owning_repository
                and evidence.owner_commit == authority.authority_commit
                and (
                    authority.owner_repository_root is None
                    or Path(evidence.owner_repository_root).resolve() == Path(authority.owner_repository_root).resolve()
                )
            )
        return True
    except (ValueError, KeyError, TypeError, OSError, AttributeError, jsonschema.ValidationError):
        return False


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
