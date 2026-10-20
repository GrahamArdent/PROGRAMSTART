"""Contract rejection and CLI outcomes, without changing owner acceptance data."""

import copy
import json
import sys
from pathlib import Path

import pytest

from scripts import programstart_autonomy_parity as parity


# Each mutation models an independently invalid declaration and names its diagnostic.
@pytest.mark.parametrize(
    "path,value,reason",
    [
        (("schema_version",), 0, "schema_version"),
        (("contract_id",), "foreign", "contract_id"),
        (("runtime_usage", "authority_role"), "execution", "derived acceptance"),
        (("runtime_usage", "retrieval_policy"), "load_all", "JIT"),
        (("source_files", 0, "path"), "missing-file.md", "source missing"),
        (("source_files", 0, "sha256"), "0" * 64, "fingerprint drift"),
        (("source_obligations", 0, "id"), "", "ids must be unique"),
        (("source_obligations", 0, "required"), False, "not marked required"),
        (("source_obligations", 0, "source_path"), "foreign.md", "unknown source"),
        (("source_obligations", 0, "anchor"), "nonexistent anchor", "anchor drift"),
        (("behaviors", 0, "id"), "", "behavior ids"),
        (("behaviors", 0, "covers"), ["foreign"], "unknown obligation"),
        (("behaviors", 0, "covers"), [], "covers no obligations"),
        (("behaviors", 0, "methodology_delta_refs"), ["foreign"], "must not claim canonical"),
        (("behaviors", 0, "machinery_state"), "wrong", "invalid machinery"),
        (("behaviors", 0, "execution_mode"), "wrong", "invalid execution mode"),
        (("behaviors", 0, "closure_status"), "wrong", "invalid closure"),
        (("behaviors", 0, "trigger"), [], "trigger must be non-empty"),
        (("conversation_decisions",), [], "conversation_decisions must"),
        (("conversation_decisions",), [None], "entries must be objects"),
        (("conversation_decisions", 0, "id"), "", "ids must be unique"),
        (("conversation_decisions", 0, "status"), "wrong", "invalid status"),
        (("conversation_decisions", 0, "durable_reference"), "", "lacks durable reference"),
        (("conversation_decisions", 0, "summary"), "", "lacks summary"),
        (("conversation_decisions", 0, "behavior_refs"), "wrong", "mappings must be lists"),
        (("conversation_decisions", 0, "behavior_refs"), ["foreign"], "unknown behavior"),
        (("conversation_decisions", 0, "methodology_delta_refs"), ["foreign"], "unknown methodology"),
        (("hop_policy", "authority_role"), "execution", "derived acceptance evidence"),
        (("hop_policy", "instance_acceptance_required"), False, "concrete instance"),
        (("hop_policy", "general_mechanism_implies_instance_acceptance"), True, "never imply"),
        (("hop_policy", "path_authority_role"), "replacement", "reference, not replace"),
        (("hop_policy", "durable_reference"), "", "lacks durable reference"),
        (("hop_instances",), [], "hop_instances must"),
        (("hop_instances",), [None], "entries must be objects"),
        (("hop_instances", 0, "id"), "invalid", "unique HOP-NNN"),
        (("hop_instances", 0, "class"), "invalid", "invalid hop class"),
        (("hop_instances", 0, "instance_status"), "invalid", "invalid hop instance"),
        (("hop_instances", 0, "source"), " ", "non-empty string"),
        (("hop_instances", 0, "required_behavior_refs"), [], "non-empty list"),
        (("hop_instances", 0, "required_behavior_refs"), ["foreign"], "unknown behavior"),
        (("hop_instances", 0, "evidence_refs"), [" "], "non-empty string list"),
        (("matrix_challenge", "status"), "invalid", "status invalid"),
        (("matrix_challenge", "adversarial_cases"), [], "at least eight"),
    ],
)
def test_invalid_contract_has_specific_diagnostic(path: tuple, value: object, reason: str) -> None:
    contract = parity.load_contract()
    target = contract
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = value
    assert any(reason in error for error in parity.validate_contract(contract))


@pytest.mark.parametrize(
    "collection,reason",
    [
        ("source_files", "paths must be unique"),
        ("source_obligations", "ids must be unique"),
        ("behaviors", "behavior ids"),
        ("conversation_decisions", "ids must be unique"),
        ("hop_instances", "unique HOP-NNN"),
    ],
)
def test_duplicate_identities_are_not_silently_coalesced(collection: str, reason: str) -> None:
    contract = parity.load_contract()
    contract[collection].append(copy.deepcopy(contract[collection][0]))
    assert any(reason in error for error in parity.validate_contract(contract))


@pytest.mark.parametrize("field", ["authority_status", "durable_reference", "narrows_current_rule", "canonical_effect"])
def test_pending_delta_requires_full_owner_meaning(field: str) -> None:
    contract = parity.load_contract()
    delta = dict(
        id="new-delta",
        authority_status="accepted_pending_canonicalization",
        durable_reference="owner#1",
        narrows_current_rule="bounded",
        canonical_effect="reconcile later",
    )
    delta[field] = ""
    contract["pending_methodology_deltas"].append(delta)
    errors = parity.validate_contract(contract)
    assert any("pending methodology delta" in error and "new-delta" in error for error in errors)


@pytest.mark.parametrize("kind,ref", [("code", "moving/main.py"), ("test", "moving/test.py"), ("live", "not-an-owner-issue")])
def test_implemented_claim_requires_exact_proof_identity(kind: str, ref: str) -> None:
    contract = parity.load_contract()
    behavior = contract["behaviors"][0]
    behavior.update(machinery_state="implemented", current_proof=[{"kind": kind, "ref": ref}])
    errors = parity.validate_contract(contract)
    assert any(f"non-exact {kind}" in error for error in errors)
    assert any("lacks code plus test/live" in error for error in errors)


def test_missing_fields_and_incomplete_mappings_are_visible() -> None:
    contract = parity.load_contract()
    contract["behaviors"][0].pop("owner")
    contract["hop_instances"][0].pop("path_authority_ref")
    contract["conversation_decisions"][0].update(
        behavior_refs=[], methodology_delta_refs=[], status="accepted_pending_methodology"
    )
    duplicate = copy.deepcopy(contract["hop_instances"][0])
    duplicate["id"] = "HOP-999"
    contract["hop_instances"].append(duplicate)
    errors = parity.validate_contract(contract)
    for reason in [
        "missing fields",
        "missing hop fields",
        "no durable mapping",
        "lacks methodology mapping",
        "duplicate concrete",
    ]:
        assert any(reason in error for error in errors)


def test_cli_write_check_selection_and_errors(monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys) -> None:
    output = tmp_path / "parity.md"
    monkeypatch.setattr(parity, "RENDERED", output)
    for args, expected in [
        (["--check"], 1),
        (["--write"], 0),
        (["--check"], 0),
        (["--select-behavior", "unknown"], 1),
        (["--select-behavior", "canonical_before_dependent"], 0),
    ]:
        monkeypatch.setattr(sys, "argv", ["parity", *args])
        assert parity.main() == expected
    selection = capsys.readouterr().out.splitlines()[-1]
    assert json.loads(selection)["selected_behavior_ids"] == ["canonical_before_dependent"]
    monkeypatch.setattr(sys, "argv", ["parity", "--check", "--select-behavior", "x"])
    with pytest.raises(SystemExit) as exc:
        parity.main()
    assert exc.value.code == 2
    monkeypatch.setattr(sys, "argv", ["parity"])
    invalid = tmp_path / "invalid.json"
    invalid.write_text("{")
    monkeypatch.setattr(parity, "CONTRACT", invalid)
    assert parity.main() == 1
    invalid.write_text(json.dumps({"schema_version": 0}))
    assert parity.main() == 1


def test_selection_rejects_invalid_or_empty_request() -> None:
    with pytest.raises(ValueError, match="invalid parity"):
        parity.select_behaviors({}, ["foreign"])
    with pytest.raises(ValueError, match="at least one"):
        parity.select_behaviors(parity.load_contract(), [])


def test_canonical_credential_behavior_cannot_remain_pending_and_delta_renders():
    contract = parity.load_contract()
    credential = next(b for b in contract["behaviors"] if b["id"] == "credential_human_enablement_leverage")
    credential["closure_status"] = "pending_methodology"
    assert any("cannot remain pending_methodology" in error for error in parity.validate_contract(contract))
    contract["pending_methodology_deltas"].append(
        dict(
            id="reference-delta",
            summary="retained finding",
            authority_status="accepted_pending_canonicalization",
            durable_reference="owner#1",
            narrows_current_rule="bounded",
            canonical_effect="reconcile later",
        )
    )
    parity.validate_contract(contract)
    assert "### reference-delta" in parity.render(contract)


def test_conversation_can_reference_a_declared_pending_methodology_delta():
    contract = parity.load_contract()
    contract["pending_methodology_deltas"].append(
        dict(
            id="reference-delta",
            summary="retained finding",
            authority_status="accepted_pending_canonicalization",
            durable_reference="owner#1",
            narrows_current_rule="bounded",
            canonical_effect="reconcile later",
        )
    )
    contract["conversation_decisions"][0]["methodology_delta_refs"] = ["reference-delta"]
    errors = parity.validate_contract(contract)
    assert not any("unknown methodology delta" in error for error in errors)
    assert "pending methodology delta not represented: reference-delta" in errors
