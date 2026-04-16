from __future__ import annotations

import json
import os
import shlex
import shutil
import stat
import subprocess
import tempfile
import time
from pathlib import Path

import nox

ROOT = Path(__file__).resolve().parent

nox.options.sessions = [
    "lint",
    "typecheck",
    "tests",
    "validate",
    "smoke_readonly",
    "smoke_isolated",
    "docs",
]


def install_dev(session: nox.Session) -> None:
    session.install(".[dev]")


def _on_rm_error(func, path: str, _exc_info) -> None:
    os.chmod(path, stat.S_IWRITE)
    func(path)


def remove_tree(path: Path) -> None:
    attempts = 6 if os.name == "nt" else 1
    last_error: PermissionError | None = None
    for attempt in range(attempts):
        try:
            shutil.rmtree(path, onerror=_on_rm_error)
            return
        except PermissionError as exc:
            last_error = exc
            if attempt == attempts - 1:
                raise
            time.sleep(0.5 * (attempt + 1))

    if last_error is not None:
        raise last_error


def reset_mutation_workspace() -> None:
    mutation_workspace = ROOT / "mutants"
    if mutation_workspace.exists():
        remove_tree(mutation_workspace)


def mutation_meta_path() -> Path:
    return ROOT / "mutants" / "scripts" / "programstart_recommend.py.meta"


def mutation_result_summary() -> dict[str, int]:
    meta_path = mutation_meta_path()
    if not meta_path.exists():
        raise RuntimeError(f"Mutation results metadata was not created: {meta_path}")

    try:
        payload = json.loads(meta_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Mutation metadata is invalid JSON: {meta_path}") from exc

    exit_code_by_key = payload.get("exit_code_by_key")
    if not isinstance(exit_code_by_key, dict):
        raise RuntimeError("Mutation metadata is missing exit_code_by_key entries")

    values = list(exit_code_by_key.values())
    total = len(values)
    pending = sum(value is None for value in values)
    killed = sum(value == 1 for value in values)
    survived = sum(value == 0 for value in values)
    other = total - pending - killed - survived
    return {
        "total": total,
        "pending": pending,
        "killed": killed,
        "survived": survived,
        "other": other,
    }


def ensure_materialized_mutation_results(session: nox.Session) -> None:
    summary = mutation_result_summary()
    if summary["total"] == 0:
        session.error("Mutation run completed without generating any mutant entries. Treating result as invalid.")
    if summary["pending"] == summary["total"]:
        session.error(
            "Mutation run completed without materializing any mutant outcomes. "
            "Treating all-pending metadata as an invalid result."
        )

    session.log(
        "Mutation results materialized: "
        f"total={summary['total']} pending={summary['pending']} killed={summary['killed']} "
        f"survived={summary['survived']} other={summary['other']}"
    )


def uv_external_env() -> dict[str, str]:
    env = os.environ.copy()
    env.pop("VIRTUAL_ENV", None)
    return env


def workspace_bin(workspace: Path, executable: str) -> str:
    scripts_dir = "Scripts" if os.name == "nt" else "bin"
    suffix = ".exe" if os.name == "nt" else ""
    return str(workspace / ".venv" / scripts_dir / f"{executable}{suffix}")


def external_temp_path(env_var: str, default_name: str) -> Path:
    configured = os.environ.get(env_var, "").strip()
    if configured:
        return Path(configured).expanduser().resolve()
    return (Path(tempfile.gettempdir()) / default_name).resolve()


def dashboard_golden_args(expect_userjourney: str) -> list[str]:
    args = [
        "python",
        "scripts/programstart_dashboard_golden.py",
        "--expect-userjourney",
        expect_userjourney,
    ]
    if os.name == "nt":
        args.extend(["--max-diff-pixels", "4000"])
    return args


def windows_path_to_wsl(path: Path) -> str:
    drive = path.drive.rstrip(":").lower()
    tail = path.as_posix()[2:]
    return f"/mnt/{drive}{tail}"


def has_wsl_python_pip() -> bool:
    result = subprocess.run(
        ["wsl.exe", "bash", "-lc", "python3 -m pip --version"],
        capture_output=True,
        text=True,
        check=False,
    )
    return result.returncode == 0


@nox.session(reuse_venv=True)
def lint(session: nox.Session) -> None:
    install_dev(session)
    if (ROOT / ".git").exists():
        session.run("pre-commit", "run", "--all-files")
        return
    session.run("pre-commit", "validate-config")
    session.run("ruff", "check", ".")
    session.run("ruff", "format", "--check", ".")
    session.run(
        "check-jsonschema",
        "--schemafile",
        "schemas/process-registry.schema.json",
        "config/process-registry.json",
    )
    session.run(
        "check-jsonschema",
        "--schemafile",
        "schemas/programbuild-state.schema.json",
        "PROGRAMBUILD/PROGRAMBUILD_STATE.json",
    )
    session.run(
        "check-jsonschema",
        "--schemafile",
        "schemas/userjourney-state.schema.json",
        "USERJOURNEY/USERJOURNEY_STATE.json",
    )


@nox.session(reuse_venv=True)
def typecheck(session: nox.Session) -> None:
    install_dev(session)
    session.run("pyright")


@nox.session(reuse_venv=True)
def tests(session: nox.Session) -> None:
    install_dev(session)
    session.run("coverage", "run", "-m", "pytest")
    session.run("coverage", "report", "-m")


@nox.session(reuse_venv=True)
def validate(session: nox.Session) -> None:
    install_dev(session)
    session.run("programstart", "drift")
    session.run("programstart", "validate", "--check", "all")
    session.run("programstart", "prompt-eval", "--json")
    session.run("programstart", "validate", "--check", "authority-sync")
    session.run("programstart", "validate", "--check", "planning-references")
    session.run("programstart", "validate", "--check", "workflow-state")
    session.run("python", "scripts/programstart_cli_smoke.py", "--workspace", str(ROOT))
    session.run("programstart", "guide", "--system", "programbuild")
    session.run("programstart", "guide", "--system", "userjourney")
    session.run("programstart", "state", "show")
    session.run("programstart", "drift")


@nox.session(reuse_venv=True)
def smoke_readonly(session: nox.Session) -> None:
    """Read-only root-workspace smoke — safe to run anytime, no mutations."""
    install_dev(session)
    session.run("python", "-m", "playwright", "install", "chromium")
    session.run("python", "scripts/programstart_dashboard_smoke_readonly.py")
    session.run(
        "python",
        "scripts/programstart_dashboard_browser_smoke.py",
        "--expect-userjourney",
        "attached",
    )
    session.run(*dashboard_golden_args("attached"))


@nox.session(reuse_venv=True)
def smoke_isolated(session: nox.Session) -> None:
    """Mutating smoke in bootstrapped temp workspaces — exercises POST routes and factory."""
    install_dev(session)
    session.run("python", "-m", "playwright", "install", "chromium")

    destination = external_temp_path("PROGRAMSTART_NOX_BOOTSTRAP_DIR", "programstart_nox_bootstrap")
    if destination.exists():
        remove_tree(destination)

    session.run(
        "programstart",
        "bootstrap",
        "--dest",
        str(destination),
        "--project-name",
        "NOX-SMOKE",
        "--variant",
        "product",
    )
    session.chdir(destination)
    external_uv = uv_external_env()
    session.run("uv", "sync", "--extra", "dev", external=True, env=external_uv)
    session.run("git", "init", "-b", "main", external=True)
    session.run("git", "add", ".", external=True)
    session.run(
        "git",
        "-c",
        "user.name=PROGRAMSTART Smoke",
        "-c",
        "user.email=programstart-smoke@example.invalid",
        "commit",
        "--no-verify",
        "-m",
        "chore: bootstrap baseline",
        external=True,
    )
    bootstrap_python = workspace_bin(destination, "python")
    bootstrap_pre_commit = workspace_bin(destination, "pre-commit")
    bootstrap_programstart = workspace_bin(destination, "programstart")
    bootstrap_skip_env = {**os.environ, "SKIP": "programstart-drift"}
    session.run(
        bootstrap_pre_commit,
        "run",
        "--all-files",
        external=True,
        env=bootstrap_skip_env,
        success_codes=[0, 1],
    )
    session.run("git", "add", ".", external=True)
    session.run(
        "git",
        "-c",
        "user.name=PROGRAMSTART Smoke",
        "-c",
        "user.email=programstart-smoke@example.invalid",
        "commit",
        "--no-verify",
        "-m",
        "chore: bootstrap hygiene",
        external=True,
        success_codes=[0, 1],
    )
    session.run(bootstrap_pre_commit, "run", "--all-files", external=True, env=bootstrap_skip_env)
    session.run(bootstrap_programstart, "validate", "--check", "all", external=True)
    session.run(bootstrap_programstart, "drift", external=True)
    session.run(
        bootstrap_python,
        "scripts/programstart_cli_smoke.py",
        "--workspace",
        str(destination),
        external=True,
    )
    session.run(bootstrap_python, "scripts/programstart_dashboard_smoke.py", external=True)
    session.run(
        bootstrap_python,
        "scripts/programstart_dashboard_browser_smoke.py",
        "--expect-userjourney",
        "absent",
        external=True,
    )
    bootstrap_golden_args = [bootstrap_python, "scripts/programstart_dashboard_golden.py", "--expect-userjourney", "absent"]
    if os.name == "nt":
        bootstrap_golden_args.extend(["--max-diff-pixels", "4000"])
    session.run(*bootstrap_golden_args, external=True)
    session.chdir(ROOT)
    session.run(
        "python",
        "scripts/programstart_factory_smoke.py",
        "--workspace",
        str(ROOT),
        "--dest-root",
        str(external_temp_path("PROGRAMSTART_NOX_FACTORY_DIR", "programstart_nox_factory_smoke")),
    )
    session.chdir(ROOT)


@nox.session(reuse_venv=True)
def smoke(session: nox.Session) -> None:
    """Run all smoke tiers (read-only + isolated). Backwards compatible."""
    for name in ("smoke_readonly", "smoke_isolated"):
        session.notify(name)


@nox.session(reuse_venv=True)
def docs(session: nox.Session) -> None:
    install_dev(session)
    session.run("mkdocs", "build", "--strict")


@nox.session(reuse_venv=True)
def gate_safe(session: nox.Session) -> None:
    """Run a local pre-merge confidence gate (includes read-only smoke)."""
    for name in ("lint", "typecheck", "tests", "validate", "smoke_readonly", "docs"):
        session.notify(name)


@nox.session(reuse_venv=True)
def quick(session: nox.Session) -> None:
    """Fast feedback — lint + typecheck only (~10s)."""
    for name in ("lint", "typecheck"):
        session.notify(name)


@nox.session(reuse_venv=True)
def mutation(session: nox.Session) -> None:
    """Run focused mutation testing for the recommendation engine."""
    target_filter = session.posargs[0] if session.posargs else ""
    reset_mutation_workspace()
    if os.name == "nt":
        if not has_wsl_python_pip():
            session.error(
                "Mutation testing requires WSL Python with pip installed. "
                "In Ubuntu run: sudo apt install python3-pip python3-venv. "
                "Then install repo dev deps inside WSL and rerun `nox -s mutation`."
            )
        repo_root = windows_path_to_wsl(ROOT)
        quoted_repo_root = shlex.quote(repo_root)
        quoted_target = shlex.quote(target_filter)
        wsl_venv = ".nox/mutation-wsl"
        mutmut_command = f"{wsl_venv}/bin/python -m mutmut run"
        if target_filter:
            mutmut_command += f" {quoted_target}"
        session.run(
            "wsl.exe",
            "bash",
            "-lc",
            (
                f"cd {quoted_repo_root} && "
                f"rm -rf {wsl_venv} && "
                f"python3 -m venv {wsl_venv} && "
                f"PIP_DISABLE_PIP_VERSION_CHECK=1 {wsl_venv}/bin/python -m pip install -e . mutmut pytest >/dev/null && "
                f'{wsl_venv}/bin/python -c "from pathlib import Path; import sys; '
                "path = next(Path(sys.prefix).glob('lib/python*/site-packages/mutmut/__main__.py')); "
                "text = path.read_text(); "
                "needle = \\\"set_start_method('fork')\\n\\\"; "
                "replacement = \\\"try:\\n    set_start_method('fork')\\nexcept RuntimeError:\\n    pass\\n\\\"; "
                "already_patched = replacement in text; "
                "has_needle = needle in text; "
                "_ = path.write_text(text.replace(needle, replacement, 1)) if has_needle else None; "
                "sys.exit('Unable to patch mutmut fork start method') if (not already_patched and not has_needle) else None\" && "
                f"{mutmut_command}"
            ),
            external=True,
        )
        ensure_materialized_mutation_results(session)
        return

    install_dev(session)
    if target_filter:
        session.run("mutmut", "run", target_filter)
    else:
        session.run("mutmut", "run")
    ensure_materialized_mutation_results(session)


@nox.session(reuse_venv=True)
def package(session: nox.Session) -> None:
    """Build a wheel and smoke the installed console script."""
    install_dev(session)
    session.run("uv", "build", external=True)
    session.run("python", "scripts/programstart_dist_smoke.py", "--dist-dir", "dist", "--workspace", str(ROOT))


@nox.session
def ci(session: nox.Session) -> None:
    """Run the full local gate used to mirror the major CI checks."""
    for name in ("lint", "typecheck", "tests", "validate", "smoke", "docs", "package", "security", "requirements"):
        session.notify(name)


@nox.session(reuse_venv=True)
def requirements(session: nox.Session) -> None:
    """Regenerate requirements.txt from the lockfile."""
    session.run(
        "uv",
        "export",
        "--format",
        "requirements-txt",
        "--extra",
        "dev",
        "--no-hashes",
        "-o",
        "requirements.txt",
        external=True,
        env=uv_external_env(),
    )
    session.log("requirements.txt updated")


@nox.session(reuse_venv=True)
def security(session: nox.Session) -> None:
    """Run security scanning (bandit + pip-audit)."""
    install_dev(session)
    session.run("bandit", "-r", "scripts/", "-ll", "--skip", "B101,B310", "-x", "tests/")
    session.run("pip-audit", "--desc", success_codes=[0, 1])


@nox.session(reuse_venv=True)
def format_check(session: nox.Session) -> None:
    """Check formatting without modifying files."""
    install_dev(session)
    session.run("ruff", "check", ".")
    session.run("ruff", "format", "--check", ".")


@nox.session(reuse_venv=True)
def format_code(session: nox.Session) -> None:
    """Auto-format code with Ruff."""
    install_dev(session)
    session.run("ruff", "check", "--fix", ".")
    session.run("ruff", "format", ".")


@nox.session
def clean(session: nox.Session) -> None:
    """Remove build and cache artifacts."""
    targets = [
        ".coverage",
        "htmlcov",
        ".pytest_cache",
        "dist",
        "build",
        "site",
        ".nox",
        ".tmp_nox_bootstrap",
        ".tmp_nox_create",
        ".tmp_nox_factory_smoke",
        ".tmp_dist_smoke",
        ".tmp_factory_smoke",
    ]
    for name in targets:
        target = ROOT / name
        if target.is_dir():
            remove_tree(target)
            session.log(f"Removed {name}/")
        elif target.is_file():
            target.unlink()
            session.log(f"Removed {name}")
