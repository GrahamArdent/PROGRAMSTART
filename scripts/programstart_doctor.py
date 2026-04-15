from __future__ import annotations

import json
import shutil
import subprocess
import sys

try:
    from .programstart_common import load_registry_from_path, warn_direct_script_invocation, workspace_path
except ImportError:  # pragma: no cover - standalone script execution fallback
    from programstart_common import load_registry_from_path, warn_direct_script_invocation, workspace_path


def _check_python_version() -> tuple[bool, str]:
    ok = sys.version_info >= (3, 12)
    version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    return ok, f"Python {version}" + ("" if ok else " (need >=3.12)")


def _check_tool_installed(name: str) -> tuple[bool, str]:
    ok = shutil.which(name) is not None
    return ok, name + ("" if ok else " not found on PATH")


def _check_playwright() -> tuple[bool, str]:
    if shutil.which("playwright") is None:
        return False, "playwright not found on PATH"
    try:
        result = subprocess.run(
            ["playwright", "--version"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0:
            return True, f"playwright {result.stdout.strip()}"
        return False, "playwright found but --version failed"
    except (subprocess.TimeoutExpired, OSError):
        return False, "playwright found but --version timed out"


def _check_git_repo() -> tuple[bool, str]:
    git_dir = workspace_path(".git")
    ok = git_dir.is_dir()
    return ok, "git repo" + ("" if ok else " — .git directory missing")


def _check_registry_schema() -> tuple[bool, str]:
    registry_path = workspace_path("config/process-registry.json")
    schema_path = workspace_path("schemas/process-registry.schema.json")
    if not registry_path.exists():
        return False, "process-registry.json not found"
    if not schema_path.exists():
        return True, "process-registry.json present (schema file missing, skipped validation)"
    try:
        load_registry_from_path(registry_path)
        return True, "process-registry.json and registry fragments valid JSON"
    except (ValueError, json.JSONDecodeError, OSError) as exc:
        return False, f"process-registry.json parse error: {exc}"


def _check_state_files() -> tuple[bool, str]:
    problems: list[str] = []
    for name in ("PROGRAMBUILD/PROGRAMBUILD_STATE.json",):
        path = workspace_path(name)
        if not path.exists():
            problems.append(f"{name} missing")
            continue
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as exc:
            problems.append(f"{name}: {exc}")
    if problems:
        return False, "; ".join(problems)
    return True, "state files valid JSON"


def run_checks() -> list[tuple[bool, str]]:
    return [
        _check_python_version(),
        _check_tool_installed("uv"),
        _check_tool_installed("pre-commit"),
        _check_playwright(),
        _check_git_repo(),
        _check_registry_schema(),
        _check_state_files(),
    ]


def main() -> int:
    results = run_checks()
    all_ok = True
    for ok, message in results:
        icon = "\u2705" if ok else "\u274c"
        print(f"  {icon}  {message}")
        if not ok:
            all_ok = False
    print()
    if all_ok:
        print("All checks passed.")
    else:
        print("Some checks failed — see above.")
    return 0 if all_ok else 1


if __name__ == "__main__":  # pragma: no cover
    warn_direct_script_invocation("'uv run programstart doctor' or 'pb doctor'")
    raise SystemExit(main())
