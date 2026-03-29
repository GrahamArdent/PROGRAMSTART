from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import venv
from pathlib import Path


def venv_python(venv_root: Path) -> Path:
    scripts_dir = "Scripts" if sys.platform == "win32" else "bin"
    executable = "python.exe" if sys.platform == "win32" else "python"
    return venv_root / scripts_dir / executable


def venv_programstart(venv_root: Path) -> Path:
    scripts_dir = "Scripts" if sys.platform == "win32" else "bin"
    executable = "programstart.exe" if sys.platform == "win32" else "programstart"
    return venv_root / scripts_dir / executable


def run_command(command: list[str], cwd: Path) -> None:
    result = subprocess.run(command, cwd=cwd, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        raise RuntimeError((result.stdout + result.stderr).strip() or f"command failed: {' '.join(command)}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build-install smoke test for the packaged PROGRAMSTART distribution.")
    parser.add_argument("--dist-dir", default="dist", help="Directory containing built wheel artifacts.")
    parser.add_argument("--workspace", default=".", help="Workspace root to run the installed tool against.")
    parser.add_argument("--venv-dir", default=".tmp_dist_smoke", help="Temporary virtual environment directory.")
    args = parser.parse_args()

    workspace = Path(args.workspace).resolve()
    dist_dir = Path(args.dist_dir).resolve()
    wheels = sorted(dist_dir.glob("*.whl"))
    wheel = wheels[0] if wheels else None
    if wheel is None:
        print(f"No wheel found in {dist_dir}")
        return 1

    venv_dir = Path(args.venv_dir).resolve()
    if venv_dir.exists():
        shutil.rmtree(venv_dir)

    venv.EnvBuilder(with_pip=True, clear=True).create(venv_dir)
    python_path = venv_python(venv_dir)
    programstart_path = venv_programstart(venv_dir)

    run_command([str(python_path), "-m", "pip", "install", "--force-reinstall", str(wheel)], workspace)
    run_command(
        [
            str(python_path),
            "-m",
            "scripts.programstart_cli_smoke",
            "--program",
            str(programstart_path),
            "--workspace",
            str(workspace),
        ],
        workspace,
    )

    print(f"Distribution smoke passed for {wheel.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
