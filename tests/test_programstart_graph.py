from __future__ import annotations

import pytest

from scripts.programstart_graph import (
    DEFAULT_IMPACT_TYPES,
    DependencyCycleError,
    DependencyGraph,
    GraphEdge,
)
from scripts.programstart_models import RelationRecord


def _relation(dependent: str, prerequisite: str, relation_type: str = "depends_on", source: str = "test") -> dict:
    return {
        "type": relation_type,
        "from": dependent,
        "to": prerequisite,
        "source": source,
    }


def test_graph_reads_context_relation_dicts_and_models() -> None:
    relations = [
        _relation("implementation", "architecture"),
        RelationRecord(type="depends_on", **{"from": "release", "to": "implementation", "source": "model"}),
    ]

    graph = DependencyGraph(relations)

    assert graph.dependencies("implementation") == ("architecture",)
    assert graph.dependencies("release") == ("implementation",)
    assert graph.dependents("implementation") == ("release",)
    assert graph.nodes == ("architecture", "implementation", "release")


def test_topological_order_places_prerequisites_before_dependents() -> None:
    graph = DependencyGraph(
        [
            _relation("implementation", "architecture"),
            _relation("architecture", "requirements"),
            _relation("release", "implementation"),
        ]
    )

    assert graph.topological_order() == ("requirements", "architecture", "implementation", "release")


def test_topological_order_is_deterministic_for_parallel_nodes() -> None:
    graph = DependencyGraph(
        [
            _relation("release", "api"),
            _relation("release", "web"),
        ]
    )

    assert graph.topological_order() == ("api", "web", "release")


def test_cycle_detection_reports_dependency_path() -> None:
    graph = DependencyGraph(
        [
            _relation("a", "b"),
            _relation("b", "c"),
            _relation("c", "a"),
        ]
    )

    assert graph.find_cycle() == ("a", "b", "c", "a")
    with pytest.raises(DependencyCycleError) as exc_info:
        graph.topological_order()

    assert exc_info.value.cycle == ("a", "b", "c", "a")
    assert "a -> b -> c -> a" in str(exc_info.value)


def test_non_dependency_relations_are_ignored_by_default() -> None:
    graph = DependencyGraph(
        [
            _relation("component", "architecture", "authority_dependency"),
            _relation("requirement", "owner", "canonical_owner"),
        ]
    )

    assert graph.nodes == ()


def test_impact_graph_can_include_authority_dependencies_explicitly() -> None:
    graph = DependencyGraph(
        [_relation("component", "architecture", "authority_dependency", source="sync-rule")],
        relation_types=DEFAULT_IMPACT_TYPES,
    )

    assert graph.dependencies("component") == ("architecture",)
    edge = graph.edges_between("component", "architecture")[0]
    assert edge.relation_type == "authority_dependency"
    assert edge.source == "sync-rule"


def test_eligibility_and_blockers_use_direct_prerequisites() -> None:
    graph = DependencyGraph(
        [
            _relation("implementation", "architecture"),
            _relation("implementation", "migration"),
        ]
    )

    assert graph.immediate_blockers("implementation", completed={"architecture"}) == ("migration",)
    assert not graph.is_eligible("implementation", completed={"architecture"})
    assert graph.is_eligible("implementation", completed={"architecture", "migration"})


def test_eligible_nodes_excludes_completed_work() -> None:
    graph = DependencyGraph(
        [
            _relation("implementation", "architecture"),
            _relation("release", "implementation"),
        ]
    )

    assert graph.eligible_nodes(completed={"architecture"}) == ("implementation",)


def test_dependent_paths_preserve_shortest_provenance() -> None:
    graph = DependencyGraph(
        [
            _relation("architecture", "requirements", source="architecture.md"),
            _relation("implementation", "architecture", source="work-packet"),
            _relation("release", "implementation", source="release-gate"),
        ]
    )

    paths = graph.dependent_paths("requirements")

    assert [path.end for path in paths] == ["architecture", "implementation", "release"]
    assert paths[-1].nodes == ("requirements", "architecture", "implementation", "release")
    assert [edge.source for edge in paths[-1].edges] == ["architecture.md", "work-packet", "release-gate"]


def test_bounded_traversal_limits_blast_radius_depth() -> None:
    graph = DependencyGraph(
        [
            _relation("architecture", "requirements"),
            _relation("implementation", "architecture"),
            _relation("release", "implementation"),
        ]
    )

    assert graph.transitive_dependents("requirements", max_depth=2) == ("architecture", "implementation")
    assert graph.transitive_dependencies("release", max_depth=1) == ("implementation",)
    assert graph.transitive_dependents("requirements", max_depth=0) == ()


def test_negative_max_depth_is_rejected() -> None:
    graph = DependencyGraph([_relation("implementation", "architecture")])

    with pytest.raises(ValueError, match="max_depth"):
        graph.dependent_paths("architecture", max_depth=-1)


def test_duplicate_edges_do_not_duplicate_dependencies() -> None:
    edge = GraphEdge("depends_on", "implementation", "architecture", "source-a")
    graph = DependencyGraph()
    graph.add_edge(edge)
    graph.add_edge(edge)

    assert graph.dependencies("implementation") == ("architecture",)
    assert graph.edges_between("implementation", "architecture") == (edge,)
