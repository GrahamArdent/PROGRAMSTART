from __future__ import annotations

# ruff: noqa: I001

import argparse
import sys
from collections.abc import Callable, Iterator
from contextlib import contextmanager

try:
    from . import (
        programstart_attach,
        programstart_bootstrap,
        programstart_checklist_progress,
        programstart_clean,
        programstart_create,
        programstart_drift_check,
        programstart_context,
        programstart_dashboard,
        programstart_impact,
        programstart_init,
        programstart_log,
        programstart_prompt_eval,
        programstart_research_delta,
        programstart_refresh_integrity,
        programstart_recommend,
        programstart_retrieval,
        programstart_serve,
        programstart_status,
        programstart_step_guide,
        programstart_validate,
        programstart_workflow_state,
    )
    from .programstart_common import warn_direct_script_invocation
    from .programstart_command_registry import CLI_COMMANDS
except ImportError:  # pragma: no cover - standalone script execution fallback
    import programstart_attach
    import programstart_bootstrap
    import programstart_checklist_progress
    import programstart_clean
    import programstart_create
    import programstart_command_registry
    import programstart_drift_check
    import programstart_context
    import programstart_dashboard
    import programstart_impact
    import programstart_init
    import programstart_log
    import programstart_prompt_eval
    import programstart_research_delta
    import programstart_refresh_integrity
    import programstart_recommend
    import programstart_retrieval
    import programstart_serve
    import programstart_status
    import programstart_step_guide
    import programstart_validate
    import programstart_workflow_state

    from programstart_common import warn_direct_script_invocation

    CLI_COMMANDS = programstart_command_registry.CLI_COMMANDS

MainFn = Callable[[], int]


@contextmanager
def temporary_argv(argv: list[str]) -> Iterator[None]:
    original = sys.argv[:]
    sys.argv = argv
    try:
        yield
    finally:
        sys.argv = original


def run_passthrough(main_fn: MainFn, argv0: str, arguments: list[str]) -> int:
    with temporary_argv([argv0, *arguments]):
        return int(main_fn())


def run_next(arguments: list[str]) -> int:
    if arguments:
        raise SystemExit("'next' does not accept additional arguments")

    print()
    print("  PROGRAMSTART - What To Do Next")
    print()

    steps = [
        run_passthrough(programstart_status.main, "programstart status", []),
        run_passthrough(programstart_step_guide.main, "programstart guide", ["--system", "programbuild"]),
        run_passthrough(programstart_step_guide.main, "programstart guide", ["--system", "userjourney"]),
    ]
    return next((code for code in steps if code != 0), 0)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Unified PROGRAMSTART command-line interface.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    for name in CLI_COMMANDS:
        subparsers.add_parser(name)

    subparsers.add_parser("help")
    return parser


def dispatch(command: str, arguments: list[str], parser: argparse.ArgumentParser) -> int:
    if command == "init":
        return run_passthrough(programstart_init.main, "programstart init", arguments)
    if command == "create":
        return run_passthrough(programstart_create.main, "programstart create", arguments)
    if command == "attach":
        return run_passthrough(programstart_attach.main, "programstart attach", arguments)
    if command == "recommend":
        return run_passthrough(programstart_recommend.main, "programstart recommend", arguments)
    if command == "impact":
        return run_passthrough(programstart_impact.main, "programstart impact", arguments)
    if command == "research":
        return run_passthrough(programstart_research_delta.main, "programstart research", arguments)
    if command == "status":
        return run_passthrough(programstart_status.main, "programstart status", arguments)
    if command == "validate":
        return run_passthrough(programstart_validate.main, "programstart validate", arguments)
    if command == "context":
        return run_passthrough(programstart_context.main, "programstart context", arguments)
    if command == "retrieval":
        return run_passthrough(programstart_retrieval.main, "programstart retrieval", arguments)
    if command == "state":
        return run_passthrough(programstart_workflow_state.main, "programstart state", arguments)
    if command == "advance":
        return run_passthrough(programstart_workflow_state.main, "programstart advance", ["advance", *arguments])
    if command == "next":
        return run_next(arguments)
    if command == "log":
        return run_passthrough(programstart_log.main, "programstart log", arguments)
    if command == "prompt-eval":
        return run_passthrough(programstart_prompt_eval.main, "programstart prompt-eval", arguments)
    if command == "progress":
        return run_passthrough(programstart_checklist_progress.main, "programstart progress", arguments)
    if command == "guide":
        return run_passthrough(programstart_step_guide.main, "programstart guide", arguments)
    if command == "drift":
        return run_passthrough(programstart_drift_check.main, "programstart drift", arguments)
    if command == "bootstrap":
        return run_passthrough(programstart_bootstrap.main, "programstart bootstrap", arguments)
    if command == "clean":
        return run_passthrough(programstart_clean.main, "programstart clean", arguments)
    if command == "refresh":
        return run_passthrough(programstart_refresh_integrity.main, "programstart refresh", arguments)
    if command == "dashboard":
        return run_passthrough(programstart_dashboard.main, "programstart dashboard", arguments)
    if command == "serve":
        return run_passthrough(programstart_serve.main, "programstart serve", arguments)
    if command == "help":
        parser.print_help()
        return 0
    raise SystemExit(f"Unknown command: {command}")


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args, arguments = parser.parse_known_args(argv)
    return dispatch(args.command, arguments, parser)


if __name__ == "__main__":  # pragma: no cover
    warn_direct_script_invocation("'uv run programstart <command>' or 'pb <command>'")
    raise SystemExit(main())
