"""Conflicting or stale evidence must never manufacture root completion."""

from typing import Literal

import pytest
from pydantic import ValidationError

from scripts import programstart_intent_compile as compiler
from scripts import programstart_objective_continuation as continuation
from tests.test_programstart_objective_continuation import _authority, _durability, _ready
from tests.test_programstart_objective_continuation import context as objective_context

context = objective_context


def completed(binding, token="inspect semantic state", identity="completed"):
    return continuation.CompletedEffectEvidence(evidence_id=identity, status="accepted", semantic_effect_token=token, **binding)


def terminal(
    binding,
    disposition: Literal["terminal", "impossible"] = "terminal",
    status: Literal["accepted", "proven"] = "proven",
    identity="terminal",
):
    return continuation.RootTerminalEvidence(
        evidence_id=identity,
        status=status,
        disposition=disposition,
        evidence_scope="root_objective",
        basis="owner outcome proof",
        durability=_durability() if status == "proven" else None,
        **binding,
    )


def human(binding, identity="human"):
    return continuation.HumanWaitEvidence(
        evidence_id=identity,
        status="accepted",
        active=True,
        admitted_gate_condition="owner approval explicitly required",
        **binding,
    )


@pytest.mark.parametrize(
    "case",
    [
        "duplicate-id",
        "duplicate-effect",
        "unknown-completion",
        "foreign-binding",
        "two-ready",
        "ready-completed",
        "terminal-ready",
        "terminal-accepted",
        "terminal-conflict",
        "wait-ready",
        "multiple-waits",
    ],
)
def test_conflicting_evidence_reorients_instead_of_selecting_effect(context, case):
    root, packet, authority, binding = context
    evidence: list[
        continuation.CompletedEffectEvidence
        | continuation.EffectReadyEvidence
        | continuation.RootTerminalEvidence
        | continuation.HumanWaitEvidence
    ] = [completed(binding)]
    if case == "duplicate-id":
        evidence *= 2
    elif case == "duplicate-effect":
        evidence.append(completed(binding, identity="second"))
    elif case == "unknown-completion":
        evidence = [completed(binding, token="unauthorized action")]
    elif case == "foreign-binding":
        evidence = [completed(dict(binding, root_id="foreign"))]
    elif case == "two-ready":
        evidence = [_ready("apply bounded change", binding), _ready("verify acceptance", binding, evidence_id="other")]
    elif case == "ready-completed":
        evidence.append(_ready("inspect semantic state", binding))
    elif case == "terminal-ready":
        evidence = [terminal(binding), _ready("apply bounded change", binding)]
    elif case == "terminal-accepted":
        evidence = [terminal(binding, status="accepted")]
    elif case == "terminal-conflict":
        evidence = [terminal(binding), terminal(binding, disposition="impossible", identity="conflicting")]
    elif case == "wait-ready":
        evidence = [human(binding), _ready("apply bounded change", binding)]
    else:
        evidence = [human(binding), human(binding, identity="second")]
    assert continuation.evaluate_objective_continuation(root, packet, authority, evidence).disposition == "reorient"


def test_accepted_evidence_cannot_carry_proven_durability(context):
    _, _, _, binding = context
    with pytest.raises(ValidationError, match="only for proven"):
        continuation.CompletedEffectEvidence(
            evidence_id="accepted", status="accepted", semantic_effect_token="inspect", durability=_durability(), **binding
        )


def test_readiness_requires_integrity_and_current_authority(context):
    root, packet, authority, binding = context
    evidence = [completed(binding)]
    damaged = packet.model_copy(update={"semantic_digest": "0" * 64})
    assert continuation.derive_effect_readiness(root, damaged, authority, evidence) is None
    drifted = authority.model_copy(update={"authority_commit": "f" * 40})
    assert continuation.derive_effect_readiness(root, packet, drifted, evidence) is None


def reseal(packet):
    # Integrity is a consistency digest, not authentication: an imported packet
    # can be internally sealed yet disagree with current owner evidence.
    body = packet.model_dump(mode="json", exclude={"specification_id", "semantic_digest"})
    digest = compiler._digest(compiler._semantic_evidence(body))
    return packet.model_copy(update={"semantic_digest": digest, "specification_id": "WPK-" + digest[:16]})


def test_consistent_digest_cannot_replace_authority_binding(context):
    root, packet, authority, binding = context
    packet = packet.model_copy(update={"evidence": packet.evidence.model_copy(update={"authority_fingerprint": "0" * 64})})
    packet = reseal(packet)
    assert compiler.verify_integrity(packet)
    assert continuation.derive_effect_readiness(root, packet, authority, [completed(binding)]) is None
    assert continuation.evaluate_objective_continuation(root, packet, authority, []).disposition == "reorient"


def test_duplicate_scope_effects_do_not_become_execution_ready(context):
    root, packet, authority, _ = context
    scope = packet.scope.model_copy(update={"allowed_effects": packet.scope.allowed_effects * 2})
    packet = reseal(packet.model_copy(update={"scope": scope}))
    assert compiler.verify_integrity(packet)
    assert continuation.evaluate_objective_continuation(root, packet, authority, []).disposition == "reorient"


def test_readiness_requires_nonduplicate_completion_evidence(context):
    root, packet, authority, binding = context
    assert continuation.derive_effect_readiness(root, packet, authority, []) is None
    item = completed(binding)
    assert continuation.derive_effect_readiness(root, packet, authority, [item, item]) is None


def test_machine_wait_must_be_an_admitted_automation_gap(context):
    root, packet, authority, binding = context
    registration = continuation.MachineWaitRegistration(
        run_id="test-run",
        work_packet_id=packet.specification_id,
        owner_repository=authority.owning_repository,
        authority_version=authority.authority_commit,
        semantic_digest=packet.semantic_digest,
        awaited_proposition="CI succeeded",
        trigger_source="github",
        trigger_type="workflow_run",
        correlation_key="CI:1",
        expected_conclusion="success",
        resume_at="owner:continuation",
        machine_safe_on_match=True,
    )
    wait = continuation.MachineWaitEvidence(
        evidence_id="wait", status="accepted", condition="unadmitted condition", active=True, wait=registration, **binding
    )
    assert continuation.evaluate_objective_continuation(root, packet, authority, [wait]).disposition == "reorient"


def test_readiness_ignores_uncompleted_rules_and_denies_unsafe_next_effect(context):
    root, _, _, _ = context
    for next_effect in ["verify acceptance", "outside authority"]:
        authority = _authority(
            effect_readiness_rules=[
                compiler.EffectReadinessRule(completed_effect="apply bounded change", ready_effect="verify acceptance"),
                compiler.EffectReadinessRule(completed_effect="inspect semantic state", ready_effect=next_effect),
            ]
        )
        packet = compiler.compile_work_packet("Continue root", authority, kind=compiler.IntentKind.CONTINUATION)
        binding = dict(
            root_id=root.root_id,
            work_packet_specification_id=packet.specification_id,
            authority_fingerprint=compiler.authority_fingerprint(authority),
        )
        result = continuation.derive_effect_readiness(root, packet, authority, [completed(binding)])
        if next_effect == "outside authority":
            assert result is None
        else:
            assert result is not None and result.semantic_effect_token == "verify acceptance"
