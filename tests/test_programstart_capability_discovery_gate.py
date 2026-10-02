import pytest
from pydantic import ValidationError

from scripts.programstart_capability_discovery_gate import (
    CapabilityConclusion,
    CapabilityDiscoveryDecision,
    PathsClassifierConstraints,
    PathsClassifierInput,
    PathsClassifierResult,
    PathsDiscoveryDurability,
    PathsDiscoveryEvidence,
    classifier_result_sha256,
    validate_capability_discovery,
)


def classifier_result(
    *,
    classification="MISSING_TYPED_EDGE",
    reason_code="EFFECT_TARGET_REGISTERED_ACTOR_EDGE_MISSING",
    ordered_candidate_refs=None,
    constraints=None,
):
    return PathsClassifierResult(
        input=PathsClassifierInput(
            actor_ref="actor:chatgpt-connected-github",
            effect_ref="effect:reviewed-en-privileged-maintenance",
            target_ref="execution-node",
            constraints=constraints
            or PathsClassifierConstraints(
                require_current=True,
                require_proven=True,
                exclude_human_transport=True,
            ),
        ),
        ordered_candidate_refs=ordered_candidate_refs or [],
        constituent_refs=[],
        missing_typed_edges=["actor-specific admitted invocation edge"] if classification == "MISSING_TYPED_EDGE" else [],
        owner_refs=[],
        evidence_refs=[],
        currentness_facts=[],
        actor_admission_state="missing",
        activation_state="unknown",
        proof_state="unknown",
        privilege_boundary=None,
        failure_domains=[],
        authorization_inferred=False,
        classification=classification,
        reason_code=reason_code,
    )


def ev(
    *,
    result: PathsClassifierResult | None = None,
    owner_refs: list[str] | None = None,
    actor_ref: str = "actor:chatgpt-connected-github",
    effect_ref: str = "effect:reviewed-en-privileged-maintenance",
    target_ref: str = "execution-node",
) -> PathsDiscoveryEvidence:
    result = result or classifier_result()
    durability = PathsDiscoveryDurability(
        status="proven",
        source_repo="GrahamArdent/paths",
        source_commit_sha="0" * 40,
        mechanism_ref="scripts/find_capability_composition.py",
        verification_ref="GrahamArdent/paths@0/scripts/validate_registry.py#OBS-005",
        result_sha256=classifier_result_sha256(result),
        invalidation_conditions=(
            "Paths classifier implementation changes",
            "Paths canonical composition inputs change",
        ),
    )
    return PathsDiscoveryEvidence(
        actor_ref=actor_ref,
        effect_ref=effect_ref,
        target_ref=target_ref,
        classifier_result=result,
        durability=durability,
        owner_native_verification_refs=owner_refs or [],
    )


@pytest.mark.parametrize(
    "conclusion",
    [
        CapabilityConclusion.HUMAN_REQUIRED,
        CapabilityConclusion.UNAVAILABLE,
        CapabilityConclusion.AUTOMATION_GAP,
        CapabilityConclusion.NEW_CAPABILITY_REQUIRED,
    ],
)
def test_absence_requires_discovery(conclusion):
    with pytest.raises(ValueError, match="requires deterministic Paths discovery"):
        validate_capability_discovery(CapabilityDiscoveryDecision(conclusion=conclusion))


def test_receipt_hash_is_fail_closed():
    result = classifier_result()
    evidence = ev(result=result)
    payload = evidence.model_dump(mode="json")
    payload["classifier_result"]["reason_code"] = "TAMPERED"
    with pytest.raises(ValidationError, match="receipt hash"):
        PathsDiscoveryEvidence.model_validate(payload)


def test_receipt_input_must_match_requested_effect():
    result = classifier_result()
    with pytest.raises(ValidationError, match="does not match discovery request"):
        ev(result=result, effect_ref="effect:different")


def test_escalation_requires_current_proven_machine_only_search():
    result = classifier_result(
        constraints=PathsClassifierConstraints(
            require_current=True,
            require_proven=True,
            exclude_human_transport=False,
        )
    )
    with pytest.raises(ValueError, match="current, proven, machine-only"):
        validate_capability_discovery(
            CapabilityDiscoveryDecision(
                conclusion=CapabilityConclusion.AUTOMATION_GAP,
                discovery=ev(result=result),
            )
        )


def test_alternate_machine_route_blocks_false_escalation():
    result = classifier_result(
        classification="DIRECT_REALIZATION",
        reason_code="EXACT_PROVEN_CURRENT_REALIZATION",
        ordered_candidate_refs=["ER-003"],
    )
    with pytest.raises(ValueError, match="conflicts with discovered usable machine realization"):
        validate_capability_discovery(
            CapabilityDiscoveryDecision(
                conclusion=CapabilityConclusion.HUMAN_REQUIRED,
                discovery=ev(result=result, owner_refs=["owner@current"]),
            )
        )


def test_selected_route_requires_owner_verification():
    result = classifier_result(
        classification="DIRECT_REALIZATION",
        reason_code="EXACT_PROVEN_CURRENT_REALIZATION",
        ordered_candidate_refs=["ER-003"],
    )
    with pytest.raises(ValueError, match="owner-native JIT verification"):
        validate_capability_discovery(
            CapabilityDiscoveryDecision(
                conclusion=CapabilityConclusion.PATH_SELECTED,
                discovery=ev(result=result),
            )
        )


def test_selected_route_passes_with_owner_verification():
    result = classifier_result(
        classification="DIRECT_REALIZATION",
        reason_code="EXACT_PROVEN_CURRENT_REALIZATION",
        ordered_candidate_refs=["ER-003"],
    )
    validate_capability_discovery(
        CapabilityDiscoveryDecision(
            conclusion=CapabilityConclusion.PATH_SELECTED,
            discovery=ev(result=result, owner_refs=["owner@current"]),
        )
    )


def test_new_capability_requires_genuinely_new_path_classification():
    with pytest.raises(ValueError, match="GENUINELY_NEW_PATH_REQUIRED"):
        validate_capability_discovery(
            CapabilityDiscoveryDecision(
                conclusion=CapabilityConclusion.NEW_CAPABILITY_REQUIRED,
                discovery=ev(result=classifier_result()),
            )
        )


def test_new_capability_passes_only_after_genuinely_new_path_receipt():
    result = classifier_result(
        classification="GENUINELY_NEW_PATH_REQUIRED",
        reason_code="NO_REGISTERED_EFFECT_TARGET_EDGE",
    )
    validate_capability_discovery(
        CapabilityDiscoveryDecision(
            conclusion=CapabilityConclusion.NEW_CAPABILITY_REQUIRED,
            discovery=ev(result=result),
        )
    )


def test_true_typed_edge_gap_can_be_automation_gap():
    validate_capability_discovery(
        CapabilityDiscoveryDecision(
            conclusion=CapabilityConclusion.AUTOMATION_GAP,
            discovery=ev(result=classifier_result()),
        )
    )


def test_human_required_needs_owner_native_gate_verification():
    result = classifier_result(
        classification="NO_SUPPORTED_COMPOSITION",
        reason_code="HUMAN_TRANSPORT_EXCLUDED",
        ordered_candidate_refs=["ER-HUMAN"],
    )
    with pytest.raises(ValueError, match="irreducible human gate"):
        validate_capability_discovery(
            CapabilityDiscoveryDecision(
                conclusion=CapabilityConclusion.HUMAN_REQUIRED,
                discovery=ev(result=result),
            )
        )
    validate_capability_discovery(
        CapabilityDiscoveryDecision(
            conclusion=CapabilityConclusion.HUMAN_REQUIRED,
            discovery=ev(result=result, owner_refs=["owner@current-human-gate"]),
        )
    )
