from __future__ import annotations

import json

try:
    import jsonschema
except ImportError as exc:  # pragma: no cover - environment issue
    raise SystemExit(f"jsonschema is required to validate the process registry: {exc}") from exc

try:
    from .programstart_common import load_registry_from_path, warn_direct_script_invocation, workspace_path
except ImportError:  # pragma: no cover - standalone script execution fallback
    from programstart_common import load_registry_from_path, warn_direct_script_invocation, workspace_path


def main() -> int:
    registry = load_registry_from_path(workspace_path("config/process-registry.json"))
    schema = json.loads(workspace_path("schemas/process-registry.schema.json").read_text(encoding="utf-8"))
    jsonschema.validate(instance=registry, schema=schema)
    return 0


if __name__ == "__main__":  # pragma: no cover
    warn_direct_script_invocation("'uv run python scripts/check_process_registry_schema.py'")
    raise SystemExit(main())
