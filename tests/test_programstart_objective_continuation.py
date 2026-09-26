from __future__ import annotations

import sys
from pathlib import Path
from typing import Literal

import pytest
from pydantic import ValidationError

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.programstart_intent_compile import (  # noqa: E402
    AuthoritySnapshot,
    IntentKind,
    authority_fingerprint,
    compile_work_packet,
)
from scripts.programstart_objective_continuation import (  # noqa: E402
    OBJECTIVE_EVIDENCE_ADAPTER,
    CompletedEffectEvidence,
    ContinuationDisposition,
    EffectReadyEvidence,
    HumanWaitEvidence,
    MachineWaitEvidence,
    RootObjective,
    RootTerminalEvidence,
    evaluate_objective_continuation,
)


def _authority(**changes: object) -> AuthoritySnapshot:
    values: dict[str, object] = {
        "project_name": "Owner",
        "owning_repository": "example/owner",
        "authority_commit": "a" * 40,
        "authority_paths": ["AGENTS.md"],
        "methodology_commit": "b" * 40,
        "execution_mode": "bounded",
        "allowed_effects": ["inspect semantic state", "apply bounded change", "verify acceptance"],
        "prohibited_effects": ["publish release"],
        "human_gate_conditions": ["owner approval explicitly required"],
        "automation_gap_conditions": ["verified actuator unavailable"],
    }
    values.update(changes)
    return AuthoritySnapshot.model_validate(values)


@pytest.fixture
def context():
    authority = _authority()
    packet = compile_work_packet(
        "Continue the root objective.",
        authority,
        kind=IntentKind.CONTINUATION,
        interpreted_objective="Deliver the accepted root outcome.",
    )
    root = RootObjective(root_id="root-113", objective="Deliver the accepted root outcome.")
    binding = {
        "root_id": root.root_id,
        "work_packet_specification_id": packet.specification_id,
        "authority_fingerprint": authority_fingerprint(authority),
    }
    return root, packet, authority, binding


def _ready(token: str, binding: dict[str, str], *, evidence_id: str = "ready") -> EffectReadyEvidence:
    return EffectReadyEvidence(
        evidence_id=evidence_id,
        status="proven",
        semantic_effect_token=token,
        preconditions_proven=True,
        root_id=binding["root_id"],
        work_packet_specification_id=binding["work_packet_specification_id"],
        authority_fingerprint=binding["authority_fingerprint"],
    )


def test_readiness_receipt_selects_effect_not_allowed_effect_order(context) -> None:
    root, packet, authority, binding = context
    evidence = [_ready("apply bounded change", binding)]
    selected = evaluate_objective_continuation(root, packet, authority, evidence)
    assert selected.semantic_effect_token == "apply bounded change"

    reordered_authority = _authority(allowed_effects=["verify acceptance", "apply bounded change", "inspect semantic state"])
    reordered_packet = compile_work_packet(
        "Continue the root objective.",
        reordered_authority,
        kind=IntentKind.CONTINUATION,
        interpreted_objective="Deliver the accepted root outcome.",
    )
    reordered_binding = {
        "root_id": root.root_id,
        "work_packet_specification_id": reordered_packet.specification_id,
        "authority_fingerprint": authority_fingerprint(reordered_authority),
    }
    reordered = evaluate_objective_continuation(
        root,
        reordered_packet,
        reordered_authority,
        [_ready("apply bounded change", reordered_binding)],
    )
    assert reordered.semantic_effect_token == selected.semantic_effect_token


def test_readiness_receipt_is_required(context) -> None:
    root, packet, authority, binding = context
    assert evaluate_objective_continuation(root, packet, authority, []).disposition == ContinuationDisposition.REORIENT
    completed = CompletedEffectEvidence(
        evidence_id="done",
        status="accepted",
        semantic_effect_token="inspect semantic state",
        **binding,
    )
    assert evaluate_objective_continuation(root, packet, authority, [completed]).disposition == ContinuationDisposition.REORIENT


def test_completed_effects_need_only_be_admitted_not_an_ordered_prefix(context) -> None:
    root, packet, authority, binding = context
    completed = CompletedEffectEvidence(
        evidence_id="done-verify",
        status="accepted",
        semantic_effect_token="verify acceptance",
        **binding,
    )
    decision = evaluate_objective_continuation(root, packet, authority, [completed, _ready("inspect semantic state", binding)])
    assert decision.semantic_effect_token == "inspect semantic state"


def test_ambiguous_replay_and_out_of_scope_readiness_fail_closed(context) -> None:
    root, packet, authority, binding = context
    ambiguous = [
        _ready("inspect semantic state", binding, evidence_id="ready-1"),
        _ready("apply bounded change", binding, evidence_id="ready-2"),
    ]
    assert evaluate_objective_continuation(root, packet, authority, ambiguous).disposition == ContinuationDisposition.REORIENT
    duplicate = [
        _ready("inspect semantic state", binding, evidence_id="ready-1"),
        _ready("inspect semantic state", binding, evidence_id="ready-2"),
    ]
    assert evaluate_objective_continuation(root, packet, authority, duplicate).disposition == ContinuationDisposition.REORIENT

    completed = CompletedEffectEvidence(
        evidence_id="done",
        status="accepted",
        semantic_effect_token="inspect semantic state",
        **binding,
    )
    replay = [completed, _ready("inspect semantic state", binding)]
    assert evaluate_objective_continuation(root, packet, authority, replay).disposition == ContinuationDisposition.REORIENT

    outside = [_ready("invent a deployment", binding)]
    assert evaluate_objective_continuation(root, packet, authority, outside).disposition == ContinuationDisposition.REORIENT


def test_ready_evidence_contract_is_strict_and_proven(context) -> None:
    _, _, _, binding = context
    with pytest.raises(ValidationError):
        EffectReadyEvidence.model_validate(
            {
                "evidence_id": "ready",
                "status": "accepted",
                "semantic_effect_token": "inspect semantic state",
                "preconditions_proven": True,
                **binding,
            }
        )
    with pytest.raises(ValidationError):
        EffectReadyEvidence.model_validate(
            {
                "evidence_id": "ready",
                "status": "proven",
                "semantic_effect_token": "inspect semantic state",
                "preconditions_proven": False,
                **binding,
            }
        )


def test_root_objective_validator_uses_renamed_root_id() -> None:
    assert RootObjective(root_id="root-1", objective="Outcome").root_id == "root-1"
    with pytest.raises(ValidationError):
        RootObjective(root_id=" root-1", objective="Outcome")


def test_executor_material_cannot_escape_as_an_effect(context) -> None:
    root, _, _, _ = context
    authority = _authority(allowed_effects=["git push origin main"])
    packet = compile_work_packet(
        "Continue the root objective.",
        authority,
        kind=IntentKind.CONTINUATION,
        interpreted_objective="Deliver the accepted root outcome.",
    )
    binding = {
        "root_id": root.root_id,
        "work_packet_specification_id": packet.specification_id,
        "authority_fingerprint": authority_fingerprint(authority),
    }
    decision = evaluate_objective_continuation(root, packet, authority, [_ready("git push origin main", binding)])
    assert decision.disposition == ContinuationDisposition.REORIENT


def test_currentness_drift_and_packet_integrity_fail_closed(context) -> None:
    root, packet, authority, _ = context
    changed = authority.model_copy(update={"authority_commit": "c" * 40})
    assert evaluate_objective_continuation(root, packet, changed, []).disposition == ContinuationDisposition.REORIENT
    corrupt = packet.model_copy(update={"semantic_digest": "0" * 64})
    assert evaluate_objective_continuation(root, corrupt, authority, []).disposition == ContinuationDisposition.REORIENT


def test_prohibited_next_effect_reorients(context) -> None:
    root, _, _, _ = context
    authority = _authority(prohibited_effects=["inspect semantic state"])
    packet = compile_work_packet(
        "Continue the root objective.",
        authority,
        kind=IntentKind.CONTINUATION,
        interpreted_objective="Deliver the accepted root outcome.",
    )
    binding = {
        "root_id": root.root_id,
        "work_packet_specification_id": packet.specification_id,
        "authority_fingerprint": authority_fingerprint(authority),
    }
    decision = evaluate_objective_continuation(root, packet, authority, [_ready("inspect semantic state", binding)])
    assert decision.disposition == ContinuationDisposition.REORIENT


def test_packet_or_pr_completion_cannot_establish_root_terminality(context) -> None:
    root, packet, authority, binding = context
    completed = [
        CompletedEffectEvidence(evidence_id=f"done-{i}", status="accepted", semantic_effect_token=token, **binding)
        for i, token in enumerate(packet.scope.allowed_effects)
    ]
    decision = evaluate_objective_continuation(root, packet, authority, completed)
    assert decision.disposition == ContinuationDisposition.REORIENT
    with pytest.raises(ValidationError):
        OBJECTIVE_EVIDENCE_ADAPTER.validate_python([{"kind": "pr_completed", **binding}])


@pytest.mark.parametrize("disposition", ["terminal", "impossible"])
def test_explicit_bound_root_terminality(context, disposition: Literal["terminal", "impossible"]) -> None:
    root, packet, authority, binding = context
    item = RootTerminalEvidence(
        evidence_id=f"root-{disposition}",
        status="proven",
        disposition=disposition,
        evidence_scope="root_objective",
        basis="Root acceptance oracle is proven.",
        **binding,
    )
    assert evaluate_objective_continuation(root, packet, authority, [item]).disposition.value == disposition


def test_root_terminality_must_be_proven_and_does_not_hide_bad_effect_evidence(context) -> None:
    root, packet, authority, binding = context
    terminal = RootTerminalEvidence(
        evidence_id="root-terminal",
        status="accepted",
        disposition="terminal",
        evidence_scope="root_objective",
        basis="A claim, not proof.",
        **binding,
    )
    assert evaluate_objective_continuation(root, packet, authority, [terminal]).disposition == ContinuationDisposition.REORIENT
    proven = terminal.model_copy(update={"status": "proven"})
    unsealed = CompletedEffectEvidence(
        evidence_id="bad-effect",
        status="accepted",
        semantic_effect_token="merge PR",
        **binding,
    )
    assert (
        evaluate_objective_continuation(root, packet, authority, [proven, unsealed]).disposition
        == ContinuationDisposition.REORIENT
    )


def test_explicit_machine_and_human_waits_require_admitted_conditions(context) -> None:
    root, packet, authority, binding = context
    machine = MachineWaitEvidence(
        evidence_id="machine", status="accepted", condition="verified actuator unavailable", active=True, **binding
    )
    human = HumanWaitEvidence(
        evidence_id="human",
        status="accepted",
        admitted_gate_condition="owner approval explicitly required",
        active=True,
        **binding,
    )
    assert evaluate_objective_continuation(root, packet, authority, [machine]).disposition == ContinuationDisposition.WAIT_MACHINE
    assert evaluate_objective_continuation(root, packet, authority, [human]).disposition == ContinuationDisposition.WAIT_HUMAN
    invented = human.model_copy(update={"admitted_gate_condition": "ask a person what to do"})
    assert evaluate_objective_continuation(root, packet, authority, [invented]).disposition == ContinuationDisposition.REORIENT


def test_malformed_and_stale_bound_evidence_are_rejected(context) -> None:
    root, packet, authority, binding = context
    with pytest.raises(ValidationError):
        CompletedEffectEvidence.model_validate(
            {"evidence_id": "x", "status": "maybe", "semantic_effect_token": "inspect semantic state", **binding}
        )
    stale = CompletedEffectEvidence(
        evidence_id="stale",
        status="accepted",
        semantic_effect_token="inspect semantic state",
        **{**binding, "authority_fingerprint": "0" * 64},
    )
    assert evaluate_objective_continuation(root, packet, authority, [stale]).disposition == ContinuationDisposition.REORIENT
