from __future__ import annotations

import os
import shutil
import stat
from pathlib import Path

import nox

ROOT = Path(__file__).resolve().parent

nox.options.sessions = [
    "lint",
    "typecheck",
    "tests",
    "validate",
    "smoke",
    "docs",
]


def install_dev(session: nox.Session) -> None:
    session.install(".[dev]")


def _on_rm_error(func, path: str, _exc_info) -> None:
    os.chmod(path, stat.S_IWRITE)
    func(path)


def remove_tree(path: Path) -> None:
    shutil.rmtree(path, onerror=_on_rm_error)


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
    session.run("programstart", "validate", "--check", "all")
    session.run("programstart", "validate", "--check", "authority-sync")
    session.run("programstart", "validate", "--check", "planning-references")
    session.run("programstart", "validate", "--check", "workflow-state")
    session.run("python", "scripts/programstart_cli_smoke.py", "--workspace", str(ROOT))
    session.run("programstart", "guide", "--system", "programbuild")
    session.run("programstart", "guide", "--system", "userjourney")
    session.run("programstart", "state", "show")


@nox.session(reuse_venv=True)
def smoke(session: nox.Session) -> None:
    install_dev(session)
    session.run("python", "-m", "playwright", "install", "chromium")
    session.run("python", "scripts/programstart_dashboard_smoke.py")
    session.run(
        "python",
        "scripts/programstart_dashboard_browser_smoke.py",
        "--expect-userjourney",
        "attached",
    )
    session.run(
        "python",
        "scripts/programstart_dashboard_golden.py",
        "--expect-userjourney",
        "attached",
    )

    destination = ROOT / ".tmp_nox_bootstrap"
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
    session.run("uv", "sync", "--extra", "dev", external=True)
    session.run("git", "init", external=True)
    session.run("git", "add", ".", external=True)
    session.run("uv", "run", "pre-commit", "run", "--all-files", external=True)
    session.run("uv", "run", "programstart", "validate", "--check", "all", external=True)
    session.run("uv", "run", "python", "scripts/programstart_cli_smoke.py", "--workspace", str(destination), external=True)
    session.run("python", "scripts/programstart_dashboard_smoke.py", external=True)
    session.run(
        "python",
        "scripts/programstart_dashboard_browser_smoke.py",
        "--expect-userjourney",
        "absent",
        external=True,
    )
    session.run(
        "python",
        "scripts/programstart_dashboard_golden.py",
        "--expect-userjourney",
        "absent",
        external=True,
    )
    session.chdir(ROOT)


@nox.session(reuse_venv=True)
def docs(session: nox.Session) -> None:
    install_dev(session)
    session.run("mkdocs", "build", "--strict")


@nox.session(reuse_venv=True)
def package(session: nox.Session) -> None:
    """Build a wheel and smoke the installed console script."""
    install_dev(session)
    session.run("uv", "build", external=True)
    session.run("python", "scripts/programstart_dist_smoke.py", "--dist-dir", "dist", "--workspace", str(ROOT))


@nox.session
def ci(session: nox.Session) -> None:
    """Run the full local gate used to mirror the major CI checks."""
    for name in ("lint", "typecheck", "tests", "validate", "smoke", "docs", "package", "security"):
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
    )
    session.log("requirements.txt updated")


@nox.session(reuse_venv=True)
def security(session: nox.Session) -> None:
    """Run security scanning (bandit + pip-audit)."""
    install_dev(session)
    session.run("bandit", "-r", "scripts/", "-ll", "--skip", "B101,B310", "-x", "tests/")
    session.run("pip-audit", "--desc", success_codes=[0, 1])


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
        ".tmp_dist_smoke",
    ]
    for name in targets:
        target = ROOT / name
        if target.is_dir():
            remove_tree(target)
            session.log(f"Removed {name}/")
        elif target.is_file():
            target.unlink()
            session.log(f"Removed {name}")
