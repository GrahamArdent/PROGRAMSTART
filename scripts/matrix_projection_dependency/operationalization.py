"""Lossless, versioned projection of the PROGRAMSTART owner manifest contract.

Source acquisition/acceptance belongs to the caller's owner resolver. These pure
functions verify consistency and reconstruction; they never authenticate a caller.
"""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
from typing import Any

import jsonschema

from .root_frontier import root_frontier

SCHEMA_PATH = Path(__file__).with_name("decision-operationalization-manifest.schema.json")
SCHEMA = json.loads(SCHEMA_PATH.read_text())


def digest(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def _repository(ref: str) -> str:
    return ref.split("@", 1)[0].split("#", 1)[0].split(":", 1)[0]


def validate_manifest(manifest: dict[str, Any]) -> None:
    jsonschema.validate(manifest, SCHEMA)
    if manifest["contract_version"] != "1.0":
        raise ValueError("unsupported manifest contract version")
    for collection in ("obligations", "planned_steps", "gates", "falsifiers"):
        ids = [x["id"] for x in manifest[collection]]
        if len(ids) != len(set(ids)):
            raise ValueError(f"duplicate {collection} identity")
    obligations = {x["id"] for x in manifest["obligations"]}
    steps = {x["id"] for x in manifest["planned_steps"]}
    gates = {x["id"] for x in manifest["gates"]}
    if obligations & steps or (obligations | steps) & {"gate:" + key for key in gates}:
        raise ValueError("ambiguous material task identity across namespaces")
    visiting: set[str] = set()
    done: set[str] = set()
    by_id = {x["id"]: x for x in manifest["planned_steps"]}

    def visit(identity: str) -> None:
        if identity in visiting:
            raise ValueError("planned step dependency cycle")
        if identity in done:
            return
        visiting.add(identity)
        step = by_id[identity]
        if not set(step["outcome_supported"]) <= obligations or not set(step["gate_refs"]) <= gates:
            raise ValueError("dangling outcome or gate reference")
        for dependency in step["depends_on"]:
            if dependency not in steps:
                raise ValueError("dangling planned step dependency")
            visit(dependency)
        visiting.remove(identity)
        done.add(identity)

    for identity in steps:
        visit(identity)


def project_operationalization(
    manifest: dict[str, Any],
    *,
    source_owner: str,
    source_ref: str,
    source_version: str,
    readiness_graph: dict[str, Any],
    root_task_id: str,
    projection_identity: str,
) -> dict[str, Any]:
    validate_manifest(manifest)
    if (
        manifest["source_ref"] != source_ref
        or manifest["source_version"] != source_version
        or _repository(manifest["owner"]) != source_owner
        or _repository(source_ref) != source_owner
    ):
        raise ValueError("owner manifest/source identity mismatch")
    if not projection_identity.strip():
        raise ValueError("projection identity required")
    graph = copy.deepcopy(readiness_graph)
    graph["operationalization_scope"] = True
    graph["tasks"] = sorted(graph.get("tasks", []), key=lambda task: task["task_id"])
    relations = graph.get("relations", [])
    keys = [json.dumps(x, sort_keys=True, separators=(",", ":")) for x in relations]
    if len(keys) != len(set(keys)):
        raise ValueError("duplicate dependency relation")
    graph["relations"] = [json.loads(key) for key in sorted(keys)]
    tasks = {task["task_id"]: task for task in graph.get("tasks", [])}
    if (
        root_task_id not in tasks
        or tasks[root_task_id].get("source_ref") != source_ref
        or tasks[root_task_id].get("source_version") != source_version
    ):
        raise ValueError("readiness root does not bind the owner manifest")
    required_ids = {x["id"] for x in manifest["obligations"] + manifest["planned_steps"]}
    required_ids |= {"gate:" + x["id"] for x in manifest["gates"]}
    if root_task_id not in required_ids:
        raise ValueError("selected root is not a material owner-plan record")
    if not required_ids <= tasks.keys():
        raise ValueError("readiness graph omits material plan records")
    for identity in required_ids | {root_task_id}:
        task = tasks[identity]
        if task.get("projection_role") != manifest["projection_role"]:
            raise ValueError("material plan role is missing or inconsistent")
    edges = {(x["source"], x["target"]) for x in graph.get("relations", []) if x.get("relation") == "DEPENDS_ON"}
    required_edges = set()
    for step in manifest["planned_steps"]:
        required_edges.update((outcome, step["id"]) for outcome in step["outcome_supported"])
        required_edges.update((step["id"], target) for target in step["depends_on"])
        required_edges.update((step["id"], "gate:" + target) for target in step["gate_refs"])
    if not required_edges <= edges:
        raise ValueError("readiness graph omits material owner dependency")
    frontier = root_frontier(graph, root_task_id)
    artifact = {
        "artifact_version": "2.0",
        "artifact_type": "ecosystem_matrix.operationalization_projection",
        "execution_authority": False,
        "source_binding": {"owner": source_owner, "ref": source_ref, "version": source_version, "currentness": "CURRENT"},
        "projection_identity": projection_identity,
        "owner_manifest": copy.deepcopy(manifest),
        "readiness_graph": graph,
        "root_task_id": root_task_id,
        "frontier": frontier,
        "matrix_bookkeeping": {
            "projection_currentness": "CURRENT",
            "ingestion_reconciliation_state": "RECONCILED",
            "reconsideration_required": False,
        },
    }
    artifact["semantic_hash"] = digest({k: artifact[k] for k in ("owner_manifest", "readiness_graph", "root_task_id")})
    return artifact


def reconstruct_operationalization(artifact: dict[str, Any]) -> dict[str, Any]:
    if (
        artifact.get("artifact_version") != "2.0"
        or artifact.get("artifact_type") != "ecosystem_matrix.operationalization_projection"
        or artifact.get("execution_authority") is not False
    ):
        raise ValueError("comprehensive non-authoritative projection required")
    source = artifact["source_binding"]
    rebuilt = project_operationalization(
        artifact["owner_manifest"],
        source_owner=source["owner"],
        source_ref=source["ref"],
        source_version=source["version"],
        readiness_graph=artifact["readiness_graph"],
        root_task_id=artifact["root_task_id"],
        projection_identity=artifact["projection_identity"],
    )
    if rebuilt != artifact:
        raise ValueError("projection content/currentness/frontier/hash inconsistent")
    return copy.deepcopy(artifact["owner_manifest"])


def reconstruction_receipt(artifact: dict[str, Any]) -> dict[str, Any]:
    recovered = reconstruct_operationalization(artifact)
    return {
        "record_type": "matrix.operationalization_reconstruction.v1",
        "execution_authority": False,
        "projection_sha256": digest(artifact),
        "reconstructed_manifest": recovered,
        "reconstructed_manifest_sha256": digest(recovered),
    }


def reconcile_operationalization(prior: dict[str, Any], manifest: dict[str, Any], **inputs: Any) -> dict[str, Any]:
    reconstruct_operationalization(prior)
    candidate = project_operationalization(manifest, **inputs)
    if (
        prior["source_binding"]["owner"] != candidate["source_binding"]["owner"]
        or prior["source_binding"]["ref"] != candidate["source_binding"]["ref"]
    ):
        raise ValueError("projection source substitution")
    if prior["source_binding"]["version"] == candidate["source_binding"]["version"] and prior != candidate:
        raise ValueError("conflicting same-version projection content")
    return candidate
