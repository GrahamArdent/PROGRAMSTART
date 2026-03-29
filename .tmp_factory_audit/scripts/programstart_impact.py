from __future__ import annotations

# ruff: noqa: I001

import argparse
import json
from pathlib import Path
from typing import Any

try:
    from .programstart_common import warn_direct_script_invocation, workspace_path
    from .programstart_context import build_context_index, default_index_path, query_context_index
except ImportError:  # pragma: no cover - standalone script execution fallback
    from programstart_common import workspace_path, warn_direct_script_invocation  # type: ignore
    from programstart_context import (  # type: ignore
        build_context_index,
        default_index_path,
        query_context_index,
    )


def load_index(index_path: str | None) -> dict[str, Any]:
    path = Path(index_path) if index_path else default_index_path()
    if not path.is_absolute():
        path = workspace_path(str(path))
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return build_context_index()


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


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Show the likely impact surface for a file, concern, route, or keyword.")
    parser.add_argument("target", help="Target file path, concern, route fragment, or keyword.")
    parser.add_argument("--index", default=None, help="Existing context index path.")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of text.")
    args = parser.parse_args(argv)

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
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print_impact_summary(args.target, result)
    return 0


if __name__ == "__main__":  # pragma: no cover
    warn_direct_script_invocation("'uv run programstart impact <target>' or 'pb impact <target>'")
    raise SystemExit(main())
