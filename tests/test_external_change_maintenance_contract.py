from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "docs" / "PROGRAMSTART_EXTERNAL_CHANGE_MAINTENANCE.md"
COPILOT_INSTRUCTIONS = ROOT / ".github" / "copilot-instructions.md"
FILE_INDEX = ROOT / "PROGRAMBUILD" / "PROGRAMBUILD_FILE_INDEX.md"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_external_change_protocol_uses_bounded_classification() -> None:
    text = _read(PROTOCOL)

    for value in (
        "no_effect",
        "evidence_refresh",
        "deterministic_maintenance",
        "bounded_behavioral_maintenance",
        "material_decision",
        "automation_failed",
    ):
        assert value in text

    assert "External monitoring should normally terminate in **maintenance**, not merely notification" in text
    assert "External news is evidence" not in text  # startup shorthand belongs in agent instructions
    assert "A monitoring event is evidence. It is not authority" in text


def test_deterministic_maintenance_does_not_erase_stronger_gates() -> None:
    text = _read(PROTOCOL)

    assert "Automatic PR creation and automatic merge are different trust levels" in text
    assert "target repository policy explicitly enables auto-merge" in text
    assert "required branch/ruleset/status/convergence gates are actually enforced and green" in text
    assert "If the repository lacks an explicit auto-merge policy" in text
    assert "the safe default is **PR-only**" in text
    assert "Do not weaken branch protection" in text


def test_external_change_protocol_preserves_project_and_portfolio_boundaries() -> None:
    text = _read(PROTOCOL)

    assert "MUST NOT mutate them as one portfolio transaction" in text
    assert "use a separate branch/PR/evidence boundary for that repository" in text
    assert "leave project sequencing, release, and closure decisions with the owning project authority" in text


def test_watchtower_is_optional_sensor_and_cannot_self_authorize_mutation() -> None:
    text = _read(PROTOCOL)

    assert "Watchtower is a natural optional **sensor / incident / evidence / later execution-plane partner**" in text
    assert "If Watchtower's current authority is observe-only" in text
    assert "PROGRAMSTART MUST treat it as a sensor/evidence source only" in text
    assert "Watchtower must not infer that detection alone authorizes a repository mutation" in text


def test_startup_instructions_route_external_changes_to_protocol() -> None:
    text = _read(COPILOT_INSTRUCTIONS)

    assert "## External Change Maintenance" in text
    assert "docs/PROGRAMSTART_EXTERNAL_CHANGE_MAINTENANCE.md" in text
    assert "Do not terminate at notification when the correct response is safely deterministic" in text
    assert "Auto-merge is a stronger trust level than automatic PR creation" in text
    assert "Watchtower may supply authenticated/deduplicated incident evidence" in text


def test_file_index_registers_support_protocol_without_project_authority() -> None:
    text = _read(FILE_INDEX)

    assert "docs/PROGRAMSTART_EXTERNAL_CHANGE_MAINTENANCE.md" in text
    assert "subordinate to project authority" in text
    assert "external-change maintenance classification/event is derived operational evidence" in text
    assert "never becomes architecture, budget, release, portfolio, or project authority by itself" in text
