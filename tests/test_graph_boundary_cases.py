"""Public graph behavior for subsets, merges, cycles and bounded traversal."""

from types import SimpleNamespace

import pytest

from scripts.programstart_graph import DependencyCycleError, DependencyGraph, GraphEdge


def edge(source, target):
    return {"type": "depends_on", "from": source, "to": target, "source": "owner:graph"}


def test_empty_cycle_and_object_relation_provenance():
    assert "unknown cycle" in str(DependencyCycleError([]))
    relation = SimpleNamespace(type="depends_on", from_="a", to="b", source="owner#1")
    assert GraphEdge.from_relation(relation).source == "owner#1"
    graph = DependencyGraph()
    assert graph.topological_order() == ()
    assert graph.find_cycle() == ()


def test_invalid_and_duplicate_edges_never_create_phantom_neighbors():
    valid = edge("a", "b")
    graph = DependencyGraph([valid, valid, {"type": "related_to", "from": "x", "to": "y"}, edge("", "b")])
    assert graph.nodes == ("a", "b")
    assert graph.dependencies("a") == ("b",)
    assert len(graph.edges_between("a", "b")) == 1
    assert graph.transitive_dependencies("a") == ("b",)
    graph.add_edge(GraphEdge("related_to", "x", "y"))
    graph.add_edge(GraphEdge("depends_on", "", "b"))
    assert graph.nodes == ("a", "b")


def test_subset_order_ignores_unselected_dependent_and_cycle_edges():
    graph = DependencyGraph([edge("a", "b"), edge("c", "b"), edge("a", "c")])
    assert graph.topological_order(["b", "c"]) == ("b", "c")
    assert graph.find_cycle(nodes=["a"]) == ()
    assert graph.find_cycle() == ()


def test_diamond_and_cycle_have_bounded_deterministic_paths():
    graph = DependencyGraph([edge("a", "b"), edge("a", "c"), edge("b", "d"), edge("c", "d"), edge("d", "a")])
    assert graph.transitive_dependencies("a", max_depth=0) == ()
    assert graph.transitive_dependencies("a", max_depth=1) == ("b", "c")
    assert graph.transitive_dependents("d", max_depth=1) == ("b", "c")
    paths = graph.dependency_paths("a")
    assert [p.end for p in paths] == ["b", "c", "d"]
    assert paths[-1].start == "a"
    with pytest.raises(ValueError, match="non-negative"):
        graph.dependent_paths("a", max_depth=-1)
    assert graph.find_cycle() == ("a", "b", "d", "a")
