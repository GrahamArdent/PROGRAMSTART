WORK_PACKET = "PROGRAMBUILD/PROGRAMBUILD_WORK_PACKET.md"
TEST_STRATEGY = "PROGRAMBUILD/TEST_STRATEGY.md"
CHALLENGE = "PROGRAMBUILD/PROGRAMBUILD_CHALLENGE_GATE.md"


def _read(path: str) -> str:
    with open(path, encoding="utf-8") as handle:
        return handle.read()


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


def test_test_strategy_distinguishes_behavior_evidence_and_acceptance() -> None:
    text = _read(TEST_STRATEGY)
    assert "Cross-System Test Authority" in text
    assert "one behavioral proposition, one test authority" in text
    assert "evidence authority" in text.lower()
    assert "acceptance authority" in text.lower()


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
