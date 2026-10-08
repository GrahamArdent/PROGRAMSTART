import pytest
from pydantic import ValidationError

from scripts.programstart_capability_discovery_gate import (
    CapabilityConclusion,
    CapabilityDiscoveryDecision,
    ContractDisposition,
    DiscoverySearchReceipt,
    FailureAction,
    FailureBoundaryEvidence,
    FailureBoundaryKind,
    FailureLocalizationDecision,
    FailureLocalizationDurability,
    FailureLocalizationEvidence,
    FailureLocalizationFacts,
    PathsClassifierConstraints,
    PathsClassifierInput,
    PathsClassifierResult,
    PathsDiscoveryDurability,
    PathsDiscoveryEvidence,
    ReusePreflight,
    classifier_result_sha256,
    failure_localization_facts_sha256,
    validate_capability_discovery,
    validate_failure_localization,
    validate_reuse_preflight,
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
    with pytest.raises(ValueError, match="DISCOVERY_INCOMPLETE"):
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


def localized_failure(
    *,
    contract_disposition: ContractDisposition = ContractDisposition.SATISFIED,
    boundary_kind: FailureBoundaryKind = FailureBoundaryKind.DISPATCHER,
    independent_degradation_refs: tuple[str, ...] = (),
    replacement_necessity_refs: tuple[str, ...] = (),
    discovery: PathsDiscoveryEvidence | None = None,
) -> FailureLocalizationEvidence:
    facts = FailureLocalizationFacts(
        capability_ref="capability:existing-reachability-actuator",
        contract_ref="contract:reachability-actuator-v1",
        prior_proof_refs=("proof:actuator-unit-and-contract",),
        contract_evidence_refs=("proof:current-actuator-contract-check",),
        contract_disposition=contract_disposition,
        first_failed_boundary=FailureBoundaryEvidence(
            boundary_ref=f"boundary:{boundary_kind.value}",
            kind=boundary_kind,
            evidence_refs=(f"proof:first-failure:{boundary_kind.value}",),
        ),
        independent_degradation_refs=independent_degradation_refs,
        replacement_necessity_refs=replacement_necessity_refs,
    )
    durability = FailureLocalizationDurability(
        status="proven",
        mechanism="deterministic failure-boundary regression",
        verification_ref="test:failure-localization",
        facts_sha256=failure_localization_facts_sha256(facts),
        invalidation_conditions=(
            "component contract changes",
            "failure-boundary evidence changes",
        ),
    )
    return FailureLocalizationEvidence(
        discovery=discovery or ev(),
        facts=facts,
        durability=durability,
    )


def test_dispatcher_gap_blocks_component_replacement_and_admits_composition_repair():
    evidence = localized_failure()
    with pytest.raises(ValueError, match="first proven failing boundary"):
        validate_failure_localization(
            FailureLocalizationDecision(
                action=FailureAction.REPLACE_EXISTING_CAPABILITY,
                evidence=evidence,
            )
        )
    validate_failure_localization(
        FailureLocalizationDecision(
            action=FailureAction.REPAIR_COMPOSITION,
            evidence=evidence,
        )
    )


def test_component_contract_contradiction_admits_repair_without_erasing_prior_proof():
    evidence = localized_failure(
        contract_disposition=ContractDisposition.CONTRADICTED,
        boundary_kind=FailureBoundaryKind.COMPONENT,
    )
    assert evidence.facts.prior_proof_refs == ("proof:actuator-unit-and-contract",)
    validate_failure_localization(
        FailureLocalizationDecision(
            action=FailureAction.REPAIR_EXISTING_CAPABILITY,
            evidence=evidence,
        )
    )


def test_insufficient_component_contract_admits_extension():
    evidence = localized_failure(
        contract_disposition=ContractDisposition.INSUFFICIENT,
        boundary_kind=FailureBoundaryKind.COMPONENT,
    )
    validate_failure_localization(
        FailureLocalizationDecision(
            action=FailureAction.EXTEND_EXISTING_CAPABILITY,
            evidence=evidence,
        )
    )


def test_replacement_requires_evidence_that_bounded_repair_or_extension_is_insufficient():
    evidence = localized_failure(
        contract_disposition=ContractDisposition.CONTRADICTED,
        boundary_kind=FailureBoundaryKind.COMPONENT,
    )
    with pytest.raises(ValueError, match="repair or extension is not"):
        validate_failure_localization(
            FailureLocalizationDecision(
                action=FailureAction.REPLACE_EXISTING_CAPABILITY,
                evidence=evidence,
            )
        )

    replacement = localized_failure(
        contract_disposition=ContractDisposition.CONTRADICTED,
        boundary_kind=FailureBoundaryKind.COMPONENT,
        replacement_necessity_refs=("proof:bounded-repair-rejected",),
    )
    validate_failure_localization(
        FailureLocalizationDecision(
            action=FailureAction.REPLACE_EXISTING_CAPABILITY,
            evidence=replacement,
        )
    )


def test_independent_external_degradation_is_isolated_without_blaming_component():
    evidence = localized_failure(
        boundary_kind=FailureBoundaryKind.EXTERNAL_DEPENDENCY,
        independent_degradation_refs=("proof:provider-degradation",),
    )
    validate_failure_localization(
        FailureLocalizationDecision(
            action=FailureAction.ISOLATE_EXTERNAL_DEGRADATION,
            evidence=evidence,
        )
    )
    with pytest.raises(ValueError, match="first proven failing boundary"):
        validate_failure_localization(
            FailureLocalizationDecision(
                action=FailureAction.REPLACE_EXISTING_CAPABILITY,
                evidence=evidence,
            )
        )


def test_stale_component_evidence_requires_reverification_before_mutation():
    evidence = localized_failure(
        contract_disposition=ContractDisposition.STALE_OR_UNKNOWN,
        boundary_kind=FailureBoundaryKind.CURRENTNESS,
    )
    validate_failure_localization(
        FailureLocalizationDecision(
            action=FailureAction.REVERIFY_CAPABILITY,
            evidence=evidence,
        )
    )
    with pytest.raises(ValueError, match="first proven failing boundary"):
        validate_failure_localization(
            FailureLocalizationDecision(
                action=FailureAction.REPLACE_EXISTING_CAPABILITY,
                evidence=evidence,
            )
        )


def test_bad_test_assumption_is_corrected_without_component_replacement():
    evidence = localized_failure(boundary_kind=FailureBoundaryKind.TEST_ASSUMPTION)
    validate_failure_localization(
        FailureLocalizationDecision(
            action=FailureAction.CORRECT_TEST_ASSUMPTION,
            evidence=evidence,
        )
    )
    with pytest.raises(ValueError, match="first proven failing boundary"):
        validate_failure_localization(
            FailureLocalizationDecision(
                action=FailureAction.REPLACE_EXISTING_CAPABILITY,
                evidence=evidence,
            )
        )


def test_failure_localization_receipt_hash_is_fail_closed():
    evidence = localized_failure()
    payload = evidence.model_dump(mode="json")
    payload["facts"]["contract_ref"] = "contract:tampered"
    with pytest.raises(ValidationError, match="facts hash"):
        FailureLocalizationEvidence.model_validate(payload)


def test_existing_capability_failure_assessment_rejects_genuinely_new_path_discovery():
    result = classifier_result(
        classification="GENUINELY_NEW_PATH_REQUIRED",
        reason_code="NO_REGISTERED_EFFECT_TARGET_EDGE",
    )
    discovery = ev(result=result)
    with pytest.raises(ValidationError, match="conflicts with GENUINELY_NEW_PATH_REQUIRED"):
        localized_failure(discovery=discovery)


OWNER = "GrahamArdent/execution-node-control"


def receipts(found=False):
    pairs = [("GrahamArdent/paths", k) for k in ("registry", "blueprint", "composition")]
    pairs += [(OWNER, k) for k in ("issues", "merged_prs", "code")]
    return tuple(
        DiscoverySearchReceipt.model_validate(
            {
                "repository": repo,
                "source_kind": kind,
                "source_commit_sha": "a" * 40,
                "query": "codex_usage_diagnostic rate_limits usageLimitExceeded",
                "observed_at": "2026-10-08T20:00:00Z",
                "coverage": "complete",
                "result_ref": f"evidence/{kind}.json",
                "result_sha256": "b" * 64,
                "matched_capability_refs": ("GrahamArdent/execution-node-control#362",) if found and kind == "merged_prs" else (),
            }
        )
        for repo, kind in pairs
    )


def preflight(searches=None, decision="NEW"):
    return ReusePreflight.model_validate(
        {
            "material_reusable_delta": True,
            "required_owner_repositories": (OWNER,),
            "searches": receipts() if searches is None else searches,
            "decision": decision,
            "rationale": "compare existing source capabilities",
        }
    )


def test_registry_miss_does_not_hide_merged_en362():
    with pytest.raises(ValueError, match="EXISTING_CAPABILITY_FOUND"):
        validate_reuse_preflight(preflight(receipts(found=True)))
    validate_reuse_preflight(preflight(receipts(found=True), "COMPOSE"))


@pytest.mark.parametrize("kind", ["registry", "blueprint", "composition", "issues", "merged_prs", "code"])
def test_each_required_source_must_be_covered(kind):
    with pytest.raises(ValueError, match="DISCOVERY_INCOMPLETE"):
        validate_reuse_preflight(preflight(tuple(s for s in receipts() if s.source_kind != kind)))


@pytest.mark.parametrize("coverage", ["failed", "truncated"])
def test_failed_or_partial_search_cannot_establish_absence(coverage):
    rows = list(receipts())
    rows[-1] = rows[-1].model_copy(update={"coverage": coverage})
    with pytest.raises(ValueError, match="DISCOVERY_INCOMPLETE"):
        validate_reuse_preflight(preflight(tuple(rows)))


def test_owner_currentness_mismatch_fails_closed():
    rows = list(receipts())
    rows[-1] = rows[-1].model_copy(update={"source_commit_sha": "c" * 40})
    with pytest.raises(ValueError, match="currentness differs"):
        validate_reuse_preflight(preflight(tuple(rows)))


def test_genuinely_novel_effect_can_pass():
    validate_reuse_preflight(preflight())


def test_nonmaterial_change_needs_no_corpus_search():
    validate_reuse_preflight(
        ReusePreflight(material_reusable_delta=False, decision="NONMATERIAL", rationale="routine status only")
    )
