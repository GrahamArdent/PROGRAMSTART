from __future__ import annotations

from pathlib import Path

CLI_COMMANDS: tuple[str, ...] = (
    "create",
    "init",
    "attach",
    "recommend",
    "impact",
    "research",
    "status",
    "validate",
    "context",
    "retrieval",
    "state",
    "advance",
    "next",
    "log",
    "prompt-eval",
    "progress",
    "guide",
    "drift",
    "bootstrap",
    "clean",
    "refresh",
    "dashboard",
    "serve",
    "health",
    "doctor",
)


def build_cli_module_command(python_executable: str, arguments: list[str]) -> list[str]:
    return [python_executable, "-m", "scripts.programstart_cli", *arguments]


def dashboard_allowed_commands(python_executable: str, scripts_dir: Path) -> dict[str, list[str]]:
    commands = {
        "create.dry": [
            "create",
            "--dest",
            ".tmp_dashboard_create",
            "--project-name",
            "DASHBOARD-CREATE",
            "--product-shape",
            "CLI tool",
            "--dry-run",
        ],
        "context.summary": ["context", "query"],
        "recommend": ["recommend"],
        "impact.workflow": ["impact", "workflow"],
        "research.python-runtime": ["research", "--track", "Python runtime and packaging"],
        "prompt-eval": ["prompt-eval", "--json"],
        "state.show": ["state", "show"],
        "state.show.programbuild": ["state", "show", "--system", "programbuild"],
        "state.show.userjourney": ["state", "show", "--system", "userjourney"],
        "guide.programbuild": ["guide", "--system", "programbuild"],
        "guide.userjourney": ["guide", "--system", "userjourney"],
        "guide.kickoff": ["guide", "--kickoff"],
        "status": ["status"],
        "validate": ["validate"],
        "validate.workflow-state": ["validate", "--check", "workflow-state"],
        "validate.bootstrap-assets": ["validate", "--check", "bootstrap-assets"],
        "validate.rule-enforcement": ["validate", "--check", "rule-enforcement"],
        "log": ["log"],
        "drift": ["drift"],
        "advance.programbuild.dry": ["advance", "--system", "programbuild", "--dry-run"],
        "advance.userjourney.dry": ["advance", "--system", "userjourney", "--dry-run"],
        "advance.programbuild": ["advance", "--system", "programbuild"],
        "advance.userjourney": ["advance", "--system", "userjourney"],
        "progress": ["progress"],
        "dashboard": ["dashboard"],
        "health": ["health"],
        "health.json": ["health", "--json"],
    }

    allowed = {key: build_cli_module_command(python_executable, value) for key, value in commands.items()}
    allowed["smoke.dashboard"] = [python_executable, str(scripts_dir / "programstart_dashboard_smoke.py")]
    allowed["smoke.browser"] = [python_executable, str(scripts_dir / "programstart_dashboard_browser_smoke.py")]
    return allowed
