from __future__ import annotations

from collections import defaultdict, deque
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from heapq import heapify, heappop, heappush
from typing import Any

DEFAULT_DEPENDENCY_TYPES = frozenset({"depends_on"})
DEFAULT_IMPACT_TYPES = frozenset({"depends_on", "authority_dependency"})


class DependencyCycleError(ValueError):
    """Raised when a dependency graph cannot be topologically ordered."""

    def __init__(self, cycle: Iterable[str]) -> None:
        self.cycle = tuple(cycle)
        rendered = " -> ".join(self.cycle) if self.cycle else "unknown cycle"
        super().__init__(f"Dependency cycle detected: {rendered}")


@dataclass(frozen=True, slots=True)
class GraphEdge:
    """One typed relation stored as dependent -> prerequisite.

    PROGRAMSTART context relations already use this direction for ``depends_on`` and
    ``authority_dependency``. Keeping the storage direction unchanged avoids a second
    source of truth; reverse adjacency is built internally for downstream impact.
    """

    relation_type: str
    dependent: str
    prerequisite: str
    source: str = ""

    @classmethod
    def from_relation(cls, relation: Mapping[str, Any] | object) -> GraphEdge:
        """Create an edge from a context-index relation dict or RelationRecord-like object."""
        if isinstance(relation, Mapping):
            relation_type = str(relation.get("type", ""))
            dependent = str(relation.get("from", relation.get("from_", "")))
            prerequisite = str(relation.get("to", ""))
            source = str(relation.get("source", ""))
        else:
            relation_type = str(getattr(relation, "type", ""))
            dependent = str(getattr(relation, "from_", getattr(relation, "from", "")))
            prerequisite = str(getattr(relation, "to", ""))
            source = str(getattr(relation, "source", ""))
        return cls(
            relation_type=relation_type,
            dependent=dependent,
            prerequisite=prerequisite,
            source=source,
        )


@dataclass(frozen=True, slots=True)
class GraphPath:
    """A provenance-preserving path through dependency relations."""

    nodes: tuple[str, ...]
    edges: tuple[GraphEdge, ...]

    @property
    def depth(self) -> int:
        return len(self.edges)

    @property
    def start(self) -> str:
        return self.nodes[0]

    @property
    def end(self) -> str:
        return self.nodes[-1]


class DependencyGraph:
    """Deterministic dependency/impact graph over existing PROGRAMSTART relations.

    Stored relation direction is ``dependent -> prerequisite``. Public helpers name
    both directions explicitly so callers do not need to remember that convention:

    - ``dependencies(node)`` returns direct prerequisites.
    - ``dependents(node)`` returns nodes directly affected by that prerequisite.
    - ``topological_order()`` returns prerequisites before their dependents.
    - ``dependent_paths()`` walks downstream impact and preserves relation provenance.
    """

    def __init__(
        self,
        relations: Iterable[Mapping[str, Any] | object] = (),
        *,
        relation_types: Iterable[str] = DEFAULT_DEPENDENCY_TYPES,
    ) -> None:
        self.relation_types = frozenset(relation_types)
        self._dependencies: dict[str, set[str]] = defaultdict(set)
        self._dependents: dict[str, set[str]] = defaultdict(set)
        self._edges_by_pair: dict[tuple[str, str], list[GraphEdge]] = defaultdict(list)
        self._nodes: set[str] = set()

        for relation in relations:
            edge = GraphEdge.from_relation(relation)
            if edge.relation_type not in self.relation_types:
                continue
            if not edge.dependent or not edge.prerequisite:
                continue
            self.add_edge(edge)

    def add_edge(self, edge: GraphEdge) -> None:
        """Add a typed edge when it belongs to this graph's configured relation types."""
        if edge.relation_type not in self.relation_types:
            return
        if not edge.dependent or not edge.prerequisite:
            return
        self._nodes.update((edge.dependent, edge.prerequisite))
        self._dependencies[edge.dependent].add(edge.prerequisite)
        self._dependents[edge.prerequisite].add(edge.dependent)
        pair = (edge.dependent, edge.prerequisite)
        if edge not in self._edges_by_pair[pair]:
            self._edges_by_pair[pair].append(edge)
            self._edges_by_pair[pair].sort(key=lambda item: (item.relation_type, item.source))

    @property
    def nodes(self) -> tuple[str, ...]:
        return tuple(sorted(self._nodes))

    def dependencies(self, node: str) -> tuple[str, ...]:
        """Return direct prerequisites of ``node`` in deterministic order."""
        return tuple(sorted(self._dependencies.get(node, set())))

    def dependents(self, node: str) -> tuple[str, ...]:
        """Return direct downstream dependents of ``node`` in deterministic order."""
        return tuple(sorted(self._dependents.get(node, set())))

    def edges_between(self, dependent: str, prerequisite: str) -> tuple[GraphEdge, ...]:
        return tuple(self._edges_by_pair.get((dependent, prerequisite), ()))

    def immediate_blockers(self, node: str, *, completed: Iterable[str]) -> tuple[str, ...]:
        """Return direct prerequisites that have not been completed."""
        completed_set = set(completed)
        return tuple(dependency for dependency in self.dependencies(node) if dependency not in completed_set)

    def is_eligible(self, node: str, *, completed: Iterable[str]) -> bool:
        """Return whether every direct prerequisite of ``node`` is completed."""
        return not self.immediate_blockers(node, completed=completed)

    def eligible_nodes(self, *, completed: Iterable[str]) -> tuple[str, ...]:
        """Return incomplete graph nodes whose direct prerequisites are complete."""
        completed_set = set(completed)
        return tuple(
            node
            for node in self.nodes
            if node not in completed_set and self.is_eligible(node, completed=completed_set)
        )

    def topological_order(self, nodes: Iterable[str] | None = None) -> tuple[str, ...]:
        """Return a stable prerequisite-before-dependent order or raise with a cycle path."""
        selected = set(nodes) if nodes is not None else set(self._nodes)
        if not selected:
            return ()

        indegree = {
            node: sum(1 for prerequisite in self._dependencies.get(node, set()) if prerequisite in selected)
            for node in selected
        }
        ready = [node for node, degree in indegree.items() if degree == 0]
        heapify(ready)
        ordered: list[str] = []

        while ready:
            prerequisite = heappop(ready)
            ordered.append(prerequisite)
            for dependent in sorted(self._dependents.get(prerequisite, set())):
                if dependent not in selected:
                    continue
                indegree[dependent] -= 1
                if indegree[dependent] == 0:
                    heappush(ready, dependent)

        if len(ordered) != len(selected):
            cycle = self.find_cycle(nodes=selected)
            raise DependencyCycleError(cycle)
        return tuple(ordered)

    def find_cycle(self, *, nodes: Iterable[str] | None = None) -> tuple[str, ...]:
        """Return one deterministic dependency-direction cycle, including its repeated start node."""
        selected = set(nodes) if nodes is not None else set(self._nodes)
        state: dict[str, int] = {}
        stack: list[str] = []
        stack_index: dict[str, int] = {}

        def visit(node: str) -> tuple[str, ...]:
            state[node] = 1
            stack_index[node] = len(stack)
            stack.append(node)
            for prerequisite in sorted(self._dependencies.get(node, set())):
                if prerequisite not in selected:
                    continue
                status = state.get(prerequisite, 0)
                if status == 0:
                    cycle = visit(prerequisite)
                    if cycle:
                        return cycle
                elif status == 1:
                    start = stack_index[prerequisite]
                    return tuple(stack[start:] + [prerequisite])
            stack.pop()
            stack_index.pop(node, None)
            state[node] = 2
            return ()

        for node in sorted(selected):
            if state.get(node, 0) != 0:
                continue
            cycle = visit(node)
            if cycle:
                return cycle
        return ()

    def dependency_paths(self, start: str, *, max_depth: int | None = None) -> tuple[GraphPath, ...]:
        """Return shortest upstream paths from ``start`` to each reachable prerequisite."""
        return self._walk_paths(start, downstream=False, max_depth=max_depth)

    def dependent_paths(self, start: str, *, max_depth: int | None = None) -> tuple[GraphPath, ...]:
        """Return shortest downstream paths from ``start`` to each affected dependent."""
        return self._walk_paths(start, downstream=True, max_depth=max_depth)

    def transitive_dependencies(self, start: str, *, max_depth: int | None = None) -> tuple[str, ...]:
        return tuple(path.end for path in self.dependency_paths(start, max_depth=max_depth))

    def transitive_dependents(self, start: str, *, max_depth: int | None = None) -> tuple[str, ...]:
        return tuple(path.end for path in self.dependent_paths(start, max_depth=max_depth))

    def _walk_paths(self, start: str, *, downstream: bool, max_depth: int | None) -> tuple[GraphPath, ...]:
        if max_depth is not None and max_depth < 0:
            raise ValueError("max_depth must be non-negative or None")
        if max_depth == 0:
            return ()

        queue: deque[GraphPath] = deque([GraphPath(nodes=(start,), edges=())])
        visited = {start}
        paths: list[GraphPath] = []

        while queue:
            path = queue.popleft()
            if max_depth is not None and path.depth >= max_depth:
                continue
            current = path.end
            neighbors = self.dependents(current) if downstream else self.dependencies(current)
            for neighbor in neighbors:
                if neighbor in visited:
                    continue
                if downstream:
                    candidate_edges = self.edges_between(neighbor, current)
                else:
                    candidate_edges = self.edges_between(current, neighbor)
                if not candidate_edges:
                    continue
                edge = candidate_edges[0]
                next_path = GraphPath(nodes=path.nodes + (neighbor,), edges=path.edges + (edge,))
                visited.add(neighbor)
                paths.append(next_path)
                queue.append(next_path)

        paths.sort(key=lambda item: (item.depth, item.nodes))
        return tuple(paths)
