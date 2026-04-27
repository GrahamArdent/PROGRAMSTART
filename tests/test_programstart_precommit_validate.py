from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts import programstart_precommit_validate as precommit_validate


def test_main_syncs_managed_prompts_before_validation(monkeypatch, capsys) -> None:
    registry = {"systems": {}}
    written_paths = [precommit_validate.ROOT / "outputs" / "generated-prompts" / "feasibility.prompt.md"]
    calls: list[tuple[str, object]] = []

    monkeypatch.setattr(precommit_validate, "load_registry", lambda: registry)
    monkeypatch.setattr(
        precommit_validate,
        "sync_managed_prompts",
        lambda loaded_registry: calls.append(("sync", loaded_registry)) or written_paths,
    )
    monkeypatch.setattr(
        precommit_validate.programstart_validate,
        "main",
        lambda argv: calls.append(("validate", argv)) or 0,
    )

    result = precommit_validate.main()

    assert result == 0
    assert calls == [
        ("sync", registry),
        ("validate", ["--check", "all", "--strict"]),
    ]
    captured = capsys.readouterr()
    assert "Wrote outputs/generated-prompts/feasibility.prompt.md" in captured.out
