"""Consumer tests adapted from Matrix PR50; exercise pinned modules without changing their bytes."""

import copy
import json
from pathlib import Path

import pytest

from scripts.matrix_projection_dependency.operationalization import (
    project_operationalization,
    reconcile_operationalization,
    reconstruct_operationalization,
    reconstruction_receipt,
    validate_manifest,
)


def inputs():
    manifest = json.loads((Path(__file__).parent / "fixtures/decision_closure/pinned_projection_test_manifest.json").read_text())
    tasks = []
    for identity in ["ISO-01", "GATE-01", "gate:GATE-01"]:
        tasks.append(
            dict(
                task_id=identity,
                owner_disposition="SATISFIED" if identity.startswith("gate:") else "OPEN",
                currentness="CURRENT",
                matrix_reconciliation="RECONCILED",
                projection_role=manifest["projection_role"],
                execution_mode="BACKBONE",
                source_ref=manifest["source_ref"],
                source_version=manifest["source_version"],
            )
        )
    graph = dict(
        execution_authority=False,
        tasks=tasks,
        relations=[
            dict(source="ISO-01", target="GATE-01", relation="DEPENDS_ON", field_class="OWNER_SOURCED"),
            dict(source="GATE-01", target="gate:GATE-01", relation="DEPENDS_ON", field_class="OWNER_SOURCED"),
        ],
    )
    return manifest, dict(
        source_owner="fixture/owner",
        source_ref=manifest["source_ref"],
        source_version=manifest["source_version"],
        readiness_graph=graph,
        root_task_id="ISO-01",
        projection_identity="fixture-plan",
    )


def test_cold_full_meaning_and_receipt():
    manifest, args = inputs()
    artifact = project_operationalization(manifest, **args)
    cold = json.loads(json.dumps(artifact))
    assert reconstruct_operationalization(cold) == manifest
    receipt = reconstruction_receipt(cold)
    assert receipt["reconstructed_manifest"]["gates"][0]["pass_condition"] == "requirements satisfied"
    assert receipt["reconstructed_manifest"]["falsifiers"][0]["consequence"] == "evaluate stronger isolation"
    assert receipt["reconstructed_manifest"]["planned_steps"][0]["gate_refs"] == ["GATE-01"]
    assert receipt["reconstructed_manifest"]["constraints"] == ["execution_authority=false"]
    assert receipt["reconstructed_manifest"]["terminal_condition"] == "protected outcome is independently proven"


def test_gate_mutation_and_same_version_conflict():
    manifest, args = inputs()
    prior = project_operationalization(manifest, **args)
    manifest["gates"][0]["pass_condition"] = "two independent receipts required"
    assert project_operationalization(manifest, **args)["semantic_hash"] != prior["semantic_hash"]
    with pytest.raises(ValueError, match="same-version"):
        reconcile_operationalization(prior, manifest, **args)


@pytest.mark.parametrize("field", ["source_owner", "source_ref", "source_version"])
def test_source_substitution(field):
    manifest, args = inputs()
    args[field] = "wrong"
    with pytest.raises(ValueError, match="identity"):
        project_operationalization(manifest, **args)


def test_reference_nonselection_and_permutation():
    manifest, args = inputs()
    a = project_operationalization(manifest, **args)
    args["readiness_graph"]["tasks"].reverse()
    args["readiness_graph"]["relations"].reverse()
    assert project_operationalization(manifest, **args) == a
    manifest["projection_role"] = "REFERENCE_PLAN"
    for task in args["readiness_graph"]["tasks"]:
        task["projection_role"] = "REFERENCE_PLAN"
    assert project_operationalization(manifest, **args)["frontier"]["selected_task_id"] is None


@pytest.mark.parametrize("change", ["duplicate", "missing-edge", "missing-step", "authority", "cycle"])
def test_bad_graph(change):
    manifest, args = inputs()
    g = args["readiness_graph"]
    if change == "duplicate":
        g["tasks"].append(copy.deepcopy(g["tasks"][0]))
    if change == "missing-edge":
        g["relations"].pop()
    if change == "missing-step":
        g["tasks"].pop(1)
    if change == "unreconciled":
        g["tasks"][0]["matrix_reconciliation"] = "RECONSIDERATION_REQUIRED"
    if change == "authority":
        g["tasks"][0]["execution_authority"] = True
    if change == "cycle":
        g["relations"].append(dict(source="GATE-01", target="ISO-01", relation="DEPENDS_ON", field_class="OWNER_SOURCED"))
    with pytest.raises(ValueError):
        project_operationalization(manifest, **args)


def test_material_stale_and_applicable_history():
    manifest, args = inputs()
    task = args["readiness_graph"]["tasks"][2]
    task["currentness"] = "STALE"
    assert project_operationalization(manifest, **args)["frontier"]["selected_task_id"] is None
    task["evidence_applicability"] = dict(
        state="APPLICABLE",
        evidence_ref="fixture:owner-current-applicability",
        source_ref=task["source_ref"],
        source_version=task["source_version"],
    )
    assert project_operationalization(manifest, **args)["frontier"]["selected_task_id"] == "GATE-01"
    task["evidence_applicability"]["state"] = "INVALIDATED"
    assert project_operationalization(manifest, **args)["frontier"]["selected_task_id"] is None


def test_material_missing_reconciliation_blocks_but_unrelated_history_does_not():
    manifest, args = inputs()
    graph = args["readiness_graph"]
    foreign = dict(task_id="foreign", owner_disposition="OPEN", currentness="CURRENT", execution_mode="BACKBONE")
    graph["tasks"].append(foreign)
    assert project_operationalization(manifest, **args)["frontier"]["selected_task_id"] == "GATE-01"
    graph["relations"].append(dict(source="GATE-01", target="foreign", relation="DEPENDS_ON", field_class="OWNER_SOURCED"))
    assert project_operationalization(manifest, **args)["frontier"]["selected_task_id"] is None
    foreign["matrix_reconciliation"] = "RECONCILED"
    assert project_operationalization(manifest, **args)["frontier"]["selected_task_id"] == "foreign"


def test_unrelated_root_and_material_identity_collision_rejected():
    manifest, args = inputs()
    extra = copy.deepcopy(args["readiness_graph"]["tasks"][0])
    extra["task_id"] = "unrelated"
    args["readiness_graph"]["tasks"].append(extra)
    args["root_task_id"] = "unrelated"
    with pytest.raises(ValueError, match="not a material"):
        project_operationalization(manifest, **args)
    manifest, args = inputs()
    manifest["planned_steps"][0]["id"] = "ISO-01"
    with pytest.raises(ValueError, match="ambiguous material"):
        project_operationalization(manifest, **args)


@pytest.mark.parametrize("collection", ["obligations", "planned_steps", "gates", "falsifiers"])
def test_manifest_rejects_duplicate_material_identity(collection):
    manifest, _ = inputs()
    manifest[collection].append(copy.deepcopy(manifest[collection][0]))
    with pytest.raises(ValueError, match=f"duplicate {collection} identity"):
        validate_manifest(manifest)


@pytest.mark.parametrize(
    "change,reason",
    [
        ("cycle", "dependency cycle"),
        ("missing-step", "dangling planned step dependency"),
        ("missing-outcome", "dangling outcome or gate reference"),
        ("missing-gate", "dangling outcome or gate reference"),
    ],
)
def test_manifest_rejects_broken_plan_links(change, reason):
    manifest, _ = inputs()
    step = manifest["planned_steps"][0]
    if change == "cycle":
        step["depends_on"] = [step["id"]]
    elif change == "missing-step":
        step["depends_on"] = ["missing"]
    elif change == "missing-outcome":
        step["outcome_supported"] = ["missing"]
    else:
        step["gate_refs"] = ["missing"]
    with pytest.raises(ValueError, match=reason):
        validate_manifest(manifest)


def test_shared_step_dependencies_are_valid_and_reconstructable():
    manifest, args = inputs()
    leaf = manifest["planned_steps"][0]
    for name in ["STEP-2", "STEP-3"]:
        step = copy.deepcopy(leaf)
        step.update(id=name, depends_on=[leaf["id"]])
        manifest["planned_steps"].append(step)
        graph = args["readiness_graph"]
        task = copy.deepcopy(graph["tasks"][1])
        task["task_id"] = name
        graph["tasks"].append(task)
        for source, target in [("ISO-01", name), (name, leaf["id"]), (name, "gate:GATE-01")]:
            graph["relations"].append(dict(source=source, target=target, relation="DEPENDS_ON", field_class="OWNER_SOURCED"))
    artifact = project_operationalization(manifest, **args)
    assert reconstruct_operationalization(artifact) == manifest
    assert artifact["frontier"]["selected_task_id"] == "GATE-01"


@pytest.mark.parametrize(
    "change,reason",
    [
        ("blank-identity", "projection identity required"),
        ("duplicate-edge", "duplicate dependency relation"),
        ("root-source", "root does not bind"),
        ("missing-role", "material plan role"),
    ],
)
def test_projection_rejects_incomplete_identity_and_graph(change, reason):
    manifest, args = inputs()
    graph = args["readiness_graph"]
    if change == "blank-identity":
        args["projection_identity"] = " "
    elif change == "duplicate-edge":
        graph["relations"].append(copy.deepcopy(graph["relations"][0]))
    elif change == "root-source":
        graph["tasks"][0]["source_ref"] = "foreign/owner#1"
    else:
        graph["tasks"][1].pop("projection_role")
    with pytest.raises(ValueError, match=reason):
        project_operationalization(manifest, **args)


@pytest.mark.parametrize("change", ["authority", "version", "type", "hash", "bookkeeping"])
def test_reconstruction_rejects_corrupt_cold_artifact(change):
    manifest, args = inputs()
    artifact = project_operationalization(manifest, **args)
    if change == "authority":
        artifact["execution_authority"] = True
    elif change == "version":
        artifact["artifact_version"] = "1.2"
    elif change == "type":
        artifact["artifact_type"] = "foreign"
    elif change == "hash":
        artifact["semantic_hash"] = "0" * 64
    else:
        artifact["matrix_bookkeeping"]["reconsideration_required"] = True
    reason = "non-authoritative projection required" if change in {"authority", "version", "type"} else "inconsistent"
    with pytest.raises(ValueError, match=reason):
        reconstruct_operationalization(json.loads(json.dumps(artifact)))


def test_reconciliation_accepts_identical_replay_and_new_version_but_not_source_substitution():
    manifest, args = inputs()
    prior = project_operationalization(manifest, **args)
    assert reconcile_operationalization(prior, manifest, **args) == prior
    manifest["source_version"] = args["source_version"] = "version-2"
    for task in args["readiness_graph"]["tasks"]:
        task["source_version"] = "version-2"
    candidate = reconcile_operationalization(prior, manifest, **args)
    assert candidate["source_binding"]["version"] == "version-2"
    assert candidate["semantic_hash"] != prior["semantic_hash"]
    manifest["source_ref"] = args["source_ref"] = "fixture/owner:other.json"
    for task in args["readiness_graph"]["tasks"]:
        task["source_ref"] = manifest["source_ref"]
    with pytest.raises(ValueError, match="projection source substitution"):
        reconcile_operationalization(prior, manifest, **args)


def test_manifest_rejects_structurally_valid_unsupported_contract_version():
    manifest, _ = inputs()
    manifest["contract_version"] = "unsupported"
    with pytest.raises(ValueError, match="unsupported manifest contract version"):
        validate_manifest(manifest)
