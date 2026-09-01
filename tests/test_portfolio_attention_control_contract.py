import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "PROGRAMBUILD" / "PROGRAMBUILD_PORTFOLIO_CONTROL.md"
REGISTRY_TEMPLATE = ROOT / "templates" / "portfolio" / "PROJECT_REGISTRY.yaml"
STATUS_TEMPLATE = ROOT / "templates" / "portfolio" / "PORTFOLIO_STATUS.md"
HISTORY_TEMPLATE = ROOT / "templates" / "portfolio" / "PORTFOLIO_HISTORY.md"
COPILOT_INSTRUCTIONS = ROOT / ".github" / "copilot-instructions.md"
WHAT_NEXT_PROMPT = ROOT / ".github" / "prompts" / "programstart-what-next.prompt.md"
PROGRAMBUILD_REGISTRY = (
    ROOT / "config" / "registry" / "systems" / "programbuild.json"
)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_portfolio_control_keeps_live_state_outside_programstart() -> None:
    text = _read(PROTOCOL)
    assert "live global project registry" in text
    assert "operator's planning workspace" in text
    assert "PROGRAMSTART / PROGRAMBUILD MUST NOT own" in text
    assert "filled live portfolio" in text
    assert "portfolio is stale" in text


def test_attention_classes_are_not_project_lifecycle_states() -> None:
    text = _read(PROTOCOL)
    values = (
        "PRIMARY_BUILD",
        "OPERATOR_GATE",
        "SECONDARY_READY",
        "WATCH",
        "PARKED",
        "UNASSESSED",
    )
    for value in values:
        assert value in text
    assert "They are not project lifecycle states" in text
    assert "Staleness is not urgency" in text


def test_default_wip_is_bounded() -> None:
    text = _read(PROTOCOL)
    assert "maximum **one `PRIMARY_BUILD`**" in text
    assert "maximum **one `OPERATOR_GATE`**" in text
    assert "maximum **one `SECONDARY_READY`**" in text
    needle = "not permission to run a second consequential build in parallel"
    assert needle in text


def test_project_authority_and_safe_execution_converge_after_selection() -> None:
    text = _read(PROTOCOL)
    authority = "Portfolio control does not become project execution authority"
    assert authority in text
    assert "Selection is nevertheless the start of execution" in text
    assert "enter PROGRAMSTART Mode C" in text
    assert "open branches/PRs" in text
    assert "resume the actual project frontier" in text

    classes = ("`AUTO`", "`PR_ONLY`", "`HUMAN_GATE`", "`BLOCKED`")
    for value in classes:
        assert value in text

    assert "actually attempt the bounded action" in text
    refresh_rule = "status-file refresh does **not** count as successful progression"
    assert refresh_rule in text
    assert "green CI/check result is evidence, not convergence" in text
    assert "reconcile the owning project inside its own repository first" in text
    assert "The portfolio never closes a project milestone" in text


def test_templates_remain_non_authoritative_and_lightweight() -> None:
    registry = _read(REGISTRY_TEMPLATE)
    status = _read(STATUS_TEMPLATE)
    history = _read(HISTORY_TEMPLATE)

    assert "Reusable schema/example only" in registry
    assert "canonical for no" in registry.lower()
    assert "One operator gate + one primary build" not in status
    assert "Canonical for no project's execution state" in status
    assert "Do not mirror repository commits" in history


def test_startup_instructions_reconcile_portfolio_checkpoints() -> None:
    text = _read(COPILOT_INSTRUCTIONS)

    assert "## Portfolio Attention Checkpoints" in text
    broad_scan = "Do **not** read, rebuild, or refresh a live portfolio workspace"
    assert broad_scan in text
    assert "meaningful portfolio checkpoint" in text
    assert "already-authorized live external portfolio workspace" in text
    assert "reconcile only the current project's row" in text
    assert "Report portfolio reconciliation as pending" in text
    assert "Staleness is never urgency" in text


def test_what_next_prompt_routes_portfolio_questions_without_broad_scan() -> None:
    text = _read(WHAT_NEXT_PROMPT)

    assert 'version: "2.1"' in text
    assert "## Scope Resolution" in text
    assert "**Portfolio scope**" in text
    assert "## Portfolio-Scope Protocol" in text
    assert "Do not rebuild the portfolio from scratch" in text
    for value in ("OPERATOR_GATE", "PRIMARY_BUILD", "SECONDARY_READY"):
        assert value in text
    handoff = "hand execution back to that project's Mode-C authority"
    assert handoff in text


def test_portfolio_protocol_is_programbuild_control_file() -> None:
    registry = json.loads(_read(PROGRAMBUILD_REGISTRY))
    controls = registry["systems"]["programbuild"]["control_files"]
    assert "PROGRAMBUILD/PROGRAMBUILD_PORTFOLIO_CONTROL.md" in controls
