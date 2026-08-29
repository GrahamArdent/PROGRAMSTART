from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLANNING = ROOT / "PROGRAMBUILD" / "PROGRAMBUILD_PLANNING_OPERATING_MODEL.md"
WORK_PACKET = ROOT / "PROGRAMBUILD" / "PROGRAMBUILD_WORK_PACKET.md"
CHECKLIST = ROOT / "PROGRAMBUILD" / "PROGRAMBUILD_CHECKLIST.md"
ORCHESTRATION_PROMPT = ROOT / ".github" / "prompts" / "start-programstart-project.prompt.md"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_ordinary_accepted_recommendation_executes_without_master_churn() -> None:
    planning = _read(PLANNING)

    assert "execute_current_authority" in planning
    assert "do not rewrite the Master/strategic spine merely because an implementation detail" in planning
    assert "ordinary bug fixes already required by the current slice" in planning


def test_authority_delta_reconciles_before_or_atomically_with_execution() -> None:
    planning = _read(PLANNING)
    packet = _read(WORK_PACKET)

    assert "reconcile_authority_then_execute" in planning
    assert "before or atomically with dependent implementation" in planning
    assert "AUTHORITY_RECONCILIATION_BEFORE_EXECUTION" in packet


def test_future_accepted_recommendation_does_not_resequence_mode_c() -> None:
    planning = _read(PLANNING)
    prompt = _read(ORCHESTRATION_PROMPT)

    assert "defer_without_resequencing" in planning
    assert "do not reorder the active spine merely because the operator liked the idea" in planning
    assert "do not resequence the current Master merely because the operator liked the idea" in prompt
    assert "Never restart the project at Stage 0" in prompt


def test_generic_acceptance_preserves_stronger_consequence_gate() -> None:
    planning = _read(PLANNING)
    packet = _read(WORK_PACKET)
    prompt = _read(ORCHESTRATION_PROMPT)

    assert "independent gate overlay" in planning
    assert "STRONGER_GATE_OVERLAY" in packet
    assert "MUST NOT silently satisfy a stronger gate" in prompt


def test_disproved_recommendation_is_not_forced_through() -> None:
    planning = _read(PLANNING)
    packet = _read(WORK_PACKET)

    assert "do not force the accepted recommendation through" in planning
    assert "actual evidence rather than forcing the original recommendation through" in packet


def test_proceed_resolution_does_not_create_second_spine_or_hidden_backlog() -> None:
    planning = _read(PLANNING)
    packet = _read(WORK_PACKET)
    prompt = _read(ORCHESTRATION_PROMPT)

    assert "do not create a hidden PROGRAMSTART backlog" in planning
    assert "a recommendation registry or hidden future-work queue" in packet
    assert "not an entry mode or second project state machine" in prompt


def test_active_checklist_requires_every_applicable_item_to_be_reconciled() -> None:
    planning = _read(PLANNING)
    packet = _read(WORK_PACKET)
    checklist = _read(CHECKLIST)

    expected_statuses = (
        "satisfied",
        "not applicable",
        "blocked",
        "deferred",
    )
    for status in expected_statuses:
        assert status in planning
        assert status in packet

    assert "unresolved required items prevent truthful `complete`/`merge-ready` status" in planning
    assert "Do not declare work complete while an applicable required item is merely forgotten" in checklist


def test_trivial_work_does_not_require_large_persistent_checklist() -> None:
    planning = _read(PLANNING)
    packet = _read(WORK_PACKET)
    checklist = _read(CHECKLIST)

    assert "Do not create a large checklist artifact for trivial low-risk single-step work" in planning
    assert "`COMPLETENESS_CHECKLIST` is `not_needed` for trivial work" in packet
    assert "Do not create a large persisted checklist for a trivial, low-risk, single-step change" in checklist


def test_agent_orchestration_handles_natural_language_without_new_cli_state_machine() -> None:
    prompt = _read(ORCHESTRATION_PROMPT)

    assert 'version: "2.8"' in prompt
    assert "is a valid orchestration input when the prior concrete recommendation is available" in prompt
    assert "MUST NOT be replaced with brittle keyword parsing or a new operator-maintained recommendation state machine" in prompt


def test_checklist_remains_derived_and_cannot_create_scope() -> None:
    checklist = _read(CHECKLIST)
    packet = _read(WORK_PACKET)

    assert "derived completeness / verification surface" in checklist
    assert "never let a checklist item silently create new project scope or sequencing" in checklist
    assert "a checklist that can invent scope" in packet
