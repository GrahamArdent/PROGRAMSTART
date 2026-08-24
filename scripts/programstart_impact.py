from __future__ import annotations

# ruff: noqa: I001

import argparse
import json
from pathlib import Path
from typing import Any

try:
    from .programstart_common import warn_direct_script_invocation, workspace_path
    from .programstart_context import build_context_index, cached_index_is_compatible, default_index_path, query_context_index
    from .programstart_graph import DEFAULT_IMPACT_TYPES, DependencyGraph, GraphPath
except ImportError:  # pragma: no cover - standalone script execution fallback
    from programstart_common import workspace_path, warn_direct_script_invocation
    from programstart_context import (
        build_context_index,
        cached_index_is_compatible,
        default_index_path,
        query_context_index,
    )
    from programstart_graph import DEFAULT_IMPACT_TYPES, DependencyGraph, GraphPath


def load_index(index_path: str | None) -> dict[str, Any]:
    path = Path(index_path) if index_path else default_index_path()
    if not path.is_absolute():
        path = workspace_path(str(path))
    if path.exists():
        index = json.loads(path.read_text(encoding="utf-8"))
        if cached_index_is_compatible(index):
            return index
    return build_context_index()


def _path_payload(path: GraphPath) -> dict[str, Any]:
    return {
        "node": path.end,
        "depth": path.depth,
        "path": list(path.nodes),
        "edges": [
            {
                "type": edge.relation_type,
                "from": edge.dependent,
                "to": edge.prerequisite,
                "source": edge.source,
            }
            for edge in path.edges
        ],
    }


def resolve_blast_radius_starts(
    graph: DependencyGraph,
    target: str,
    related_result: dict[str, Any],
) -> tuple[str, ...]:
    """Resolve an impact target to existing graph nodes without inventing edges.

    Exact graph-node matches win. Otherwise, use graph nodes surfaced by the existing
    impact query plus graph-node substring matches. This keeps the old fuzzy discovery
    behavior for navigation while dependency propagation itself remains deterministic.
    """
    needle = target.strip().lower()
    if not needle:
        return ()

    exact = tuple(node for node in graph.nodes if node.lower() == needle)
    if exact:
        return exact

    graph_nodes = set(graph.nodes)
    candidates: set[str] = set()

    for item in related_result.get("documents", []):
        path = str(item.get("path", ""))
        if path in graph_nodes:
            candidates.add(path)

    for item in related_result.get("concerns", []):
        for value in (
            str(item.get("concern", "")),
            str(item.get("owner_file", "")),
            *(str(entry) for entry in item.get("supporting_files", [])),
        ):
            if value in graph_nodes:
                candidates.add(value)

    candidates.update(node for node in graph.nodes if needle in node.lower())
    return tuple(sorted(candidates))


def build_blast_radius(
    index: dict[str, Any],
    target: str,
    related_result: dict[str, Any],
    *,
    max_depth: int | None = None,
) -> dict[str, Any]:
    """Return deterministic downstream dependency paths for the resolved target.

    Only explicit dependency relation types participate. Semantic retrieval matches,
    KB relationships, routes, and other loose associations remain discovery evidence
    and are never promoted into dependency edges by this function.
    """
    graph = DependencyGraph(index.get("relations", []), relation_types=DEFAULT_IMPACT_TYPES)
    starts = resolve_blast_radius_starts(graph, target, related_result)

    best_by_node: dict[str, GraphPath] = {}
    for start in starts:
        for path in graph.dependent_paths(start, max_depth=max_depth):
            current = best_by_node.get(path.end)
            if current is None or (path.depth, path.nodes) < (current.depth, current.nodes):
                best_by_node[path.end] = path

    ordered_paths = sorted(best_by_node.values(), key=lambda item: (item.depth, item.nodes))
    return {
        "start_nodes": list(starts),
        "relation_types": sorted(DEFAULT_IMPACT_TYPES),
        "max_depth": max_depth,
        "affected": [_path_payload(path) for path in ordered_paths],
    }


def print_impact_summary(target: str, result: dict[str, Any]) -> None:
    print(f"Impact summary for: {target}")
    print(f"- documents: {len(result.get('documents', []))}")
    print(f"- concerns: {len(result.get('concerns', []))}")
    print(f"- relations: {len(result.get('relations', []))}")
    print(f"- routes: {len(result.get('routes', []))}")
    print(f"- cli commands: {len(result.get('cli', []))}")
    print(f"- dashboard commands: {len(result.get('dashboard', []))}")
    print(f"- stacks: {len(result.get('stacks', []))}")
    print(f"- integration patterns: {len(result.get('integration_patterns', []))}")
    print(f"- decision rules: {len(result.get('decision_rules', []))}")
    print(f"- KB relationships: {len(result.get('relationships', []))}")
    print(f"- comparisons: {len(result.get('comparisons', []))}")

    blast_radius = result.get("blast_radius", {})
    affected = blast_radius.get("affected", []) if isinstance(blast_radius, dict) else []
    if isinstance(blast_radius, dict):
        print(f"- graph start nodes: {len(blast_radius.get('start_nodes', []))}")
        print(f"- dependency blast radius: {len(affected)}")

    if result.get("documents"):
        print("- related documents:")
        for item in result["documents"][:10]:
            print(f"  - {item['path']}")
    if result.get("concerns"):
        print("- related concerns:")
        for item in result["concerns"][:10]:
            print(f"  - {item['concern']} -> {item['owner_file']}")
    if result.get("relations"):
        print("- first relations:")
        for item in result["relations"][:10]:
            print(f"  - {item['type']}: {item['from']} -> {item['to']}")
    if affected:
        print("- dependency blast-radius paths:")
        for item in affected[:10]:
            print(f"  - depth {item['depth']}: {' -> '.join(item['path'])}")
    if result.get("decision_rules"):
        print("- decision rules:")
        for item in result["decision_rules"][:5]:
            print(f"  - {item['title']}")
    if result.get("relationships"):
        print("- KB relationships:")
        for item in result["relationships"][:5]:
            print(f"  - {item['subject']} {item['relation']} {item['object']}")
    if result.get("comparisons"):
        print("- comparisons:")
        for item in result["comparisons"][:5]:
            print(f"  - {item['name']}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Show the likely impact surface for a file, concern, route, or keyword.")
    parser.add_argument("target", help="Target file path, concern, route fragment, or keyword.")
    parser.add_argument("--index", default=None, help="Existing context index path.")
    parser.add_argument(
        "--max-depth",
        type=int,
        default=None,
        help="Optional maximum dependency traversal depth. Defaults to the full reachable dependency graph.",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of text.")
    args = parser.parse_args(argv)

    if args.max_depth is not None and args.max_depth < 0:
        parser.error("--max-depth must be non-negative")

    index = load_index(args.index)
    result = query_context_index(
        index,
        concern=None,
        file_path=None,
        command=None,
        route=None,
        stack=None,
        capability=None,
        impact=args.target,
    )
    result["blast_radius"] = build_blast_radius(index, args.target, result, max_depth=args.max_depth)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print_impact_summary(args.target, result)
    return 0


if __name__ == "__main__":  # pragma: no cover
    warn_direct_script_invocation("'uv run programstart impact <target>' or 'pb impact <target>'")
    raise SystemExit(main())
