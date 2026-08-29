from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "PROGRAMBUILD" / "PROGRAMBUILD_PORTFOLIO_CONTROL.md"
REGISTRY_TEMPLATE = ROOT / "templates" / "portfolio" / "PROJECT_REGISTRY.yaml"
STATUS_TEMPLATE = ROOT / "templates" / "portfolio" / "PORTFOLIO_STATUS.md"
HISTORY_TEMPLATE = ROOT / "templates" / "portfolio" / "PORTFOLIO_HISTORY.md"


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
    for value in (
        "PRIMARY_BUILD",
        "OPERATOR_GATE",
        "SECONDARY_READY",
        "WATCH",
        "PARKED",
        "UNASSESSED",
    ):
        assert value in text
    assert "They are not project lifecycle states" in text
    assert "Staleness is not urgency" in text


def test_default_wip_is_bounded() -> None:
    text = _read(PROTOCOL)
    assert 'maximum **one `PRIMARY_BUILD`**' in text
    assert 'maximum **one `OPERATOR_GATE`**' in text
    assert 'maximum **one `SECONDARY_READY`**' in text
    assert "not permission to run a second consequential build in parallel" in text


def test_project_authority_takes_over_after_selection() -> None:
    text = _read(PROTOCOL)
    assert "Portfolio control ends when a project is selected" in text
    assert "enter PROGRAMSTART Mode C" in text
    assert "project’s own execution spine" in text or "project's current execution spine" in text
    assert "The portfolio never closes a project milestone" in text


def test_templates_remain_non_authoritative_and_lightweight() -> None:
    registry = _read(REGISTRY_TEMPLATE)
    status = _read(STATUS_TEMPLATE)
    history = _read(HISTORY_TEMPLATE)

    assert "Reusable schema/example only" in registry
    assert "canonical for no" in registry.lower()
    assert "One operator gate + one primary build" not in status  # template stays generic
    assert "Canonical for no project's execution state" in status
    assert "Do not mirror repository commits" in history
