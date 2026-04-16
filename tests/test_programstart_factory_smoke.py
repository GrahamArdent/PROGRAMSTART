from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts import programstart_factory_smoke as factory_smoke


def test_validate_created_repo_establishes_git_baseline_before_cli_smoke(monkeypatch) -> None:
    commands: list[list[str]] = []

    def fake_run_command(command: list[str], cwd: Path, *, timeout: int = 0) -> str:
        del cwd, timeout
        commands.append(command)
        return ""

    monkeypatch.setattr(factory_smoke, "run_command", fake_run_command)
    scenario = factory_smoke.FactoryScenario(slug="cli", project_name="SMOKE CLI", product_shape="CLI tool")

    factory_smoke.validate_created_repo(Path("/tmp/generated"), scenario)

    assert commands[0] == ["uv", "sync", "--extra", "dev"]
    assert commands[1] == ["git", "init", "-b", "main"]
    assert commands[2] == ["git", "add", "."]
    assert commands[3][-3:] == ["--no-verify", "-m", "chore: factory smoke baseline"]
    assert commands[-1] == ["uv", "run", "python", "scripts/programstart_cli_smoke.py", "--workspace", "."]
