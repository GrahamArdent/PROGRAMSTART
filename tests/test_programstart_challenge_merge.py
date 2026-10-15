from __future__ import annotations

import base64
import copy
import json
from pathlib import Path

import pytest

from scripts import programstart_challenge_merge as adapter
from scripts.programstart_challenge_merge import MARKER, AdmissionDenied, admit, guarded_merge

REPO = "GrahamArdent/PROGRAMSTART"
HEAD = "a" * 40
POLICY = "b" * 40


def record(*, result="clear", head=HEAD, findings=None, resolutions=None):
    return {
        "repository": REPO,
        "pr": 7,
        "head_sha": head,
        "methodology_sha": POLICY,
        "scope": "repository_merge",
        "result": result,
        "findings": findings or [],
        "resolutions": resolutions or [],
        "evidence_refs": ["https://github.com/owner/review/1"],
    }


def comment(number=1, payload=None, *, user_id=42):
    return {
        "id": number,
        "user": {"id": user_id, "login": "GrahamArdent"},
        "created_at": "2026-10-15T18:00:00Z",
        "updated_at": "2026-10-15T18:00:00Z",
        "body": MARKER + json.dumps(payload if payload is not None else record()),
    }


def snapshot():
    return {
        "methodology_sha": POLICY,
        "repository": {"full_name": REPO, "owner": {"id": 42, "login": "GrahamArdent"}},
        "pull": {
            "number": 7,
            "base": {"repo": {"full_name": REPO}, "sha": "c" * 40},
            "head": {"sha": HEAD},
            "draft": False,
            "state": "open",
            "merged": False,
            "mergeable": True,
            "mergeable_state": "clean",
        },
        "reviews": [],
        "comments": [comment()],
    }


def check(value):
    return admit(value, REPO, 7, HEAD, POLICY)


def test_authenticated_exact_candidate_clear():
    assert len(check(snapshot())) == 64


@pytest.mark.parametrize(
    "mutation",
    [
        lambda s: s["comments"].clear(),
        lambda s: s["comments"][0]["user"].update(id=666),
        lambda s: s["comments"][0]["user"].update(login="attacker"),
        lambda s: s["comments"][0].update(updated_at="2026-10-15T18:01:00Z"),
        lambda s: s["comments"][0].update(body=MARKER + '{"result":"clear"}'),
        lambda s: s["pull"]["head"].update(sha="d" * 40),
        lambda s: s["pull"].update(mergeable=None),
        lambda s: s["pull"].update(mergeable_state="blocked"),
        lambda s: s["pull"].update(draft=True),
        lambda s: s["reviews"].append({"state": "CHANGES_REQUESTED", "commit_id": "d" * 40}),
    ],
)
def test_missing_forged_stale_or_blocking_evidence_denies(mutation):
    value = snapshot()
    mutation(value)
    with pytest.raises(AdmissionDenied):
        check(value)


def test_changed_methodology_invalidates_clear():
    with pytest.raises(AdmissionDenied, match="methodology changed"):
        admit(snapshot(), REPO, 7, HEAD, "e" * 40)


def test_new_clear_does_not_erase_prior_candidate_blocker():
    value = snapshot()
    value["comments"] = [comment(payload=record(result="blocked", head="d" * 40, findings=["F1"])), comment(2)]
    with pytest.raises(AdmissionDenied, match="retained"):
        check(value)
    value["comments"][1] = comment(2, record(resolutions=[{"finding_id": "F1", "evidence_refs": ["proof://current/F1"]}]))
    assert check(value)


def test_old_head_cannot_resolve_current_blocker():
    value = snapshot()
    value["comments"] = [
        comment(payload=record(result="blocked", findings=["F1"])),
        comment(2, record(head="d" * 40, resolutions=[{"finding_id": "F1", "evidence_refs": ["proof://old"]}])),
    ]
    with pytest.raises(AdmissionDenied, match="current candidate"):
        check(value)


def test_historical_resolutions_can_be_reverified_after_head_changes():
    value = snapshot()
    proof = [{"finding_id": "F1", "evidence_refs": ["proof://F1"]}]
    value["comments"] = [
        comment(payload=record(result="blocked", head="d" * 40, findings=["F1"])),
        comment(2, record(head="e" * 40, resolutions=proof)),
        comment(3, record(resolutions=proof)),
    ]
    assert check(value)


def test_legacy_owner_blocker_survives_structured_clear():
    value = snapshot()
    legacy = comment()
    legacy["body"] = "## Exact head review\n\n**Disposition: CHANGES REQUIRED. Do not merge this head.**"
    value["comments"] = [legacy, comment(2)]
    with pytest.raises(AdmissionDenied, match="retained"):
        check(value)
    value["comments"][1] = comment(
        2, record(resolutions=[{"finding_id": "github-comment:1", "evidence_refs": ["proof://legacy-remediation"]}])
    )
    assert check(value)


def test_late_same_head_blocker_prevents_effect():
    original = snapshot()
    late = copy.deepcopy(original)
    late["comments"].append(comment(2, record(result="blocked", findings=["LATE"])))
    reads = iter([original, late])
    effects = []

    def merge(head):
        effects.append(head)
        return {"merged": True, "sha": "f" * 40}

    with pytest.raises(AdmissionDenied):
        guarded_merge(lambda: next(reads), merge, REPO, 7, HEAD, POLICY)
    assert effects == []


def merged(value):
    result = copy.deepcopy(value)
    result["pull"].update(state="closed", merged=True, merge_commit_sha="f" * 40)
    return result


def test_clear_candidate_can_merge_but_never_grants_activation():
    value = snapshot()
    reads = iter([value, value, merged(value)])
    effects = []

    def merge(head):
        effects.append(head)
        return {"merged": True, "sha": "f" * 40}

    result = guarded_merge(lambda: next(reads), merge, REPO, 7, HEAD, POLICY)
    assert effects == [HEAD]
    assert result["status"] == "MERGED_REQUIRES_OWNER_RECONCILIATION"
    assert result["atomic_challenge_fence"] is False
    assert result["activation_permitted"] is False


def test_blocker_in_remote_get_put_gap_is_merged_but_unaccepted():
    value = snapshot()
    late = merged(value)
    late["comments"].append(comment(2, record(result="blocked", findings=["RACE"])))
    reads = iter([value, value, late])
    result = guarded_merge(lambda: next(reads), lambda _: {"merged": True, "sha": "f" * 40}, REPO, 7, HEAD, POLICY)
    assert result["status"] == "MERGED_BUT_UNACCEPTED"
    assert result["activation_permitted"] is False
    assert result["retry_merge"] is False


def test_lost_effect_response_remains_unknown_without_retry():
    value = snapshot()
    calls = []

    def merge(head):
        calls.append(head)
        raise TimeoutError("lost response")

    result = guarded_merge(lambda: value, merge, REPO, 7, HEAD, POLICY)
    assert calls == [HEAD]
    assert result == {"status": "UNKNOWN", "activation_permitted": False, "retry_merge": False}


def test_candidate_modified_consumer_does_not_match_accepted_source(monkeypatch):
    github = adapter.GitHub()
    remote = {"encoding": "base64", "content": base64.b64encode(b"candidate-controlled code").decode()}
    monkeypatch.setattr(github, "api", lambda _: remote)
    with pytest.raises(AdmissionDenied, match="differs from accepted"):
        github.verify_consumer(POLICY)
    remote["content"] = base64.b64encode(Path(adapter.__file__).read_bytes()).decode()
    github.verify_consumer(POLICY)


def test_no_silent_truncation_at_full_api_page(monkeypatch):
    github = adapter.GitHub()
    calls = []

    def api(path):
        calls.append(path)
        return [{"id": i} for i in range(100)] if len(calls) == 1 else [{"id": 101}]

    monkeypatch.setattr(github, "api", api)
    assert len(github.pages("repos/OWNER/REPO/issues/7/comments")) == 101
    assert calls[-1].endswith("page=2")
