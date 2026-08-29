from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLANNING = ROOT / "PROGRAMBUILD" / "PROGRAMBUILD_PLANNING_OPERATING_MODEL.md"
CANONICAL = ROOT / "PROGRAMBUILD" / "PROGRAMBUILD_CANONICAL.md"
IDEA_INTAKE = ROOT / "PROGRAMBUILD" / "PROGRAMBUILD_IDEA_INTAKE.md"
IDEA_LEDGER = ROOT / "PROGRAMBUILD" / "IDEA_LEDGER.md"
FILE_INDEX = ROOT / "PROGRAMBUILD" / "PROGRAMBUILD_FILE_INDEX.md"
ORCHESTRATION_PROMPT = (
    ROOT / ".github" / "prompts" / "start-programstart-project.prompt.md"
)
PROGRAMBUILD_REGISTRY = ROOT / "config" / "registry" / "systems" / "programbuild.json"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_capture_is_distinct_from_promotion_and_execution() -> None:
    planning = _read(PLANNING)

    assert "Capture broadly. Promote deliberately. Execute only from authority." in planning
    assert "**Capture** — preserve an idea because it is worth remembering." in planning
    assert "**Promote** — deliberately evaluate/adopt the idea" in planning
    assert "**Execute** — perform work only after current authority permits it." in planning
    assert "Not authority-worthy does not mean not worth remembering." in planning


def test_idea_ledger_supports_non_authoritative_lifecycle() -> None:
    ledger = _read(IDEA_LEDGER)

    for status in (
        "CAPTURED",
        "CANDIDATE",
        "INVESTIGATING",
        "SHELVED",
        "ACCEPTED",
        "REJECTED",
        "SUPERSEDED",
    ):
        assert status in ledger

    assert "This was worth remembering." in ledger
    assert "does **not** mean" in ledger
    assert "Promotion Rule" in ledger
    assert "execute only from that reconciled authority" in ledger


def test_capture_does_not_require_full_idea_intake() -> None:
    intake = _read(IDEA_INTAKE)
    prompt = _read(ORCHESTRATION_PROMPT)

    assert "not** required merely to preserve a worthwhile idea" in intake
    assert "Do **not** require this protocol just to save an interesting idea" in intake
    assert "do not launch Idea Intake merely to save it" in prompt
    assert "Do not force every captured idea through full Idea Intake" in prompt


def test_captured_idea_cannot_become_authority_by_storage() -> None:
    canonical = _read(CANONICAL)
    planning = _read(PLANNING)
    prompt = _read(ORCHESTRATION_PROMPT)

    assert "recording it MUST NOT imply priority, scope, sequencing, budget, architecture, or permission to execute" in canonical
    assert "capture status does not imply priority" in planning
    assert "Idea Records never substitute for it" in prompt


def test_live_portfolio_idea_state_stays_outside_programstart() -> None:
    canonical = _read(CANONICAL)
    ledger = _read(IDEA_LEDGER)
    prompt = _read(ORCHESTRATION_PROMPT)

    assert "A live cross-project idea portfolio MUST NOT be stored in PROGRAMSTART itself" in canonical
    assert "portfolio-wide instance belongs in the operator's planning workspace" in ledger
    assert "Do not make PROGRAMSTART itself the operator's live portfolio-wide idea registry" in prompt


def test_optional_ledger_is_not_auto_materialized_in_every_generated_project() -> None:
    index = _read(FILE_INDEX)
    registry = _read(PROGRAMBUILD_REGISTRY)

    assert "`IDEA_LEDGER.md` | derived/reference output | optional" in index
    assert '"PROGRAMBUILD/IDEA_LEDGER.md"' not in registry


def test_shelved_and_rejected_reasoning_is_preserved_for_revisit() -> None:
    ledger = _read(IDEA_LEDGER)
    intake = _read(IDEA_INTAKE)

    assert "Do not delete useful reasoning merely because the idea is not current." in ledger
    assert "preserve the rationale and any evidence that would justify reconsideration" in ledger
    assert "preserve enough rationale to avoid repeating the same analysis later" in intake
