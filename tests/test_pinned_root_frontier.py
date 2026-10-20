import copy
from typing import Any

import pytest

from scripts.matrix_projection_dependency.root_frontier import RootFrontierError, root_frontier


def minimal_graph() -> dict[str, Any]:
    return dict(
        execution_authority=False,
        tasks=[
            dict(
                task_id="root",
                owner_disposition="OPEN",
                currentness="CURRENT",
                execution_mode="BACKBONE",
                matrix_reconciliation="RECONCILED",
            )
        ],
        relations=[],
    )


def test_dependency_cannot_derive_owner_authority():
    graph = minimal_graph()
    graph["relations"] = [dict(source="root", target="root", relation="DEPENDS_ON", field_class="DERIVED")]
    with pytest.raises(RootFrontierError, match="owner-sourced"):
        root_frontier(graph, "root")


@pytest.mark.parametrize(
    "change,reason",
    [
        ("authority", "must not grant execution authority"),
        ("tasks", "tasks must be a list"),
        ("missing-id", "task_id is required"),
        ("relations", "relations must be a list"),
        ("dangling", "dangling DEPENDS_ON relation"),
        ("missing-root", "selected root is absent"),
    ],
)
def test_malformed_frontier_never_selects_work(change, reason):
    graph = minimal_graph()
    if change == "authority":
        graph["execution_authority"] = True
    elif change == "tasks":
        graph["tasks"] = {}
    elif change == "missing-id":
        graph["tasks"][0].pop("task_id")
    elif change == "relations":
        graph["relations"] = {}
    elif change == "dangling":
        graph["relations"] = [dict(source="root", target="missing", relation="DEPENDS_ON", field_class="OWNER_SOURCED")]
    else:
        graph["tasks"] = []
    with pytest.raises(RootFrontierError, match=reason):
        root_frontier(graph, "root")


def test_shared_dependencies_and_non_dependency_relations_do_not_duplicate_frontier():
    graph = minimal_graph()
    for name in ["branch", "leaf"]:
        task = copy.deepcopy(graph["tasks"][0])
        task["task_id"] = name
        graph["tasks"].append(task)
    graph["relations"] = [None, dict(relation="RELATED_TO")]
    for source, target in [("root", "branch"), ("root", "leaf"), ("branch", "leaf")]:
        graph["relations"].append(dict(source=source, target=target, relation="DEPENDS_ON", field_class="OWNER_SOURCED"))
    result = root_frontier(graph, "root")
    assert result["selected_task_id"] == "leaf"
    assert result["reachable_task_ids"] == ["branch", "leaf", "root"]
    assert result["unresolved_leaf_ids"] == ["leaf"]


@pytest.mark.parametrize(
    "proof",
    [
        {},
        {"state": "INVALIDATED"},
        dict(state="APPLICABLE", evidence_ref="owner#1", source_ref="foreign", source_version="1"),
    ],
)
def test_invalid_applicability_blocks_even_current_task(proof):
    graph = minimal_graph()
    graph["tasks"][0].update(source_ref="owner#1", source_version="1", evidence_applicability=proof)
    result = root_frontier(graph, "root")
    assert result["selected_task_id"] is None
    assert result["readiness_blocker_ids"] == ["root"]
