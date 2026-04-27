from __future__ import annotations

import json
import logging
import os
import re
import subprocess
import sys
import tempfile
import time
import tomllib
import warnings
from fnmatch import fnmatch
from pathlib import Path
from typing import TYPE_CHECKING, Any

from filelock import FileLock

if TYPE_CHECKING:
    from .programstart_models import ProcessRegistry

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Standalone execution compatibility
# ---------------------------------------------------------------------------


def _ensure_scripts_importable() -> None:
    """Ensure the scripts directory is on sys.path for standalone execution.

    Scripts that need bare imports (e.g. ``from programstart_validate import X``)
    during standalone execution (``python scripts/X.py``) should call this helper
    in their ``except ImportError`` fallback block *before* the bare imports.

    Python already prepends the script's directory to ``sys.path`` when running
    a script directly, so this is typically a no-op when invoked from
    ``scripts/``.  It is safe to call from package context too.
    """
    scripts_dir = str(Path(__file__).parent)
    if scripts_dir not in sys.path:
        sys.path.insert(0, scripts_dir)


# ---------------------------------------------------------------------------
# Terminal colour helpers — respects NO_COLOR env var and non-TTY pipes
# ---------------------------------------------------------------------------


def _use_color() -> bool:
    if os.environ.get("NO_COLOR"):
        return False
    return sys.stdout.isatty()


def _c(code: str, text: str) -> str:
    return f"\033[{code}m{text}\033[0m" if _use_color() else text


def clr_green(text: str) -> str:
    return _c("32", text)


def clr_yellow(text: str) -> str:
    return _c("33", text)


def clr_red(text: str) -> str:
    return _c("31", text)


def clr_cyan(text: str) -> str:
    return _c("36", text)


def clr_bold(text: str) -> str:
    return _c("1", text)


def clr_dim(text: str) -> str:
    return _c("2", text)


def status_color(status: str) -> str:
    """Apply terminal color to a workflow status string."""
    if status == "completed":
        return clr_green(status)
    if status == "in_progress":
        return clr_yellow(status)
    if status == "blocked":
        return clr_red(status)
    return clr_dim(status)  # planned


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
REGISTRY_MANIFEST_RELATIVE_PATH = "config/process-registry.json"
REGISTRY_INCLUDE_KEY = "include"


def detect_workspace_root(start_dir: Path | None = None) -> Path:
    override = os.environ.get("PROGRAMSTART_ROOT")
    if override:
        return Path(override).expanduser().resolve()

    current = (start_dir or Path.cwd()).resolve()
    for candidate in (current, *current.parents):
        if (candidate / REGISTRY_MANIFEST_RELATIVE_PATH).exists():
            return candidate

    warnings.warn(
        f"detect_workspace_root: no process-registry.json found from {current}; falling back to PACKAGE_ROOT ({PACKAGE_ROOT})",
        stacklevel=2,
    )
    return PACKAGE_ROOT


ROOT = detect_workspace_root()


def _merge_registry_fragment(base: dict[str, Any], fragment: dict[str, Any]) -> dict[str, Any]:
    merged = dict(base)
    for key, value in fragment.items():
        existing = merged.get(key)
        if isinstance(existing, dict) and isinstance(value, dict):
            merged[key] = _merge_registry_fragment(existing, value)
            continue
        merged[key] = value
    return merged


def load_registry_from_path(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"Registry manifest at {path} must be a JSON object")

    includes = data.get(REGISTRY_INCLUDE_KEY, [])
    merged = {key: value for key, value in data.items() if key != REGISTRY_INCLUDE_KEY}
    config_root = path.parent
    if includes:
        if not isinstance(includes, list) or not all(isinstance(item, str) for item in includes):
            raise ValueError(f"Registry manifest at {path} must declare '{REGISTRY_INCLUDE_KEY}' as a list of strings")
        for relative_path in includes:
            fragment_path = config_root / relative_path
            fragment = json.loads(fragment_path.read_text(encoding="utf-8"))
            if not isinstance(fragment, dict):
                raise ValueError(f"Registry fragment at {fragment_path} must be a JSON object")
            merged = _merge_registry_fragment(merged, fragment)

    if "version" not in merged:
        warnings.warn(
            "config/process-registry.json is missing 'version' key — registry integrity may be degraded",
            stacklevel=2,
        )
    return merged


def load_registry() -> dict[str, Any]:
    return load_registry_from_path(workspace_path(REGISTRY_MANIFEST_RELATIVE_PATH))


def load_validated_registry() -> ProcessRegistry:
    """Load and validate the process registry through the Pydantic model.

    Returns a :class:`ProcessRegistry` instance.  Import is deferred to avoid
    a hard dependency on Pydantic at module-load time.
    """
    from .programstart_models import ProcessRegistry

    raw = load_registry()
    return ProcessRegistry.model_validate(raw)


def _pyproject_dependency_surface(payload: bytes) -> tuple[tuple[str, ...], tuple[tuple[str, tuple[str, ...]], ...]]:
    parsed = tomllib.loads(payload.decode("utf-8"))
    project = parsed.get("project", {})
    dependencies = tuple(project.get("dependencies", []) or [])
    optional = project.get("optional-dependencies", {}) or {}
    optional_dependencies = tuple(sorted((name, tuple(values)) for name, values in optional.items()))
    return dependencies, optional_dependencies


def pyproject_dependency_sync_required() -> bool:
    pyproject = workspace_path("pyproject.toml")
    if not pyproject.exists():
        return True

    try:
        current_surface = _pyproject_dependency_surface(pyproject.read_bytes())
    except (OSError, tomllib.TOMLDecodeError, UnicodeDecodeError):
        return True

    previous = subprocess.run(
        ["git", "show", "HEAD:pyproject.toml"],
        cwd=workspace_path("."),
        capture_output=True,
        check=False,
    )
    if previous.returncode != 0 or not previous.stdout:
        return True

    try:
        previous_surface = _pyproject_dependency_surface(previous.stdout)
    except (tomllib.TOMLDecodeError, UnicodeDecodeError):
        return True

    return current_surface != previous_surface


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, content: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(content, indent=2) + "\n"
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False, dir=path.parent) as handle:
        handle.write(payload)
        temp_path = Path(handle.name)
    for attempt in range(3):
        try:
            temp_path.replace(path)
            return
        except PermissionError:
            if attempt == 2:
                raise
            time.sleep(0.05)


def workspace_path(relative_path: str) -> Path:
    return ROOT / relative_path


def to_posix(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def generated_outputs_root(registry: dict[str, Any] | None = None) -> Path:
    registry = registry or load_registry()
    workspace = dict(registry.get("workspace", {}))
    configured = str(workspace.get("generated_outputs_root", "outputs")).strip() or "outputs"
    return workspace_path(configured)


def display_workspace_path(path: Path) -> str:
    try:
        return to_posix(path)
    except ValueError:
        return str(path)


def warn_direct_script_invocation(preferred_command: str) -> None:
    if Path(sys.argv[0]).suffix != ".py":
        return

    logger.warning(
        "Direct script invocation is deprecated and will be removed in a future release. Use %s instead.",
        preferred_command,
    )


def metadata_prefixes(registry: dict[str, Any]) -> list[str]:
    return list(registry["metadata_rules"]["required_prefixes"])


def workflow_state_config(registry: dict[str, Any], system: str) -> dict[str, Any]:
    return dict(registry.get("workflow_state", {}).get(system, {}))


def workflow_state_path(registry: dict[str, Any], system: str) -> Path:
    config = workflow_state_config(registry, system)
    return workspace_path(str(config["state_file"]))


def create_default_workflow_state(registry: dict[str, Any], system: str) -> dict[str, Any]:
    config = workflow_state_config(registry, system)
    active_key = str(config["active_key"])
    initial_step = str(config["initial_step"])
    step_order = list(config["step_order"])
    entry_key = "stages" if system == "programbuild" else "phases"
    entries: dict[str, Any] = {}
    for step in step_order:
        entries[step] = {
            "status": "in_progress" if step == initial_step else "planned",
            "signoff": {
                "decision": "",
                "date": "",
                "notes": "",
            },
        }

    state: dict[str, Any] = {
        "system": system,
        active_key: initial_step,
        entry_key: entries,
    }
    if system == "programbuild":
        state["variant"] = "product"
    return state


def load_workflow_state(registry: dict[str, Any], system: str) -> dict[str, Any]:
    path = workflow_state_path(registry, system)
    if not path.exists():
        return create_default_workflow_state(registry, system)
    return load_json(path)


def validate_state_against_schema(state: dict[str, Any], system: str) -> None:
    """Validate state dict against the appropriate JSON schema before writing."""
    schema_map = {
        "programbuild": "schemas/programbuild-state.schema.json",
        "userjourney": "schemas/userjourney-state.schema.json",
    }
    schema_rel = schema_map.get(system, "")
    if not schema_rel:
        return
    schema_path = workspace_path(schema_rel)
    if not schema_path.exists():
        return  # Schema not found — skip validation (bootstrap scenario)
    import jsonschema

    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    jsonschema.validate(instance=state, schema=schema)


def save_workflow_state(
    registry: dict[str, Any],
    system: str,
    state: dict[str, Any],
    *,
    acquire_lock: bool = True,
) -> None:
    validate_state_against_schema(state, system)
    state_path = workflow_state_path(registry, system)
    if not acquire_lock:
        write_json(state_path, state)
        return
    lock = FileLock(str(state_path) + ".lock", timeout=10)
    with lock:
        write_json(state_path, state)


def system_is_optional_and_absent(registry: dict[str, Any], system_name: str) -> bool:
    """Return True if the system is marked optional and its root directory is missing."""
    system_cfg = registry["systems"][system_name]
    return bool(system_cfg.get("optional")) and not workspace_path(system_cfg["root"]).exists()


def system_is_attached(registry: dict[str, Any], system_name: str) -> bool:
    """Return True if the system's root directory exists on disk."""
    system_cfg = registry["systems"][system_name]
    root = system_cfg.get("root", "")
    return bool(root) and workspace_path(root).exists()


def workflow_steps(registry: dict[str, Any], system: str) -> list[str]:
    return list(workflow_state_config(registry, system).get("step_order", []))


def workflow_active_step(registry: dict[str, Any], system: str, state: dict[str, Any] | None = None) -> str:
    config = workflow_state_config(registry, system)
    state = state or load_workflow_state(registry, system)
    return str(state[str(config["active_key"])])


def workflow_entry_key(system: str) -> str:
    return "stages" if system == "programbuild" else "phases"


def workflow_step_files(registry: dict[str, Any], system: str, step: str) -> list[str]:
    config = workflow_state_config(registry, system)
    return list(config.get("step_files", {}).get(step, []))


def _normalise_stage_name(value: str) -> str:
    return value.replace("_", " ").strip().casefold()


def _normalise_gate_proceed(value: str) -> str:
    lowered = value.strip().casefold()
    if lowered == "yes":
        return "yes"
    if lowered == "conditional":
        return "conditional"
    if lowered == "no":
        return "no"
    return ""


def challenge_gate_record_from_log(active_step: str) -> dict[str, Any] | None:
    gate_path = workspace_path("PROGRAMBUILD/PROGRAMBUILD_CHALLENGE_GATE.md")
    if not gate_path.exists():
        return None

    try:
        lines = gate_path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return None

    in_log_section = False
    table_lines: list[str] = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("#"):
            heading = stripped.lstrip("#").strip()
            if heading == "Challenge Gate Log":
                in_log_section = True
                table_lines = []
                continue
            if in_log_section:
                break
        if in_log_section:
            if stripped.startswith("|"):
                table_lines.append(stripped)
            elif table_lines and stripped:
                break

    if len(table_lines) < 2:
        return None

    headers = [cell.strip() for cell in table_lines[0].strip("|").split("|")]
    excluded_headers = {"From Stage", "To Stage", "Date", "Proceed?", "Notes"}
    wanted_stage = _normalise_stage_name(active_step)
    for row in table_lines[2:]:
        values = [cell.strip() for cell in row.strip("|").split("|")]
        if len(values) != len(headers):
            continue
        entry = dict(zip(headers, values, strict=False))
        from_stage = _normalise_stage_name(entry.get("From Stage", ""))
        if from_stage != wanted_stage:
            continue

        checks = {header: value for header, value in entry.items() if header not in excluded_headers and value}
        proceed = _normalise_gate_proceed(entry.get("Proceed?", ""))
        blocking_checks = any("❌" in value for value in checks.values())
        warning_checks = any("⚠" in value for value in checks.values())
        result = "clear"
        if proceed == "no" or blocking_checks:
            result = "blocked"
        elif proceed == "conditional" or warning_checks:
            result = "warning"

        return {
            "source": "challenge_gate_log",
            "from_stage": entry.get("From Stage", "").strip(),
            "to_stage": entry.get("To Stage", "").strip(),
            "date": entry.get("Date", "").strip(),
            "proceed": proceed,
            "result": result,
            "notes": entry.get("Notes", "").strip(),
            "checks": checks,
        }

    return None


def metadata_value(text: str, prefix: str) -> str | None:
    for line in text.splitlines()[:20]:
        stripped = line.strip()
        if stripped.startswith(prefix):
            return stripped.removeprefix(prefix).strip()
        if stripped == "---":
            break
    return None


def has_required_metadata(text: str, prefixes: list[str]) -> list[str]:
    missing: list[str] = []
    lines = text.splitlines()
    header_lines: list[str] = []

    for line in lines[:20]:
        stripped = line.strip()
        header_lines.append(stripped)
        if stripped == "---":
            break

    for prefix in prefixes:
        if not any(line.startswith(prefix) for line in header_lines):
            missing.append(prefix)

    return missing


def extract_numbered_items(text: str, heading: str) -> list[str]:
    lines = text.splitlines()
    in_section = False
    items: list[str] = []

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("##"):
            current_heading = stripped.lstrip("#").strip()
            if in_section and current_heading != heading:
                break
            in_section = current_heading == heading
            continue

        if not in_section:
            continue

        match = re.match(r"^\d+\.\s+(.*)$", stripped)
        if match:
            items.append(match.group(1))

    return items


def parse_markdown_table(text: str, heading: str) -> list[dict[str, str]]:
    lines = text.splitlines()
    in_section = False
    table_lines: list[str] = []

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("##"):
            current_heading = stripped.lstrip("#").strip()
            if in_section and current_heading != heading:
                break
            in_section = current_heading == heading
            continue

        if in_section and stripped.startswith("|"):
            table_lines.append(stripped)

    if len(table_lines) < 2:
        return []

    headers = [cell.strip() for cell in table_lines[0].strip("|").split("|")]
    rows: list[dict[str, str]] = []
    for row in table_lines[2:]:
        values = [cell.strip() for cell in row.strip("|").split("|")]
        if len(values) != len(headers):
            continue
        rows.append(dict(zip(headers, values, strict=False)))
    return rows


def git_changed_files() -> list[str]:
    commands = [
        ["git", "diff", "--name-only", "--cached"],
        ["git", "diff", "--name-only"],
        ["git", "ls-files", "--others", "--exclude-standard"],  # untracked new files
    ]
    changed: list[str] = []

    for command in commands:
        try:
            result = subprocess.run(
                command,
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
        except OSError:
            continue

        if result.returncode != 0:
            continue

        for line in result.stdout.splitlines():
            stripped = line.strip().replace("\\", "/")
            if stripped and stripped not in changed:
                changed.append(stripped)

    return changed


def collect_registry_integrity_files(registry: dict[str, Any]) -> list[Path]:
    integrity = dict(registry.get("integrity", {}))
    manifest_collection = dict(integrity.get("manifest_collection", {}))
    include_system_file_groups = list(
        manifest_collection.get(
            "include_system_file_groups",
            ["control_files", "output_files", "core_files"],
        )
    )
    excluded_prefixes = [str(prefix).rstrip("/") for prefix in manifest_collection.get("exclude_prefixes", [])]
    excluded_names = set(str(name) for name in manifest_collection.get("exclude_names", []))
    excluded_globs = tuple(str(pattern) for pattern in manifest_collection.get("exclude_globs", []))

    def is_excluded(relative_path: str) -> bool:
        normalized = relative_path.replace("\\", "/")
        if any(normalized == prefix or normalized.startswith(prefix + "/") for prefix in excluded_prefixes):
            return True
        if Path(normalized).name in excluded_names:
            return True
        return any(fnmatch(normalized, pattern) for pattern in excluded_globs)

    candidates: set[str] = set()
    workspace = dict(registry.get("workspace", {}))
    if manifest_collection.get("include_workspace_readme", True):
        root_readme = str(workspace.get("root_readme", "")).strip()
        if root_readme:
            candidates.add(root_readme)

    if manifest_collection.get("include_bootstrap_assets", True):
        candidates.update(str(path) for path in workspace.get("bootstrap_assets", []))

    for system in registry.get("systems", {}).values():
        for group in include_system_file_groups:
            candidates.update(str(path) for path in system.get(group, []))

    baselines = list(integrity.get("baselines", []))
    if manifest_collection.get("include_baseline_roots", True):
        for baseline in baselines:
            root = str(baseline.get("root", "")).strip()
            if root:
                candidates.add(root)

    for baseline in baselines:
        manifest = str(baseline.get("manifest", "")).strip()
        if manifest:
            candidates.add(manifest)

    files: dict[str, Path] = {}
    for relative_path in sorted(candidates):
        if not relative_path or is_excluded(relative_path):
            continue
        candidate_path = workspace_path(relative_path)
        if candidate_path.is_file():
            files.setdefault(relative_path, candidate_path)
            continue
        if not candidate_path.is_dir():
            continue
        for path in sorted(candidate_path.rglob("*")):
            if not path.is_file():
                continue
            relative = to_posix(path)
            if is_excluded(relative):
                continue
            files.setdefault(relative, path)

    return sorted(files.values())
