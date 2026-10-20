"""Real supported standalone imports and read-only CLI help, including child traces."""

import ast
import builtins
import os
import runpy
import subprocess
import sys
import tomllib
from pathlib import Path

import pytest
from coverage import Coverage

ROOT = Path(__file__).resolve().parents[1]
CONFIG = tomllib.loads((ROOT / "pyproject.toml").read_text())
SOURCES = CONFIG["tool"]["coverage"]["run"]["source"]


def test_missing_schema_dependency_has_actionable_diagnostic(monkeypatch):
    original = builtins.__import__

    def missing(name, globals=None, locals=None, fromlist=(), level=0):
        if name == "jsonschema":
            raise ImportError("dependency absent")
        return original(name, globals, locals, fromlist, level)

    monkeypatch.setattr(builtins, "__import__", missing)
    with pytest.raises(SystemExit, match="jsonschema is required"):
        runpy.run_path(str(ROOT / "scripts/check_process_registry_schema.py"), run_name="dependency_probe")


def supported_standalone_sources() -> list[str]:
    selected = []
    for name in SOURCES:
        path = ROOT / (name.replace(".", "/") + ".py")
        tree = ast.parse(path.read_text())
        # Direct invocation is supported when the module explicitly supplies a
        # main entry point or a relative-import fallback. Other library modules
        # have no standalone execution contract.
        fallback = any(
            isinstance(n, ast.ExceptHandler) and isinstance(n.type, ast.Name) and n.type.id == "ImportError"
            for n in ast.walk(tree)
        )
        main = any(isinstance(n, ast.If) and "__main__" in ast.unparse(n.test) for n in tree.body)
        if fallback or main:
            selected.append(name)
    return selected


@pytest.mark.parametrize("module", supported_standalone_sources())
def test_standalone_help_or_library_import(module: str, tmp_path: Path) -> None:
    active = Coverage.current()
    data_file = tmp_path / "child.coverage"
    command = [sys.executable]
    if active is not None:
        included_paths = [str(ROOT / (name.replace(".", "/") + ".py")) for name in SOURCES]
        command += [
            "-m",
            "coverage",
            "run",
            "--rcfile=/dev/null",
            "--branch",
            "--include=" + ",".join(included_paths),
            "--data-file",
            str(data_file),
        ]
    arguments = ["--help"]
    workspace = ROOT
    if module == "scripts.programstart_advance":
        # Its compatibility wrapper deliberately has add_help=False and delegates
        # parser help after the required system is identified.
        arguments = ["--system", "programbuild", "--dry-run", "--help"]
    elif module == "scripts.check_commit_msg":
        message = tmp_path / "message.txt"
        message.write_text("test: validate standalone invocation\n")
        arguments = [str(message)]
    elif module == "scripts.programstart_repo_clean_check":
        workspace = tmp_path / "clean"
        workspace.mkdir()
        subprocess.run(["git", "init", "--quiet", str(workspace)], check=True)
        arguments = []
    if module == "scripts.programstart_intent_compile":
        command += ["-m", module, *arguments]
    else:
        command += [str(ROOT / (module.replace(".", "/") + ".py")), *arguments]
    env = dict(os.environ, PROGRAMSTART_READONLY="1", PROGRAMSTART_ROOT=str(workspace))
    result = subprocess.run(command, cwd=ROOT, env=env, capture_output=True, text=True, timeout=30, check=False)
    assert result.returncode == 0, f"{module}: {result.stderr}\n{result.stdout}"
    assert "Traceback" not in result.stderr
    # Help is a real parser result; library-only files simply import successfully.
    tree = ast.parse((ROOT / (module.replace(".", "/") + ".py")).read_text())
    if any(isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr == "parse_args" for n in ast.walk(tree)):
        assert "usage:" in result.stdout.lower(), module
    if active is not None:
        child = Coverage(data_file=str(data_file))
        child.load()
        active.get_data().update(child.get_data())
