from __future__ import annotations

import json
from pathlib import Path

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
