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
