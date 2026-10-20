"""Selection rules and re-evaluation preserve evidence and explain drift."""

import argparse
import json

from scripts import programstart_recommend as recommend


def test_recommendation_inputs_infer_capabilities_from_real_kickoff(tmp_path, monkeypatch):
    folder = tmp_path / "PROGRAMBUILD"
    folder.mkdir()
    (folder / "PROGRAMBUILD_KICKOFF_PACKET.md").write_text(
        "PRODUCT_SHAPE: web app\nCORE_PROBLEM: email notifications and authentication\n"
    )
    monkeypatch.setattr(recommend, "workspace_path", lambda relative: tmp_path / relative)
    shape, needs = recommend.load_recommendation_inputs(argparse.Namespace(product_shape=None, need=[]))
    assert shape == "web app"
    assert "email" in needs and "authentication" in needs
    assert recommend.parse_kickoff_inputs(tmp_path / "missing") == {}
    assert recommend.list_of_dicts(None) == []
    assert recommend.list_of_strings(None) == []


def test_preference_caution_and_duplicate_candidates_are_explained():
    entries = [
        {"name": ""},
        {"name": "Preferred", "notes": ["keep", "keep"]},
        {"name": "Preferred"},
        {"name": "Cautioned", "trigger_services": ["base"]},
    ]
    rules = [
        {"title": "bounded", "match_product_shapes": ["web app"], "prefer_items": ["Preferred"], "avoid_items": ["Cautioned"]}
    ]
    selected, notes, evidence, _ = recommend.select_triggered_entries(
        entries=entries,
        product_shape="web app",
        needs=set(),
        stack_names=[],
        service_names=["base"],
        decision_rules=rules,
        min_score=0,
        category="third_party_apis",
    )
    assert selected == ["Preferred"]
    assert notes == ["keep"]
    assert any("KB rule preference" in reason for row in evidence for reason in row["reasons"])


def test_project_reevaluation_records_registry_and_variant_drift(tmp_path):
    folder = tmp_path / "PROGRAMBUILD"
    folder.mkdir()
    (folder / "PROGRAMBUILD_KICKOFF_PACKET.md").write_text("PRODUCT_SHAPE: web app\nCORE_PROBLEM: email delivery\n")
    (folder / "PROGRAMBUILD_STATE.json").write_text(json.dumps({"variant": "enterprise"}))
    (tmp_path / "config").mkdir()
    (tmp_path / "config/process-registry.json").write_text(json.dumps({"version": "old"}))
    report = recommend.re_evaluate_project(str(tmp_path))
    assert any("Registry version drift" in item for item in report["deltas"])
    assert any("Variant drift" in item for item in report["deltas"])
    (folder / "PROGRAMBUILD_STATE.json").unlink()
    assert recommend.re_evaluate_project(str(tmp_path))["project_state"]["variant"] == ""


def test_reevaluation_cli_explains_real_registry_drift(tmp_path, capsys):
    folder = tmp_path / "config"
    folder.mkdir()
    (folder / "process-registry.json").write_text('{"version":"outdated"}')
    assert recommend.main(["--re-evaluate", str(tmp_path)]) == 0
    output = capsys.readouterr().out
    assert "deltas detected" in output and "Registry version drift" in output


def test_blank_stack_and_unmapped_alias_do_not_create_recommendations(monkeypatch):
    monkeypatch.setattr(recommend, "CAPABILITY_ALIASES", {"owner-specific": ["custom alias"]})
    assert recommend.infer_domain_names("unclassified", {"custom alias"}, False, {}) == []
    result = recommend.build_stack_candidates("unclassified", set(), False, {"stacks": [{"name": " "}]})
    assert result[2] == []
    monkeypatch.setattr(recommend, "load_knowledge_base", lambda: {})
    result = recommend.build_recommendation(product_shape="unclassified", needs=set(), regulated=False, attach_userjourney=False)
    assert any("Developer experience, quality, and supply chain" in line for line in result.rationale)
