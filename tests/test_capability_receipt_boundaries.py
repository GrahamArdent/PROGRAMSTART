"""Validate receipt provenance and localization before consequential conclusions."""

import pytest
from pydantic import ValidationError

from scripts import programstart_capability_discovery_gate as gate
from tests.test_programstart_capability_discovery_gate import classifier_result, ev, localized_failure, preflight, receipts


@pytest.mark.parametrize(
    "model,field,value,reason",
    [
        (gate.PathsClassifierResult, "owner_refs", ["x", "x"], "duplicates"),
        (gate.PathsClassifierResult, "evidence_refs", [" x"], "normalized"),
        (gate.PathsDiscoveryDurability, "verification_ref", " x", "normalized"),
        (gate.PathsDiscoveryDurability, "invalidation_conditions", [" "], "normalized"),
        (gate.PathsDiscoveryEvidence, "actor_ref", " x", "normalized"),
        (gate.PathsDiscoveryEvidence, "owner_native_verification_refs", ["x", "x"], "unique"),
        (gate.PathsDiscoveryEvidence, "owner_native_verification_refs", [" "], "normalized"),
        (gate.FailureBoundaryEvidence, "boundary_ref", " x", "normalized"),
        (gate.FailureBoundaryEvidence, "evidence_refs", ["x", "x"], "unique"),
        (gate.FailureLocalizationFacts, "capability_ref", " x", "normalized"),
        (gate.FailureLocalizationFacts, "prior_proof_refs", ["x", "x"], "unique"),
        (gate.FailureLocalizationDurability, "mechanism", " x", "normalized"),
        (gate.DiscoverySearchReceipt, "query", " x", "normalized"),
        (gate.DiscoverySearchReceipt, "matched_capability_refs", ["x", "x"], "unique"),
    ],
)
def test_malformed_receipt_cannot_pass_model_validation(model, field, value, reason):
    evidence = localized_failure()
    examples = {
        gate.PathsClassifierResult: classifier_result(),
        gate.PathsDiscoveryDurability: ev().durability,
        gate.PathsDiscoveryEvidence: ev(),
        gate.FailureBoundaryEvidence: evidence.facts.first_failed_boundary,
        gate.FailureLocalizationFacts: evidence.facts,
        gate.FailureLocalizationDurability: evidence.durability,
        gate.DiscoverySearchReceipt: receipts()[0],
    }
    payload = examples[model].model_dump(mode="json")
    payload[field] = value
    with pytest.raises(ValidationError, match=reason):
        model.model_validate(payload)


@pytest.mark.parametrize("action", list(gate.FailureAction))
def test_localization_action_requires_matching_failure_contract(action):
    # One authentic, self-consistent receipt of an unknown component contract;
    # only re-verification may proceed from this state.
    evidence = localized_failure(contract_disposition=gate.ContractDisposition.STALE_OR_UNKNOWN)
    decision = gate.FailureLocalizationDecision(action=action, evidence=evidence)
    if action == gate.FailureAction.REVERIFY_CAPABILITY:
        gate.validate_failure_localization(decision)
    else:
        with pytest.raises(ValueError, match="requires|replacement"):
            gate.validate_failure_localization(decision)


def test_missing_localization_and_constrained_discovery_fail_closed():
    with pytest.raises(ValueError, match="durable failure-localization"):
        gate.validate_failure_localization(gate.FailureLocalizationDecision(action=gate.FailureAction.REPAIR_COMPOSITION))
    result = classifier_result(constraints=gate.PathsClassifierConstraints())
    with pytest.raises(ValidationError, match="machine-only"):
        localized_failure(discovery=ev(result=result))


@pytest.mark.parametrize(
    "classification,candidates,reason",
    [
        ("MISSING_TYPED_EDGE", [], "usable Paths"),
        ("DIRECT_REALIZATION", [], "at least one"),
    ],
)
def test_selection_requires_usable_realization(classification, candidates, reason):
    evidence = ev(
        result=classifier_result(classification=classification, ordered_candidate_refs=candidates), owner_refs=["owner#1"]
    )
    with pytest.raises(ValueError, match=reason):
        gate.validate_capability_discovery(
            gate.CapabilityDiscoveryDecision(conclusion=gate.CapabilityConclusion.PATH_SELECTED, discovery=evidence)
        )


@pytest.mark.parametrize(
    "change,reason",
    [
        ("no-owners", "unique relevant"),
        ("duplicate-owners", "unique relevant"),
        ("material-nonmaterial", "material delta"),
        ("nonmaterial-new", "nonmaterial changes"),
    ],
)
def test_reuse_scope_cannot_claim_absence_without_coverage(change, reason):
    payload = preflight().model_dump(mode="json")
    if change == "no-owners":
        payload["required_owner_repositories"] = []
    elif change == "duplicate-owners":
        payload["required_owner_repositories"] *= 2
    elif change == "material-nonmaterial":
        payload["decision"] = "NONMATERIAL"
    else:
        payload["material_reusable_delta"] = False
    with pytest.raises(ValueError, match=reason):
        gate.validate_reuse_preflight(gate.ReusePreflight.model_validate(payload))


def test_new_capability_requires_material_new_reuse_decision():
    evidence = ev(result=classifier_result(classification="GENUINELY_NEW_PATH_REQUIRED"))
    decision = gate.CapabilityDiscoveryDecision(
        conclusion=gate.CapabilityConclusion.NEW_CAPABILITY_REQUIRED,
        discovery=evidence,
        reuse_preflight=preflight(decision="REUSE"),
    )
    with pytest.raises(ValueError, match="material NEW"):
        gate.validate_capability_discovery(decision)


def test_localization_revalidates_action_semantics_after_public_model_mutation():
    decision = gate.FailureLocalizationDecision(action=gate.FailureAction.REVERIFY_CAPABILITY, evidence=localized_failure())
    with pytest.raises(ValueError, match="stale_or_unknown"):
        gate.validate_failure_localization(decision)
    evidence = localized_failure(
        boundary_kind=gate.FailureBoundaryKind.COMPONENT, contract_disposition=gate.ContractDisposition.SATISFIED
    )
    decision = gate.FailureLocalizationDecision(action=gate.FailureAction.REPLACE_EXISTING_CAPABILITY, evidence=evidence)
    with pytest.raises(ValueError, match="contradicted, insufficient, or superseded"):
        gate.validate_failure_localization(decision)
    # These models permit assignment. The action consumer must still fail closed
    # if a caller changes an already constructed decision before invoking it.
    setattr(decision, "action", "foreign_action")
    with pytest.raises(ValueError, match="unsupported"):
        gate.validate_failure_localization(decision)


def test_genuinely_new_capability_requires_material_new_reuse_decision():
    evidence = ev(result=classifier_result(classification="GENUINELY_NEW_PATH_REQUIRED"))
    reused = preflight(decision="COMPOSE")
    with pytest.raises(ValueError, match="material NEW"):
        gate.validate_capability_discovery(
            gate.CapabilityDiscoveryDecision(
                conclusion=gate.CapabilityConclusion.NEW_CAPABILITY_REQUIRED, discovery=evidence, reuse_preflight=reused
            )
        )
    gate.validate_capability_discovery(
        gate.CapabilityDiscoveryDecision(
            conclusion=gate.CapabilityConclusion.NEW_CAPABILITY_REQUIRED, discovery=evidence, reuse_preflight=preflight()
        )
    )
