"""Composed Matrix producer -> owner Git resolver -> actual Work Packet compiler."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

import pytest

from scripts.matrix_projection_dependency.operationalization import digest, project_operationalization, reconstruction_receipt
from scripts.programstart_authority_resolver import (
    RepositoryAuthorityObservation,
    compose_decision_operationalization_currentness,
    resolve_operationalization_binding,
    resolve_repository_authority,
)
from scripts.programstart_intent_compile import AuthoritySnapshot, IntentKind, compile_work_packet

ROOT = Path(__file__).resolve().parents[1]


def git(root: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(root), *args], check=True, capture_output=True, text=True).stdout.strip()


def commit(root: Path) -> str:
    git(root, "add", ".")
    git(root, "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "commit", "-qm", "fixture evidence")
    return git(root, "rev-parse", "HEAD")


def write(root: Path, path: str, value: object) -> None:
    p = root / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(value, indent=2) + "\n")


def build(tmp_path: Path):
    owner = tmp_path / "owner"
    matrix = tmp_path / "matrix"
    for root in [owner, matrix]:
        root.mkdir()
        git(root, "init", "-q", "-b", "main")
    manifest = json.loads((ROOT / "tests/fixtures/decision_closure/operationalization_manifest_reference.json").read_text())
    manifest = json.loads(
        json.dumps(manifest).replace("GrahamArdent/programstart-compute-spine#135", "fixture/owner:manifest.json")
    )
    manifest["projection_role"] = "ACTIVE_OPERATIONALIZATION"
    manifest["planned_steps"][0]["gate_refs"] = ["GATE-01"]
    tasks: list[dict[str, Any]] = [
        dict(
            task_id=x,
            owner_disposition="SATISFIED" if x.startswith("gate:") else "OPEN",
            currentness="CURRENT",
            matrix_reconciliation="RECONCILED",
            projection_role="ACTIVE_OPERATIONALIZATION",
            execution_mode="BACKBONE",
            source_ref=manifest["source_ref"],
            source_version=manifest["source_version"],
        )
        for x in ["ISO-01", "GATE-01", "gate:GATE-01"]
    ]
    graph: dict[str, Any] = dict(
        execution_authority=False,
        tasks=tasks,
        relations=[
            dict(source="ISO-01", target="GATE-01", relation="DEPENDS_ON", field_class="OWNER_SOURCED"),
            dict(source="GATE-01", target="gate:GATE-01", relation="DEPENDS_ON", field_class="OWNER_SOURCED"),
        ],
    )
    artifact = project_operationalization(
        manifest,
        source_owner="fixture/owner",
        source_ref=manifest["source_ref"],
        source_version=manifest["source_version"],
        readiness_graph=graph,
        root_task_id="ISO-01",
        projection_identity="fixture-rich-plan",
    )
    write(matrix, "projection.json", artifact)
    matrix_commit = commit(matrix)
    descriptor = dict(
        contract_version="programstart.accepted-operationalization.v1",
        manifest_path="manifest.json",
        accepted_manifest_sha256=digest(manifest),
        owner_decision_ref=manifest["decision_refs"][0],
        readiness_path="graph.json",
        reconstruction_path="receipt.json",
        root_task_id="ISO-01",
        projection_ref=f"GrahamArdent/ecosystem-matrix@{matrix_commit}:projection.json",
    )
    write(owner, "manifest.json", manifest)
    write(owner, "graph.json", graph)
    write(owner, "receipt.json", reconstruction_receipt(artifact))
    write(owner, "operationalization.json", descriptor)
    write(
        owner,
        "PROGRAMSTART_AUTHORITY.json",
        dict(
            schema_version="programstart.owner-authority.v1",
            project_name="Fixture",
            owning_repository="fixture/owner",
            execution_mode="mode_c_existing_project",
            authority_paths=["MASTER.md"],
            decision_operationalization_path="operationalization.json",
        ),
    )
    (owner / "MASTER.md").write_text("Fixture owner accepts only its declared current operationalization.\n")
    commit(owner)

    def authority():
        return resolve_repository_authority(
            RepositoryAuthorityObservation(
                repository_root=owner,
                owning_repository="fixture/owner",
                observed_head=git(owner, "rev-parse", "HEAD"),
                methodology_commit=git(ROOT, "rev-parse", "HEAD"),
            )
        )

    snapshot = authority()
    binding = resolve_operationalization_binding(snapshot, matrix)
    return owner, matrix, manifest, graph, artifact, descriptor, snapshot, binding, authority


def compile(snapshot: AuthoritySnapshot):
    return compile_work_packet("Run bounded selected step.", snapshot, kind=IntentKind.BOUNDED_EXECUTION)


def test_real_composed_positive_and_cold_reconstruction(tmp_path):
    *_, snapshot, binding, _ = build(tmp_path)
    current = compose_decision_operationalization_currentness(snapshot, binding)
    packet = compile(current)
    assert packet.admission_hint == "ready_for_controller_admission"
    recovered = AuthoritySnapshot.model_validate_json(current.model_dump_json())
    assert compile(recovered).semantic_digest == packet.semantic_digest
    full = packet.authority.decision_operationalization
    assert full is not None and full.projection_ready


def test_declared_scope_cannot_omit_or_strip_binding(tmp_path):
    *_, snapshot, binding, _ = build(tmp_path)
    with pytest.raises(ValueError, match="missing"):
        compile(snapshot)
    bound = compose_decision_operationalization_currentness(snapshot, binding)
    with pytest.raises(ValueError):
        compile(bound.model_copy(update={"decision_operationalization": None}))
    thin = binding.model_copy(update={"reconstruction_evidence": None})
    with pytest.raises(ValueError):
        compile(snapshot.model_copy(update={"decision_operationalization": thin}))


@pytest.mark.parametrize(
    "change",
    [
        "reference",
        "gate",
        "source",
        "thin",
        "receipt",
        "coverage-only",
        "unreconciled",
        "stale",
        "missing-edge",
        "wrong-root",
        "duplicate-key",
    ],
)
def test_native_consumer_negatives(tmp_path, change):
    owner, matrix, manifest, graph, artifact, descriptor, snapshot, binding, authority = build(tmp_path)
    if change == "reference":
        manifest["projection_role"] = "REFERENCE_PLAN"
    if change == "gate":
        manifest["gates"][0]["pass_condition"] = "two independent proofs"
    if change == "source":
        manifest["source_ref"] = "wrong/owner#2"
    if change in ["reference", "gate", "source"]:
        write(owner, "manifest.json", manifest)
        descriptor["accepted_manifest_sha256"] = digest(manifest)
    if change == "unreconciled":
        graph["tasks"][0]["matrix_reconciliation"] = "RECONSIDERATION_REQUIRED"
    if change == "stale":
        graph["tasks"][2]["currentness"] = "STALE"
    if change == "missing-edge":
        graph["relations"].pop()
    if change in ["unreconciled", "stale", "missing-edge"]:
        write(owner, "graph.json", graph)
    if change == "wrong-root":
        descriptor["root_task_id"] = "GATE-01"
    if change in ["receipt", "coverage-only"]:
        write(owner, "receipt.json", {"coverage": "challenged", "status": "PASS", "semantic_hash": artifact["semantic_hash"]})
    if change == "thin":
        artifact.pop("owner_manifest")
        write(matrix, "projection.json", artifact)
        h = commit(matrix)
        descriptor["projection_ref"] = f"GrahamArdent/ecosystem-matrix@{h}:projection.json"
    write(owner, "operationalization.json", descriptor)
    if change == "duplicate-key":
        (owner / "manifest.json").write_text('{"projection_role":"REFERENCE_PLAN","projection_role":"ACTIVE_OPERATIONALIZATION"}')
    commit(owner)
    # Old snapshot cannot survive the new owner head, even if copied with positive labels.
    assert not binding.projection_ready
    with pytest.raises(ValueError):
        compile(snapshot.model_copy(update={"decision_operationalization": binding}))
    with pytest.raises((ValueError, KeyError)):
        resolve_operationalization_binding(authority(), matrix)


def test_missing_binding_ingress_routes_machine_reconciliation(tmp_path):
    from test_programstart_intent_compile import harvest

    from scripts.programstart_intent_ingress import ContextualIntentRequest, resolve_contextual_intent

    *_, snapshot, _, _ = build(tmp_path)
    result = resolve_contextual_intent(ContextualIntentRequest(harvest=harvest(), authority=snapshot))
    assert result.operator_intervention_required is False
    assert "owner-selected operationalization" in (result.next_system_requirement or "")


@pytest.mark.parametrize(
    "field,value", [("artifact_version", "1.2"), ("projection_role", "REFERENCE_PLAN"), ("reconstruction_evidence", None)]
)
def test_copied_rich_evidence_cannot_downgrade(tmp_path, field, value):
    *_, snapshot, bound, _ = build(tmp_path)
    if field == "reconstruction_evidence":
        changed = bound.model_copy(update={field: value})
    else:
        changed = bound.model_copy(deep=True)
        assert changed.matrix_projection is not None
        changed.matrix_projection = changed.matrix_projection.model_copy(update={field: value})
    with pytest.raises(ValueError):
        compile(snapshot.model_copy(update={"decision_operationalization": changed}))


def test_legacy_independent_authority_unchanged():
    ordinary = AuthoritySnapshot(
        project_name="Independent",
        owning_repository="fixture/independent",
        authority_commit="a" * 40,
        methodology_commit="b" * 40,
        authority_paths=["MASTER.md"],
        execution_mode="mode_c_existing_project",
    )
    assert compile(ordinary).admission_hint == "ready_for_controller_admission"


def test_applicable_history_at_actual_consumer(tmp_path):
    owner, matrix, manifest, graph, artifact, descriptor, snapshot, binding, authority = build(tmp_path)
    task = graph["tasks"][2]
    task["currentness"] = "STALE"
    task["evidence_applicability"] = dict(
        state="APPLICABLE",
        evidence_ref="fixture:owner-applicability",
        source_ref=task["source_ref"],
        source_version=task["source_version"],
    )
    artifact = project_operationalization(
        manifest,
        source_owner="fixture/owner",
        source_ref=manifest["source_ref"],
        source_version=manifest["source_version"],
        readiness_graph=graph,
        root_task_id="ISO-01",
        projection_identity="fixture-rich-plan",
    )
    write(matrix, "projection.json", artifact)
    h = commit(matrix)
    descriptor["projection_ref"] = f"GrahamArdent/ecosystem-matrix@{h}:projection.json"
    write(owner, "graph.json", graph)
    write(owner, "receipt.json", reconstruction_receipt(artifact))
    write(owner, "operationalization.json", descriptor)
    commit(owner)
    snapshot = authority()
    binding = resolve_operationalization_binding(snapshot, matrix)
    assert (
        compile(compose_decision_operationalization_currentness(snapshot, binding)).admission_hint
        == "ready_for_controller_admission"
    )


def test_cold_checkout_locations_do_not_change_packet_meaning(tmp_path):
    owner, matrix, *_, snapshot, bound, _ = build(tmp_path)
    first = compile(compose_decision_operationalization_currentness(snapshot, bound))
    cold_owner, cold_matrix = tmp_path / "cold-owner", tmp_path / "cold-matrix"
    subprocess.run(["git", "clone", "-q", str(owner), str(cold_owner)], check=True)
    subprocess.run(["git", "clone", "-q", str(matrix), str(cold_matrix)], check=True)
    cold = resolve_repository_authority(
        RepositoryAuthorityObservation(
            repository_root=cold_owner,
            owning_repository="fixture/owner",
            observed_head=git(cold_owner, "rev-parse", "HEAD"),
            methodology_commit=git(ROOT, "rev-parse", "HEAD"),
        )
    )
    cold_bound = resolve_operationalization_binding(cold, cold_matrix)
    assert compile(compose_decision_operationalization_currentness(cold, cold_bound)).semantic_digest == first.semantic_digest


def test_unchanged_snapshot_cannot_hide_source_drift(tmp_path):
    from scripts.programstart_intent_compile import assess_authority_drift

    owner, _, *_, snapshot, bound, _ = build(tmp_path)
    ready = compose_decision_operationalization_currentness(snapshot, bound)
    packet = compile(ready)
    (owner / "unrelated.md").write_text("Owner acquisition must be re-read")
    commit(owner)
    assert assess_authority_drift(packet, ready).status == "recompile_required"


def test_matrix_dependency_pins_and_owner_schema_are_exact():
    import hashlib

    dependency = ROOT / "scripts/matrix_projection_dependency"
    pins = json.loads((dependency / "UPSTREAM.json").read_text())
    assert pins["source_commit"] == "9238ae74d1e1bad052852cd4a7a0464202cf0ed6"
    for name, expected in pins["files"].items():
        assert hashlib.sha256((dependency / name).read_bytes()).hexdigest() == expected
    assert (dependency / "decision-operationalization-manifest.schema.json").read_bytes() == (
        ROOT / "schemas/decision-operationalization-manifest.schema.json"
    ).read_bytes()


def test_owner_advancing_during_evidence_read_is_rejected(tmp_path, monkeypatch):
    from scripts import programstart_authority_resolver as resolver

    owner, matrix, *_, snapshot, _, _ = build(tmp_path)
    original = resolver._json_artifact

    def read(root, version, path):
        result = original(root, version, path)
        if path == "receipt.json":
            (owner / "concurrent-owner-change.md").write_text("Current owner advanced")
            commit(owner)
        return result

    monkeypatch.setattr(resolver, "_json_artifact", read)
    with pytest.raises(resolver.AuthorityResolutionError, match="head is stale"):
        resolve_operationalization_binding(snapshot, matrix)


def test_reconstruction_uses_packaged_schema_without_checkout_schema_path(tmp_path, monkeypatch):
    from scripts import programstart_authority_resolver as resolver

    _, matrix, *_, snapshot, _, _ = build(tmp_path)
    monkeypatch.setattr(resolver, "__file__", str(tmp_path / "installed/scripts/programstart_authority_resolver.py"))
    bound = resolve_operationalization_binding(snapshot, matrix)
    assert bound.projection_ready
