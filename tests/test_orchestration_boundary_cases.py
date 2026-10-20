"""Mode/environment conflicts are rejected; local dependency guidance stays explicit."""

from typing import Any

import pytest

from scripts.programstart_orchestrate import build_plan, main


@pytest.mark.parametrize(
    "updates,reason",
    [
        ({"repo": "/tmp/project", "repository": "owner/project"}, "either"),
        ({"environment": "local", "repository": "owner/project"}, "requires connected-tools"),
        ({"mode": "c", "repo": "/tmp/project", "research_backed": True}, "compatible only"),
        ({"request": " "}, "must not be empty"),
        ({"mode": "c", "repository": "owner/project", "related_repository": "owner/project"}, "different"),
    ],
)
def test_conflicting_or_empty_requests_fail_before_handoff(updates, reason):
    values: dict[str, Any] = dict(request="Continue current scope")
    values.update(updates)
    with pytest.raises(ValueError, match=reason):
        build_plan(**values)


@pytest.mark.parametrize("state", ["unknown", "unsatisfied", "satisfied"])
def test_local_mode_c_retains_related_owner_and_dependency_disposition(state):
    plan = build_plan(
        request="Continue accepted local scope",
        repo="/tmp/project",
        mode="c",
        environment="local",
        related_repository="owner/producer",
        relationship_type="product_contract",
        dependency_state=state,
    )
    assert plan.mode == "c" and plan.environment == "local"
    assert any("target --repo" in text for text in plan.orientation_actions)
    assert any("owner/producer" in text for text in plan.orientation_actions)
    text = " ".join(plan.cross_repository_guidance)
    if state == "satisfied":
        assert "reuse it" in text
    elif state == "unsatisfied":
        assert "prerequisite" in text
    else:
        assert "determine whether" in text
    assert any("central PROGRAMSTART target" in text for text in plan.execution_handoff)


def test_local_mode_c_without_related_repository_is_complete():
    plan = build_plan(request="Continue", repo="/tmp/project", mode="c")
    assert plan.related_repositories == ()
    assert any("central PROGRAMSTART target" in text for text in plan.execution_handoff)


def test_cli_invalid_request_reports_parser_error():
    with pytest.raises(SystemExit) as exc:
        main(["--request", " "])
    assert exc.value.code == 2
