import pytest
from pydantic import ValidationError

from scripts.programstart_capability_discovery_gate import (
    CapabilityConclusion,
    CapabilityDiscoveryDecision,
    FailureLocalizationClass,
    FailureLocalizationConclusion,
    FailureLocalizationDecision,
    FailureLocalizationEvidence,
    PathsClassifierConstraints,
    PathsClassifierInput,
    PathsClassifierResult,
    PathsDiscoveryDurability,
    PathsDiscoveryEvidence,
    classifier_result_sha256,
    validate_capability_discovery,
    validate_failure_localization,
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


def loc(
    classification: FailureLocalizationClass,
    *,
    preserved=None,
    contradictory=None,
    invalidated=None,
    degradation=None,
    requirement_gaps=None,
    boundary="boundary:dispatcher",
) -> FailureLocalizationEvidence:
    return FailureLocalizationEvidence(
        observed_failure_ref="evidence:higher-order-e2e-failure",
        component_ref="capability:existing-reachability-actuator",
        component_contract_ref="contract:reachability-actuator-v1",
        classification=classification,
        first_failed_boundary_ref=boundary,
        preserved_evidence_refs=preserved or [],
        contradictory_component_evidence_refs=contradictory or [],
        invalidated_component_evidence_refs=invalidated or [],
        independent_degradation_refs=degradation or [],
        requirement_gap_refs=requirement_gaps or [],
        authorization_inferred=False,
    )


def test_composed_failure_preserves_actuator_and_repairs_missing_dispatcher():
    discovery = ev(
        result=classifier_result(
            classification="DIRECT_REALIZATION",
            reason_code="EXACT_PROVEN_CURRENT_REALIZATION",
            ordered_candidate_refs=["ER-ACTUATOR"],
        )
    )
    validate_failure_localization(
        FailureLocalizationDecision(
            conclusion=FailureLocalizationConclusion.PRESERVE_COMPONENT_AND_REPAIR_BOUNDARY,
            discovery=discovery,
            localization=loc(
                FailureLocalizationClass.COMPOSITION_OR_WIRING_GAP,
                preserved=["proof:reachability-actuator-v1"],
                boundary="boundary:dispatcher-wiring",
            ),
        )
    )


def test_composed_failure_cannot_replace_proven_actuator_without_component_counterevidence():
    discovery = ev()
    with pytest.raises(ValueError, match="replacement requires component contract failure"):
        validate_failure_localization(
            FailureLocalizationDecision(
                conclusion=FailureLocalizationConclusion.COMPONENT_REPLACEMENT_REQUIRED,
                discovery=discovery,
                localization=loc(
                    FailureLocalizationClass.COMPOSITION_OR_WIRING_GAP,
                    preserved=["proof:reachability-actuator-v1"],
                    boundary="boundary:dispatcher-wiring",
                ),
            )
        )


def test_component_defect_requires_counterevidence_and_explicit_invalidation():
    discovery = ev()
    weak = loc(
        FailureLocalizationClass.COMPONENT_CONTRACT_FAILURE,
        contradictory=["evidence:actuator-contract-violation"],
        boundary="boundary:actuator-contract",
    )
    with pytest.raises(ValueError, match="contradictory evidence and explicit component-proof invalidation"):
        validate_failure_localization(
            FailureLocalizationDecision(
                conclusion=FailureLocalizationConclusion.COMPONENT_DEFECTIVE,
                discovery=discovery,
                localization=weak,
            )
        )

    strong = loc(
        FailureLocalizationClass.COMPONENT_CONTRACT_FAILURE,
        contradictory=["evidence:actuator-contract-violation"],
        invalidated=["proof:reachability-actuator-v1"],
        boundary="boundary:actuator-contract",
    )
    validate_failure_localization(
        FailureLocalizationDecision(
            conclusion=FailureLocalizationConclusion.COMPONENT_DEFECTIVE,
            discovery=discovery,
            localization=strong,
        )
    )
    validate_failure_localization(
        FailureLocalizationDecision(
            conclusion=FailureLocalizationConclusion.COMPONENT_REPLACEMENT_REQUIRED,
            discovery=discovery,
            localization=strong,
        )
    )


def test_contract_insufficiency_can_require_replacement_without_erasing_historical_proof():
    discovery = ev()
    validate_failure_localization(
        FailureLocalizationDecision(
            conclusion=FailureLocalizationConclusion.COMPONENT_REPLACEMENT_REQUIRED,
            discovery=discovery,
            localization=loc(
                FailureLocalizationClass.COMPONENT_CONTRACT_INSUFFICIENT,
                preserved=["proof:reachability-actuator-v1"],
                requirement_gaps=["requirement:effect-needs-semantic-not-covered-by-v1"],
                boundary="boundary:component-contract-scope",
            ),
        )
    )


def test_independent_degradation_is_not_component_replacement_evidence():
    discovery = ev()
    degradation = loc(
        FailureLocalizationClass.INDEPENDENT_DEGRADATION,
        preserved=["proof:reachability-actuator-v1"],
        degradation=["evidence:external-provider-degraded"],
        boundary="boundary:external-provider",
    )
    validate_failure_localization(
        FailureLocalizationDecision(
            conclusion=FailureLocalizationConclusion.INDEPENDENT_DEGRADATION,
            discovery=discovery,
            localization=degradation,
        )
    )
    with pytest.raises(ValueError, match="replacement requires component contract failure"):
        validate_failure_localization(
            FailureLocalizationDecision(
                conclusion=FailureLocalizationConclusion.COMPONENT_REPLACEMENT_REQUIRED,
                discovery=discovery,
                localization=degradation,
            )
        )


def test_currentness_failure_requires_recheck_not_replacement():
    discovery = ev()
    currentness = loc(
        FailureLocalizationClass.CURRENTNESS_OR_ACTIVATION_FAILURE,
        preserved=["proof:historical-actuator-proof"],
        boundary="boundary:runtime-currentness",
    )
    validate_failure_localization(
        FailureLocalizationDecision(
            conclusion=FailureLocalizationConclusion.CURRENTNESS_RECHECK_REQUIRED,
            discovery=discovery,
            localization=currentness,
        )
    )
    with pytest.raises(ValueError, match="replacement requires component contract failure"):
        validate_failure_localization(
            FailureLocalizationDecision(
                conclusion=FailureLocalizationConclusion.COMPONENT_REPLACEMENT_REQUIRED,
                discovery=discovery,
                localization=currentness,
            )
        )


def test_test_assumption_failure_requires_correction_not_replacement():
    discovery = ev()
    assumption = loc(
        FailureLocalizationClass.TEST_OR_ASSUMPTION_FAILURE,
        preserved=["proof:reachability-actuator-v1"],
        boundary="boundary:test-assumption",
    )
    validate_failure_localization(
        FailureLocalizationDecision(
            conclusion=FailureLocalizationConclusion.TEST_ASSUMPTION_CORRECTION_REQUIRED,
            discovery=discovery,
            localization=assumption,
        )
    )
    with pytest.raises(ValueError, match="replacement requires component contract failure"):
        validate_failure_localization(
            FailureLocalizationDecision(
                conclusion=FailureLocalizationConclusion.COMPONENT_REPLACEMENT_REQUIRED,
                discovery=discovery,
                localization=assumption,
            )
        )


def test_unknown_boundary_can_only_request_further_localization():
    discovery = ev()
    unresolved = loc(FailureLocalizationClass.UNKNOWN, boundary="boundary:unresolved")
    validate_failure_localization(
        FailureLocalizationDecision(
            conclusion=FailureLocalizationConclusion.FURTHER_LOCALIZATION_REQUIRED,
            discovery=discovery,
            localization=unresolved,
        )
    )
    with pytest.raises(ValueError, match="replacement requires component contract failure"):
        validate_failure_localization(
            FailureLocalizationDecision(
                conclusion=FailureLocalizationConclusion.COMPONENT_REPLACEMENT_REQUIRED,
                discovery=discovery,
                localization=unresolved,
            )
        )


def test_failure_localization_requires_current_proven_discovery_context():
    weak_discovery = ev(
        result=classifier_result(
            constraints=PathsClassifierConstraints(
                require_current=False,
                require_proven=True,
                exclude_human_transport=True,
            )
        )
    )
    with pytest.raises(ValueError, match="requires current and proven Paths discovery context"):
        validate_failure_localization(
            FailureLocalizationDecision(
                conclusion=FailureLocalizationConclusion.PRESERVE_COMPONENT_AND_REPAIR_BOUNDARY,
                discovery=weak_discovery,
                localization=loc(
                    FailureLocalizationClass.COMPOSITION_OR_WIRING_GAP,
                    preserved=["proof:reachability-actuator-v1"],
                ),
            )
        )
