from __future__ import annotations

from typing import Any

TERMINAL_DISPOSITIONS = frozenset(
    {
        "CLOSED",
        "COMPLETE",
        "COMPLETED",
        "SATISFIED",
        "SUPERSEDED",
        "TERMINAL",
    }
)
ACTIONABLE_DISPOSITIONS = frozenset(
    {
        "OPEN",
        "IN_PROGRESS",
        "READY",
    }
)
MACHINE_EXECUTION_MODES = frozenset(
    {
        "BACKBONE",
        "EMULATED_BACKBONE",
    }
)


class RootFrontierError(ValueError):
    pass


def _task_index(db: dict[str, Any]) -> dict[str, dict[str, Any]]:
    if db.get("execution_authority") is not False:
        raise RootFrontierError("Matrix task database must not grant execution authority")
    tasks = db.get("tasks")
    if not isinstance(tasks, list):
        raise RootFrontierError("Matrix task database tasks must be a list")
    by_id: dict[str, dict[str, Any]] = {}
    for task in tasks:
        task_id = task.get("task_id") if isinstance(task, dict) else None
        if isinstance(task, dict) and task.get("execution_authority", False) is not False:
            raise RootFrontierError("task must not grant execution authority")
        if not isinstance(task_id, str) or not task_id:
            raise RootFrontierError("task_id is required")
        if task_id in by_id:
            raise RootFrontierError(f"duplicate task_id: {task_id}")
        by_id[task_id] = task
    return by_id


def _dependency_map(db: dict[str, Any], by_id: dict[str, dict[str, Any]]) -> dict[str, list[str]]:
    relations = db.get("relations", [])
    if not isinstance(relations, list):
        raise RootFrontierError("Matrix task database relations must be a list")
    deps = {task_id: [] for task_id in by_id}
    for relation in relations:
        if not isinstance(relation, dict) or relation.get("relation") != "DEPENDS_ON":
            continue
        source = relation.get("source")
        target = relation.get("target")
        if source not in by_id or target not in by_id:
            raise RootFrontierError("dangling DEPENDS_ON relation")
        if relation.get("field_class") != "OWNER_SOURCED":
            raise RootFrontierError("dependency graph must be owner-sourced")
        deps[source].append(target)
    for task_id in deps:
        deps[task_id].sort()
    return deps


def _is_terminal(task: dict[str, Any]) -> bool:
    return str(task.get("owner_disposition", "")).upper() in TERMINAL_DISPOSITIONS


def root_frontier(db: dict[str, Any], root_task_id: str) -> dict[str, Any]:
    """Return the deepest unresolved current leaf for one selected root.

    The result is derived routing evidence only. It never authorizes execution.
    """

    by_id = _task_index(db)
    if root_task_id not in by_id:
        raise RootFrontierError("selected root is absent from Matrix task database")
    deps = _dependency_map(db, by_id)

    reachable: set[str] = set()
    visiting: set[str] = set()
    visited: set[str] = set()

    def walk(task_id: str) -> None:
        if task_id in visiting:
            raise RootFrontierError("dependency cycle detected")
        if task_id in visited:
            return
        visiting.add(task_id)
        reachable.add(task_id)
        for target in deps[task_id]:
            walk(target)
        visiting.remove(task_id)
        visited.add(task_id)

    walk(root_task_id)

    unresolved = {task_id for task_id in reachable if not _is_terminal(by_id[task_id])}
    leaves: list[str] = []
    for task_id in sorted(unresolved):
        unresolved_dependencies = [target for target in deps[task_id] if target in unresolved]
        if not unresolved_dependencies:
            leaves.append(task_id)
    currentness_divergences = [task_id for task_id in leaves if by_id[task_id].get("currentness") != "CURRENT"]
    executable = [
        task_id
        for task_id in leaves
        if by_id[task_id].get("currentness") == "CURRENT"
        and by_id[task_id].get("execution_mode") in MACHINE_EXECUTION_MODES
        and str(by_id[task_id].get("owner_disposition", "")).upper() in ACTIONABLE_DISPOSITIONS
    ]
    human_gates = [
        task_id
        for task_id in leaves
        if by_id[task_id].get("currentness") == "CURRENT" and by_id[task_id].get("execution_mode") == "HUMAN_GATE"
    ]

    def applicable(task: dict[str, Any]) -> bool:
        proof = task.get("evidence_applicability")
        valid_proof = bool(
            isinstance(proof, dict)
            and proof.get("state") == "APPLICABLE"
            and proof.get("evidence_ref")
            and proof.get("source_ref")
            and proof.get("source_version")
            and proof.get("source_ref") == task.get("source_ref")
            and proof.get("source_version") == task.get("source_version")
        )
        if proof is not None and not valid_proof:
            return False
        return task.get("currentness") == "CURRENT" or (_is_terminal(task) and valid_proof)

    blocking = sorted(
        task_id
        for task_id in reachable
        if not applicable(by_id[task_id])
        or by_id[task_id].get("matrix_reconciliation", "RECONCILED") != "RECONCILED"
        or by_id[task_id].get("projection_role") == "REFERENCE_PLAN"
        or (
            ("projection_role" in by_id[task_id] or db.get("operationalization_scope") is True)
            and by_id[task_id].get("matrix_reconciliation") != "RECONCILED"
        )
    )
    if blocking:
        executable = []
    selected = executable[0] if len(executable) == 1 and not currentness_divergences else None
    return {
        "root_task_id": root_task_id,
        "readiness_blocker_ids": blocking,
        "reachable_task_ids": sorted(reachable),
        "unresolved_leaf_ids": leaves,
        "executable_leaf_ids": executable,
        "human_gate_ids": human_gates,
        "currentness_divergence_ids": currentness_divergences,
        "selected_task_id": selected,
        "selection_field_class": "DERIVED",
        "execution_authority": False,
    }
