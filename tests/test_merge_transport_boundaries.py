"""Merge admission observes native transport failures without performing a merge."""

import json
from types import SimpleNamespace

import pytest

from scripts import programstart_challenge_merge as merge
from tests.test_programstart_challenge_merge import HEAD, POLICY, REPO, comment, snapshot


@pytest.mark.parametrize("payload", [None, {"sha": HEAD}])
def test_gh_transport_encodes_only_explicit_payload(monkeypatch, payload):
    calls = []

    def run(argv, **kwargs):
        calls.append((argv, kwargs))
        return SimpleNamespace(returncode=0, stdout='{"ok":true}')

    monkeypatch.setattr(merge.subprocess, "run", run)
    assert merge.GitHub().api("repos/owner/repo", method="GET", payload=payload) == {"ok": True}
    argv, options = calls[0]
    assert argv[:6] == ["gh", "api", "--hostname", "github.com", "--method", "GET"]
    assert ("--input" in argv) == (payload is not None)
    assert options["input"] == (json.dumps(payload) if payload is not None else None)
    assert options["timeout"] == 60 and options["check"] is False


def test_gh_error_does_not_expose_provider_details(monkeypatch):
    monkeypatch.setattr(merge.subprocess, "run", lambda *_a, **_k: SimpleNamespace(returncode=1, stderr="sensitive detail"))
    with pytest.raises(merge.AdmissionDenied, match="result may require reconciliation") as exc:
        merge.GitHub().api("repos/owner/repo")
    assert "sensitive detail" not in str(exc.value)


def test_pagination_bound_cannot_be_treated_as_complete(monkeypatch):
    client = merge.GitHub()
    monkeypatch.setattr(client, "api", lambda _path: [{}] * 100)
    with pytest.raises(merge.AdmissionDenied, match="history exceeds bounded"):
        client.pages("repos/owner/repo/issues/1/comments")


@pytest.mark.parametrize("body", ["{", '{"repository":"one","repository":"two"}'])
def test_malformed_owner_disposition_is_not_clear(body):
    value = snapshot()
    entry = comment()
    entry["body"] = merge.MARKER + body
    value["comments"] = [entry]
    with pytest.raises(merge.AdmissionDenied, match="invalid owner disposition"):
        merge.admit(value, REPO, 7, HEAD, POLICY)


def test_explicit_merge_refusal_never_allows_activation():
    result = merge.guarded_merge(snapshot, lambda _head: {"merged": False}, REPO, 7, HEAD, POLICY)
    assert result == {"status": "MERGE_REFUSED", "activation_permitted": False, "retry_merge": False}


@pytest.mark.parametrize("arguments,status", [([], "ADMISSIBLE_SNAPSHOT_ONLY"), (["--merge"], "MERGE_REFUSED")])
def test_cli_uses_admission_and_reports_no_activation(monkeypatch, capsys, arguments, status):
    class FakeGitHub:
        def verify_consumer(self, sha):
            assert sha == POLICY

        def snapshot(self, repository, pr):
            assert repository == REPO and pr == 7
            return snapshot()

        def api(self, path, *, method, payload):
            assert method == "PUT" and payload["sha"] == HEAD
            return {"merged": False}

    monkeypatch.setattr(merge, "GitHub", FakeGitHub)
    result = merge.main([REPO, "7", "--expected-head", HEAD, "--methodology-sha", POLICY, *arguments])
    assert result == (0 if not arguments else 1)
    output = json.loads(capsys.readouterr().out)
    assert output["status"] == status and output["activation_permitted"] is False


def test_cli_invalid_identity_is_blocked_before_transport(capsys):
    assert merge.main(["invalid", "7", "--expected-head", HEAD, "--methodology-sha", POLICY]) == 1
    assert json.loads(capsys.readouterr().out)["status"] == "BLOCKED"


@pytest.mark.parametrize("merged,raw", [(False, False), (True, False), (True, True)])
def test_snapshot_reads_native_merge_parents_and_unenrolled_objective(monkeypatch, merged, raw):
    value = snapshot()
    pull = dict(value["pull"], merged=merged, merge_commit_sha="c" * 40)
    client = merge.GitHub()
    if raw:
        import runpy

        client = runpy.run_path(merge.__file__, run_name="standalone_probe")["GitHub"]()
    calls = []

    def api(path):
        calls.append(path)
        if "/contents" in path:
            return []
        if path.endswith("/pulls/7"):
            return pull
        if "/git/commits/" in path:
            return {"parents": [{"sha": "d" * 40}]}
        if "/git/ref/heads/" in path:
            return {"ref": "refs/heads/main", "object": {"sha": POLICY}}
        return value["repository"]

    monkeypatch.setattr(client, "api", api)
    monkeypatch.setattr(client, "pages", lambda _: [])
    result = client.snapshot(REPO, 7)
    assert result["merge_parent_shas"] == (["d" * 40] if merged else [])
    assert result["objective_proof"]["coverage"] == "UNENROLLED"


def test_old_head_withdrawal_and_unrelated_owner_prose_do_not_erase_clear():
    from tests.test_programstart_challenge_merge import record, withdrawal

    value = snapshot()
    old = comment(1, record(head="c" * 40))
    prose = comment(3)
    prose["body"] = "Read-only observation, no disposition change."
    value["comments"] = [old, withdrawal(old, 2), prose, comment(4)]
    assert len(merge.admit(value, REPO, 7, HEAD, POLICY)) == 64
