"""Synthetic authority controls and real consumer routes, never provider truth."""

from __future__ import annotations

import base64
import copy
import hashlib
import json
import subprocess
from datetime import date, timedelta

import pytest
from test_programstart_objective_proof import authority as objective_authority
from test_programstart_objective_proof import fixture as objective_fixture

from scripts import programstart_objective_proof as objective
from scripts import programstart_research_admission as gate

REPO = "GrahamArdent/card-vault"
BASE, HEAD = "b" * 40, "a" * 40


def fixture():
    c, p, files = objective_fixture()
    p["claim"] = "slice"
    files.update(
        {
            "research.md": b"Independent capability review",
            "decisions.md": b"D-01 research scope",
            "packet.md": b"Current research work",
            "capture.txt": b"Provider primary excerpt, synthetic fixture only",
        }
    )
    today = date.today()

    def binding(name):
        return {"path": name, "sha256": hashlib.sha256(files[name]).hexdigest()}

    record = {
        "version": 1,
        "owner_ref": c["owner_ref"],
        "objective_contract_sha256": objective.digest(c),
        "research_path": "research.md",
        "decision_ref": {"path": "decisions.md", "id": "D-01"},
        "entrypoints": ["packet.md"],
        "bindings": [binding(x) for x in ["research.md", "decisions.md", "packet.md"]],
        "work": {
            "kind": "product",
            "phase": "implementation",
            "objective_ids": ["O3"],
            "allowed_paths": ["docs/", gate.RECORD, "research.md"],
            "excluded_claims": ["No real market valuation from fixture"],
            "parent_terminal_condition": "Real suitable sales and usable outcome",
        },
        "questions": [
            {
                "id": "R1",
                "objective_ids": ["O3"],
                "question": "Does selected source expose completed transactions?",
                "required_before": "architecture",
                "status": "supported",
                "finding": "Supported only in synthetic authority fixture",
                "next_action": "Run actual source retest",
                "invalidation": ["Source/access/rights or scope changes"],
                "evidence": [
                    {
                        **binding("capture.txt"),
                        "source_url": "https://vendor.example/documentation",
                        "kind": "primary",
                        "observed_at": today.isoformat(),
                        "valid_until": (today + timedelta(days=7)).isoformat(),
                        "observed_capability": "Fixture has required fields",
                        "limitations": "Not live provider proof",
                    }
                ],
            }
        ],
    }
    return c, p, files, record


def receipt(r, previous=None):
    return {
        "record_sha256": objective.digest(r),
        "previous_sha256": previous,
        "result": "accepted",
        "reason": "Synthetic accepted scope",
        "objective_contract_sha256": r["objective_contract_sha256"],
        "scope_sha256": objective.digest(r["work"]),
    }


def native(r, c, p):
    a = objective_authority(c, p)
    a["comments"] += [
        {
            "id": 3,
            "user": {"id": 42, "login": "GrahamArdent"},
            "created_at": "2026-10-17T10:00:00Z",
            "updated_at": "2026-10-17T10:00:00Z",
            "issue_url": a["issue"]["url"],
            "body": gate.MARKER + json.dumps(receipt(r)),
        }
    ]
    return a


class API:
    def __init__(self, c, p, files, r):
        self.c, self.p, self.files, self.r = c, p, files, r
        self.a, self.old, self.removed = native(r, c, p), True, False
        self.changes = [{"filename": "docs/research-result.md"}]

    def api(self, route):
        if "/contents" in route:
            rel = route.split("/contents", 1)[1].split("?", 1)[0].strip("/")
            data = {
                **self.files,
                objective.CONTRACT: json.dumps(self.c).encode(),
                objective.PROOF: json.dumps(self.p).encode(),
                gate.RECORD: json.dumps(self.r).encode(),
            }
            if ("ref=" + BASE in route and not self.old) or ("ref=" + HEAD in route and self.removed):
                data.pop(gate.RECORD)

            def blob(raw):
                return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw, usedforsecurity=False).hexdigest()

            if rel in data:
                return {
                    "type": "file",
                    "encoding": "base64",
                    "content": base64.b64encode(data[rel]).decode(),
                    "sha": blob(data[rel]),
                }
            prefix = rel + "/" if rel else ""
            return [
                {
                    "name": n,
                    "type": "file" if prefix + n in data else "dir",
                    "sha": blob(data[prefix + n]) if prefix + n in data else "0" * 40,
                }
                for n in sorted({x[len(prefix) :].split("/")[0] for x in data if x.startswith(prefix)})
            ]
        if "/compare/" in route:
            return {"files": self.changes}
        if "/git/ref/heads/" in route:
            return {"object": {"sha": BASE}}
        if route == f"repos/{REPO}":
            return self.a["repository"]
        if route == f"repos/{REPO}/issues/6":
            return self.a["issue"]
        raise AssertionError(route)

    def pages(self, route):
        return self.a["comments"]


def check(c, f, r, phase="implementation"):
    return gate.inspect(r, c, lambda p: f[p], phase)


def test_positive_research_is_not_product_completion():
    c, p, f, r = fixture()
    assert check(c, f, r)["product_admitted"] is True
    r["questions"][0]["status"] = "unsupported"
    assert check(c, f, r, "research")["product_admitted"] is False
    with pytest.raises(ValueError, match="unresolved"):
        check(c, f, r)
    assert gate.merge_snapshot(API(c, p, f, fixture()[3]), REPO, BASE, HEAD)["coverage"] == "ENROLLED"


@pytest.mark.parametrize(
    "mutation,reason",
    [
        ("empty", "prerequisites missing"),
        ("duplicate", "duplicate research question"),
        ("omitted", "coverage omitted"),
        ("unknown", "unresolved"),
        ("unsupported", "unresolved"),
        ("self", "independent"),
        ("expired", "expired"),
        ("future", "future"),
        ("binding", "stale"),
        ("entry", "entrypoint"),
        ("bool", "version"),
        ("traversal", "unsafe"),
        ("scope", "scope"),
        ("derived", "independent"),
        ("no_capture", "independent"),
        ("bad_url", "source URL"),
    ],
)
def test_adversarial_record_cannot_earn_admission(mutation, reason):
    c, p, f, r = fixture()
    q = r["questions"][0]
    e = q["evidence"][0]
    if mutation == "empty":
        r["questions"] = []
    elif mutation == "duplicate":
        r["questions"].append(copy.deepcopy(q))
    elif mutation == "omitted":
        r["work"]["objective_ids"].append("O2")
    elif mutation in {"unknown", "unsupported"}:
        q["status"] = mutation
    elif mutation == "self":
        e["source_url"] = "https://github.com/GrahamArdent/another-plan/blob/main/README.md"
    elif mutation == "expired":
        e["valid_until"] = (date.today() - timedelta(days=1)).isoformat()
    elif mutation == "future":
        e["observed_at"] = (date.today() + timedelta(days=1)).isoformat()
    elif mutation == "binding":
        f["capture.txt"] = b"changed source"
    elif mutation == "entry":
        r["bindings"].pop()
    elif mutation == "bool":
        r["version"] = True
    elif mutation == "traversal":
        r["bindings"][0]["path"] = "../research.md"
    elif mutation == "scope":
        r["work"]["phase"] = "research"
    elif mutation == "derived":
        e["kind"] = "derived"
    elif mutation == "no_capture":
        q["evidence"] = []
    elif mutation == "bad_url":
        e["source_url"] = "https://user:secret@vendor.example/path"  # pragma: allowlist secret
    with pytest.raises(ValueError, match=reason):
        check(c, f, r)


@pytest.mark.parametrize("attack", ["missing", "edited", "foreign", "revoked", "scope", "broken_history", "redirect"])
def test_native_acceptance_is_not_candidate_claim(attack):
    c, p, f, r = fixture()
    a = native(r, c, p)
    if attack == "missing":
        a["comments"] = []
    elif attack == "edited":
        a["comments"][-1]["updated_at"] = "later"
    elif attack == "foreign":
        a["comments"][-1]["user"]["id"] = 41
    elif attack == "revoked":
        row = copy.deepcopy(a["comments"][-1])
        row["id"] += 1
        obj = receipt(r, objective.digest(r))
        obj["result"] = "rejected"
        row["body"] = gate.MARKER + json.dumps(obj)
        a["comments"].append(row)
    elif attack in {"scope", "broken_history"}:
        obj = receipt(r)
        obj["scope_sha256" if attack == "scope" else "previous_sha256"] = "0" * 64
        a["comments"][-1]["body"] = gate.MARKER + json.dumps(obj)
    elif attack == "redirect":
        r["owner_ref"] = "https://github.com/other/repo/issues/6"
    with pytest.raises(ValueError):
        gate.accept(r, REPO, a, None)


def test_scope_change_requires_preserved_owner_history():
    c, p, f, r = fixture()
    old = copy.deepcopy(r)
    r["work"]["excluded_claims"].append("Additional exclusion")
    a = native(old, c, p)
    row = copy.deepcopy(a["comments"][-1])
    row["id"] += 1
    row["body"] = gate.MARKER + json.dumps(receipt(r, objective.digest(old)))
    a["comments"].append(row)
    gate.accept(r, REPO, a, old)
    a["comments"].pop(-2)
    with pytest.raises(ValueError):
        gate.accept(r, REPO, a, old)


def test_actual_enrolled_merge_snapshot_and_existing_objective_composition():
    c, p, f, r = fixture()
    api = API(c, p, f, r)
    assert objective.merge_objective_snapshot(api, REPO, BASE, HEAD)["research_admission"]["product_admitted"]
    api.removed = True
    with pytest.raises(ValueError, match="removed research"):
        gate.merge_snapshot(api, REPO, BASE, HEAD)
    api.removed = False
    api.changes = [{"filename": "application.py"}]
    with pytest.raises(ValueError, match="outside accepted"):
        gate.merge_snapshot(api, REPO, BASE, HEAD)
    api.changes = [{"filename": "docs/new.md", "previous_filename": "application.py"}]
    with pytest.raises(ValueError, match="outside accepted"):
        gate.merge_snapshot(api, REPO, BASE, HEAD)
    api.changes = [{"filename": "docs/x"}] * 300
    with pytest.raises(ValueError, match="truncated"):
        gate.merge_snapshot(api, REPO, BASE, HEAD)


def test_research_label_cannot_promote_full_completion_or_experiment_default_merge():
    c, p, f, r = fixture()
    r["work"]["phase"] = "research"
    p["claim"] = "objective_complete"
    with pytest.raises(ValueError, match="scope"):
        gate.merge_snapshot(API(c, p, f, r), REPO, BASE, HEAD)
    p["claim"] = "slice"
    r["work"].update(kind="experiment", phase="implementation")
    r["questions"][0]["status"] = "unknown"
    api = API(c, p, f, r)
    with pytest.raises(ValueError, match="default product"):
        gate.merge_snapshot(api, REPO, BASE, HEAD)
    assert gate.merge_snapshot(api, REPO, "c" * 40, HEAD)["product_admitted"] is False
    with pytest.raises(ValueError):
        check(c, f, r, "release")


def test_unrelated_edit_reuses_acceptance_but_relevant_edit_does_not():
    c, p, f, r = fixture()
    a = native(r, c, p)
    f["unrelated.txt"] = b"ordinary edit"
    check(c, f, r)
    gate.accept(r, REPO, a, r)
    f["packet.md"] = b"stale entry pointer"
    with pytest.raises(ValueError, match="stale"):
        check(c, f, r)


def setup_git(tmp_path, c, p, f, r):
    data = {
        **f,
        objective.CONTRACT: json.dumps(c).encode(),
        objective.PROOF: json.dumps(p).encode(),
        gate.RECORD: json.dumps(r).encode(),
    }
    for name, raw in data.items():
        file = tmp_path / name
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_bytes(raw)
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
            "fixture",
        ],
        check=True,
    )
    return subprocess.check_output(["git", "-C", str(tmp_path), "rev-parse", "HEAD"], text=True).strip()


def test_real_git_local_phase_and_uncommitted_research_fail_closed(tmp_path):
    c, p, f, r = fixture()
    head = setup_git(tmp_path, c, p, f, r)
    api = API(c, p, f, r)
    assert gate.local_check(tmp_path, "test_strategy", api, REPO, head, head)["product_admitted"]
    (tmp_path / "capture.txt").write_bytes(b"uncommitted evidence")
    with pytest.raises(ValueError, match="uncommitted"):
        gate.local_check(tmp_path, "test_strategy", api, REPO, head, head)


@pytest.mark.parametrize("stage", ["requirements_and_ux", "research", "research_and_unknowns"])
def test_cli_skip_and_dashboard_do_not_advance_unresolved_product(tmp_path, monkeypatch, capsys, stage):
    from scripts import programstart_serve as dashboard
    from scripts import programstart_workflow_state as cli
    from scripts.programstart_challenge_merge import GitHub

    c, p, f, r = fixture()
    r["questions"][0]["status"] = "unknown"
    head = setup_git(tmp_path, c, p, f, r)
    api = API(c, p, f, r)
    original = api.api
    monkeypatch.setattr(
        GitHub, "api", lambda self, route: {"object": {"sha": head}} if "/git/ref/heads/" in route else original(route)
    )
    monkeypatch.setattr(GitHub, "pages", lambda self, route: api.pages(route))
    state = {"active_stage": stage, "stages": {stage: {"status": "in_progress", "signoff": {}}}}
    writes = []
    for module in [cli, dashboard]:
        monkeypatch.setattr(module, "load_registry", lambda: {})
        monkeypatch.setattr(module, "load_workflow_state", lambda *a: state)
        monkeypatch.setattr(module, "workflow_active_step", lambda *a: stage)
        monkeypatch.setattr(module, "workflow_steps", lambda *a: [stage, "architecture_and_risk_spikes"])
        monkeypatch.setattr(module, "workspace_path", lambda name: tmp_path / name)
        monkeypatch.setattr(module, "save_workflow_state", lambda *a, **k: writes.append(a))
        monkeypatch.setattr(module, "system_is_optional_and_absent", lambda *a: False, raising=False)
    monkeypatch.setattr(
        "sys.argv", ["workflow", "advance", "--system", "programbuild", "--skip-preflight", "--skip-gate-check", "--dry-run"]
    )
    assert cli.main() == 1
    assert "required research unresolved" in capsys.readouterr().out
    assert (
        dashboard.advance_workflow_with_signoff("programbuild", "approved", "2026-10-17", "", False, gate_result="clear")[
            "exit_code"
        ]
        == 1
    )
    assert not writes and state["stages"][stage]["status"] == "in_progress"


def test_bootstrap_preserves_research_and_new_unaccepted_placeholders(tmp_path):
    from scripts.programstart_bootstrap import write_project_agent_entry

    write_project_agent_entry(tmp_path, project_name="fixture", variant="product", external_runtime=True, dry_run=False)
    record = tmp_path / gate.RECORD
    assert json.loads(record.read_text())["status"] == "UNACCEPTED_DISCOVERY"
    record.write_text("owner existing data")
    write_project_agent_entry(tmp_path, project_name="fixture", variant="product", external_runtime=True, dry_run=False)
    assert record.read_text() == "owner existing data"


def test_research_label_cannot_adopt_application_even_with_accepted_path():
    c, p, f, r = fixture()
    r["work"].update(phase="research", allowed_paths=["app.py"])
    with pytest.raises(ValueError, match="research-only scope"):
        gate.allowed(["app.py"], r)


def test_full_completion_cannot_omit_research_objective_scope():
    c, p, f, r = fixture()
    p["claim"] = "objective_complete"
    api = API(c, p, f, r)
    with pytest.raises(ValueError, match="omits research objective scope"):
        gate.merge_snapshot(api, REPO, BASE, HEAD)


def test_documented_schema_matches_runtime_record():
    from pathlib import Path

    import jsonschema

    c, p, f, r = fixture()
    schema = json.loads((Path(__file__).resolve().parents[1] / "schemas/research-evidence.schema.json").read_text())
    jsonschema.validate(r, schema, format_checker=jsonschema.FormatChecker())
    check(c, f, r)
    r["extra"] = True
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(r, schema)
    with pytest.raises(ValueError, match="fields"):
        check(c, f, r)


def test_admission_stage_names_cover_the_actual_workflow_registry():
    from scripts.programstart_common import load_registry, workflow_steps

    actual = set(workflow_steps(load_registry(), "programbuild"))
    assert "research" in actual
    assert actual - {"inputs_and_mode_selection", "feasibility"} <= set(gate.STAGES)
