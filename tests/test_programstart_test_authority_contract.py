from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORK_PACKET = ROOT / "PROGRAMBUILD" / "PROGRAMBUILD_WORK_PACKET.md"
CHALLENGE = ROOT / "PROGRAMBUILD" / "PROGRAMBUILD_CHALLENGE_GATE.md"
CHECKLIST = ROOT / "PROGRAMBUILD" / "PROGRAMBUILD_CHECKLIST.md"
CANONICAL = ROOT / "PROGRAMBUILD" / "PROGRAMBUILD_CANONICAL.md"
AUTONOMY = ROOT / "docs" / "PROGRAMSTART_EFFECTIVE_AUTONOMY.md"
AGENTS = ROOT / "AGENTS.md"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_material_cross_system_test_has_explicit_authority_envelope() -> None:
    text = _read(WORK_PACKET)
    required = (
        "TEST_ID:",
        "BEHAVIOR_UNDER_TEST:",
        "TEST_AUTHORITY:",
        "GOAL_AUTHORITY:",
        "EXECUTION_AUTHORITY:",
        "PARTICIPATING_SYSTEMS:",
        "START_CONDITION:",
        "AUTHORIZED_TEST_EFFECTS:",
        "PROHIBITED_TEST_EFFECTS:",
        "OBSERVABLE_SUCCESS:",
        "OBSERVABLE_FAILURE:",
        "EVIDENCE_PRODUCERS:",
        "EVIDENCE_AUTHORITY:",
        "ACCEPTANCE_AUTHORITY:",
        "STOP_CONDITION:",
        "CLEANUP_OWNER:",
        "OWNER_HANDOFFS:",
    )
    for token in required:
        assert token in text


def test_test_authority_is_not_execution_or_evidence_authority() -> None:
    text = _read(WORK_PACKET)
    assert "exactly one `TEST_AUTHORITY`" in text
    assert "TEST_AUTHORITY does not grant execution authority" in text
    assert "Evidence authority validates evidence" in text
    assert "Participation does not transfer backlog, closure, or execution ownership" in text


def test_foreign_observations_become_handoffs_not_shadow_closure() -> None:
    text = _read(WORK_PACKET).lower()
    assert "cross-owner test finding / handoff rule" in text
    assert "mere participation or observation is not a closure dependency" in text
    assert "must not remain as an unchecked foreign-owner closure item" in text


def test_accepted_recommendation_obligations_are_bounded_and_terminal() -> None:
    text = _read(WORK_PACKET)
    lower = text.lower()
    assert "material independently dispositionable obligations" in lower
    for disposition in (
        "implemented_and_accepted",
        "rejected_with_evidence",
        "superseded_by_accepted_solution",
        "explicitly_deferred_to_owner",
    ):
        assert disposition in text
    assert "receiving owner implemented or accepted the work" in lower
    assert "trivial recommendations" in lower
    assert "global obligation registry" in lower


def test_challenge_checks_test_scope_and_chat_detachment() -> None:
    text = _read(CHALLENGE)
    assert "test authority" in text.lower()
    assert "test envelope" in text.lower()
    assert "chat" in text.lower()
    assert "participant" in text.lower()


def test_recovery_challenge_matches_health_claim_to_useful_progress() -> None:
    text = _read(CHALLENGE).lower()
    assert "identify the normal control path and the recovery path" in text
    assert "useful end-to-end transaction/progress proof" in text
    assert "no recovery claim may depend exclusively on the mechanism it is responsible for repairing" in text
    assert "no capability-health claim may be stronger than the transaction/progress evidence actually observed" in text


def test_uncertain_concepts_are_falsifiable_and_exploration_is_bounded() -> None:
    work_packet = _read(WORK_PACKET)
    autonomy = _read(AUTONOMY)
    canonical = _read(CANONICAL)

    for token in (
        "CONCEPT:",
        "MINIMUM_FALSIFICATION_TEST:",
        "FALSIFICATION_CONDITION:",
        "CONCEPT_STATUS: [untested | supported | inconclusive | falsified]",
        "EXPLORATION_BUDGET:",
        "LAST_ATTEMPT_DELTA:",
    ):
        assert token in work_packet

    assert "expected information value" in autonomy
    assert "not by a universal retry count" in autonomy
    assert "A repeated attempt is justified only when **something material changed**" in autonomy
    assert "A falsified concept MUST NOT be kept alive" in canonical


def test_human_gate_requires_technical_readiness_and_human_only_remainder() -> None:
    work_packet = _read(WORK_PACKET)
    autonomy = _read(AUTONOMY)
    checklist = _read(CHECKLIST)
    challenge = _read(CHALLENGE)

    assert "GATE_READINESS: [not_ready | ready]" in work_packet
    assert "HUMAN_ONLY_REMAINDER:" in work_packet
    assert "An automation failure count by itself can never make a gate ready" in work_packet
    assert "Human attention is a protected resource" in autonomy
    assert "the human is not the debugger of unvalidated machine instructions" in autonomy
    assert "before notifying the operator, establish `GATE_READINESS: ready`" in checklist
    assert "human-gate readiness" in challenge.lower()
    assert "operator had to correct command syntax" in challenge.lower()


def test_codex_execution_contract_routes_to_methodology_without_becoming_authority() -> None:
    agents = _read(AGENTS)
    canonical = _read(CANONICAL)

    assert "PROGRAMSTART Execution Contract" in agents
    assert "PROGRAMBUILD/PROGRAMBUILD_CANONICAL.md" in agents
    assert "docs/PROGRAMSTART_EFFECTIVE_AUTONOMY.md" in agents
    assert "Concept viability before implementation persistence" in agents
    assert "Human attention / credentials / manual boundaries" in agents
    assert "Final self-review requirement" in agents
    assert "does not replace PROGRAMSTART project/methodology authority" in agents
    assert "`AGENTS.md`/`AGENTS.override.md`" in canonical


def test_final_self_review_makes_changed_mind_and_failures_explicit() -> None:
    agents = _read(AGENTS).lower()
    assert "which goals were achieved" in agents
    assert "which were not achieved and why" in agents
    assert "material change of mind" in agents
    assert "verification limitations or unresolved blockers" in agents
