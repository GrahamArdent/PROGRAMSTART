from __future__ import annotations

import copy

from scripts import programstart_autonomy_parity as parity


def _errors(contract):
    return parity.validate_contract(copy.deepcopy(contract))


def test_current_contract_is_complete_and_rendered_view_is_derived() -> None:
    contract = parity.load_contract()
    assert _errors(contract) == []
    checked = copy.deepcopy(contract)
    assert parity.validate_contract(checked) == []
    assert checked["_summary"]["source_obligations"] == 422
    assert checked["_summary"]["behaviors"] == 49
    assert checked["_summary"]["conversation_decisions"] == 27
    assert checked["_summary"]["hop_instances"] == 37
    obligations = checked["source_obligations"]
    assert sum(x["id"].startswith("prompt.step.") for x in obligations) == 25
    assert sum(x["id"].startswith("prompt.preflight.") for x in obligations) == 17
    assert sum(x["id"].startswith("prompt.guardrail.") for x in obligations) == 45
    assert sum(x["id"].startswith("prompt.verification.") for x in obligations) == 32
    assert sum(x["id"].startswith("jit.rule.") for x in obligations) == 7
    assert sum(x["id"].startswith("jit.temporal.") for x in obligations) == 4
    assert parity.RENDERED.read_text(encoding="utf-8") == parity.render(checked)


def test_prompt_closure_inventory_matches_contract_exactly() -> None:
    import re

    contract = parity.load_contract()
    prompt = (parity.ROOT / ".github/prompts/start-programstart-project.prompt.md").read_text(encoding="utf-8")

    def section(start: str, end: str | None = None) -> str:
        text = prompt.split(start, 1)[1]
        return text.split(end, 1)[0] if end else text

    expected = {
        "prompt.preflight.": [
            line for line in section("## Pre-flight", "## Environment Boundary").splitlines() if re.match(r"^\d+[a-z]?\. ", line)
        ],
        "prompt.guardrail.": [
            line for line in section("## Automation Guardrails", "## Verification Gate").splitlines() if line.startswith("- ")
        ],
        "prompt.verification.": [line for line in section("## Verification Gate").splitlines() if re.match(r"^\d+\. ", line)],
    }
    for prefix, anchors in expected.items():
        actual = [item["anchor"] for item in contract["source_obligations"] if item["id"].startswith(prefix)]
        assert actual == anchors


def test_supporting_methodology_heading_inventory_matches_contract() -> None:
    contract = parity.load_contract()
    specs = {
        "support.work_packet.": "PROGRAMBUILD/PROGRAMBUILD_WORK_PACKET.md",
        "support.planning.": "PROGRAMBUILD/PROGRAMBUILD_PLANNING_OPERATING_MODEL.md",
        "support.challenge.": "PROGRAMBUILD/PROGRAMBUILD_CHALLENGE_GATE.md",
        "support.effective_autonomy.": "docs/PROGRAMSTART_EFFECTIVE_AUTONOMY.md",
        "support.learning.": "docs/PROGRAMSTART_LEARNING_LOOP.md",
        "support.cost.": "docs/PROGRAMSTART_COST_GOVERNANCE.md",
    }
    expected_counts = {
        "support.work_packet.": 25,
        "support.planning.": 15,
        "support.challenge.": 12,
        "support.effective_autonomy.": 14,
        "support.learning.": 13,
        "support.cost.": 13,
    }
    for prefix, rel in specs.items():
        headings = [line for line in (parity.ROOT / rel).read_text(encoding="utf-8").splitlines() if line.startswith("## ")]
        actual = [item["anchor"] for item in contract["source_obligations"] if item["id"].startswith(prefix)]
        assert actual == headings
        assert len(actual) == expected_counts[prefix]


def test_every_prompt_normative_clause_is_explicitly_inventoried() -> None:
    import re

    contract = parity.load_contract()
    prompt = (parity.ROOT / ".github/prompts/start-programstart-project.prompt.md").read_text(encoding="utf-8")
    expected = []
    for raw in prompt.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("### ") or line.startswith("- ") or re.match(r"^\d+[a-z]?\. ", line):
            expected.append(line)
    # Exact-anchor set: duplicate textual clauses need only one source obligation.
    expected_unique = set(expected)
    actual = {
        item["anchor"]
        for item in contract["source_obligations"]
        if item["source_path"] == ".github/prompts/start-programstart-project.prompt.md"
    }
    assert expected_unique <= actual
    assert len(expected_unique - actual) == 0


def test_every_prompt_prose_block_is_explicitly_inventoried() -> None:
    import re

    contract = parity.load_contract()
    lines = (parity.ROOT / ".github/prompts/start-programstart-project.prompt.md").read_text(encoding="utf-8").splitlines()
    expected = []
    buf = []
    in_code = False
    in_front = False
    for i, raw in enumerate(lines):
        line = raw.strip()
        if i == 0 and line == "---":
            in_front = True
            continue
        if in_front:
            if line == "---":
                in_front = False
            continue
        if line.startswith(chr(96) * 3):
            if buf:
                expected.append(" ".join(buf))
                buf = []
            in_code = not in_code
            continue
        if in_code:
            continue
        if not line:
            if buf:
                expected.append(" ".join(buf))
                buf = []
            continue
        if line.startswith("#") or line.startswith("- ") or re.match(r"^\d+[a-z]?\.\s", line) or line.startswith("|"):
            if buf:
                expected.append(" ".join(buf))
                buf = []
            continue
        buf.append(line)
    if buf:
        expected.append(" ".join(buf))

    actual = {
        item["anchor"]
        for item in contract["source_obligations"]
        if item["source_path"] == ".github/prompts/start-programstart-project.prompt.md"
    }
    assert set(expected) <= actual


def test_every_prompt_contract_code_block_is_explicitly_inventoried() -> None:
    contract = parity.load_contract()
    lines = (parity.ROOT / ".github/prompts/start-programstart-project.prompt.md").read_text(encoding="utf-8").splitlines()
    expected = []
    in_code = False
    code = []
    in_front = False
    for i, raw in enumerate(lines):
        line = raw.strip()
        if i == 0 and line == "---":
            in_front = True
            continue
        if in_front:
            if line == "---":
                in_front = False
            continue
        if line.startswith(chr(96) * 3):
            if not in_code:
                in_code = True
                code = []
            else:
                in_code = False
                expected.append("\n".join(code))
            continue
        if in_code:
            code.append(raw.rstrip())

    actual = {
        item["anchor"]
        for item in contract["source_obligations"]
        if item["source_path"] == ".github/prompts/start-programstart-project.prompt.md"
    }
    assert set(expected) <= actual


def test_accepted_conversation_decision_set_is_exact_and_fully_mapped() -> None:
    contract = parity.load_contract()
    expected = {
        "chat_transition_input_not_runtime_authority",
        "three_way_completeness",
        "explicit_mapping_for_material_chat_decisions",
        "jit_is_cross_cutting",
        "evidence_reuse_until_invalidation",
        "autonomy_prompt_becomes_oracle",
        "no_second_orchestrator",
        "third_party_frameworks_reference_only_now",
        "matrix_before_machinery",
        "coverage_not_parity",
        "credential_human_enablement_precedes_expensive_workaround",
        "backbone_prepares_minimal_human_gate",
        "eliminate_human_transport_preserve_human_enablement",
        "cross_owner_generic_observation_owner_specific_admission",
        "observation_does_not_create_authority",
        "ecosystem_contracts_first_live_integration",
        "ordinary_intent_should_be_sufficient",
        "chatgpt_bootstrap_not_recurring_orchestrator",
        "matrix_makes_omission_mechanically_visible",
        "supporting_methodology_remains_canonical_jit",
        "reuse_current_learning_gate_for_promotion",
        "parity_matrix_not_vector_authority",
        "first_wave_machinery_priority",
        "cross_owner_observation_extends_existing_repository_broker",
        "credential_enablement_leverage_dimensions",
        "credential_exception_not_general_human_gate_preference",
        "general_mechanism_does_not_satisfy_instance_acceptance",
    }
    actual = {item["id"] for item in contract["conversation_decisions"]}
    assert actual == expected
    assert len(actual) == 27
    for item in contract["conversation_decisions"]:
        expected_ref = (
            "GrahamArdent/PROGRAMSTART#147"
            if item["id"] == "general_mechanism_does_not_satisfy_instance_acceptance"
            else "GrahamArdent/PROGRAMSTART#141"
        )
        assert item["durable_reference"] == expected_ref
        assert item["behavior_refs"] or item["methodology_delta_refs"]


def test_conversation_decision_unknown_behavior_fails_closed() -> None:
    contract = parity.load_contract()
    contract["conversation_decisions"][0]["behavior_refs"] = ["does_not_exist"]
    errors = _errors(contract)
    assert any("references unknown behavior" in x for x in errors)


def test_conversation_decision_without_mapping_fails_closed() -> None:
    contract = parity.load_contract()
    contract["conversation_decisions"][0]["behavior_refs"] = []
    contract["conversation_decisions"][0]["methodology_delta_refs"] = []
    errors = _errors(contract)
    assert any("has no durable mapping" in x for x in errors)


def test_credential_human_enablement_decision_is_canonicalized() -> None:
    contract = parity.load_contract()
    target = next(
        x for x in contract["conversation_decisions"] if x["id"] == "credential_human_enablement_precedes_expensive_workaround"
    )
    assert target["status"] == "accepted_reconciled"
    assert target["methodology_delta_refs"] == []


def test_conversation_reconciliation_behavior_is_required() -> None:
    contract = parity.load_contract()
    contract["behaviors"] = [x for x in contract["behaviors"] if x["id"] != "conversation_decision_reconciliation"]
    errors = _errors(contract)
    assert any("required cross-cutting behavior missing: conversation_decision_reconciliation" in x for x in errors)


def test_source_fingerprint_drift_fails_closed() -> None:
    contract = parity.load_contract()
    contract["source_files"][0]["sha256"] = "0" * 64
    errors = _errors(contract)
    assert any("source fingerprint drift" in x for x in errors)


def test_uncovered_prompt_obligation_fails_closed() -> None:
    contract = parity.load_contract()
    target = "prompt.step.25"
    for behavior in contract["behaviors"]:
        behavior["covers"] = [x for x in behavior["covers"] if x != target]
    errors = _errors(contract)
    assert f"uncovered obligation: {target}" in errors


def test_matrix_cannot_become_load_all_runtime_contract() -> None:
    contract = parity.load_contract()
    contract["runtime_usage"]["load_entire_contract_per_effect"] = True
    errors = _errors(contract)
    assert any("must remain JIT" in x for x in errors)


def test_documentation_only_row_cannot_be_inflated_to_implemented() -> None:
    contract = parity.load_contract()
    behavior = next(x for x in contract["behaviors"] if x["id"] == "data_grounding_instruction_isolation")
    behavior["machinery_state"] = "implemented"
    errors = _errors(contract)
    assert any("lacks code plus test/live proof" in x for x in errors)


def test_credential_human_enablement_is_canonical_not_pending() -> None:
    contract = parity.load_contract()
    assert "credential_human_enablement_v1" not in {x["id"] for x in contract["pending_methodology_deltas"]}
    behavior = next(x for x in contract["behaviors"] if x["id"] == "credential_human_enablement_leverage")
    assert behavior["machinery_state"] == "partial"
    assert behavior["closure_status"] == "partial"
    assert "support.effective_autonomy.09" in behavior["covers"]


def test_canonical_credential_human_enablement_cannot_regress_to_missing() -> None:
    contract = parity.load_contract()
    behavior = next(x for x in contract["behaviors"] if x["id"] == "credential_human_enablement_leverage")
    behavior["machinery_state"] = "missing"
    errors = _errors(contract)
    assert any("canonical credential human-enablement behavior must remain at least partial" in x for x in errors)


def test_required_cross_cutting_jit_row_cannot_disappear() -> None:
    contract = parity.load_contract()
    contract["behaviors"] = [x for x in contract["behaviors"] if x["id"] != "jit_context_evidence_governor"]
    errors = _errors(contract)
    assert any("required cross-cutting behavior missing" in x for x in errors)


def test_implemented_rows_require_exact_repo_commit_path_proof_references() -> None:
    contract = parity.load_contract()
    behavior = next(x for x in contract["behaviors"] if x["id"] == "replay_idempotency")
    behavior["current_proof"][0]["ref"] = "some replay code"
    errors = _errors(contract)
    assert any("non-exact code proof reference" in x for x in errors)


def test_canonical_credential_human_enablement_coverage_cannot_disappear() -> None:
    contract = parity.load_contract()
    behavior = next(x for x in contract["behaviors"] if x["id"] == "credential_human_enablement_leverage")
    behavior["covers"] = []
    errors = _errors(contract)
    assert any("canonical credential human-enablement behavior must cover Effective Autonomy section 9" in x for x in errors)


def test_coverage_is_not_mistaken_for_backbone_parity() -> None:
    contract = parity.load_contract()
    checked = copy.deepcopy(contract)
    assert parity.validate_contract(checked) == []
    states = checked["_summary"]["machinery_states"]
    assert states["implemented"] < checked["_summary"]["behaviors"]
    assert states["partial"] >= 1
    assert states["prompt_only"] >= 1
    assert checked["matrix_challenge"]["status"] == "clear"


def test_jit_behavior_selector_returns_only_requested_behavior_and_source_refs() -> None:
    contract = parity.load_contract()
    selected = parity.select_behaviors(contract, ["jit_context_evidence_governor"])
    assert selected["authority_role"] == "derived_acceptance_evidence"
    assert selected["retrieval_policy"] == "jit_by_trigger"
    assert selected["canonical_source_required"] is True
    assert selected["selected_behavior_ids"] == ["jit_context_evidence_governor"]
    assert "behaviors" not in selected
    assert len(selected["selections"]) == 1
    result = selected["selections"][0]
    assert result["behavior"]["id"] == "jit_context_evidence_governor"
    expected = next(x for x in contract["behaviors"] if x["id"] == "jit_context_evidence_governor")
    assert {x["obligation_id"] for x in result["canonical_source_refs"]} == set(expected["covers"])
    assert all("source_path" in x and "anchor" in x for x in result["canonical_source_refs"])
    assert all("source_text" not in x for x in result["canonical_source_refs"])


def test_jit_behavior_selector_preserves_exact_order_and_deduplicates() -> None:
    contract = parity.load_contract()
    selected = parity.select_behaviors(
        contract,
        ["evidence_reuse_invalidation", "jit_context_evidence_governor", "evidence_reuse_invalidation"],
    )
    assert selected["selected_behavior_ids"] == [
        "evidence_reuse_invalidation",
        "jit_context_evidence_governor",
    ]
    assert [x["behavior"]["id"] for x in selected["selections"]] == selected["selected_behavior_ids"]


def test_jit_behavior_selector_fails_closed_on_unknown_behavior() -> None:
    contract = parity.load_contract()
    try:
        parity.select_behaviors(contract, ["does_not_exist"])
    except ValueError as exc:
        assert "unknown parity behavior id" in str(exc)
    else:
        raise AssertionError("unknown behavior id did not fail closed")


def test_jit_behavior_selector_rejects_contract_drift_before_selection() -> None:
    contract = parity.load_contract()
    contract["source_files"][0]["sha256"] = "0" * 64
    try:
        parity.select_behaviors(contract, ["jit_context_evidence_governor"])
    except ValueError as exc:
        assert "source fingerprint drift" in str(exc)
    else:
        raise AssertionError("selector returned routing evidence from an invalid contract")


def test_material_hop_inventory_is_exact_and_instance_scoped() -> None:
    contract = parity.load_contract()
    assert _errors(contract) == []
    hop_ids = [item["id"] for item in contract["hop_instances"]]
    assert hop_ids == [f"HOP-{n:03d}" for n in range(1, 38)]
    assert len(hop_ids) == 37
    assert contract["hop_policy"]["instance_acceptance_required"] is True
    assert contract["hop_policy"]["general_mechanism_implies_instance_acceptance"] is False
    assert contract["hop_policy"]["path_authority_role"] == "referenced_not_replaced"
    assert any(item["target"] == "Paths Project / Path Authority logical owner" for item in contract["hop_instances"])


def test_generic_hop_mechanism_cannot_imply_instance_acceptance() -> None:
    contract = parity.load_contract()
    contract["hop_policy"]["general_mechanism_implies_instance_acceptance"] = True
    errors = _errors(contract)
    assert any("must never imply instance acceptance" in x for x in errors)


def test_duplicate_concrete_hop_fails_closed() -> None:
    contract = parity.load_contract()
    duplicate = copy.deepcopy(contract["hop_instances"][0])
    duplicate["id"] = "HOP-999"
    contract["hop_instances"].append(duplicate)
    errors = _errors(contract)
    assert any("duplicate concrete hop instance" in x for x in errors)


def test_hop_unknown_behavior_reference_fails_closed() -> None:
    contract = parity.load_contract()
    contract["hop_instances"][0]["required_behavior_refs"] = ["does_not_exist"]
    errors = _errors(contract)
    assert any("references unknown behavior" in x for x in errors)


def test_owner_hop_cannot_drop_cross_owner_safety_refs() -> None:
    contract = parity.load_contract()
    owner = next(x for x in contract["hop_instances"] if x["class"] == "owner_instance")
    owner["required_behavior_refs"] = [x for x in owner["required_behavior_refs"] if x != "repository_independence"]
    errors = _errors(contract)
    assert any("owner instance missing required behavior: repository_independence" in x for x in errors)
