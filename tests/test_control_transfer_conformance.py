import json
from pathlib import Path

FIXTURE = Path(__file__).parents[1] / "docs" / "acceptance" / "fixtures" / "control_transfer_conformance_v1.json"
REQUIRED_IDS = set("ABCDEFGHIJKLMNOPQR")
ALLOWED = {
    "EXISTS_AND_ADEQUATE",
    "EXISTS_TEST_GAP",
    "EXISTS_CONFORMANCE_GAP",
    "EXISTS_INTEGRATION_GAP",
    "GENUINE_MISSING_CAPABILITY",
    "DISPROVEN_OR_UNNECESSARY",
}

def test_control_transfer_fixture_is_complete_and_non_authoritative():
    data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    assert data["schema_version"] == "1.0"
    assert "never execution authority" in data["purpose"]
    cases = data["cases"]
    assert {case["id"] for case in cases} == REQUIRED_IDS
    assert all(case["coverage"] in ALLOWED for case in cases)

def test_control_transfer_fixture_preserves_branch_scope_and_false_terminality_guards():
    data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    for case in data["cases"]:
        assert case["expected_scope"] == "smallest_affected_branch_or_consequence"
        assert "independent authorized machine-actionable work remains" in case["parent_rule"]
        assert "report_as_stop" in case["forbidden"]
        assert "local_success_as_parent_completion" in case["forbidden"]
        assert "stale_approval_consequence" in case["forbidden"]
        assert "duplicate_semantic_effect" in case["forbidden"]


def test_earned_cross_owner_cases_have_explicit_dispositions():
    data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    by_id = {case["id"]: case for case in data["cases"]}
    expected = {
        "I": ("park_child_gate_continue_independent_siblings", "ACTIVE"),
        "J": ("fence_colliding_child_continue_disjoint_siblings", "ACTIVE"),
        "K": ("wait_dependent_descendant_continue_independent_work", "ACTIVE"),
        "L": ("preserve_parent_until_all_objective_obligations_terminal", "ACTIVE"),
        "M": ("report_and_continue", "UNCHANGED"),
        "P": ("validate_subjective_branch_continue_independent_siblings", "ACTIVE"),
        "Q": ("protect_risky_consequence_continue_safe_remediation_and_unrelated_work", "ACTIVE"),
        "R": ("invalidate_stale_approval_revalidate_before_consequence", "ACTIVE_OR_WAITING"),
    }
    for case_id, (disposition, parent) in expected.items():
        assert by_id[case_id]["expected_disposition"] == disposition
        assert by_id[case_id]["expected_parent_disposition"] == parent

def test_blocked_exhaustion_is_not_a_casual_terminal_state():
    data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    by_id = {case["id"]: case for case in data["cases"]}
    assert by_id["O"]["expected_disposition"] == "exhaustion_classification_only_after_bounded_search"
    assert by_id["O"]["expected_parent_disposition"] == "ACTIVE_OR_WAITING"
    assert by_id["N"]["expected_disposition"] == "use_authorized_alternative_or_owner_route_then_resume"
