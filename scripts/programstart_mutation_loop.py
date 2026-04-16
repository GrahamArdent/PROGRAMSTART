from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

try:
    from .programstart_common import load_json, warn_direct_script_invocation, workspace_path
except ImportError:  # pragma: no cover - standalone script execution fallback
    from programstart_common import load_json, warn_direct_script_invocation, workspace_path

MATERIALIZED_RE = re.compile(
    r"Mutation results materialized: total=(?P<total>\d+) pending=(?P<pending>\d+) killed=(?P<killed>\d+) survived=(?P<survived>\d+) other=(?P<other>\d+)"
)
SPEED_RE = re.compile(r"(?P<speed>\d+(?:\.\d+)?) mutations/second")
SURVIVOR_KEY_RE = re.compile(r"^scripts\.programstart_recommend\.x_(.+)__mutmut_\d+$")


@dataclass(slots=True)
class MutationRunRecord:
    cycle: int
    started_at: str
    finished_at: str
    total: int
    pending: int
    killed: int
    survived: int
    other: int
    mutations_per_second: float | None
    top_hotspots: list[dict[str, int | str]]


def parse_materialized_summary(output: str) -> dict[str, int] | None:
    match = MATERIALIZED_RE.search(output)
    if not match:
        return None
    return {key: int(value) for key, value in match.groupdict().items()}


def parse_mutation_speed(output: str) -> float | None:
    match = SPEED_RE.search(output)
    if not match:
        return None
    return float(match.group("speed"))


def active_mutation_processes() -> list[str]:
    result = subprocess.run(
        [
            "wsl.exe",
            "bash",
            "-lc",
            "ps -ef | grep -E 'python -m mutmut run|mutmut:' | grep -v grep",
        ],
        cwd=workspace_path("."),
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode not in (0, 1):
        raise RuntimeError(result.stderr.strip() or "Unable to inspect active WSL mutmut processes")
    return [line for line in result.stdout.splitlines() if line.strip()]


def wait_for_no_active_mutation(poll_seconds: float, max_wait_seconds: float = 600.0) -> None:
    deadline = time.monotonic() + max_wait_seconds
    while True:
        active = active_mutation_processes()
        if not active:
            return
        if time.monotonic() >= deadline:
            raise SystemExit(
                f"Timed out after {max_wait_seconds}s waiting for {len(active)} active mutation "
                f"process(es) to finish. Orphan WSL processes may need manual cleanup."
            )
        print(f"Waiting for existing mutation run to finish ({len(active)} active process(es))...")
        time.sleep(poll_seconds)


def run_shell_command(command: list[str]) -> int:
    process = subprocess.Popen(
        command,
        cwd=workspace_path("."),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    assert process.stdout is not None
    for line in process.stdout:
        print(line, end="")
    return process.wait()


def run_mutation_command() -> tuple[int, str]:
    process = subprocess.Popen(
        ["uv", "run", "nox", "-s", "mutation"],
        cwd=workspace_path("."),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    assert process.stdout is not None
    transcript_lines: list[str] = []
    for line in process.stdout:
        transcript_lines.append(line)
        print(line, end="")
    return process.wait(), "".join(transcript_lines)


def top_survivor_hotspots(limit: int = 7) -> list[dict[str, int | str]]:
    meta_path = workspace_path("mutants/scripts/programstart_recommend.py.meta")
    if not meta_path.exists():
        return []
    payload = load_json(meta_path)
    exit_codes = dict(payload.get("exit_code_by_key", {}))
    counts: dict[str, int] = {}
    for key, exit_code in exit_codes.items():
        if exit_code != 0:
            continue
        match = SURVIVOR_KEY_RE.match(str(key))
        if not match:
            continue
        name = match.group(1)
        counts[name] = counts.get(name, 0) + 1
    ordered = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    return [{"name": name, "count": count} for name, count in ordered[:limit]]


def append_record(path: Path, record: MutationRunRecord) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(asdict(record), sort_keys=True) + "\n")


def update_status(path: Path, record: MutationRunRecord, cycles_remaining: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "updated_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "latest_run": asdict(record),
        "cycles_remaining": cycles_remaining,
    }
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run repeated canonical mutation cycles with timer-driven polling.")
    parser.add_argument("--cycles", type=int, default=25, help="Number of mutation cycles to run.")
    parser.add_argument(
        "--poll-seconds",
        type=float,
        default=30.0,
        help="How often to poll for an existing active mutation run before starting the next cycle.",
    )
    parser.add_argument(
        "--sleep-seconds",
        type=float,
        default=15.0,
        help="Delay between completed cycles before launching the next one.",
    )
    parser.add_argument(
        "--status-file",
        default="outputs/research/mutation_loop_status.json",
        help="Status JSON file updated after each settled run.",
    )
    parser.add_argument(
        "--history-file",
        default="outputs/research/mutation_loop_runs.jsonl",
        help="JSONL history file that records each settled run.",
    )
    parser.add_argument(
        "--before-cycle-command",
        help="Optional shell command to run before each cycle (for example an external edit hook).",
    )
    parser.add_argument(
        "--skip-gates",
        action="store_true",
        help="Skip drift and validate-all before each cycle.",
    )
    parser.add_argument(
        "--allow-repeat-without-edits",
        action="store_true",
        help="Keep rerunning mutation even if no edit hook is configured. Use this only when repeated measurement is intentional.",
    )
    parser.add_argument(
        "--max-wait-seconds",
        type=float,
        default=600.0,
        help="Maximum seconds to wait for an existing mutation run to finish before aborting (default: 600).",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.cycles < 1:
        raise SystemExit("--cycles must be at least 1")

    if not args.before_cycle_command and not args.allow_repeat_without_edits:
        raise SystemExit(
            "Refusing to run repeated mutation cycles without an edit hook. "
            "Pass --before-cycle-command or explicitly allow repeats with --allow-repeat-without-edits."
        )

    status_path = workspace_path(args.status_file)
    history_path = workspace_path(args.history_file)

    for cycle in range(1, args.cycles + 1):
        print(f"\n=== Mutation Loop Cycle {cycle}/{args.cycles} ===")
        wait_for_no_active_mutation(args.poll_seconds, args.max_wait_seconds)

        if args.before_cycle_command:
            print(f"Running before-cycle command: {args.before_cycle_command}")
            hook_code = subprocess.call(args.before_cycle_command, cwd=workspace_path("."), shell=True)
            if hook_code != 0:
                raise SystemExit(f"before-cycle command failed with exit code {hook_code}")

        if not args.skip_gates:
            print("Running drift gate...")
            drift_code = run_shell_command(["uv", "run", "programstart", "drift"])
            if drift_code != 0:
                raise SystemExit(f"drift failed in cycle {cycle} with exit code {drift_code}")

            print("Running validate-all gate...")
            validate_code = run_shell_command(["uv", "run", "programstart", "validate", "--check", "all"])
            if validate_code != 0:
                raise SystemExit(f"validate --check all failed in cycle {cycle} with exit code {validate_code}")

        started_at = datetime.now(UTC).isoformat(timespec="seconds")
        mutation_code, transcript = run_mutation_command()
        finished_at = datetime.now(UTC).isoformat(timespec="seconds")
        if mutation_code != 0:
            raise SystemExit(f"mutation failed in cycle {cycle} with exit code {mutation_code}")

        summary = parse_materialized_summary(transcript)
        if summary is None:
            raise SystemExit(f"mutation cycle {cycle} completed without a materialized summary line")

        record = MutationRunRecord(
            cycle=cycle,
            started_at=started_at,
            finished_at=finished_at,
            total=summary["total"],
            pending=summary["pending"],
            killed=summary["killed"],
            survived=summary["survived"],
            other=summary["other"],
            mutations_per_second=parse_mutation_speed(transcript),
            top_hotspots=top_survivor_hotspots(),
        )
        append_record(history_path, record)
        update_status(status_path, record, args.cycles - cycle)
        print(
            "Settled mutation result: "
            f"total={record.total} pending={record.pending} killed={record.killed} survived={record.survived} other={record.other}"
        )

        if cycle < args.cycles:
            print(f"Sleeping {args.sleep_seconds} second(s) before the next cycle...")
            time.sleep(args.sleep_seconds)

    print(f"Completed {args.cycles} mutation cycle(s).")
    print(f"History file: {history_path}")
    print(f"Status file: {status_path}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    warn_direct_script_invocation("'uv run programstart mutation-loop' or 'pb mutation-loop'")
    raise SystemExit(main())