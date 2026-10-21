"""Conditional executable-route guidance is retained across existing PROGRAMSTART emitters.

Structural coverage here is not real ChatGPT fresh-context tool invocation or
mechanical interception of arbitrary built-in connector calls.
"""

import json
from pathlib import Path

from scripts.programstart_intent_compile import (
    AuthoritySnapshot, IntentKind, compile_work_packet, render_chatgpt_prompt,
)
from scripts.programstart_orchestrate import build_plan, render_text
from scripts.programstart_prompt_build import build_context_prompt, build_prompt

ROOT = Path(__file__).resolve().parents[1]


def test_registry_and_context_stage_prompts_keep_recovery_rules() -> None:
    for output in (
        build_prompt("implementation_loop"),
        build_context_prompt({"goal": "Verify private research publication"}),
    ):
        assert "actor, effect, exact target" in output
        assert "actually connected in this execution session" in output
        assert "first callable tool/action" in output
        assert "DIAGNOSE_LOOKUP_FAILURE" in output
        assert "generic operator-retry request" in output
        assert "ESCALATION_NOT_PRECLUDED_BY_PATHS" in output
        assert "original identity" in output
        assert "control-plane write" in output
        assert "Independently verify the actual target" in output


def test_connected_orchestration_includes_real_lookup_continuation() -> None:
    plan = build_plan(
        request="Verify the existing JoyHub repo publication",
        repository="GrahamArdent/joyhub-research",
        environment="connected-tools", mode="c",
    )
    output = render_text(plan)
    assert "actor/effect/exact target" in output
    assert "first callable action" in output
    assert "DIAGNOSE_LOOKUP_FAILURE" in output
    assert "generic operator retry" in output
    assert "ESCALATION_NOT_PRECLUDED_BY_PATHS" in output
    assert "original identity" in output
    assert "control-plane state" in output
    assert "Verify the actual target" in output


def test_unresolved_entry_mode_does_not_drop_continuation() -> None:
    plan = build_plan(
        request="Continue a repository workflow",
        repository="GrahamArdent/joyhub-research",
    )
    assert plan.mode == "unresolved"
    assert any("DIAGNOSE_LOOKUP_FAILURE" in x for x in plan.execution_handoff)
    assert any("original identity" in x for x in plan.execution_handoff)


def test_sealed_chatgpt_prompt_preserves_effect_route_and_scope() -> None:
    fixture = ROOT / "tests/fixtures/intent_compilation/real_cases.json"
    cases = json.loads(fixture.read_text(encoding="utf-8"))["cases"]
    case = next(c for c in cases if c["name"] == "resume_creator_parallel_safe_continuation")
    authority = AuthoritySnapshot.model_validate(case["authority"])
    packet = compile_work_packet(case["intent"], authority, kind=IntentKind.CONTINUATION)
    output = render_chatgpt_prompt(packet)
    assert "This rendered prompt grants no authority" in output
    assert "Mutable surfaces:" in output
    assert "first callable action" in output
    assert "DIAGNOSE_LOOKUP_FAILURE" in output
    assert "original identity" in output
    assert "independent target readback" in output


def test_cycle_challenge_requires_real_action_and_no_false_escalation() -> None:
    content = (ROOT / ".github/prompts/programstart-convergence-packet.prompt.md").read_text(encoding="utf-8")
    assert "first" in content and "actually callable connected tool" in content
    assert "same-attempt unknown-result recovery" in content
    assert "global-unavailability claim" in content
    assert "control-plane write" in content
