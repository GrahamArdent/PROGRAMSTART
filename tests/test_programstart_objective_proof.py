from __future__ import annotations

import base64
import copy
import hashlib
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts import programstart_objective_proof as gate

REPO = "GrahamArdent/card-vault"
OWNER = f"https://github.com/{REPO}/issues/6"
ISSUE_API = f"https://api.github.com/repos/{REPO}/issues/6"
HEAD = "a" * 40


def fixture():
    outcomes = [
        "Reliable inventory",
        "Credible identity",
        "Credible pricing",
        "Efficient safe discovery",
        "Correct report",
        "Reconstructable foundation",
    ]
    contract = {
        "version": 1,
        "owner_ref": OWNER,
        "protected_outcome": "Credible value per total operator effort",
        "proof_workflow": ".github/workflows/proof.yml",
        "objectives": [
            {"id": f"O{i}", "outcome": outcome, "success_criteria": [f"Observable composed result for {outcome}"]}
            for i, outcome in enumerate(outcomes, 1)
        ],
    }
    files = {
        ".github/workflows/proof.yml": b"name: trusted proof\n",
        "requirements.md": b"accepted requirements",
        "implementation.py": b"print('fixture')",
        "scenario.json": b'{"expected":42}',
        "environment.json": b'{"python":"3.12"}',
        "results.json": b'{"actual":42,"pass":true}',
    }
    bindings = {
        k: [{"path": p, "sha256": hashlib.sha256(files[p]).hexdigest()}]
        for k, p in zip(
            ["requirements", "implementation", "scenario", "environment", "evidence"],
            [p for p in files if not p.startswith(".github/")],
            strict=True,
        )
    }
    proof = {
        "version": 1,
        "contract_sha256": gate.digest(contract),
        "claim": "objective_complete",
        "objectives": [
            {"id": row["id"], "status": "passed", **copy.deepcopy(bindings), "reason": "", "resume_when": ""}
            for row in contract["objectives"]
        ],
    }
    return contract, proof, files


def acceptance(contract, proof, *, claim="baseline", result="accepted", head=None, previous=None, reason=""):
    return {
        "claim": claim,
        "result": result,
        "contract_sha256": gate.digest(contract),
        "previous_contract_sha256": previous,
        "scope_change_reason": reason,
        "head_sha": head,
        "proof_sha256": gate.digest(proof) if claim == "completion" else None,
        "run_id": 123 if claim == "completion" else None,
    }


def comment(record, number=1):
    return {
        "id": number,
        "user": {"id": 42, "login": "GrahamArdent"},
        "issue_url": ISSUE_API,
        "created_at": "2026-10-17T14:00:00Z",
        "updated_at": "2026-10-17T14:00:00Z",
        "body": gate.MARKER + json.dumps(record),
    }


def authority(contract, proof):
    return {
        "repository": {"full_name": REPO, "owner": {"id": 42, "login": "GrahamArdent"}, "default_branch": "main"},
        "issue": {"number": 6, "url": ISSUE_API, "html_url": OWNER},
        "comments": [
            comment(acceptance(contract, proof)),
            comment(acceptance(contract, proof, claim="completion", head=HEAD), 2),
        ],
        "proof_runs": {
            "123": {
                "id": 123,
                "head_sha": HEAD,
                "status": "completed",
                "conclusion": "success",
                "path": contract["proof_workflow"],
                "repository": {"full_name": REPO},
            }
        },
    }


def test_complete_fixture_requires_exact_native_owner_acceptance():
    c, p, files = fixture()
    gate.inspect_proof(c, p, files.__getitem__, complete=True)
    gate.accept_owner_records(c, p, authority(c, p), HEAD, complete=True, prior_contract=c)


def test_card_vault_green_auditor_cannot_close_original_goal():
    c, p, files = fixture()
    for row in p["objectives"]:
        if row["id"] in {"O2", "O3", "O4"}:
            row.update(
                status="pending",
                reason="Identification, pricing and measured efficiency not implemented",
                resume_when="Accepted implementation plus composed proof",
            )
    with pytest.raises(gate.ObjectiveDenied, match="O2 is pending"):
        gate.inspect_proof(c, p, files.__getitem__, complete=True)
    p["claim"] = "slice"
    gate.inspect_proof(c, p, files.__getitem__, complete=False)
    with pytest.raises(gate.ObjectiveDenied, match="slice success"):
        gate.inspect_proof(c, p, files.__getitem__, complete=True)


@pytest.mark.parametrize(
    "mutation",
    [
        lambda p: p["objectives"].pop(),
        lambda p: p["objectives"].append(copy.deepcopy(p["objectives"][0])),
        lambda p: p.update(contract_sha256="0" * 64),
        lambda p: p["objectives"][0].update(status="deferred"),
        lambda p: p["objectives"][0].update(evidence=[]),
        lambda p: p["objectives"][0].update(scenario=[]),
        lambda p: p["objectives"][0]["implementation"][0].update(path="../outside"),
        lambda p: p["objectives"][0]["evidence"][0].update(path=gate.PROOF),
        lambda p: p.update(passed=True),
    ],
)
def test_missing_or_forged_coverage_rejected(mutation):
    c, p, files = fixture()
    mutation(p)
    with pytest.raises(gate.ObjectiveDenied):
        gate.inspect_proof(c, p, files.__getitem__, complete=True)


@pytest.mark.parametrize("path", ["requirements.md", "implementation.py", "scenario.json", "environment.json", "results.json"])
def test_changes_invalidate_affected_proof(path):
    c, p, files = fixture()
    files[path] += b"changed"
    with pytest.raises(gate.ObjectiveDenied, match="stale or tampered"):
        gate.inspect_proof(c, p, files.__getitem__, complete=True)


@pytest.mark.parametrize(
    "mutation",
    [
        lambda a: a["comments"].clear(),
        lambda a: a["comments"][0]["user"].update(id=99),
        lambda a: a["comments"][1]["user"].update(login="impostor"),
        lambda a: a["comments"][1].update(updated_at="later"),
        lambda a: a["comments"][1].update(issue_url=ISSUE_API + "9"),
        lambda a: a["comments"].pop(),
    ],
)
def test_native_acceptance_not_a_self_asserted_label(mutation):
    c, p, _ = fixture()
    a = authority(c, p)
    mutation(a)
    with pytest.raises(gate.ObjectiveDenied):
        gate.accept_owner_records(c, p, a, HEAD, complete=True)


def test_changed_head_and_revocation_block():
    c, p, _ = fixture()
    a = authority(c, p)
    with pytest.raises(gate.ObjectiveDenied):
        gate.accept_owner_records(c, p, a, "b" * 40, complete=True)
    a["comments"].append(comment(acceptance(c, p, claim="completion", result="rejected", head=HEAD), 3))
    with pytest.raises(gate.ObjectiveDenied):
        gate.accept_owner_records(c, p, a, HEAD, complete=True)


@pytest.mark.parametrize(
    "change",
    [
        {"conclusion": "failure"},
        {"status": "in_progress"},
        {"head_sha": "b" * 40},
        {"path": ".github/workflows/other.yml"},
        {"repository": {"full_name": "Other/repo"}},
    ],
)
def test_candidate_pass_label_does_not_replace_native_run(change):
    c, p, _ = fixture()
    a = authority(c, p)
    a["proof_runs"]["123"].update(change)
    with pytest.raises(gate.ObjectiveDenied):
        gate.accept_owner_records(c, p, a, HEAD, complete=True)


def test_scope_removal_needs_explicit_owner_chain():
    old, p, _ = fixture()
    new = copy.deepcopy(old)
    new["objectives"].pop()
    a = authority(old, p)
    with pytest.raises(gate.ObjectiveDenied):
        gate.accept_owner_records(new, p, a, HEAD, complete=False, prior_contract=old)
    a["comments"].append(
        comment(
            acceptance(new, p, previous=gate.digest(old), reason="Owner explicitly retires O6 from this selected objective"), 3
        )
    )
    gate.accept_owner_records(new, p, a, HEAD, complete=False, prior_contract=old)
    redirected = copy.deepcopy(new)
    redirected["owner_ref"] = OWNER + "1"
    with pytest.raises(gate.ObjectiveDenied):
        gate.accept_owner_records(redirected, p, a, HEAD, complete=False, prior_contract=old)


def test_duplicate_json_and_symlink_are_not_evidence(tmp_path):
    with pytest.raises(gate.ObjectiveDenied):
        gate.parse('{"version":1,"version":1}')
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    (tmp_path / "link").symlink_to("/etc/passwd")
    subprocess.run(["git", "-C", str(tmp_path), "add", "link"], check=True)
    subprocess.run(
        [
            "git",
            "-C",
            str(tmp_path),
            "-c",
            "user.name=Fixture",
            "-c",
            "user.email=fixture@example.invalid",
            "commit",
            "-qm",
            "fixture",
        ],
        check=True,
    )
    with pytest.raises(gate.ObjectiveDenied):
        gate.git_file(tmp_path, "HEAD", "link")


def test_cli_skip_flags_and_dashboard_cannot_close_missing_objectives(tmp_path, monkeypatch, capsys):
    from scripts import programstart_serve as dashboard
    from scripts import programstart_workflow_state as cli

    state = {"active_stage": "post_launch_review", "stages": {"post_launch_review": {"status": "in_progress", "signoff": {}}}}
    writes = []
    for module in [cli, dashboard]:
        monkeypatch.setattr(module, "load_registry", lambda: {})
        monkeypatch.setattr(module, "load_workflow_state", lambda *a: state)
        monkeypatch.setattr(module, "workflow_active_step", lambda *a: "post_launch_review")
        monkeypatch.setattr(module, "workflow_steps", lambda *a: ["post_launch_review"])
        monkeypatch.setattr(module, "workspace_path", lambda p: tmp_path / p)
        monkeypatch.setattr(module, "save_workflow_state", lambda *a, **k: writes.append(a))
        monkeypatch.setattr(module, "system_is_optional_and_absent", lambda *a: False, raising=False)
    monkeypatch.setattr(
        "sys.argv", ["workflow", "advance", "--system", "programbuild", "--skip-preflight", "--skip-gate-check", "--dry-run"]
    )
    assert cli.main() == 1
    assert "Objective proof gate blocked" in capsys.readouterr().out
    assert (
        dashboard.advance_workflow_with_signoff("programbuild", "approved", "2026-10-17", "", False, gate_result="clear")[
            "exit_code"
        ]
        == 1
    )
    assert not writes and state["stages"]["post_launch_review"]["status"] == "in_progress"


def test_checkpoint_closeout_never_claims_objective_complete(tmp_path, monkeypatch):
    from scripts import programstart_closeout as closeout

    for name in ["validate_adr_coverage", "validate_adr_coherence", "validate_authority_sync"]:
        monkeypatch.setattr(closeout, name, lambda *a: [])
    monkeypatch.setattr(closeout, "load_registry", lambda: {})
    monkeypatch.setattr(closeout, "git_changed_files", lambda: [])
    monkeypatch.setattr(closeout, "evaluate_drift", lambda *a: ([], []))
    monkeypatch.setattr(closeout, "workspace_path", lambda p: tmp_path / p)
    value = closeout.build_evidence(label="green slice", adr_result="not-required", adr_ids=[], notes="")
    assert value["status"] == "passed" and value["objective_complete"] is False and value["scope"] == "checkpoint"
    value = closeout.build_evidence(label="complete", adr_result="not-required", adr_ids=[], notes="", objective_complete=True)
    assert value["status"] == "failed" and value["objective_complete"] is False


class NativeAPI:
    """Synthetic native metadata for adapter tests, never production acceptance."""

    def __init__(self, contract, proof, files):
        self.contract, self.proof, self.files = contract, proof, files

    def api(self, path):
        if path == f"repos/{REPO}/actions/runs/123":
            return authority(self.contract, self.proof)["proof_runs"]["123"]
        if "/contents" in path:
            rel = path.split("/contents", 1)[1].split("?", 1)[0].strip("/")
            data = {gate.CONTRACT: json.dumps(self.contract).encode(), gate.PROOF: json.dumps(self.proof).encode(), **self.files}
            if rel in data:
                return {
                    "type": "file",
                    "sha": blob_sha(data[rel]),
                    "encoding": "base64",
                    "content": base64.b64encode(data[rel]).decode(),
                }
            prefix = rel + "/" if rel else ""
            return [
                {
                    "name": n,
                    "type": "file" if prefix + n in data else "dir",
                    "sha": blob_sha(data[prefix + n]) if prefix + n in data else "0" * 40,
                }
                for n in sorted({p[len(prefix) :].split("/")[0] for p in data if p.startswith(prefix)})
            ]
        if path == f"repos/{REPO}":
            return authority(self.contract, self.proof)["repository"]
        if path == f"repos/{REPO}/issues/6":
            return authority(self.contract, self.proof)["issue"]
        raise AssertionError(path)

    def pages(self, path):
        return authority(self.contract, self.proof)["comments"]


def test_enrolled_merge_adapter_blocks_omission_and_accepts_bound_complete_fixture():
    c, p, files = fixture()
    adapter = NativeAPI(c, p, files)
    result = gate.merge_objective_snapshot(adapter, REPO, "b" * 40, HEAD)
    assert result["objective_complete"] is True
    p["objectives"].pop()
    with pytest.raises(gate.ObjectiveDenied, match="coverage omitted"):
        gate.merge_objective_snapshot(adapter, REPO, "b" * 40, HEAD)


def test_authenticated_reads_fail_closed_instead_of_legacy_downgrade():
    class Outage:
        def api(self, _):
            raise ValueError("API unavailable")

    with pytest.raises(ValueError):
        gate.merge_objective_snapshot(Outage(), REPO, "b" * 40, HEAD)


@pytest.mark.parametrize("raw,complete", [(False, True), (True, True), (True, False)])
def test_local_workflow_positive_acceptance_binds_real_git_bytes(tmp_path, monkeypatch, raw, complete):
    from scripts.programstart_challenge_merge import GitHub

    c, p, files = fixture()
    for name, data in {**files, gate.CONTRACT: json.dumps(c).encode(), gate.PROOF: json.dumps(p).encode()}.items():
        target = tmp_path / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    subprocess.run(["git", "-C", str(tmp_path), "remote", "add", "origin", f"https://github.com/{REPO}.git"], check=True)
    subprocess.run(["git", "-C", str(tmp_path), "add", "."], check=True)
    subprocess.run(
        [
            "git",
            "-C",
            str(tmp_path),
            "-c",
            "user.name=Fixture",
            "-c",
            "user.email=fixture@example.invalid",
            "commit",
            "-qm",
            "accepted fixture",
        ],
        check=True,
    )
    head = subprocess.check_output(["git", "-C", str(tmp_path), "rev-parse", "HEAD"], text=True).strip()
    api = NativeAPI(c, p, files)
    original = api.api

    def read(_self, path):
        if "/git/ref/heads/" in path:
            return {"object": {"sha": head}}
        if "/actions/runs/" in path:
            return {**authority(c, p)["proof_runs"]["123"], "head_sha": head}
        return original(path)

    rows = authority(c, p)["comments"]
    rows[1] = comment(acceptance(c, p, claim="completion", head=head), 2)
    monkeypatch.setattr(GitHub, "api", read)
    monkeypatch.setattr(GitHub, "pages", lambda *_: rows)
    check = gate.workflow_problems
    if raw:
        import importlib
        import runpy

        namespace = runpy.run_path(str(Path(gate.__file__)), run_name="standalone_probe")
        raw_github = importlib.import_module("programstart_challenge_merge").GitHub
        monkeypatch.setattr(raw_github, "api", read)
        monkeypatch.setattr(raw_github, "pages", lambda *_: rows)
        check = namespace["workflow_problems"]
        assert namespace["merge_objective_snapshot"](api, REPO, "b" * 40, HEAD)["objective_complete"] is True
    stage = "post_launch_review" if complete else "requirements_and_ux"
    assert check(tmp_path, stage) == []
    (tmp_path / "environment.json").write_text("changed runtime")
    assert "stale or tampered" in check(tmp_path, stage)[0]


def test_intake_transition_and_renamed_terminal_stage_are_not_bypasses(tmp_path):
    assert gate.workflow_problems(tmp_path, "inputs_and_mode_selection")
    assert gate.workflow_problems(tmp_path, "custom-finished", terminal=True)


def test_ci_policy_precedes_candidate_installation():
    import yaml

    workflow = yaml.safe_load((ROOT / ".github/workflows/pr-validation.yml").read_text())
    steps = workflow["jobs"]["required-pr-gate"]["steps"]
    index = next(i for i, step in enumerate(steps) if step.get("name") == "Check objective claims with accepted base policy")
    assert all("uses" in step and "run" not in step for step in steps[:index])
    assert index < next(i for i, step in enumerate(steps) if step.get("name") == "Sync development environment")


def blob_sha(raw):
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw, usedforsecurity=False).hexdigest()


@pytest.mark.parametrize("kind", ["symlink", "foreign-blob", "changed-bytes"])
def test_native_contents_cannot_substitute_link_or_blob(kind):
    c, p, files = fixture()

    class Changed(NativeAPI):
        def api(self, path):
            result = super().api(path)
            if isinstance(result, list) and "contents/PROGRAMBUILD?" in path:
                for entry in result:
                    if entry["name"] == "OBJECTIVES.json":
                        if kind == "symlink":
                            entry["type"] = "symlink"
                        if kind == "foreign-blob":
                            entry["sha"] = "0" * 40
            if isinstance(result, dict) and "contents/PROGRAMBUILD/OBJECTIVES.json?" in path and kind == "changed-bytes":
                result["content"] = base64.b64encode(b"{}").decode()
            return result

    with pytest.raises(gate.ObjectiveDenied, match="regular directory entry|directory/blob identity"):
        gate.merge_objective_snapshot(Changed(c, p, files), REPO, "b" * 40, HEAD)


def test_owner_acceptance_rejects_invalid_owner_before_provider_lookup():
    c, p, _ = fixture()
    a = authority(c, p)
    c["owner_ref"] = "https://example.invalid/forged"
    with pytest.raises(gate.ObjectiveDenied, match="invalid owner"):
        gate.accept_owner_records(c, p, a, HEAD, complete=False)


def test_revoked_prior_baseline_and_noncompletion_owner_comments_are_not_proof():
    c, p, files = fixture()
    a = authority(c, p)
    revoked = acceptance(c, p, result="rejected", previous=gate.digest(c), reason="withdrawn")
    a["comments"].append(comment(revoked, 3))
    with pytest.raises(gate.ObjectiveDenied, match="unaccepted or revoked"):
        gate.accept_owner_records(c, p, a, HEAD, complete=False)
    baseline_only = authority(c, p)
    baseline_only["comments"] = baseline_only["comments"][:1]
    gate.load_proof_runs(NativeAPI(c, p, files), REPO, baseline_only)
    assert baseline_only["proof_runs"] == {}


def test_research_without_enrollment_is_nonterminal_not_proof(tmp_path):
    assert gate.workflow_problems(tmp_path, "research") == []


def test_symlinked_local_evidence_cannot_escape_workspace(tmp_path):
    c, p, files = fixture()
    for name, data in {**files, gate.CONTRACT: json.dumps(c).encode(), gate.PROOF: json.dumps(p).encode()}.items():
        target = tmp_path / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    target = tmp_path / "requirements.md"
    target.unlink()
    target.symlink_to(tmp_path / "implementation.py")
    assert "evidence escapes workspace" in gate.workflow_problems(tmp_path, "release_readiness")[0]


def test_optional_contract_cannot_be_removed_by_candidate():
    c, p, files = fixture()

    class Removed(NativeAPI):
        def api(self, path):
            if f"ref={HEAD}" in path and "/contents/PROGRAMBUILD?" in path:
                return []
            return super().api(path)

    with pytest.raises(gate.ObjectiveDenied, match="removed the accepted objective"):
        gate.merge_objective_snapshot(Removed(c, p, files), REPO, "b" * 40, HEAD)


def test_unenrolled_merge_reports_no_completion():
    class Empty:
        def api(self, path):
            return []

    assert gate.merge_objective_snapshot(Empty(), REPO, "b" * 40, HEAD)["objective_complete"] is False


def test_noncompletion_owner_comment_does_not_create_proof_run():
    c, p, files = fixture()
    a = authority(c, p)
    a["comments"].append({"id": 3, "user": {"id": 0}, "body": "untrusted prose"})
    gate.load_proof_runs(NativeAPI(c, p, files), REPO, a)
    assert set(a["proof_runs"]) == {"123"}


def test_unmapped_nonterminal_stage_never_claims_completion(tmp_path):
    assert gate.workflow_problems(tmp_path, "owner-custom-navigation") == []
