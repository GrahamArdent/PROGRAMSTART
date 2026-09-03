from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "docs" / "PROGRAMSTART_AUTHORITY_GAP_RECONCILIATION.md"
CHECKLIST = ROOT / "PROGRAMBUILD" / "PROGRAMBUILD_CHECKLIST.md"
PLANNING = ROOT / "PROGRAMBUILD" / "PROGRAMBUILD_PLANNING_OPERATING_MODEL.md"
LEARNING = ROOT / "docs" / "PROGRAMSTART_LEARNING_LOOP.md"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_derived_finding_never_becomes_execution_authority() -> None:
    protocol = _read(PROTOCOL)
    checklist = _read(CHECKLIST)

    assert "A derived finding may discover missing work, but it cannot create execution authority" in protocol
    assert "must not execute as authority" in checklist
    assert "routing condition, not a new project state" in protocol


def test_authority_gap_reuses_existing_mode_c_reconciliation() -> None:
    protocol = _read(PROTOCOL)
    planning = _read(PLANNING)

    assert "reconcile_authority_then_execute" in protocol
    assert "reconcile_authority_then_execute" in planning
    assert "Do not use `AUTHORITY_GAP` as a fourth accepted-recommendation disposition" in protocol
    assert "before or atomically with dependent implementation" in protocol


def test_unowned_finding_stays_non_authoritative() -> None:
    protocol = _read(PROTOCOL)

    assert "No legitimate owner yet" in protocol
    assert "do not execute from the derived finding" in protocol
    assert "create a new project/repository only when normal PROGRAMSTART idea/promotion rules earn it" in protocol


def test_authority_gap_routes_learning_without_creating_mandatory_new_lesson() -> None:
    protocol = _read(PROTOCOL)
    learning = _read(LEARNING)

    assert "Why was the material finding absent or mismatched?" in protocol
    assert "Search the existing learning ledger before creating a new lesson" in protocol
    assert "no reusable lesson" in learning
    assert "prefer extending an existing mechanism over adding a new lifecycle/artifact/agent" in learning


def test_originating_flow_resumes_after_reconciliation() -> None:
    protocol = _read(PROTOCOL)

    assert "Return to the originating flow" in protocol
    assert "do not require a redundant generic `proceed`" in protocol
    assert "Continue the Autonomy Closure Checklist" in protocol


def test_checklist_integration_invokes_authority_gap_protocol() -> None:
    checklist = _read(CHECKLIST)

    assert "PROGRAMSTART_AUTHORITY_GAP_RECONCILIATION.md" in checklist
    assert "no checklist/audit silently became authority" in checklist
    assert "existing Learning Gate" in checklist
