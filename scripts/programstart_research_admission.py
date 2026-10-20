"""Evidence-bound prerequisite admission. Native acceptance does not prove source truth."""

from __future__ import annotations

import hashlib
import subprocess
from collections.abc import Callable
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any, cast
from urllib.parse import quote, unquote, urlsplit

try:
    from .programstart_objective_proof import (
        CONTRACT,
        HEX,
        OWNER,
        PROOF,
        contract_ids,
        digest,
        git_file,
        parse,
        read_api_file,
        require,
        text,
    )
except ImportError:
    from programstart_objective_proof import (
        CONTRACT,
        HEX,
        OWNER,
        PROOF,
        contract_ids,
        digest,
        git_file,
        parse,
        read_api_file,
        require,
        text,
    )

RECORD = "PROGRAMBUILD/RESEARCH_EVIDENCE.json"
MARKER = "PROGRAMSTART_RESEARCH_ADMISSION_V1\n"
PHASES = {"research": 0, "architecture": 1, "implementation": 2, "release": 3}
STAGES = {
    "research": "architecture",
    "research_and_unknowns": "architecture",
    "requirements_and_ux": "architecture",
    "architecture_and_risk_spikes": "architecture",
    "scaffold_and_guardrails": "implementation",
    "test_strategy": "implementation",
    "implementation_loop": "implementation",
    "release_readiness": "release",
    "audit_and_drift_control": "release",
    "post_launch_review": "release",
}


def fields(value: Any, keys: set[str], label: str) -> None:
    require(isinstance(value, dict) and set(value) == keys, f"invalid {label} fields")


def strings(value: Any, label: str) -> list[str]:
    require(isinstance(value, list) and value and all(text(x) for x in value), f"missing {label}")
    require(len(set(value)) == len(value), f"duplicate {label}")
    return value


def path(value: Any, *, prefix: bool = False) -> str:
    require(isinstance(value, str) and bool(value), "invalid research path")
    p = value[:-1] if prefix and value.endswith("/") else value
    require(
        p and not p.startswith("/") and "\\" not in p and all(x.casefold() not in {"", ".", "..", ".git"} for x in p.split("/")),
        "unsafe research path",
    )
    require(not any(c in p for c in "*?[]:\x00\n\r"), "research path is not literal")
    return value


def bound(binding: Any, read: Callable[[str], bytes]) -> str:
    fields(binding, {"path", "sha256"}, "binding")
    p = path(binding["path"])
    require(p != RECORD and isinstance(binding["sha256"], str) and HEX.fullmatch(binding["sha256"]), "invalid research binding")
    raw = read(p)
    require(isinstance(raw, bytes) and len(raw) <= 1024 * 1024, "research evidence bytes unavailable or oversized")
    require(hashlib.sha256(raw).hexdigest() == binding["sha256"], f"stale research binding: {p}")
    return p


def inspect(
    record: dict[str, Any], contract: dict[str, Any], read: Callable[[str], bytes], phase: str, *, today: date | None = None
) -> dict[str, Any]:
    require(phase in PHASES, "unknown research admission phase")
    today = today or datetime.now(UTC).date()
    fields(
        record,
        {
            "version",
            "owner_ref",
            "objective_contract_sha256",
            "research_path",
            "decision_ref",
            "entrypoints",
            "bindings",
            "work",
            "questions",
        },
        "research record",
    )
    require(type(record["version"]) is int and record["version"] == 1, "unsupported research version")
    ids = set(contract_ids(contract))
    require(
        record["owner_ref"] == contract["owner_ref"] and record["objective_contract_sha256"] == digest(contract),
        "research objective/owner binding changed",
    )
    research = path(record["research_path"])
    fields(record["decision_ref"], {"path", "id"}, "research decision")
    decision = path(record["decision_ref"]["path"])
    require(text(record["decision_ref"]["id"]), "research decision identity missing")
    entries = strings(record["entrypoints"], "entrypoints")
    for p in entries:
        path(p)
    require(isinstance(record["bindings"], list), "research bindings missing")
    bindings = [bound(b, read) for b in record["bindings"]]
    require(len(bindings) == len(set(bindings)), "duplicate research binding")
    require({research, decision, *entries} <= set(bindings), "research/decision/entrypoint bindings omitted")
    work = record["work"]
    fields(
        work, {"kind", "phase", "objective_ids", "allowed_paths", "excluded_claims", "parent_terminal_condition"}, "research work"
    )
    require(work["kind"] in {"product", "experiment"} and work["phase"] in PHASES, "invalid accepted work scope")
    selected = set(strings(work["objective_ids"], "work objective IDs"))
    require(selected <= ids, "research work refers to unknown objective")
    require(PHASES[phase] <= PHASES[work["phase"]], "requested phase exceeds accepted research scope")
    for p in strings(work["allowed_paths"], "allowed paths"):
        path(p, prefix=True)
    strings(work["excluded_claims"], "excluded claims")
    require(text(work["parent_terminal_condition"]), "parent terminal condition missing")
    questions = record["questions"]
    require(isinstance(questions, list) and questions, "research prerequisites missing")
    seen, covered, unresolved = set(), set(), []
    for q in questions:
        fields(
            q,
            {
                "id",
                "objective_ids",
                "question",
                "required_before",
                "status",
                "finding",
                "next_action",
                "invalidation",
                "evidence",
            },
            "research question",
        )
        require(text(q["id"]) and q["id"] not in seen, "missing/duplicate research question ID")
        seen.add(q["id"])
        qids = set(strings(q["objective_ids"], "question objective IDs"))
        require(qids <= selected, "research question refers outside selected objectives")
        covered |= qids
        require(all(text(q[k]) for k in ["question", "finding", "next_action"]), "research finding/action missing")
        strings(q["invalidation"], "invalidation conditions")
        require(q["required_before"] in {"architecture", "implementation", "release"}, "invalid prerequisite boundary")
        require(q["status"] in {"supported", "unsupported", "unknown", "not_applicable"}, "invalid prerequisite disposition")
        require(isinstance(q["evidence"], list), "research evidence missing")
        independent = False
        for e in q["evidence"]:
            fields(
                e,
                {"path", "sha256", "source_url", "kind", "observed_at", "valid_until", "observed_capability", "limitations"},
                "research evidence",
            )
            bound({k: e[k] for k in ["path", "sha256"]}, read)
            url = urlsplit(e["source_url"])
            require(e["kind"] in {"primary", "observation", "derived"}, "invalid source kind")
            require(
                url.scheme == "https" and url.hostname and not url.username and not url.password and not url.fragment,
                "invalid research source URL",
            )
            owner = OWNER.fullmatch(record["owner_ref"])
            require(owner is not None, "research owner invalid")
            owner_name = cast(Any, owner).group(1).split("/")[0].lower()
            host, urlpath = cast(str, url.hostname).lower().rstrip("."), unquote(url.path).lower()
            own = host in {"github.com", "raw.githubusercontent.com"} and urlpath.startswith("/" + owner_name + "/")
            require(not own or e["kind"] == "derived", "own plan/mock cannot establish independent research")
            observed, until = date.fromisoformat(e["observed_at"]), date.fromisoformat(e["valid_until"])
            require(observed <= today <= until, "research evidence expired or from the future")
            require(text(e["observed_capability"]) and text(e["limitations"]), "inspection finding/limitations missing")
            independent |= e["kind"] in {"primary", "observation"}
        require(q["status"] != "supported" or independent, "supported prerequisite lacks independent evidence")
        if q["status"] in {"unknown", "unsupported"} and PHASES[q["required_before"]] <= PHASES[phase]:
            unresolved.append(q["id"])
    require(covered == selected, "selected objective research coverage omitted")
    require(work["kind"] == "experiment" or not unresolved, "required research unresolved: " + ", ".join(unresolved))
    require(work["kind"] != "experiment" or phase != "release", "experiment cannot authorize product release")
    return {
        "coverage": "ENROLLED",
        "phase": phase,
        "work_kind": work["kind"],
        "product_admitted": work["kind"] == "product" and phase != "research",
        "unresolved": unresolved,
        "record_sha256": digest(record),
    }


def accept(record: dict[str, Any], repository: str, authority: dict[str, Any], prior: dict[str, Any] | None) -> None:
    owner = authority["repository"]["owner"]
    require(authority["repository"]["full_name"] == repository, "foreign research repository")
    match = OWNER.fullmatch(record["owner_ref"])
    require(match is not None and match.group(1) == repository, "foreign research owner")
    issue = authority["issue"]
    require(
        issue["number"] == int(cast(Any, match).group(2)) and issue["html_url"] == record["owner_ref"], "foreign research issue"
    )
    rows = authority["comments"]
    require(len({x["id"] for x in rows}) == len(rows), "duplicate research acceptance observation")
    previous, accepted, latest = None, set(), None
    for c in sorted(rows, key=lambda x: x["id"]):
        user, body = c.get("user") or {}, c.get("body") or ""
        if user.get("id") != owner["id"] or user.get("login") != owner["login"] or not body.startswith(MARKER):
            continue
        require(
            c.get("created_at") == c.get("updated_at") and c.get("issue_url") == issue["url"],
            "edited/foreign research acceptance",
        )
        r = parse(body[len(MARKER) :])
        fields(
            r,
            {"record_sha256", "previous_sha256", "result", "reason", "objective_contract_sha256", "scope_sha256"},
            "research acceptance",
        )
        require(r["result"] in {"accepted", "rejected"} and text(r["reason"]), "invalid research acceptance")
        require(isinstance(r["record_sha256"], str) and HEX.fullmatch(r["record_sha256"]), "invalid accepted research digest")
        require(r["previous_sha256"] == previous, "research acceptance history broken")
        if r["result"] == "accepted":
            previous = r["record_sha256"]
            accepted.add(previous)
        latest = r
    require(
        latest is not None and latest["result"] == "accepted" and previous == digest(record), "research is unaccepted or revoked"
    )
    latest = cast(dict[str, Any], latest)
    require(
        latest["objective_contract_sha256"] == record["objective_contract_sha256"]
        and latest["scope_sha256"] == digest(record["work"]),
        "accepted research scope/objective changed",
    )
    if prior is not None:
        require(prior["owner_ref"] == record["owner_ref"] and digest(prior) in accepted, "prior research baseline/owner missing")


def authority(adapter: Any, repository: str, record: dict[str, Any]) -> dict[str, Any]:
    match = OWNER.fullmatch(record["owner_ref"])
    require(match is not None and match.group(1) == repository, "foreign research owner")
    issue = cast(Any, match).group(2)
    return {
        "repository": adapter.api(f"repos/{repository}"),
        "issue": adapter.api(f"repos/{repository}/issues/{issue}"),
        "comments": adapter.pages(f"repos/{repository}/issues/{issue}/comments"),
    }


def allowed(paths: list[str], record: dict[str, Any]) -> None:
    for changed in paths:
        path(changed)
        if record["work"]["kind"] == "product" and record["work"]["phase"] == "research":
            metadata = changed in {
                "README.md",
                "GAMEPLAN.md",
                "DECISIONS.md",
                "EXECUTION_PROMPT.md",
                "NEXT_WORK_PACKET.md",
                "AGENTS.md",
            }
            evidence = changed.startswith(("docs/", "PROGRAMBUILD/")) and changed.endswith((".md", ".json", ".txt", ".csv"))
            require(metadata or evidence, "research-only scope cannot adopt application/policy code")
        require(
            any(changed == p or p.endswith("/") and changed.startswith(p) for p in record["work"]["allowed_paths"]),
            f"change outside accepted research scope: {changed}",
        )


def merge_snapshot(adapter: Any, repository: str, target: str, head: str) -> dict[str, Any]:
    old = read_api_file(adapter, repository, target, RECORD, optional=True)
    raw = read_api_file(adapter, repository, head, RECORD, optional=True)
    if old is None and raw is None:
        return {"coverage": "UNENROLLED", "product_admitted": False}
    require(raw is not None, "candidate removed research enrollment")
    record = parse(cast(bytes, raw))
    contract_raw = read_api_file(adapter, repository, head, CONTRACT)
    require(contract_raw is not None, "research requires objective contract")
    proof_raw = read_api_file(adapter, repository, head, PROOF)
    require(proof_raw is not None, "research requires outcome trace")
    contract_raw = cast(bytes, contract_raw)
    proof_raw = cast(bytes, proof_raw)
    full = parse(proof_raw).get("claim") == "objective_complete"
    if full:
        require(
            set(record["work"]["objective_ids"]) == set(contract_ids(parse(contract_raw))),
            "full completion omits research objective scope",
        )
    phase = "release" if full else record["work"]["phase"]

    def read_required(p: str) -> bytes:
        value = read_api_file(adapter, repository, head, p)
        require(value is not None, "research evidence missing")
        return cast(bytes, value)

    result = inspect(record, parse(contract_raw), read_required, phase)
    native = authority(adapter, repository, record)
    accept(record, repository, native, parse(old) if old else None)
    compared = adapter.api(f"repos/{repository}/compare/{target}...{head}")
    changed = compared.get("files")
    require(
        isinstance(changed, list)
        and len(changed) < 300
        and all(isinstance(x, dict) and text(x.get("filename")) for x in changed),
        "research changed-file coverage unavailable/truncated",
    )
    paths = [x["filename"] for x in changed] + [x["previous_filename"] for x in changed if "previous_filename" in x]
    allowed(paths, record)
    if record["work"]["kind"] == "experiment":
        branch = quote(native["repository"]["default_branch"], safe="")
        default = adapter.api(f"repos/{repository}/git/ref/heads/{branch}")["object"]["sha"]
        require(target != default, "experiment cannot adopt into default product branch")
    return {**result, "authority_sha256": digest(native), "changed_paths_sha256": digest(paths)}


def local_check(
    root: Path, stage: str, adapter: Any, repository: str, base: str, head: str, *, terminal: bool = False
) -> dict[str, Any]:
    phase = "release" if terminal else STAGES.get(stage)
    if phase is None:
        return {"coverage": "NOT_REQUIRED", "product_admitted": False}
    old = read_api_file(adapter, repository, base, RECORD, optional=True)
    local = root / RECORD
    if old is None and not local.exists():
        return {"coverage": "UNENROLLED", "product_admitted": False}
    require(local.exists(), "local research enrollment removed")
    raw = git_file(root, head, RECORD)
    require(raw == local.read_bytes(), "uncommitted research record")
    record = parse(raw)
    result = inspect(record, parse(git_file(root, head, CONTRACT)), lambda p: git_file(root, head, p), phase)

    def working(p: str) -> bytes:
        file = root / p
        require(file.resolve().is_relative_to(root.resolve()) and not file.is_symlink(), "research working path escapes root")
        return file.read_bytes()

    for b in record["bindings"]:
        require(working(b["path"]) == git_file(root, head, b["path"]), "uncommitted research input")
    for q in record["questions"]:
        for e in q["evidence"]:
            require(working(e["path"]) == git_file(root, head, e["path"]), "uncommitted research evidence")
    native = authority(adapter, repository, record)
    accept(record, repository, native, parse(old) if old else None)
    changed = (
        subprocess.check_output(["git", "-C", str(root), "diff", "--no-renames", "--name-only", "-z", base, head], timeout=15)
        .decode()
        .split("\0")
    )
    allowed([p for p in changed if p], record)
    dirty = subprocess.check_output(
        ["git", "-C", str(root), "status", "--porcelain=v1", "-z", "--untracked-files=all"], timeout=15
    )
    require(not dirty, "research admission requires a clean worktree")
    return result
