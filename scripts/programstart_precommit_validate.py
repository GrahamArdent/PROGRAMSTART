from __future__ import annotations

try:
    from . import programstart_validate
    from .programstart_common import load_registry, warn_direct_script_invocation
    from .programstart_prompt_build import ROOT, sync_managed_prompts
except ImportError:  # pragma: no cover - standalone script execution fallback
    import programstart_validate
    from programstart_prompt_build import ROOT, sync_managed_prompts

    from programstart_common import load_registry, warn_direct_script_invocation


def main() -> int:
    registry = load_registry()
    written = sync_managed_prompts(registry)
    for path in written:
        print(f"Wrote {path.relative_to(ROOT).as_posix()}")
    return programstart_validate.main(["--check", "all", "--strict"])


if __name__ == "__main__":
    warn_direct_script_invocation("'uv run python scripts/programstart_precommit_validate.py'")
    raise SystemExit(main())
