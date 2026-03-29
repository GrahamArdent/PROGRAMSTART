from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


def run_check(program: str, arguments: list[str], workspace: Path) -> tuple[bool, str]:
    result = subprocess.run(
        [program, *arguments],
        cwd=workspace,
        capture_output=True,
        text=True,
        check=False,
    )
    output = (result.stdout + result.stderr).strip()
    if result.returncode == 0:
        return True, output
    return False, output or f"command exited with code {result.returncode}"


def main() -> int:
    parser = argparse.ArgumentParser(description="Smoke test the unified programstart CLI command surface.")
    parser.add_argument("--program", default="programstart", help="CLI executable or full path to execute.")
    parser.add_argument("--workspace", default=".", help="Workspace root to run commands against.")
    args = parser.parse_args()

    workspace = Path(args.workspace).resolve()
    checks = [
        ["help"],
        ["status"],
        ["clean", "--dry-run"],
        ["validate", "--check", "workflow-state"],
        ["guide", "--system", "programbuild"],
        ["state", "show"],
        ["next"],
    ]

    failures = 0
    for command in checks:
        ok, detail = run_check(args.program, command, workspace)
        marker = "PASS" if ok else "FAIL"
        print(f"[{marker}] {' '.join([args.program, *command])}")
        if detail:
            print(detail)
        if not ok:
            failures += 1

    if failures:
        print(f"\nCLI smoke failed: {failures} command(s) failed.")
        return 1

    print(f"\nCLI smoke passed: {len(checks)} command(s) succeeded.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
