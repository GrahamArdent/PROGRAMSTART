"""Objective preservation gate. Candidate records are claims, never owner acceptance.

The local workflow uses authenticated GitHub reads through the existing gh adapter.
No candidate-defined command is executed. Raw GitHub writes and uninstrumented release
consumers remain outside this gate; this module does not promise universal interception.
"""

from __future__ import annotations

import base64
import hashlib
import json
import re
import subprocess
from pathlib import Path, PurePosixPath
from typing import Any
from urllib.parse import quote

CONTRACT = "PROGRAMBUILD/OBJECTIVES.json"
PROOF = "PROGRAMBUILD/OUTCOME_PROOF.json"
MARKER = "PROGRAMSTART_OBJECTIVE_ACCEPTANCE_V1\n"
HEX = re.compile(r"^[0-9a-f]{64}$")
SHA = re.compile(r"^[0-9a-f]{40}$")
OWNER = re.compile(r"https://github\.com/([\w.-]+/[\w.-]+)/issues/([1-9][0-9]*)$")
IMPLEMENTATION_STAGES = {
    "inputs_and_mode_selection",
    "requirements_and_ux",
    "architecture_and_risk_spikes",
    "scaffold_and_guardrails",
    "test_strategy",
}
COMPLETION_STAGES = {"implementation_loop", "release_readiness", "audit_and_drift_control", "post_launch_review"}


class ObjectiveDenied(ValueError):
    """The declared objective claim cannot be accepted."""


def require(condition: Any, message: str) -> None:
    if not condition:
        raise ObjectiveDenied(message)


def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, "duplicate JSON key")
        result[key] = value
    return result


def parse(raw: bytes | str) -> dict[str, Any]:
    require(len(raw) <= 1024 * 1024, "objective record exceeds 1 MiB")
    value = json.loads(raw, object_pairs_hook=unique)
    require(isinstance(value, dict), "objective record must be an object")
    return value


def digest(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()).hexdigest()


def text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def contract_ids(contract: dict[str, Any]) -> list[str]:
    require(
        set(contract) == {"version", "owner_ref", "protected_outcome", "objectives", "proof_workflow"},
        "invalid objective contract fields",
    )
    require(type(contract["version"]) is int and contract["version"] == 1, "unsupported objective contract version")
    require(
        isinstance(contract["owner_ref"], str) and OWNER.fullmatch(contract["owner_ref"]), "owner_ref must be a native issue URL"
    )
    require(text(contract["protected_outcome"]), "protected outcome missing")
    require(
        isinstance(contract["proof_workflow"], str)
        and re.fullmatch(r"\.github/workflows/[\w.-]+\.ya?ml", contract["proof_workflow"]),
        "owner-selected proof workflow missing",
    )
    objectives = contract["objectives"]
    require(isinstance(objectives, list) and objectives, "no objectives")
    ids = []
    for row in objectives:
        require(isinstance(row, dict) and set(row) == {"id", "outcome", "success_criteria"}, "invalid objective fields")
        require(text(row["id"]) and text(row["outcome"]), "objective identity/outcome missing")
        require(
            isinstance(row["success_criteria"], list)
            and row["success_criteria"]
            and all(text(x) for x in row["success_criteria"]),
            "observable success criteria missing",
        )
        ids.append(row["id"])
    require(len(ids) == len(set(ids)), "duplicate objective id")
    return ids


def inspect_proof(contract: dict[str, Any], proof: dict[str, Any], read_file: Any, *, complete: bool) -> None:
    ids = contract_ids(contract)
    require(set(proof) == {"version", "contract_sha256", "claim", "objectives"}, "invalid proof fields")
    require(type(proof["version"]) is int and proof["version"] == 1, "unsupported proof version")
    require(proof["contract_sha256"] == digest(contract), "proof uses a different objective baseline")
    require(proof["claim"] in {"slice", "objective_complete"}, "unknown completion scope")
    require(not complete or proof["claim"] == "objective_complete", "slice success cannot close the objective")
    rows = proof["objectives"]
    require(isinstance(rows, list) and all(isinstance(x, dict) for x in rows), "invalid proof rows")
    row_ids = [x.get("id") for x in rows]
    require(len(row_ids) == len(set(row_ids)) and set(row_ids) == set(ids), "objective coverage omitted, duplicated or added")
    for row in rows:
        require(
            set(row)
            == {"id", "status", "requirements", "implementation", "scenario", "environment", "evidence", "reason", "resume_when"},
            "invalid objective trace fields",
        )
        require(row["status"] in {"pending", "blocked", "deferred", "passed"}, "invalid objective status")
        if row["status"] != "passed":
            require(not complete, f"required objective {row['id']} is {row['status']}")
            require(text(row["reason"]) and text(row["resume_when"]), "incomplete objective needs reason and resume condition")
        roles = ["requirements", "scenario", "environment"]
        if row["status"] == "passed":
            roles += ["implementation", "evidence"]
        for role in roles:
            bindings = row[role]
            require(isinstance(bindings, list) and bindings, f"{row['id']}: missing {role} binding")
            paths = []
            for binding in bindings:
                require(isinstance(binding, dict) and set(binding) == {"path", "sha256"}, "invalid evidence binding")
                path = binding["path"]
                require(
                    isinstance(path, str)
                    and path
                    and "\\" not in path
                    and not PurePosixPath(path).is_absolute()
                    and all(x not in {".", "..", ".git"} for x in path.split("/")),
                    "unsafe evidence path",
                )
                require(path not in {CONTRACT, PROOF}, "proof cannot bind itself as implementation/evidence")
                require(isinstance(binding["sha256"], str) and HEX.fullmatch(binding["sha256"]), "invalid evidence digest")
                data = read_file(path)
                require(hashlib.sha256(data).hexdigest() == binding["sha256"], f"stale or tampered {role}: {path}")
                paths.append(path)
            require(len(paths) == len(set(paths)), "duplicate evidence path")


def accept_owner_records(
    contract: dict[str, Any],
    proof: dict[str, Any],
    authority: dict[str, Any],
    head: str,
    *,
    complete: bool,
    prior_contract: dict[str, Any] | None = None,
) -> None:
    """authority must be supplied by the authenticated API adapter, never project JSON."""
    match = OWNER.fullmatch(contract["owner_ref"])
    if match is None:
        raise ObjectiveDenied("invalid owner")
    repository, issue = match.groups()
    require(authority["repository"]["full_name"] == repository, "foreign objective owner repository")
    require(
        authority["issue"]["number"] == int(issue) and authority["issue"]["html_url"] == contract["owner_ref"],
        "foreign objective owner issue",
    )
    owner = authority["repository"]["owner"]
    rows = authority["comments"]
    require(len({r["id"] for r in rows}) == len(rows), "duplicate owner observation")
    records = []
    for comment in sorted(rows, key=lambda x: x["id"]):
        user = comment.get("user") or {}
        body = comment.get("body") or ""
        if user.get("id") != owner["id"] or user.get("login") != owner["login"] or not body.startswith(MARKER):
            continue
        require(comment.get("created_at") == comment.get("updated_at"), "objective acceptance was edited")
        require(comment.get("issue_url") == authority["issue"]["url"], "acceptance belongs to another issue")
        record = parse(body[len(MARKER) :])
        require(
            set(record)
            == {
                "claim",
                "result",
                "contract_sha256",
                "previous_contract_sha256",
                "scope_change_reason",
                "head_sha",
                "proof_sha256",
                "run_id",
            },
            "invalid objective acceptance fields",
        )
        require(
            record["claim"] in {"baseline", "completion"} and record["result"] in {"accepted", "rejected"},
            "invalid owner disposition",
        )
        require(
            isinstance(record["contract_sha256"], str) and HEX.fullmatch(record["contract_sha256"]),
            "invalid accepted contract digest",
        )
        records.append(record)
    baselines = [r for r in records if r["claim"] == "baseline"]
    require(baselines, "no authenticated objective baseline acceptance")
    previous = None
    for record in baselines:
        require(record["previous_contract_sha256"] == previous, "objective baseline history broken")
        require(previous is None or text(record["scope_change_reason"]), "scope change lacks owner rationale")
        if record["result"] == "accepted":
            previous = record["contract_sha256"]
    require(baselines[-1]["result"] == "accepted" and previous == digest(contract), "objective baseline is unaccepted or revoked")
    if prior_contract is not None:
        require(prior_contract["owner_ref"] == contract["owner_ref"], "objective owner redirection")
        require(
            digest(prior_contract) in {r["contract_sha256"] for r in baselines if r["result"] == "accepted"},
            "accepted target baseline missing from owner history",
        )
    if complete:
        require(isinstance(head, str) and SHA.fullmatch(head), "candidate identity unavailable")
        completions = [r for r in records if r["claim"] == "completion" and r["head_sha"] == head]
        require(completions, "no authenticated exact-head outcome proof acceptance")
        current = completions[-1]
        require(
            current["result"] == "accepted"
            and current["contract_sha256"] == digest(contract)
            and current["proof_sha256"] == digest(proof),
            "outcome proof unaccepted, stale or revoked",
        )
        run_id = current["run_id"]
        require(type(run_id) is int and run_id > 0, "native proof run identity missing")
        run = authority.get("proof_runs", {}).get(str(run_id), {})
        require(run.get("id") == run_id and run.get("head_sha") == head, "native proof run does not bind this candidate")
        require(run.get("status") == "completed" and run.get("conclusion") == "success", "native proof run not successful")
        require(
            run.get("repository", {}).get("full_name") == repository and run.get("path") == contract["proof_workflow"],
            "foreign native proof workflow",
        )


def load_proof_runs(adapter: Any, repository: str, authority: dict[str, Any]) -> None:
    """Only provider-native run truth is consumed, never a candidate green label."""
    owner = authority["repository"]["owner"]
    ids = set()
    for row in authority["comments"]:
        user = row.get("user") or {}
        body = row.get("body") or ""
        if user.get("id") == owner["id"] and user.get("login") == owner["login"] and body.startswith(MARKER):
            record = parse(body[len(MARKER) :])
            if record.get("claim") == "completion" and type(record.get("run_id")) is int:
                ids.add(record["run_id"])
    require(len(ids) <= 100, "too many proof runs for bounded read")
    authority["proof_runs"] = {str(run_id): adapter.api(f"repos/{repository}/actions/runs/{run_id}") for run_id in sorted(ids)}


def git_file(root: Path, ref: str, path: str) -> bytes:
    mode = subprocess.run(["git", "-C", str(root), "ls-tree", ref, "--", path], capture_output=True, check=False, timeout=15)
    require(
        mode.returncode == 0 and mode.stdout.split(b" ", 1)[0] in {b"100644", b"100755"},
        f"evidence is not a regular Git file: {path}",
    )
    result = subprocess.run(["git", "-C", str(root), "show", f"{ref}:{path}"], capture_output=True, check=False, timeout=15)
    require(result.returncode == 0, f"missing committed evidence: {path}")
    return result.stdout


def read_api_file(adapter: Any, repository: str, ref: str, path: str, *, optional: bool = False) -> bytes | None:
    # List the parent first so a missing file is distinct from an API/auth failure.
    parent, _, name = path.rpartition("/")
    root_listing = adapter.api(f"repos/{repository}/contents?ref={ref}")
    require(isinstance(root_listing, list), "repository listing unavailable")
    require(len(root_listing) < 1000, "repository listing may be truncated")
    if parent and not any(x.get("name") == parent.split("/")[0] for x in root_listing):
        require(optional, f"missing objective directory: {parent}")
        return None
    listing = adapter.api(f"repos/{repository}/contents/{quote(parent, safe='/')}?ref={ref}") if parent else root_listing
    require(isinstance(listing, list), "objective directory unavailable")
    require(len(listing) < 1000, "objective directory listing may be truncated")
    entry = next((x for x in listing if x.get("name") == name), None)
    if entry is None:
        require(optional, f"missing objective contract: {path}")
        return None
    require(entry.get("type") == "file", "objective path is not a regular directory entry")
    item = adapter.api(f"repos/{repository}/contents/{quote(path, safe='/')}?ref={ref}")
    require(
        item.get("encoding") == "base64" and item.get("type") == "file" and "target" not in item,
        "objective file bytes unavailable or not regular",
    )
    raw = base64.b64decode(item["content"], validate=False)
    blob = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
    require(entry.get("sha") == item.get("sha") == blob, "objective directory/blob identity mismatch")
    return raw


def workflow_problems(root: Path, stage: str, *, terminal: bool = False) -> list[str]:
    if not terminal and stage not in IMPLEMENTATION_STAGES | COMPLETION_STAGES:
        return []
    try:
        contract = parse((root / CONTRACT).read_bytes())
        proof = parse((root / PROOF).read_bytes())
        complete = terminal or stage in COMPLETION_STAGES

        # Local byte bindings are checked, then authenticated native owner acceptance.
        def local(path: str) -> bytes:
            p = root / path
            require(p.resolve().is_relative_to(root.resolve()) and not p.is_symlink(), "evidence escapes workspace")
            return p.read_bytes()

        inspect_proof(contract, proof, local, complete=complete)
        try:
            from .programstart_challenge_merge import GitHub
        except ImportError:  # pragma: no cover
            from programstart_challenge_merge import GitHub
        adapter = GitHub()
        owner = OWNER.fullmatch(contract["owner_ref"])
        if owner is None:
            raise ObjectiveDenied("invalid owner")
        repository = owner.group(1)
        remote = (
            subprocess.check_output(["git", "-C", str(root), "remote", "get-url", "origin"], text=True, timeout=15)
            .strip()
            .removesuffix(".git")
        )
        require(
            remote in {f"https://github.com/{repository}", f"git@github.com:{repository}"},
            "objective owner does not match repository origin",
        )
        repo = adapter.api(f"repos/{repository}")
        branch = repo["default_branch"]
        base_sha = adapter.api(f"repos/{repository}/git/ref/heads/{quote(branch, safe='')}")["object"]["sha"]
        old = read_api_file(adapter, repository, base_sha, CONTRACT, optional=True)
        prior = parse(old) if old is not None else None
        issue = owner.group(2)
        authority = {
            "repository": repo,
            "issue": adapter.api(f"repos/{repository}/issues/{issue}"),
            "comments": adapter.pages(f"repos/{repository}/issues/{issue}/comments"),
        }
        head = subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], text=True, timeout=15).strip()
        if complete:
            load_proof_runs(adapter, repository, authority)
            require(
                read_api_file(adapter, repository, base_sha, contract["proof_workflow"])
                == git_file(root, head, contract["proof_workflow"]),
                "candidate changed the trusted proof workflow",
            )
        require(
            git_file(root, head, CONTRACT) == (root / CONTRACT).read_bytes()
            and git_file(root, head, PROOF) == (root / PROOF).read_bytes(),
            "objective records have uncommitted edits",
        )
        # Bind all referenced evidence to the exact commit accepted by the owner.
        inspect_proof(contract, proof, lambda path: git_file(root, head, path), complete=complete)
        accept_owner_records(contract, proof, authority, head, complete=complete, prior_contract=prior)
        return []
    except (OSError, ValueError, KeyError, TypeError, subprocess.SubprocessError) as exc:
        return [f"Objective proof gate blocked: {exc}"]


def merge_objective_snapshot(adapter: Any, repository: str, target: str, head: str) -> dict[str, Any]:
    """Enrolled merge preflight: no full-completion inference from a slice PR."""
    base = read_api_file(adapter, repository, target, CONTRACT, optional=True)
    candidate = read_api_file(adapter, repository, head, CONTRACT, optional=True)
    if base is None and candidate is None:
        return {"coverage": "UNENROLLED", "objective_complete": False}
    if candidate is None:
        raise ObjectiveDenied("candidate removed the accepted objective contract")
    contract = parse(candidate)
    raw = read_api_file(adapter, repository, head, PROOF)
    if raw is None:
        raise ObjectiveDenied("objective trace missing")
    proof = parse(raw)
    complete = proof.get("claim") == "objective_complete"
    inspect_proof(contract, proof, lambda path: read_api_file(adapter, repository, head, path), complete=complete)
    owner = OWNER.fullmatch(contract["owner_ref"])
    if owner is None:
        raise ObjectiveDenied("invalid owner")
    require(owner.group(1) == repository, "foreign objective owner")
    issue = owner.group(2)
    authority = {
        "repository": adapter.api(f"repos/{repository}"),
        "issue": adapter.api(f"repos/{repository}/issues/{issue}"),
        "comments": adapter.pages(f"repos/{repository}/issues/{issue}/comments"),
    }
    if complete:
        load_proof_runs(adapter, repository, authority)
        workflow = contract["proof_workflow"]
        require(
            read_api_file(adapter, repository, target, workflow) == read_api_file(adapter, repository, head, workflow),
            "candidate changed the trusted proof workflow",
        )
    accept_owner_records(
        contract, proof, authority, head, complete=complete, prior_contract=parse(base) if base is not None else None
    )
    return {
        "coverage": "ENROLLED",
        "objective_complete": complete,
        "contract_sha256": digest(contract),
        "proof_sha256": digest(proof),
        "authority_sha256": digest(authority),
    }
