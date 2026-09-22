import json
import subprocess
from pathlib import Path

import pytest

from scripts.programstart_authority_resolver import (
    AuthorityResolutionError,
    RepositoryAuthorityObservation,
    compose_owner_local_intent,
    resolve_repository_authority,
)
from scripts.programstart_intent_compile import SurfaceType, authority_fingerprint
from scripts.programstart_intent_ingress import (
    SEMANTIC_PRODUCER_RESPONSE_VERSION,
    BoundedIntentEnvelope,
    ContextualTransitionAction,
    SemanticProducerRejection,
    SemanticProducerRequest,
)

OWNER = "owner/product"
METHODOLOGY_COMMIT = subprocess.run(["git", "rev-parse", "HEAD"], check=True, capture_output=True, text=True).stdout.strip()


def _git(root: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(root), *args], check=True, capture_output=True, text=True).stdout.strip()


def _declaration(**updates: object) -> dict[str, object]:
    value: dict[str, object] = {
        "schema_version": "programstart.owner-authority.v1",
        "project_name": "Product",
        "owning_repository": OWNER,
        "execution_mode": "existing_project_mode_c",
        "authority_paths": ["docs/MASTER_GAMEPLAN.md"],
        "current_work_refs": ["CURRENT_WORK_PACKET.md"],
        "mutable_surfaces": [{"surface_type": "repository", "identifier": OWNER, "consequential": False}],
        "read_only_surfaces": [],
        "allowed_effects": ["bounded repository implementation"],
        "prohibited_effects": ["provider mutation"],
        "acceptance_conditions": ["focused tests pass"],
        "parallel_work": [
            {
                "name": "release lane",
                "owner": "release-owner",
                "protected_surfaces": [{"surface_type": "provider", "identifier": "prod", "consequential": True}],
                "evidence_ref": "docs/PARALLEL_OWNERSHIP.md",
            }
        ],
    }
    value.update(updates)
    return value


def _repo(tmp_path: Path, declaration: dict[str, object] | None = None) -> tuple[Path, str]:
    root = tmp_path / "owner"
    (root / ".programstart").mkdir(parents=True)
    (root / "docs").mkdir()
    (root / "docs/MASTER_GAMEPLAN.md").write_text("# current strategic authority\n", encoding="utf-8")
    (root / "CURRENT_WORK_PACKET.md").write_text("# derived current work\n", encoding="utf-8")
    (root / "docs/PARALLEL_OWNERSHIP.md").write_text("release-owner owns prod mutations\n", encoding="utf-8")
    if declaration is not None:
        (root / ".programstart/authority.json").write_text(json.dumps(declaration), encoding="utf-8")
    _git(root, "init")
    _git(root, "config", "user.email", "test@example.com")
    _git(root, "config", "user.name", "Test")
    _git(root, "add", ".")
    _git(root, "commit", "-m", "owner authority")
    return root, _git(root, "rev-parse", "HEAD")


def _observation(root: Path, head: str) -> RepositoryAuthorityObservation:
    return RepositoryAuthorityObservation(
        repository_root=root,
        owning_repository=OWNER,
        observed_head=head,
        methodology_commit=METHODOLOGY_COMMIT,
    )


def _envelope() -> BoundedIntentEnvelope:
    return BoundedIntentEnvelope(
        context_ref="ctx-owner-local",
        latest_operator_utterance="Continue the current bounded implementation.",
        source_principal="operator",
        captured_at="2026-09-22T10:00:00Z",
    )


def _semantic_response(envelope: BoundedIntentEnvelope) -> dict[str, object]:
    request = SemanticProducerRequest.from_envelope(envelope)
    return {
        "schema_version": SEMANTIC_PRODUCER_RESPONSE_VERSION,
        "semantic_effect_id": request.semantic_effect_id,
        "status": "succeeded",
        "candidate": {
            "objective": "Continue the current bounded implementation.",
            "intent_kind": "bounded_execution",
            "converged": True,
            "producer": "accepted-execution-node",
            "producer_version": "b9d6e0b",
        },
    }


def test_valid_explicit_owner_authority_compiles_and_retains_parallel_owner(tmp_path: Path) -> None:
    root, head = _repo(tmp_path, _declaration())
    envelope = _envelope()

    result = compose_owner_local_intent(envelope, _semantic_response(envelope), _observation(root, head))

    assert result.semantic_validation.accepted is True
    assert result.resolution.action == ContextualTransitionAction.COMPILE_FOR_ADMISSION
    assert result.resolution.packet is not None
    assert result.authority.authority_commit == head
    assert result.authority.authority_paths == [
        ".programstart/authority.json",
        "docs/MASTER_GAMEPLAN.md",
    ]
    assert result.authority.current_work_refs == ["CURRENT_WORK_PACKET.md"]
    assert result.authority.parallel_work[0].owner == "release-owner"
    assert result.resolution.packet.dependencies.active_parallel_work[0].owner == "release-owner"
    assert result.resolution.packet.scope.allowed_effects == ["bounded repository implementation"]
    prod = next(surface for surface in result.resolution.packet.scope.surfaces if surface.identifier == "prod")
    assert prod.access == "read_only"


def test_semantic_authority_manufacture_is_rejected_and_no_packet_is_created(tmp_path: Path) -> None:
    root, head = _repo(tmp_path, _declaration())
    envelope = _envelope()
    response = _semantic_response(envelope)
    response["candidate"]["authority_snapshot"] = {"allowed_effects": ["deploy"]}  # type: ignore[index]

    result = compose_owner_local_intent(envelope, response, _observation(root, head))

    assert result.semantic_validation.rejection == SemanticProducerRejection.ATTEMPTED_AUTHORITY_MANUFACTURE
    assert result.resolution.packet is None
    assert result.resolution.action == ContextualTransitionAction.SYNTHESIZE_CURRENT_CONCLUSION


def test_stale_observed_head_is_rejected(tmp_path: Path) -> None:
    root, head = _repo(tmp_path, _declaration())
    (root / "docs/MASTER_GAMEPLAN.md").write_text("changed\n", encoding="utf-8")
    _git(root, "add", ".")
    _git(root, "commit", "-m", "advance owner")

    with pytest.raises(AuthorityResolutionError, match="stale"):
        resolve_repository_authority(_observation(root, head))


def test_stale_methodology_head_is_rejected(tmp_path: Path) -> None:
    root, head = _repo(tmp_path, _declaration())
    observation = _observation(root, head).model_copy(update={"methodology_commit": "0" * 40})

    with pytest.raises(AuthorityResolutionError, match="methodology"):
        resolve_repository_authority(observation)


def test_missing_or_ambiguous_owner_authority_fails_closed(tmp_path: Path) -> None:
    missing_root, missing_head = _repo(tmp_path / "missing", None)
    with pytest.raises(AuthorityResolutionError, match="exactly one"):
        resolve_repository_authority(_observation(missing_root, missing_head))

    root, _ = _repo(tmp_path / "ambiguous", _declaration())
    (root / "PROGRAMSTART_AUTHORITY.json").write_text(json.dumps(_declaration()), encoding="utf-8")
    _git(root, "add", ".")
    _git(root, "commit", "-m", "ambiguous authority")
    with pytest.raises(AuthorityResolutionError, match="exactly one"):
        resolve_repository_authority(_observation(root, _git(root, "rev-parse", "HEAD")))


def test_unsafe_or_missing_authority_artifact_is_rejected(tmp_path: Path) -> None:
    root, head = _repo(tmp_path / "unsafe", _declaration(authority_paths=["../AUTHORITY.md"]))
    with pytest.raises(AuthorityResolutionError, match="unsafe"):
        resolve_repository_authority(_observation(root, head))

    root, head = _repo(tmp_path / "missing-ref", _declaration(authority_paths=["docs/DOES_NOT_EXIST.md"]))
    with pytest.raises(AuthorityResolutionError, match="regular file"):
        resolve_repository_authority(_observation(root, head))


def test_symlink_authority_artifact_and_undeclared_current_packet_are_rejected(tmp_path: Path) -> None:
    root, _ = _repo(tmp_path / "symlink", _declaration())
    (root / "docs/MASTER_GAMEPLAN.md").unlink()
    (root / "docs/MASTER_GAMEPLAN.md").symlink_to("../CURRENT_WORK_PACKET.md")
    _git(root, "add", ".")
    _git(root, "commit", "-m", "symlink authority")
    with pytest.raises(AuthorityResolutionError, match="regular file"):
        resolve_repository_authority(_observation(root, _git(root, "rev-parse", "HEAD")))

    root, head = _repo(tmp_path / "undeclared", _declaration(current_work_refs=[]))
    with pytest.raises(AuthorityResolutionError, match="not explicitly declared"):
        resolve_repository_authority(_observation(root, head))


def test_owner_declaration_cannot_invent_effects_from_repository_existence(tmp_path: Path) -> None:
    root, head = _repo(
        tmp_path,
        _declaration(mutable_surfaces=[], allowed_effects=[], read_only_surfaces=[]),
    )
    envelope = _envelope()
    result = compose_owner_local_intent(envelope, _semantic_response(envelope), _observation(root, head))

    assert result.resolution.packet is not None
    assert result.resolution.packet.scope.allowed_effects == []
    assert result.resolution.packet.scope.mutable_identifiers == []


def test_identical_mechanical_inputs_replay_at_effect_and_snapshot_boundaries(tmp_path: Path) -> None:
    root, head = _repo(tmp_path, _declaration())
    envelope = _envelope()
    response = _semantic_response(envelope)
    observation = _observation(root, head)

    first = compose_owner_local_intent(envelope, response, observation)
    second = compose_owner_local_intent(envelope, response, observation)

    assert first.semantic_validation.semantic_effect_id == second.semantic_validation.semantic_effect_id
    assert authority_fingerprint(first.authority) == authority_fingerprint(second.authority)
    assert first.resolution.packet is not None and second.resolution.packet is not None
    assert first.resolution.packet.specification_id == second.resolution.packet.specification_id
    assert first.authority.mutable_surfaces[0].surface_type == SurfaceType.REPOSITORY
