from __future__ import annotations

import json
import subprocess
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from scripts import programstart_mutation_loop as mutation_loop


def test_parse_materialized_summary_extracts_totals() -> None:
    output = "nox > Mutation results materialized: total=3281 pending=0 killed=2189 survived=1092 other=0"

    assert mutation_loop.parse_materialized_summary(output) == {
        "total": 3281,
        "pending": 0,
        "killed": 2189,
        "survived": 1092,
        "other": 0,
    }


def test_parse_materialized_summary_returns_none_when_missing() -> None:
    assert mutation_loop.parse_materialized_summary("no summary here") is None


def test_parse_mutation_speed_extracts_float() -> None:
    assert mutation_loop.parse_mutation_speed("4.09 mutations/second") == 4.09


def test_top_survivor_hotspots_counts_survivors(monkeypatch) -> None:
    payload = {
        "exit_code_by_key": {
            "scripts.programstart_recommend.x_build_stack_candidates__mutmut_1": 0,
            "scripts.programstart_recommend.x_build_stack_candidates__mutmut_2": 0,
            "scripts.programstart_recommend.x_main__mutmut_1": 0,
            "scripts.programstart_recommend.x_build_recommendation__mutmut_1": 1,
        }
    }
    monkeypatch.setattr(mutation_loop, "workspace_path", lambda relative: Path("meta.json"))
    monkeypatch.setattr(mutation_loop, "load_json", lambda path: payload)
    monkeypatch.setattr(Path, "exists", lambda self: True)

    assert mutation_loop.top_survivor_hotspots() == [
        {"name": "build_stack_candidates", "count": 2},
        {"name": "main", "count": 1},
    ]


def test_main_rejects_repeat_loop_without_edit_hook() -> None:
    with pytest.raises(SystemExit, match="Refusing to run repeated mutation cycles without an edit hook"):
        mutation_loop.main(["--cycles", "2"])


def test_append_record_writes_jsonl(tmp_path: Path) -> None:
    path = tmp_path / "runs.jsonl"
    record = mutation_loop.MutationRunRecord(
        cycle=1,
        started_at="2026-04-16T12:00:00+00:00",
        finished_at="2026-04-16T12:20:00+00:00",
        total=3281,
        pending=0,
        killed=2189,
        survived=1092,
        other=0,
        mutations_per_second=3.59,
        top_hotspots=[{"name": "build_stack_candidates", "count": 180}],
    )

    mutation_loop.append_record(path, record)

    payload = json.loads(path.read_text(encoding="utf-8").strip())
    assert payload["cycle"] == 1
    assert payload["killed"] == 2189


# --- wait_for_no_active_mutation tests ---


def test_wait_returns_immediately_when_no_active_processes(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(mutation_loop, "active_mutation_processes", lambda: [])
    mutation_loop.wait_for_no_active_mutation(poll_seconds=0.01, max_wait_seconds=1.0)


def test_wait_returns_when_processes_clear(monkeypatch: pytest.MonkeyPatch) -> None:
    call_count = 0

    def _fake_active() -> list[str]:
        nonlocal call_count
        call_count += 1
        return ["mutmut: worker"] if call_count < 3 else []

    monkeypatch.setattr(mutation_loop, "active_mutation_processes", _fake_active)
    monkeypatch.setattr(mutation_loop.time, "sleep", lambda _s: None)
    mutation_loop.wait_for_no_active_mutation(poll_seconds=0.01, max_wait_seconds=60.0)
    assert call_count == 3


def test_wait_raises_on_timeout(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(mutation_loop, "active_mutation_processes", lambda: ["mutmut: zombie"])

    clock = [0.0]

    def _fake_monotonic() -> float:
        val = clock[0]
        clock[0] += 100.0
        return val

    monkeypatch.setattr(mutation_loop.time, "monotonic", _fake_monotonic)
    monkeypatch.setattr(mutation_loop.time, "sleep", lambda _s: None)

    with pytest.raises(SystemExit, match="Timed out after 5.0s waiting for 1 active mutation process"):
        mutation_loop.wait_for_no_active_mutation(poll_seconds=0.01, max_wait_seconds=5.0)


def test_wait_timeout_message_includes_process_count(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(mutation_loop, "active_mutation_processes", lambda: ["mutmut: w1", "mutmut: w2", "mutmut: w3"])

    clock = [0.0]

    def _fake_monotonic() -> float:
        val = clock[0]
        clock[0] += 999.0
        return val

    monkeypatch.setattr(mutation_loop.time, "monotonic", _fake_monotonic)
    monkeypatch.setattr(mutation_loop.time, "sleep", lambda _s: None)

    with pytest.raises(SystemExit, match="3 active mutation process"):
        mutation_loop.wait_for_no_active_mutation(poll_seconds=0.01, max_wait_seconds=10.0)


# --- active_mutation_processes ---


def test_active_mutation_processes_returns_lines(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr(mutation_loop, "workspace_path", lambda relative: tmp_path / relative)
    result = subprocess.CompletedProcess(args=[], returncode=0, stdout="mutmut: worker1\nmutmut: worker2\n")
    with patch.object(subprocess, "run", return_value=result):
        lines = mutation_loop.active_mutation_processes()
    assert lines == ["mutmut: worker1", "mutmut: worker2"]


def test_active_mutation_processes_empty_when_grep_no_match(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr(mutation_loop, "workspace_path", lambda relative: tmp_path / relative)
    result = subprocess.CompletedProcess(args=[], returncode=1, stdout="")
    with patch.object(subprocess, "run", return_value=result):
        assert mutation_loop.active_mutation_processes() == []


def test_active_mutation_processes_raises_on_wsl_error(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr(mutation_loop, "workspace_path", lambda relative: tmp_path / relative)
    result = subprocess.CompletedProcess(args=[], returncode=2, stdout="", stderr="wsl error")
    with patch.object(subprocess, "run", return_value=result):
        with pytest.raises(RuntimeError, match="wsl error"):
            mutation_loop.active_mutation_processes()


# --- run_shell_command ---


def test_run_shell_command_returns_exit_code(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr(mutation_loop, "workspace_path", lambda relative: tmp_path / relative)

    mock_proc = MagicMock()
    mock_proc.stdout = iter(["line 1\n", "line 2\n"])
    mock_proc.wait.return_value = 0

    with patch.object(subprocess, "Popen", return_value=mock_proc):
        code = mutation_loop.run_shell_command(["echo", "hello"])
    assert code == 0


# --- run_mutation_command ---


def test_run_mutation_command_captures_transcript(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr(mutation_loop, "workspace_path", lambda relative: tmp_path / relative)

    mock_proc = MagicMock()
    mock_proc.stdout = iter(
        [
            "Running mutation...\n",
            "Mutation results materialized: total=10 pending=0 killed=8 survived=2 other=0\n",
        ]
    )
    mock_proc.wait.return_value = 0

    with patch.object(subprocess, "Popen", return_value=mock_proc):
        code, transcript = mutation_loop.run_mutation_command()
    assert code == 0
    assert "total=10" in transcript


# --- update_status ---


def test_update_status_writes_json(tmp_path: Path) -> None:
    path = tmp_path / "status.json"
    record = mutation_loop.MutationRunRecord(
        cycle=3,
        started_at="t0",
        finished_at="t1",
        total=100,
        pending=0,
        killed=90,
        survived=10,
        other=0,
        mutations_per_second=5.0,
        top_hotspots=[],
    )
    mutation_loop.update_status(path, record, 2)
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["cycles_remaining"] == 2
    assert data["latest_run"]["killed"] == 90


# --- main loop (single cycle, all gates skipped) ---


def test_main_single_cycle_skip_gates(monkeypatch, tmp_path: Path, capsys) -> None:
    monkeypatch.setattr(mutation_loop, "workspace_path", lambda relative: tmp_path / relative)
    monkeypatch.setattr(mutation_loop, "active_mutation_processes", lambda: [])
    monkeypatch.setattr(mutation_loop, "top_survivor_hotspots", lambda limit=7: [])

    transcript = "Mutation results materialized: total=50 pending=0 killed=45 survived=5 other=0\n3.5 mutations/second"
    monkeypatch.setattr(mutation_loop, "run_mutation_command", lambda: (0, transcript))

    result = mutation_loop.main(
        [
            "--cycles",
            "1",
            "--skip-gates",
            "--allow-repeat-without-edits",
            "--status-file",
            str(tmp_path / "status.json"),
            "--history-file",
            str(tmp_path / "history.jsonl"),
        ]
    )
    assert result == 0
    assert (tmp_path / "status.json").exists()
    assert (tmp_path / "history.jsonl").exists()
    out = capsys.readouterr().out
    assert "Completed 1 mutation cycle(s)" in out


def test_main_rejects_zero_cycles() -> None:
    with pytest.raises(SystemExit, match="--cycles must be at least 1"):
        mutation_loop.main(["--cycles", "0", "--allow-repeat-without-edits"])


def test_main_mutation_failure_raises(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr(mutation_loop, "workspace_path", lambda relative: tmp_path / relative)
    monkeypatch.setattr(mutation_loop, "active_mutation_processes", lambda: [])
    monkeypatch.setattr(mutation_loop, "run_mutation_command", lambda: (1, "fail"))

    with pytest.raises(SystemExit, match="mutation failed"):
        mutation_loop.main(
            [
                "--cycles",
                "1",
                "--skip-gates",
                "--allow-repeat-without-edits",
                "--status-file",
                str(tmp_path / "s.json"),
                "--history-file",
                str(tmp_path / "h.jsonl"),
            ]
        )


def test_main_missing_summary_raises(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr(mutation_loop, "workspace_path", lambda relative: tmp_path / relative)
    monkeypatch.setattr(mutation_loop, "active_mutation_processes", lambda: [])
    monkeypatch.setattr(mutation_loop, "run_mutation_command", lambda: (0, "no summary"))

    with pytest.raises(SystemExit, match="without a materialized summary"):
        mutation_loop.main(
            [
                "--cycles",
                "1",
                "--skip-gates",
                "--allow-repeat-without-edits",
                "--status-file",
                str(tmp_path / "s.json"),
                "--history-file",
                str(tmp_path / "h.jsonl"),
            ]
        )


def test_main_with_before_cycle_command(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr(mutation_loop, "workspace_path", lambda relative: tmp_path / relative)
    monkeypatch.setattr(mutation_loop, "active_mutation_processes", lambda: [])
    monkeypatch.setattr(mutation_loop, "top_survivor_hotspots", lambda limit=7: [])
    monkeypatch.setattr(subprocess, "call", lambda *_a, **_kw: 0)

    transcript = "Mutation results materialized: total=10 pending=0 killed=9 survived=1 other=0\n"
    monkeypatch.setattr(mutation_loop, "run_mutation_command", lambda: (0, transcript))

    result = mutation_loop.main(
        [
            "--cycles",
            "1",
            "--skip-gates",
            "--before-cycle-command",
            "echo hello",
            "--status-file",
            str(tmp_path / "s.json"),
            "--history-file",
            str(tmp_path / "h.jsonl"),
        ]
    )
    assert result == 0


def test_main_before_cycle_command_failure_raises(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr(mutation_loop, "workspace_path", lambda relative: tmp_path / relative)
    monkeypatch.setattr(mutation_loop, "active_mutation_processes", lambda: [])
    monkeypatch.setattr(subprocess, "call", lambda *_a, **_kw: 1)

    with pytest.raises(SystemExit, match="before-cycle command failed"):
        mutation_loop.main(
            [
                "--cycles",
                "1",
                "--skip-gates",
                "--before-cycle-command",
                "false",
                "--status-file",
                str(tmp_path / "s.json"),
                "--history-file",
                str(tmp_path / "h.jsonl"),
            ]
        )


def test_main_with_gates(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr(mutation_loop, "workspace_path", lambda relative: tmp_path / relative)
    monkeypatch.setattr(mutation_loop, "active_mutation_processes", lambda: [])
    monkeypatch.setattr(mutation_loop, "top_survivor_hotspots", lambda limit=7: [])
    monkeypatch.setattr(mutation_loop, "run_shell_command", lambda cmd: 0)

    transcript = "Mutation results materialized: total=10 pending=0 killed=9 survived=1 other=0\n"
    monkeypatch.setattr(mutation_loop, "run_mutation_command", lambda: (0, transcript))

    result = mutation_loop.main(
        [
            "--cycles",
            "1",
            "--allow-repeat-without-edits",
            "--status-file",
            str(tmp_path / "s.json"),
            "--history-file",
            str(tmp_path / "h.jsonl"),
        ]
    )
    assert result == 0


def test_main_drift_gate_failure_raises(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr(mutation_loop, "workspace_path", lambda relative: tmp_path / relative)
    monkeypatch.setattr(mutation_loop, "active_mutation_processes", lambda: [])

    call_count = [0]

    def _mock_shell(cmd: list[str]) -> int:
        call_count[0] += 1
        return 1  # drift fails

    monkeypatch.setattr(mutation_loop, "run_shell_command", _mock_shell)

    with pytest.raises(SystemExit, match="drift failed"):
        mutation_loop.main(
            [
                "--cycles",
                "1",
                "--allow-repeat-without-edits",
                "--status-file",
                str(tmp_path / "s.json"),
                "--history-file",
                str(tmp_path / "h.jsonl"),
            ]
        )
