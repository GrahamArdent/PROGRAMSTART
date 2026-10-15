from __future__ import annotations

import base64
import copy
import hashlib
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
        "target_ref": "refs/heads/main",
        "target_sha": "c" * 40,
        "repository": {"full_name": REPO, "owner": {"id": 42, "login": "GrahamArdent"}},
        "pull": {
            "number": 7,
            "base": {"repo": {"full_name": REPO}, "ref": "main", "sha": "c" * 40},
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


def withdrawal(target, number=3, **overrides):
    payload = {
        "repository": REPO,
        "pr": 7,
        "comment_id": target["id"],
        "body_sha256": hashlib.sha256(target["body"].encode()).hexdigest(),
        "reason": "withdraw positive assertion; append a corrected review",
        "evidence_refs": ["proof://actual-owner-correction"],
    }
    payload.update(overrides)
    value = comment(number)
    value["body"] = adapter.WITHDRAWAL_MARKER + json.dumps(payload)
    return value


def test_malformed_positive_record_requires_exact_owner_withdrawal_then_new_clear():
    value = snapshot()
    bad = comment(2, record(resolutions=[{"finding_id": "unknown", "evidence_refs": ["proof://unretained"]}]))
    value["comments"] = [comment(), bad]
    with pytest.raises(AdmissionDenied):
        check(value)
    value["comments"].append(withdrawal(bad))
    with pytest.raises(AdmissionDenied, match="no authenticated exact-head CLEAR"):
        check(value)  # older CLEAR must not silently revive
    value["comments"].append(comment(4))
    assert check(value)


def test_withdrawing_clear_restores_its_resolved_blockers():
    value = snapshot()
    block = comment(1, record(result="blocked", findings=["F1"]))
    clear = comment(2, record(resolutions=[{"finding_id": "F1", "evidence_refs": ["proof://actual"]}]))
    value["comments"] = [block, clear]
    assert check(value)
    value["comments"].extend([withdrawal(clear), comment(4)])
    with pytest.raises(AdmissionDenied, match="retained"):
        check(value)
    value["comments"][-1] = comment(4, record(resolutions=[{"finding_id": "F1", "evidence_refs": ["proof://fresh"]}]))
    assert check(value)


@pytest.mark.parametrize(
    "mutation",
    [
        lambda w: w["user"].update(id=666),
        lambda w: w["user"].update(login="other"),
        lambda w: w.update(updated_at="2026-10-15T19:00:00Z"),
    ],
)
def test_forged_or_edited_withdrawal_never_cures_bad_positive(mutation):
    value = snapshot()
    bad = comment(1, record(resolutions=[{"finding_id": "unknown", "evidence_refs": ["proof://x"]}]))
    w = withdrawal(bad, 2)
    mutation(w)
    value["comments"] = [bad, w, comment(3)]
    with pytest.raises(AdmissionDenied):
        check(value)


@pytest.mark.parametrize(
    "overrides",
    [
        {"comment_id": True},
        {"comment_id": 4},
        {"comment_id": 999},
        {"body_sha256": "0" * 64},
        {"repository": "foreign/repo"},
        {"pr": True},
        {"reason": ""},
        {"evidence_refs": []},
    ],
)
def test_unknown_moved_or_unbound_withdrawal_denies(overrides):
    value = snapshot()
    target = value["comments"][0]
    value["comments"].extend([withdrawal(target, 2, **overrides), comment(3)])
    with pytest.raises(AdmissionDenied):
        check(value)


@pytest.mark.parametrize("legacy", [False, True])
def test_blocked_or_legacy_negative_record_cannot_be_withdrawn(legacy):
    value = snapshot()
    target = comment(1, record(result="blocked", findings=["F1"]))
    if legacy:
        target["body"] = "CHANGES REQUIRED. Actual material blocker."
    value["comments"] = [target, withdrawal(target, 2), comment(3)]
    with pytest.raises(AdmissionDenied):
        check(value)


def test_revocation_after_another_clear_requires_a_still_later_clear():
    value = snapshot()
    first = comment()
    value["comments"] = [first, comment(2), withdrawal(first, 3)]
    with pytest.raises(AdmissionDenied):
        check(value)
    value["comments"].append(comment(4))
    assert check(value)


def test_revocation_on_confirmation_read_holds_the_effect():
    before = snapshot()
    confirmation = copy.deepcopy(before)
    confirmation["comments"].append(withdrawal(before["comments"][0], 2))
    reads = iter([before, confirmation])
    calls = []

    def merge(head):
        calls.append(head)
        return {"merged": True, "sha": "f" * 40}

    with pytest.raises(AdmissionDenied):
        guarded_merge(lambda: next(reads), merge, REPO, 7, HEAD, POLICY)
    assert calls == []


def test_revocation_in_remote_gap_is_merged_but_unaccepted():
    before = snapshot()
    after = merged(before)
    after["comments"].append(withdrawal(before["comments"][0], 2))
    reads = iter([before, before, after])
    calls = []

    def merge(head):
        calls.append(head)
        return {"merged": True, "sha": "f" * 40}

    result = guarded_merge(lambda: next(reads), merge, REPO, 7, HEAD, POLICY)
    assert calls == [HEAD]
    assert result["status"] == "MERGED_BUT_UNACCEPTED"
    assert result["activation_permitted"] is False and result["retry_merge"] is False


def test_edited_or_deleted_target_and_duplicate_json_cannot_be_withdrawn():
    for change in ("edited", "deleted", "duplicate"):
        value = snapshot()
        target = value["comments"][0]
        w = withdrawal(target, 2)
        if change == "edited":
            target["updated_at"] = "2026-10-15T19:00:00Z"
        elif change == "deleted":
            value["comments"].clear()
        else:
            w["body"] = w["body"].replace("{", '{"pr": 7,', 1)
        value["comments"].extend([w, comment(3)])
        with pytest.raises(AdmissionDenied):
            check(value)


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
    result["merge_parent_shas"] = [value["target_sha"]]
    result["target_sha"] = "f" * 40
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


def test_own_merge_methodology_and_base_advance_do_not_self_invalidate():
    value = snapshot()
    after = merged(value)
    after["methodology_sha"] = "f" * 40
    after["pull"]["base"]["sha"] = "f" * 40
    reads = iter([value, value, after])
    result = guarded_merge(lambda: next(reads), lambda _: {"merged": True, "sha": "f" * 40}, REPO, 7, HEAD, POLICY)
    assert result["status"] == "MERGED_REQUIRES_OWNER_RECONCILIATION"


@pytest.mark.parametrize("change", ["methodology", "parent", "base"])
def test_unrelated_authority_or_base_advance_is_not_normalized(change):
    value = snapshot()
    after = merged(value)
    if change == "methodology":
        after["methodology_sha"] = "e" * 40
    elif change == "parent":
        after["merge_parent_shas"] = ["e" * 40]
    else:
        after["target_sha"] = "e" * 40
    reads = iter([value, value, after])
    result = guarded_merge(lambda: next(reads), lambda _: {"merged": True, "sha": "f" * 40}, REPO, 7, HEAD, POLICY)
    assert result["status"] == "MERGED_BUT_UNACCEPTED"


def test_lost_effect_response_remains_unknown_without_retry():
    value = snapshot()
    calls = []

    def merge(head):
        calls.append(head)
        raise TimeoutError("lost response")

    result = guarded_merge(lambda: value, merge, REPO, 7, HEAD, POLICY)
    assert calls == [HEAD]
    assert result == {"status": "UNKNOWN", "activation_permitted": False, "retry_merge": False}


@pytest.mark.parametrize("payload", [{}, {"merged": None}, {"merged": True}, {"merged": True, "sha": "invalid"}])
def test_incomplete_merge_response_is_unknown_not_refusal(payload):
    value = snapshot()
    result = guarded_merge(lambda: value, lambda _: payload, REPO, 7, HEAD, POLICY)
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


def test_old_pr_base_metadata_does_not_replace_live_target_ref():
    value = snapshot()
    value["pull"]["base"]["sha"] = "d" * 40
    reads = iter([value, value, merged(value)])
    result = guarded_merge(lambda: next(reads), lambda _: {"merged": True, "sha": "f" * 40}, REPO, 7, HEAD, POLICY)
    assert result["status"] == "MERGED_REQUIRES_OWNER_RECONCILIATION"


def test_target_moves_between_reads_no_effect_even_if_pr_base_stays_old():
    before = snapshot()
    after = copy.deepcopy(before)
    after["target_sha"] = "d" * 40
    effects = []
    reads = iter([before, after])
    with pytest.raises(AdmissionDenied, match="evidence changed"):
        guarded_merge(lambda: next(reads), lambda h: effects.append(h) or {"merged": False}, REPO, 7, HEAD, POLICY)
    assert effects == []


@pytest.mark.parametrize("change", [{"target_ref": "refs/heads/foreign"}, {"target_sha": None}, {"target_sha": "bad"}])
def test_missing_or_foreign_live_target_denies(change):
    value = snapshot()
    value.update(change)
    with pytest.raises(AdmissionDenied):
        check(value)


def test_api_adapter_reads_actual_named_target_reference(monkeypatch):
    github = adapter.GitHub()
    value = snapshot()
    value["pull"]["base"]["sha"] = "d" * 40
    value["target_sha"] = POLICY
    calls = []

    def api(path):
        calls.append(path)
        if path.endswith("/pulls/7"):
            return value["pull"]
        if path.endswith("/git/ref/heads/main") and path.startswith("repos/" + REPO):
            return {"ref": "refs/heads/main", "object": {"type": "commit", "sha": POLICY}}
        if path == "repos/GrahamArdent/PROGRAMSTART/git/ref/heads/main":
            return {"object": {"sha": POLICY}}
        if path == "repos/" + REPO:
            return value["repository"]
        raise AssertionError(path)

    monkeypatch.setattr(github, "api", api)
    monkeypatch.setattr(github, "pages", lambda path: value["comments"] if "/comments" in path else [])
    actual = github.snapshot(REPO, 7)
    assert actual["target_sha"] == POLICY
    assert actual["pull"]["base"]["sha"] == "d" * 40
    assert check(actual) == check(value)
    assert "repos/" + REPO + "/git/ref/heads/main" in calls
