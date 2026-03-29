"""Show the sign-off history for PROGRAMBUILD stages and USERJOURNEY phases."""

from __future__ import annotations

import argparse
from typing import Any, cast

try:
    from .programstart_common import (
        clr_bold,
        clr_cyan,
        clr_dim,
        clr_green,
        load_registry,
        load_workflow_state,
        status_color,
        warn_direct_script_invocation,
        workflow_active_step,
        workflow_entry_key,
        workflow_steps,
        workspace_path,
    )
except ImportError:  # pragma: no cover - standalone script execution fallback
    from programstart_common import (
        clr_bold,
        clr_cyan,
        clr_dim,
        clr_green,
        load_registry,
        load_workflow_state,
        status_color,
        warn_direct_script_invocation,
        workflow_active_step,
        workflow_entry_key,
        workflow_steps,
        workspace_path,
    )


def system_is_optional_and_absent(registry: dict[str, Any], system: str) -> bool:
    system_cfg = cast(dict[str, Any], registry["systems"][system])
    return bool(system_cfg.get("optional")) and not workspace_path(cast(str, system_cfg["root"])).exists()


def print_log(system: str, registry: dict[str, Any]) -> None:
    state = load_workflow_state(registry, system)
    active_step = workflow_active_step(registry, system, state)
    steps = workflow_steps(registry, system)
    entry_key = workflow_entry_key(system)
    entries = cast(dict[str, Any], state.get(entry_key, {}))

    print(clr_bold(clr_cyan(f"{system.upper()} Sign-off Log")))
    if system == "programbuild":
        print(clr_dim(f"variant: {state.get('variant', 'product')}"))
    print()

    for step in steps:
        entry = cast(dict[str, Any], entries.get(step, {}))
        status = str(entry.get("status", "planned"))
        signoff = cast(dict[str, Any], entry.get("signoff", {}))
        decision = str(signoff.get("decision", ""))
        date = str(signoff.get("date", ""))
        notes = str(signoff.get("notes", ""))
        is_active = step == active_step

        # Build status line
        marker = clr_cyan(" ◀ active") if is_active else ""
        print(f"  {clr_bold(step)}{marker}")
        print(f"    status:   {status_color(status)}")
        if decision:
            print(f"    decision: {clr_green(decision)}")
        if date:
            print(f"    date:     {clr_dim(date)}")
        if notes:
            print(f"    notes:    {clr_dim(notes)}")
        if status == "planned" and not is_active:
            print(f"    {clr_dim('(not started)')}")
        print()


def main() -> int:
    parser = argparse.ArgumentParser(description="Show sign-off history for all workflow stages and phases.")
    parser.add_argument(
        "--system", choices=["all", "programbuild", "userjourney"], default="all", help="Which system to show log for."
    )
    args = parser.parse_args()

    registry = load_registry()
    systems = [args.system] if args.system != "all" else ["programbuild", "userjourney"]

    for i, system in enumerate(systems):
        if i > 0:
            print()
        if system_is_optional_and_absent(registry, system):
            print(clr_bold(clr_cyan(f"{system.upper()} Sign-off Log")))
            print(clr_dim("not attached in this repository"))
            continue
        print_log(system, registry)

    return 0


if __name__ == "__main__":  # pragma: no cover
    warn_direct_script_invocation("'uv run programstart log' or 'pb log'")
    raise SystemExit(main())
