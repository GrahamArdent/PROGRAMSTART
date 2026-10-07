"""Natural owner gate and adversarial resource-policy checks."""

import hashlib
import json
import subprocess

import pytest
from pydantic import ValidationError

from scripts.programstart_authority_resolver import (
    AuthorityResolutionError,
    resolve_repository_authority,
)
from scripts.programstart_intent_compile import (
    IntentKind,
    assess_authority_drift,
    compile_work_packet,
    verify_integrity,
)
from scripts.programstart_resource_preflight import ResourcePreflight
from tests.test_programstart_authority_resolver import METHODOLOGY_COMMIT, _declaration, _git, _observation, _repo


def _plan(**updates):
    value = {
        "schema_version": "programstart.resource-preflight.v1",
        "work_ref": "CURRENT_WORK_PACKET.md",
        "work_sha256": hashlib.sha256(b"# derived current work\n").hexdigest(),
        "policy_ref": f"GrahamArdent/PROGRAMSTART@{METHODOLOGY_COMMIT}:docs/PROGRAMSTART_COST_GOVERNANCE.md",
        "working_set": ["CURRENT_WORK_PACKET.md", "docs/MASTER_GAMEPLAN.md"],
        "reusable_evidence": [],
        "invalidation_triggers": ["owner work, policy, approved profile or capability changes"],
        "steps": [
            {"task": "Verify exact state and focused checks", "task_kind": "mechanical", "execution_class": "deterministic"}
        ],
        "no_progress_disposition": "stop_and_reorient",
        "capability_gap_disposition": "return_capability_gap",
        "telemetry_sink_ref": "owner/product#1",
        "missing_telemetry": "unknown",
        "preserves_required_verification": True,
        "execution_authority": False,
    }
    value.update(updates)
    return value


def _ready_repo(tmp_path):
    root, _ = _repo(
        tmp_path,
        _declaration(
            resource_preflight_required=True,
            resource_preflight_path=".programstart/resource-preflight.json",
        ),
    )
    (root / ".programstart/resource-preflight.json").write_text(json.dumps(_plan()))
    _git(root, "add", ".")
    _git(root, "commit", "-m", "bind current resource preflight")
    return root, _git(root, "rev-parse", "HEAD")


def test_missing_required_gate_fails_before_packet(tmp_path):
    root, head = _repo(tmp_path, _declaration(resource_preflight_required=True))
    with pytest.raises(AuthorityResolutionError, match="preflight is missing"):
        resolve_repository_authority(_observation(root, head))


def test_current_owner_preflight_compiles_and_cold_reconstructs(tmp_path):
    root, head = _ready_repo(tmp_path)
    first = resolve_repository_authority(_observation(root, head))
    packet = compile_work_packet("Continue selected work", first, kind=IntentKind.CONTINUATION)
    cold = tmp_path / "cold"
    subprocess.run(["git", "clone", "--quiet", str(root), str(cold)], check=True)
    second = resolve_repository_authority(_observation(cold, head))
    replay = compile_work_packet("Continue selected work", second, kind=IntentKind.CONTINUATION)
    assert verify_integrity(packet)
    assert packet.semantic_digest == replay.semantic_digest
    assert packet.scope.allowed_effects == first.allowed_effects
    assert packet.authority.resource_preflight.execution_authority is False


def test_changed_work_invalidates_preflight(tmp_path):
    root, _ = _ready_repo(tmp_path)
    (root / "CURRENT_WORK_PACKET.md").write_text("# broader scope\n")
    _git(root, "add", ".")
    _git(root, "commit", "-m", "changed scope")
    with pytest.raises(AuthorityResolutionError, match="work digest is stale"):
        resolve_repository_authority(_observation(root, _git(root, "rev-parse", "HEAD")))


@pytest.mark.parametrize(
    "change",
    [
        {"policy_ref": "GrahamArdent/PROGRAMSTART@" + "0" * 40 + ":docs/PROGRAMSTART_COST_GOVERNANCE.md"},
        {"work_ref": "docs/MASTER_GAMEPLAN.md"},
        {"extra_permission": "publish"},
        {"execution_authority": True},
    ],
)
def test_invalid_or_stale_owner_plan_rejected(tmp_path, change):
    root, _ = _ready_repo(tmp_path)
    (root / ".programstart/resource-preflight.json").write_text(json.dumps(_plan(**change)))
    _git(root, "add", ".")
    _git(root, "commit", "-m", "invalid resource plan")
    with pytest.raises(AuthorityResolutionError):
        resolve_repository_authority(_observation(root, _git(root, "rev-parse", "HEAD")))


@pytest.mark.parametrize(
    "change",
    [
        {"execution_class": "approved_stronger", "approved_profile_ref": "owner/compute#approved"},
        {
            "task_kind": "bounded_reasoning",
            "execution_class": "approved_stronger",
            "approved_profile_ref": "owner/compute#approved",
            "escalation_reason": "missing_credentials",
            "escalation_evidence": "credential absent",
            "step_down_condition": "credential arrives",
        },
        {
            "task_kind": "unresolved_decision",
            "execution_class": "approved_stronger",
            "approved_profile_ref": "owner/compute#approved",
            "escalation_reason": "conflicting_evidence",
            "escalation_evidence": "owner/evidence#1",
        },
    ],
)
def test_premium_misuse_or_missing_stepdown_rejected(change):
    step = {"task": "check", "task_kind": "mechanical", "execution_class": "deterministic"}
    step.update(change)
    with pytest.raises(ValidationError):
        ResourcePreflight.model_validate(_plan(steps=[step]))


def test_escalation_then_deterministic_stepdown_is_representable():
    plan = ResourcePreflight.model_validate(
        _plan(
            steps=[
                {
                    "task": "Resolve conflicting owner evidence",
                    "task_kind": "unresolved_decision",
                    "execution_class": "approved_stronger",
                    "approved_profile_ref": "owner/compute#approved",
                    "escalation_reason": "conflicting_evidence",
                    "escalation_evidence": "owner/evidence#1",
                    "step_down_condition": "contradiction resolved with exact current owner receipt",
                },
                {"task": "Run focused verification", "task_kind": "mechanical", "execution_class": "deterministic"},
            ]
        )
    )
    assert plan.steps[1].execution_class == "deterministic"


def test_missing_compilation_binding_is_rejected_even_after_resolution(tmp_path):
    root, head = _ready_repo(tmp_path)
    authority = resolve_repository_authority(_observation(root, head))
    authority.resource_preflight = None
    with pytest.raises(ValueError, match="preflight is missing"):
        compile_work_packet("Continue", authority, kind=IntentKind.CONTINUATION)


def test_preflight_tampering_changes_fingerprint_and_invalidates_packet(tmp_path):
    root, head = _ready_repo(tmp_path)
    authority = resolve_repository_authority(_observation(root, head))
    packet = compile_work_packet("Continue", authority, kind=IntentKind.CONTINUATION)
    changed = authority.model_copy(deep=True)
    changed.resource_preflight.telemetry_sink_ref = "owner/product#2"
    assert assess_authority_drift(packet, changed).status == "recompile_required"
    packet.authority.resource_preflight.telemetry_sink_ref = "owner/product#2"
    assert not verify_integrity(packet)


def test_legacy_snapshot_serialization_does_not_add_resource_fields(tmp_path):
    root, head = _repo(tmp_path, _declaration())
    authority = resolve_repository_authority(_observation(root, head))
    payload = authority.model_dump(mode="json")
    assert not any(key.startswith("resource_preflight") for key in payload)
    packet = compile_work_packet("Continue", authority, kind=IntentKind.CONTINUATION)
    assert not any(key.startswith("resource_preflight") for key in packet.model_dump(mode="json")["authority"])
    assert verify_integrity(packet)
