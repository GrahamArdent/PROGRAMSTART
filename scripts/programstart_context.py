from __future__ import annotations

# ruff: noqa: I001

import argparse
import functools
import json
import re
from pathlib import Path
from typing import Any

try:
    from .programstart_command_registry import CLI_COMMANDS, dashboard_allowed_commands
    from .programstart_common import (
        generated_outputs_root,
        load_registry,
        load_workflow_state,
        metadata_value,
        parse_markdown_table,
        warn_direct_script_invocation,
        workspace_path,
        write_json,
    )
    from .programstart_models import ContextIndex, KnowledgeBase
except ImportError:  # pragma: no cover - standalone script execution fallback
    from programstart_command_registry import CLI_COMMANDS, dashboard_allowed_commands
    from programstart_common import (
        generated_outputs_root,
        load_registry,
        load_workflow_state,
        metadata_value,
        parse_markdown_table,
        warn_direct_script_invocation,
        workspace_path,
        write_json,
    )
    from programstart_models import ContextIndex, KnowledgeBase


GET_ROUTE_RE = re.compile(r'parsed\.path\s+==\s+"([^"]+)"')
POST_ROUTE_RE = re.compile(r'parsed\.path\s+==\s+"([^"]+)"')


def _compute_index_version() -> str:
    """Derive a short version tag from the build_context_index schema shape.

    Uses today's date so the version advances whenever the code is deployed,
    avoiding stale hard-coded date strings (KB-1).
    """
    from datetime import date, timezone, datetime

    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def default_index_path() -> Path:
    return generated_outputs_root() / "context" / "context-index.json"


def split_metadata_list(value: str | None) -> list[str]:
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


def markdown_title(text: str) -> str:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            return stripped.lstrip("#").strip()
    return ""


def markdown_headings(text: str) -> list[str]:
    headings: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("##"):
            headings.append(stripped.lstrip("#").strip())
    return headings


def clean_markdown_cell(value: str) -> str:
    return value.strip().strip("`")


def relative_workspace_path(path: Path) -> str:
    return path.relative_to(workspace_path(".")).as_posix()


def document_record(relative_path: str) -> dict[str, Any] | None:
    path = workspace_path(relative_path)
    if not path.exists() or path.suffix.lower() != ".md":
        return None

    text = path.read_text(encoding="utf-8")
    return {
        "path": relative_path,
        "title": markdown_title(text),
        "purpose": metadata_value(text, "Purpose:"),
        "owner": metadata_value(text, "Owner:"),
        "last_updated": metadata_value(text, "Last updated:"),
        "depends_on": split_metadata_list(metadata_value(text, "Depends on:")),
        "authority": metadata_value(text, "Authority:"),
        "headings": markdown_headings(text),
    }


def extract_documents(registry: dict[str, Any]) -> list[dict[str, Any]]:
    candidates: set[str] = {
        str(registry["workspace"].get("root_readme", "README.md")),
        "PROGRAMBUILD/PROGRAMBUILD_CANONICAL.md",
        "PROGRAMBUILD/PROGRAMBUILD_FILE_INDEX.md",
        "USERJOURNEY/README.md",
        "USERJOURNEY/DELIVERY_GAMEPLAN.md",
        "USERJOURNEY/ROUTE_AND_STATE_FREEZE.md",
        "USERJOURNEY/STATES_AND_RULES.md",
        "USERJOURNEY/REUSE_STRATEGY.md",
        "docs/workflow-model.md",
        "docs/dashboard-api.md",
        "docs/knowledge-base.md",
        "docs/reusable-patterns.md",
        "docs/defaults-review.md",
    }
    docs_root = workspace_path("docs")
    if docs_root.exists():
        for path in docs_root.rglob("*.md"):
            candidates.add(relative_workspace_path(path))
    for relative_path in registry["systems"]["programbuild"]["control_files"]:
        if str(relative_path).endswith(".md"):
            candidates.add(str(relative_path))
    for relative_path in registry["systems"]["programbuild"]["output_files"]:
        if str(relative_path).endswith(".md"):
            candidates.add(str(relative_path))
    for relative_path in registry["systems"]["userjourney"]["core_files"]:
        if str(relative_path).endswith(".md"):
            candidates.add(str(relative_path))

    records = [document_record(relative_path) for relative_path in sorted(candidates)]
    return [record for record in records if record is not None]


@functools.lru_cache(maxsize=1)
def load_knowledge_base() -> dict[str, Any]:
    knowledge_base_path = workspace_path("config/knowledge-base.json")
    payload = json.loads(knowledge_base_path.read_text(encoding="utf-8"))
    retrieval_guidance = dict(payload.get("retrieval_guidance", {}))
    if not payload.get("prompt_engineering_guidance") and retrieval_guidance.get("prompt_engineering_guidance"):
        payload["prompt_engineering_guidance"] = retrieval_guidance.get("prompt_engineering_guidance", {})
    return KnowledgeBase.model_validate(payload).model_dump()


def extract_programbuild_concerns() -> list[dict[str, Any]]:
    text = workspace_path("PROGRAMBUILD/PROGRAMBUILD_CANONICAL.md").read_text(encoding="utf-8")
    rows = parse_markdown_table(text, "3. Authority Map")
    concerns: list[dict[str, Any]] = []
    for row in rows:
        concerns.append(
            {
                "system": "programbuild",
                "concern": clean_markdown_cell(row.get("Concern", "")),
                "owner_file": clean_markdown_cell(row.get("Canonical file", "")),
                "supporting_files": [],
                "source": "PROGRAMBUILD/PROGRAMBUILD_CANONICAL.md",
                "relation": "canonical_owner",
            }
        )
    return concerns


def extract_userjourney_concerns() -> list[dict[str, Any]]:
    delivery_gameplan_path = workspace_path("USERJOURNEY/DELIVERY_GAMEPLAN.md")
    if not delivery_gameplan_path.exists():
        return []

    text = delivery_gameplan_path.read_text(encoding="utf-8")
    rows = parse_markdown_table(text, "Source Of Truth Matrix")
    concerns: list[dict[str, Any]] = []
    for row in rows:
        concerns.append(
            {
                "system": "userjourney",
                "concern": clean_markdown_cell(row.get("Concern", "")),
                "owner_file": clean_markdown_cell(row.get("Source Of Truth", "")),
                "supporting_files": [
                    clean_markdown_cell(item) for item in row.get("Supporting Files", "").split(",") if item.strip()
                ],
                "source": "USERJOURNEY/DELIVERY_GAMEPLAN.md",
                "relation": "source_of_truth",
            }
        )
    return concerns


def extract_dashboard_routes() -> list[dict[str, str]]:
    text = workspace_path("scripts/programstart_serve.py").read_text(encoding="utf-8")
    routes: list[dict[str, str]] = [
        {"method": "GET", "path": "/", "purpose": "Dashboard HTML shell"},
        {"method": "GET", "path": "/index.html", "purpose": "Dashboard HTML shell"},
    ]
    route_purposes = {
        "/api/state": "Dashboard state payload",
        "/api/doc": "Workspace document preview",
        "/api/uj-phase": "Update USERJOURNEY implementation-tracker phase",
        "/api/uj-slice": "Update USERJOURNEY implementation-tracker slice",
        "/api/workflow-signoff": "Save workflow signoff metadata",
        "/api/workflow-advance": "Advance workflow with signoff",
        "/api/bootstrap": "Run validated bootstrap flow",
        "/api/run": "Run whitelisted dashboard command",
    }

    get_block = text.split("def do_GET", maxsplit=1)[1].split("def do_POST", maxsplit=1)[0]
    for route in sorted(set(GET_ROUTE_RE.findall(get_block))):
        routes.append({"method": "GET", "path": route, "purpose": route_purposes.get(route, "Internal dashboard route")})

    post_block = text.split("def do_POST", maxsplit=1)[1].split("def main", maxsplit=1)[0]
    for route in sorted(set(POST_ROUTE_RE.findall(post_block))):
        routes.append({"method": "POST", "path": route, "purpose": route_purposes.get(route, "Internal dashboard route")})

    seen: set[tuple[str, str]] = set()
    deduped: list[dict[str, str]] = []
    for route in routes:
        key = (route["method"], route["path"])
        if key in seen:
            continue
        seen.add(key)
        deduped.append(route)
    return deduped


def build_relations(
    documents: list[dict[str, Any]],
    concerns: list[dict[str, Any]],
    registry: dict[str, Any],
) -> list[dict[str, str]]:
    relations: list[dict[str, str]] = []
    for document in documents:
        for dependency in document["depends_on"]:
            relations.append(
                {
                    "type": "depends_on",
                    "from": document["path"],
                    "to": dependency,
                    "source": document["path"],
                }
            )
    for concern in concerns:
        relations.append(
            {
                "type": concern["relation"],
                "from": concern["concern"],
                "to": concern["owner_file"],
                "source": concern["source"],
            }
        )
    for sync_rule in registry.get("sync_rules", []):
        for dependent in sync_rule.get("dependent_files", []):
            for authority in sync_rule.get("authority_files", []):
                relations.append(
                    {
                        "type": "authority_dependency",
                        "from": str(dependent),
                        "to": str(authority),
                        "source": str(sync_rule.get("name", "sync_rule")),
                    }
                )
    return relations


def build_context_index() -> dict[str, Any]:
    registry = load_registry()
    documents = extract_documents(registry)
    concerns = extract_programbuild_concerns() + extract_userjourney_concerns()
    dashboard_commands = sorted(dashboard_allowed_commands("python", workspace_path("scripts")).keys())
    knowledge_base = load_knowledge_base()

    return {
        "version": _compute_index_version(),
        "workspace": {
            "name": registry["workspace"]["name"],
            "description": registry["workspace"]["description"],
            "root_readme": registry["workspace"]["root_readme"],
            "generated_outputs_root": registry["workspace"].get("generated_outputs_root", "outputs"),
        },
        "systems": registry["systems"],
        "runtime": {
            "programbuild": load_workflow_state(registry, "programbuild"),
            "userjourney_attached": workspace_path(registry["systems"]["userjourney"]["root"]).exists(),
            "userjourney": load_workflow_state(registry, "userjourney")
            if workspace_path(registry["systems"]["userjourney"]["root"]).exists()
            else None,
        },
        "documents": documents,
        "knowledge_base": knowledge_base,
        "concerns": concerns,
        "commands": {
            "cli": list(CLI_COMMANDS),
            "dashboard": dashboard_commands,
        },
        "routes": extract_dashboard_routes(),
        "relations": build_relations(documents, concerns, registry),
    }


def find_file(index: dict[str, Any], file_path: str) -> dict[str, Any]:
    needle = file_path.lower()
    documents = [doc for doc in index["documents"] if needle in doc["path"].lower()]
    relations = [
        relation for relation in index["relations"] if needle in relation["from"].lower() or needle in relation["to"].lower()
    ]
    concerns = [
        concern
        for concern in index["concerns"]
        if needle in concern["owner_file"].lower() or any(needle in item.lower() for item in concern["supporting_files"])
    ]
    return {"documents": documents, "relations": relations, "concerns": concerns}


def matches_kb_text(needle: str, *values: Any) -> bool:
    normalized_needle = needle.replace("-", " ").replace("_", " ")
    needle_tokens = [token for token in normalized_needle.split() if token]

    def matches_text(value: str) -> bool:
        normalized_value = value.lower().replace("-", " ").replace("_", " ")
        return (
            needle in value.lower()
            or normalized_needle in normalized_value
            or all(token in normalized_value for token in needle_tokens)
        )

    for value in values:
        if isinstance(value, str):
            if matches_text(value):
                return True
        if isinstance(value, list) and any(isinstance(item, str) and matches_text(item) for item in value):
            return True
    return False


def stack_relationships(knowledge_base: dict[str, Any], stack_matches: list[dict[str, Any]]) -> list[dict[str, Any]]:
    matched_names = {item["name"].lower() for item in stack_matches}
    matched_aliases = {alias.lower() for item in stack_matches for alias in item.get("aliases", [])}
    needles = matched_names | matched_aliases
    return [
        item
        for item in knowledge_base.get("relationships", [])
        if item.get("subject", "").lower() in needles or item.get("object", "").lower() in needles
    ]


def stack_comparisons(knowledge_base: dict[str, Any], stack_matches: list[dict[str, Any]]) -> list[dict[str, Any]]:
    names = {item["name"].lower() for item in stack_matches}
    aliases = {alias.lower() for item in stack_matches for alias in item.get("aliases", [])}
    needles = names | aliases
    return [
        item
        for item in knowledge_base.get("comparisons", [])
        if any(related.lower() in needles for related in item.get("related_items", []))
    ]


def query_context_index(
    index: dict[str, Any],
    *,
    concern: str | None,
    file_path: str | None,
    command: str | None,
    route: str | None,
    stack: str | None,
    capability: str | None,
    impact: str | None,
) -> dict[str, Any]:
    if concern:
        needle = concern.lower()
        return {
            "concerns": [item for item in index["concerns"] if needle in item["concern"].lower()],
            "relations": [item for item in index["relations"] if needle in item["from"].lower()],
        }
    if file_path:
        return find_file(index, file_path)
    if command:
        needle = command.lower()
        return {
            "cli": [item for item in index["commands"]["cli"] if needle in item.lower()],
            "dashboard": [item for item in index["commands"]["dashboard"] if needle in item.lower()],
        }
    if route:
        needle = route.lower()
        return {"routes": [item for item in index["routes"] if needle in item["path"].lower()]}
    if stack:
        needle = stack.lower()
        knowledge_base = index["knowledge_base"]
        stacks = [
            item
            for item in knowledge_base["stacks"]
            if needle in item["name"].lower() or any(needle in alias.lower() for alias in item.get("aliases", []))
        ]
        patterns = [
            item
            for item in knowledge_base["integration_patterns"]
            if any(
                any(component.lower() == stack_item["name"].lower() for component in item.get("components", []))
                for stack_item in stacks
            )
        ]
        return {
            "stacks": stacks,
            "integration_patterns": patterns,
            "relationships": stack_relationships(knowledge_base, stacks),
            "comparisons": stack_comparisons(knowledge_base, stacks),
        }
    if capability:
        needle = capability.lower()
        knowledge_base = index["knowledge_base"]
        return {
            "stacks": [
                item
                for item in knowledge_base["stacks"]
                if any(needle in value.lower() for value in item.get("capabilities", []))
                or any(needle in value.lower() for value in item.get("best_for", []))
                or any(needle in value.lower() for value in item.get("strengths", []))
                or any(needle in value.lower() for value in item.get("best_practices", []))
            ],
            "integration_patterns": [
                item
                for item in knowledge_base["integration_patterns"]
                if any(needle in value.lower() for value in item.get("fit_for", []))
                or any(needle in value.lower() for value in item.get("notes", []))
            ],
            "decision_rules": [
                item
                for item in knowledge_base.get("decision_rules", [])
                if matches_kb_text(
                    needle,
                    item.get("title", ""),
                    item.get("when", ""),
                    item.get("prefer", ""),
                    item.get("because", ""),
                    item.get("avoid", []),
                    item.get("related_items", []),
                )
            ],
            "relationships": [
                item
                for item in knowledge_base.get("relationships", [])
                if matches_kb_text(
                    needle,
                    item.get("subject", ""),
                    item.get("object", ""),
                    item.get("relation", ""),
                    item.get("rationale", ""),
                    item.get("tags", []),
                )
            ],
            "comparisons": [
                item
                for item in knowledge_base.get("comparisons", [])
                if matches_kb_text(
                    needle,
                    item.get("name", ""),
                    item.get("scope", []),
                    item.get("related_items", []),
                    item.get("summary", ""),
                    item.get("decision", ""),
                )
                or any(
                    matches_kb_text(
                        needle,
                        finding.get("area", ""),
                        finding.get("summary", ""),
                        finding.get("option_a", ""),
                        finding.get("option_b", ""),
                        finding.get("recommendation", ""),
                    )
                    for finding in item.get("findings", [])
                )
            ],
            "retrieval_guidance": {
                key: [value for value in values if needle in value.lower()]
                for key, values in knowledge_base.get("retrieval_guidance", {}).items()
                if isinstance(values, list) and any(needle in value.lower() for value in values)
            },
        }
    if impact:
        needle = impact.lower()
        knowledge_base = index["knowledge_base"]
        matched_documents = [
            item
            for item in index["documents"]
            if needle in item["path"].lower()
            or needle in item.get("title", "").lower()
            or any(needle in heading.lower() for heading in item.get("headings", []))
        ]
        matched_concerns = [
            item
            for item in index["concerns"]
            if needle in item["concern"].lower()
            or needle in item["owner_file"].lower()
            or any(needle in value.lower() for value in item.get("supporting_files", []))
        ]
        relation_targets = (
            {item["path"].lower() for item in matched_documents}
            | {item["concern"].lower() for item in matched_concerns}
            | {item["owner_file"].lower() for item in matched_concerns}
        )
        return {
            "documents": matched_documents,
            "concerns": matched_concerns,
            "relations": [
                item
                for item in index["relations"]
                if needle in item["from"].lower()
                or needle in item["to"].lower()
                or needle in item["source"].lower()
                or item["from"].lower() in relation_targets
                or item["to"].lower() in relation_targets
            ],
            "routes": [item for item in index["routes"] if needle in item["path"].lower() or needle in item["purpose"].lower()],
            "cli": [item for item in index["commands"]["cli"] if needle in item.lower()],
            "dashboard": [item for item in index["commands"]["dashboard"] if needle in item.lower()],
            "stacks": [
                item
                for item in knowledge_base["stacks"]
                if needle in item["name"].lower()
                or any(needle in alias.lower() for alias in item.get("aliases", []))
                or any(needle in value.lower() for value in item.get("capabilities", []))
                or any(needle in value.lower() for value in item.get("best_for", []))
                or any(needle in value.lower() for value in item.get("best_practices", []))
            ],
            "integration_patterns": [
                item
                for item in knowledge_base["integration_patterns"]
                if needle in item["name"].lower()
                or any(needle in value.lower() for value in item.get("fit_for", []))
                or any(needle in component.lower() for component in item.get("components", []))
            ],
            "decision_rules": [
                item
                for item in knowledge_base.get("decision_rules", [])
                if matches_kb_text(
                    needle,
                    item.get("title", ""),
                    item.get("when", ""),
                    item.get("prefer", ""),
                    item.get("because", ""),
                    item.get("avoid", []),
                    item.get("related_items", []),
                )
            ],
            "relationships": [
                item
                for item in knowledge_base.get("relationships", [])
                if matches_kb_text(
                    needle,
                    item.get("subject", ""),
                    item.get("relation", ""),
                    item.get("object", ""),
                    item.get("rationale", ""),
                    item.get("tags", []),
                )
            ],
            "comparisons": [
                item
                for item in knowledge_base.get("comparisons", [])
                if matches_kb_text(
                    needle,
                    item.get("name", ""),
                    item.get("scope", []),
                    item.get("compared_versions", []),
                    item.get("summary", ""),
                    item.get("decision", ""),
                    item.get("related_items", []),
                )
                or any(
                    matches_kb_text(
                        needle,
                        finding.get("area", ""),
                        finding.get("summary", ""),
                        finding.get("option_a", ""),
                        finding.get("option_b", ""),
                        finding.get("recommendation", ""),
                        finding.get("migration_risk", ""),
                    )
                    for finding in item.get("findings", [])
                )
            ],
        }
    return {
        "workspace": index["workspace"],
        "document_count": len(index["documents"]),
        "knowledge_base_stacks": len(index["knowledge_base"]["stacks"]),
        "knowledge_base_patterns": len(index["knowledge_base"]["integration_patterns"]),
        "knowledge_base_decision_rules": len(index["knowledge_base"].get("decision_rules", [])),
        "knowledge_base_relationships": len(index["knowledge_base"].get("relationships", [])),
        "knowledge_base_comparisons": len(index["knowledge_base"].get("comparisons", [])),
        "concern_count": len(index["concerns"]),
        "cli_commands": len(index["commands"]["cli"]),
        "dashboard_commands": len(index["commands"]["dashboard"]),
        "routes": len(index["routes"]),
    }


def print_query_result(result: dict[str, Any]) -> None:
    print(json.dumps(result, indent=2))


def cached_index_is_compatible(index: dict[str, Any]) -> bool:
    knowledge_base = index.get("knowledge_base")
    return (
        isinstance(knowledge_base, dict)
        and "decision_rules" in knowledge_base
        and "relationships" in knowledge_base
        and "comparisons" in knowledge_base
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build and query a structured context index for PROGRAMSTART.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    build_parser = subparsers.add_parser("build")
    build_parser.add_argument("--output", default=None, help="Output path. Defaults to outputs/context/context-index.json.")

    query_parser = subparsers.add_parser("query")
    query_parser.add_argument(
        "--index",
        default=None,
        help="Existing index path. Defaults to outputs/context/context-index.json.",
    )
    query_parser.add_argument("--concern", help="Find concern ownership and relations.")
    query_parser.add_argument("--file", dest="file_path", help="Find document metadata and relations for a file.")
    query_parser.add_argument("--command", dest="command_key", help="Find matching CLI or dashboard commands.")
    query_parser.add_argument("--route", help="Find matching dashboard routes.")
    query_parser.add_argument("--stack", help="Find stack guidance from the knowledge base.")
    query_parser.add_argument("--capability", help="Find stack and pattern guidance by capability or fit.")
    query_parser.add_argument("--impact", help="Find nearby documents, relations, routes, commands, and stacks for a target.")

    args = parser.parse_args(argv)

    if args.command == "build":
        index = ContextIndex.model_validate(build_context_index()).model_dump(by_alias=True)
        output_path = Path(args.output) if args.output else default_index_path()
        if not output_path.is_absolute():
            output_path = workspace_path(str(output_path))
        write_json(output_path, index)
        print(f"Wrote context index to {output_path}")
        return 0

    index_path = Path(args.index) if args.index else default_index_path()
    if not index_path.is_absolute():
        index_path = workspace_path(str(index_path))
    if index_path.exists():
        index = json.loads(index_path.read_text(encoding="utf-8"))
        if not cached_index_is_compatible(index):
            index = build_context_index()
    else:
        index = build_context_index()
    result = query_context_index(
        index,
        concern=args.concern,
        file_path=args.file_path,
        command=args.command_key,
        route=args.route,
        stack=args.stack,
        capability=args.capability,
        impact=args.impact,
    )
    print_query_result(result)
    return 0


if __name__ == "__main__":  # pragma: no cover
    warn_direct_script_invocation("'uv run programstart context <subcommand>' or 'pb context <subcommand>'")
    raise SystemExit(main())
