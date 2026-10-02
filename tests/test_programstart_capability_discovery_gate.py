import pytest
from scripts.programstart_capability_discovery_gate import CapabilityConclusion,CapabilityDiscoveryDecision,PathsDiscoveryEvidence,validate_capability_discovery

def ev(**u):
    d=dict(actor_ref="actor:chatgpt-connected-github",effect_ref="effect:reviewed-en-privileged-maintenance",target_ref="execution-node",query_ref="paths:effect-reachability@observed-sha",realization_ids=[],widened_search_performed=False,owner_native_verification_refs=[])
    d.update(u); return PathsDiscoveryEvidence(**d)

@pytest.mark.parametrize("c",[CapabilityConclusion.HUMAN_REQUIRED,CapabilityConclusion.UNAVAILABLE,CapabilityConclusion.AUTOMATION_GAP,CapabilityConclusion.NEW_CAPABILITY_REQUIRED])
def test_absence_requires_discovery(c):
    with pytest.raises(ValueError,match="requires deterministic Paths discovery"):
        validate_capability_discovery(CapabilityDiscoveryDecision(conclusion=c))

def test_obvious_surface_failure_requires_widening():
    with pytest.raises(ValueError,match="requires widened"):
        validate_capability_discovery(CapabilityDiscoveryDecision(conclusion=CapabilityConclusion.AUTOMATION_GAP,discovery=ev()))

def test_alternate_route_blocks_false_escalation():
    with pytest.raises(ValueError,match="conflicts with discovered realization"):
        validate_capability_discovery(CapabilityDiscoveryDecision(conclusion=CapabilityConclusion.HUMAN_REQUIRED,discovery=ev(realization_ids=["ER-003"],widened_search_performed=True,owner_native_verification_refs=["owner@current"])))

def test_selected_route_requires_owner_verification():
    with pytest.raises(ValueError,match="owner-native JIT verification"):
        validate_capability_discovery(CapabilityDiscoveryDecision(conclusion=CapabilityConclusion.PATH_SELECTED,discovery=ev(realization_ids=["ER-003"])))

def test_selected_route_passes_with_owner_verification():
    validate_capability_discovery(CapabilityDiscoveryDecision(conclusion=CapabilityConclusion.PATH_SELECTED,discovery=ev(realization_ids=["ER-003"],owner_native_verification_refs=["owner@current"])))

def test_true_gap_requires_zero_result_widened_search():
    validate_capability_discovery(CapabilityDiscoveryDecision(conclusion=CapabilityConclusion.AUTOMATION_GAP,discovery=ev(widened_search_performed=True)))
