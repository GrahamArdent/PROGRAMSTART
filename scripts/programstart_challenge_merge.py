"""Bounded GitHub CLI merge admission; not an atomic release-acceptance service.

Run from an accepted methodology checkout, never from the candidate checkout.
GitHub authenticates API authors. Only the repository owner's explicit records
can supply clearance; native changes-requested reviews remain blocking.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import re
import subprocess
from collections.abc import Callable
from pathlib import Path
from typing import Any
from urllib.parse import quote

MARKER = "PROGRAMSTART_CHALLENGE_DISPOSITION_V1\n"
WITHDRAWAL_MARKER = "PROGRAMSTART_CHALLENGE_CLEAR_WITHDRAWAL_V1\n"
SHA = re.compile(r"^[0-9a-f]{40}$")
REPOSITORY = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
FIELDS = {"repository", "pr", "head_sha", "methodology_sha", "scope", "result", "findings", "resolutions", "evidence_refs"}
WITHDRAWAL_FIELDS = {"repository", "pr", "comment_id", "body_sha256", "reason", "evidence_refs"}


class AdmissionDenied(ValueError):
    """Required current evidence is absent, conflicting or blocking."""


def _require(condition: bool, reason: str) -> None:
    if not condition:
        raise AdmissionDenied(reason)


def _strings(value: Any, *, nonempty: bool = False) -> bool:
    return (
        isinstance(value, list)
        and (bool(value) or not nonempty)
        and all(isinstance(item, str) and bool(item.strip()) for item in value)
        and len(value) == len(set(value))
    )


def _unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        _require(key not in result, "duplicate disposition field")
        result[key] = value
    return result


def _is_owner(comment: dict[str, Any], owner: dict[str, Any]) -> bool:
    user = comment.get("user") or {}
    return user.get("id") == owner["id"] and user.get("login") == owner["login"]


def _clear_withdrawals(comments, owner, repository, pr):
    """Append-only revocation of positive assertions; never erase a blocker.

    Preprocess references so an invalid positive record can be withdrawn before
    its invalid resolutions are interpreted. Original body/author/order remain
    authenticated and hashed. At the withdrawal event a same-head CLEAR barrier
    is applied, so falling back to an older CLEAR cannot undo revocation.
    """
    by_id = {comment["id"]: comment for comment in comments}
    withdrawn = set()
    barriers = {}
    for comment in sorted(comments, key=lambda item: item["id"]):
        body = comment.get("body") or ""
        if not _is_owner(comment, owner) or not body.startswith(WITHDRAWAL_MARKER):
            continue
        _require(comment.get("created_at") == comment.get("updated_at"), "withdrawal was edited")
        try:
            record = json.loads(body[len(WITHDRAWAL_MARKER) :], object_pairs_hook=_unique)
            _require(isinstance(record, dict) and set(record) == WITHDRAWAL_FIELDS, "invalid withdrawal fields")
            _require(
                record["repository"] == repository and type(record["pr"]) is int and record["pr"] == pr,
                "withdrawal work item mismatch",
            )
            target_id = record["comment_id"]
            _require(type(target_id) is int and 0 < target_id < comment["id"], "invalid withdrawal reference")
            _require(
                isinstance(record["reason"], str) and bool(record["reason"].strip()) and len(record["reason"]) <= 1024,
                "withdrawal reason missing",
            )
            _require(_strings(record["evidence_refs"], nonempty=True), "withdrawal proof missing")
            target = by_id.get(target_id)
            if target is None:
                raise AdmissionDenied("withdrawal target is unavailable")
            _require(_is_owner(target, owner), "withdrawal target is foreign")
            _require(target.get("created_at") == target.get("updated_at"), "withdrawal target was edited")
            target_body = target.get("body") or ""
            _require(target_body.startswith(MARKER), "only structured positive dispositions can be withdrawn")
            _require(
                record["body_sha256"] == hashlib.sha256(target_body.encode("utf-8")).hexdigest(),
                "withdrawal body identity mismatch",
            )
            positive = json.loads(target_body[len(MARKER) :], object_pairs_hook=_unique)
            _require(isinstance(positive, dict) and set(positive) == FIELDS, "withdrawal target shape is unknown")
            _require(
                positive["repository"] == repository and type(positive["pr"]) is int and positive["pr"] == pr,
                "withdrawal target work item mismatch",
            )
            _require(
                positive["result"] == "clear" and positive["findings"] == [] and positive["scope"] == "repository_merge",
                "withdrawal cannot erase negative evidence",
            )
            _require(
                all(isinstance(positive[k], str) and SHA.fullmatch(positive[k]) for k in ("head_sha", "methodology_sha")),
                "withdrawal target candidate is unknown",
            )
        except (TypeError, ValueError, KeyError) as exc:
            raise AdmissionDenied("invalid authenticated CLEAR withdrawal") from exc
        withdrawn.add(target_id)
        barriers[comment["id"]] = positive["head_sha"]
    return withdrawn, barriers


def admit(
    snapshot: dict[str, Any],
    repository: str,
    pr: int,
    head: str,
    methodology: str,
    *,
    after_merge: bool = False,
    admitted_base: str | None = None,
) -> str:
    """Consume a live authenticated API snapshot, not a caller-supplied CLEAR.

    The API adapter is the trust boundary. Offline JSON is useful for tests but
    is deliberately not exposed as a production CLI input.
    """
    pull = snapshot["pull"]
    _require("objective_proof" in snapshot, "objective gate observation missing")
    _require("research_admission" in snapshot["objective_proof"], "research gate observation missing")
    owner = snapshot["repository"]["owner"]
    own_methodology_advance = (
        after_merge and repository == "GrahamArdent/PROGRAMSTART" and snapshot["methodology_sha"] == pull.get("merge_commit_sha")
    )
    _require(snapshot["methodology_sha"] == methodology or own_methodology_advance, "accepted methodology changed")
    _require(snapshot["repository"]["full_name"] == repository, "repository mismatch")
    _require(pull["number"] == pr and pull["base"]["repo"]["full_name"] == repository, "PR mismatch")
    _require(pull["head"]["sha"] == head, "candidate changed")
    _require(not pull["draft"], "draft PR")
    target_ref = snapshot.get("target_ref")
    target_sha = snapshot.get("target_sha")
    _require(isinstance(pull["base"].get("ref"), str) and bool(pull["base"]["ref"]), "target branch unavailable")
    _require(target_ref == "refs/heads/" + pull["base"]["ref"], "target reference mismatch")
    _require(isinstance(target_sha, str) and SHA.fullmatch(target_sha) is not None, "target reference SHA unavailable")
    if after_merge:
        _require(pull["state"] == "closed" and pull["merged"] is True, "merge poststate unavailable")
        _require(admitted_base is not None, "admitted base missing")
        _require(snapshot["merge_parent_shas"] == [admitted_base], "squash merge parent differs from admitted base")
        _require(target_sha in {admitted_base, pull["merge_commit_sha"]}, "base advanced beyond observed effect")
    else:
        _require(pull["state"] == "open" and not pull["merged"], "PR is not open and unmerged")
        _require(pull["mergeable"] is True and pull["mergeable_state"] == "clean", "native merge readiness unavailable")

    # GitHub reviews are immutable submissions; dismissal is an explicit native
    # operation. A later APPROVED submission must not silently erase an earlier
    # unresolved CHANGES_REQUESTED submission, including one on an ancestor.
    for review in snapshot["reviews"]:
        _require(review.get("state") != "CHANGES_REQUESTED", "unresolved native changes-requested review")

    retained: dict[str, tuple[str, str] | None] = {}
    latest: dict[str, Any] | None = None
    comments = snapshot["comments"]
    _require(len({c["id"] for c in comments}) == len(comments), "duplicate API comment")
    withdrawn, barriers = _clear_withdrawals(comments, owner, repository, pr)
    for comment in sorted(comments, key=lambda item: item["id"]):
        if comment["id"] in barriers:
            if barriers[comment["id"]] == head:
                latest = None
            continue
        if comment["id"] in withdrawn:
            continue
        body = comment.get("body") or ""
        # Login text in the body, author_association and reviewer labels confer
        # no authority. Bind both provider identity and login to the API owner.
        if not _is_owner(comment, owner):
            continue
        if not body.startswith(MARKER):
            # A structured CLEAR cannot erase an existing owner prose blocker.
            if re.search(r"\bCHANGES REQUIRED\b", body, re.IGNORECASE):
                retained[f"github-comment:{comment['id']}"] = None
            continue
        _require(comment.get("created_at") == comment.get("updated_at"), "owner disposition was edited; append a replacement")
        try:
            record = json.loads(body[len(MARKER) :], object_pairs_hook=_unique)
        except (TypeError, ValueError) as exc:
            raise AdmissionDenied("invalid owner disposition") from exc
        _require(isinstance(record, dict) and set(record) == FIELDS, "invalid disposition fields")
        _require(
            record["repository"] == repository and type(record["pr"]) is int and record["pr"] == pr,
            "disposition work item mismatch",
        )
        _require(
            isinstance(record["head_sha"], str) and SHA.fullmatch(record["head_sha"]) is not None, "invalid disposition head"
        )
        _require(
            isinstance(record["methodology_sha"], str) and SHA.fullmatch(record["methodology_sha"]) is not None,
            "invalid methodology identity",
        )
        _require(record["scope"] == "repository_merge", "disposition scope mismatch")
        _require(record["result"] in {"clear", "blocked"}, "invalid disposition result")
        _require(
            _strings(record["findings"]) and _strings(record["evidence_refs"], nonempty=True), "missing disposition evidence"
        )
        _require(isinstance(record["resolutions"], list), "invalid resolutions")
        if record["resolutions"]:
            _require(record["result"] == "clear", "only CLEAR can resolve a retained blocker")
        for resolution in record["resolutions"]:
            _require(
                isinstance(resolution, dict) and set(resolution) == {"finding_id", "evidence_refs"}, "invalid finding resolution"
            )
            _require(
                isinstance(resolution["finding_id"], str) and resolution["finding_id"] in retained,
                "resolution does not identify a retained blocker",
            )
            _require(_strings(resolution["evidence_refs"], nonempty=True), "resolution lacks proof references")
            retained[resolution["finding_id"]] = (record["head_sha"], record["methodology_sha"])
        _require(record["result"] != "blocked" or bool(record["findings"]), "blocked disposition lacks finding identity")
        _require(record["result"] != "clear" or not record["findings"], "CLEAR contains unresolved findings")
        retained.update({finding: None for finding in record["findings"]})
        if record["head_sha"] == head:
            latest = record
    _require(
        all(binding == (head, methodology) for binding in retained.values()),
        "retained Challenge blockers remain unresolved for current candidate",
    )
    _require(latest is not None and latest["result"] == "clear", "no authenticated exact-head CLEAR")
    if latest is None:
        raise AdmissionDenied("no authenticated exact-head CLEAR")
    _require(latest["methodology_sha"] == methodology, "Challenge methodology changed")
    evidence = {
        "repository": repository,
        "owner": owner,
        "pr": pr,
        "head": head,
        "base": admitted_base if after_merge else target_sha,
        "target_ref": target_ref,
        "reviews": snapshot["reviews"],
        "comments": comments,
        "objective_proof": snapshot["objective_proof"],
    }
    return hashlib.sha256(json.dumps(evidence, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


class GitHub:
    """Use the existing gh authentication without reading/exporting credentials."""

    def api(self, path: str, *, method: str = "GET", payload: dict[str, Any] | None = None) -> Any:
        argv = ["gh", "api", "--hostname", "github.com", "--method", method, path]
        if payload is not None:
            argv += ["--input", "-"]
        result = subprocess.run(
            argv,
            input=json.dumps(payload) if payload is not None else None,
            text=True,
            capture_output=True,
            check=False,
            timeout=60,
        )
        if result.returncode:
            # gh stderr can include provider/request detail; retain it locally,
            # not as a purported safe machine acceptance receipt.
            raise AdmissionDenied("GitHub API failed; effect result may require reconciliation")
        return json.loads(result.stdout)

    def pages(self, path: str) -> list[dict[str, Any]]:
        rows: list[dict[str, Any]] = []
        for page in range(1, 1001):
            batch = self.api(f"{path}?per_page=100&page={page}")
            _require(isinstance(batch, list), "invalid paginated GitHub response")
            rows.extend(batch)
            if len(batch) < 100:
                return rows
        raise AdmissionDenied("GitHub history exceeds bounded read; no truncated acceptance")

    def verify_consumer(self, methodology: str) -> None:
        remote = self.api(f"repos/GrahamArdent/PROGRAMSTART/contents/scripts/programstart_challenge_merge.py?ref={methodology}")
        _require(remote.get("encoding") == "base64", "accepted consumer source unavailable")
        accepted = base64.b64decode(remote["content"], validate=False)
        _require(accepted == Path(__file__).read_bytes(), "consumer differs from accepted methodology source")
        objective_source = self.api(
            f"repos/GrahamArdent/PROGRAMSTART/contents/scripts/programstart_objective_proof.py?ref={methodology}"
        )
        _require(objective_source.get("encoding") == "base64", "accepted objective consumer unavailable")
        _require(
            base64.b64decode(objective_source["content"])
            == Path(__file__).with_name("programstart_objective_proof.py").read_bytes(),
            "objective consumer differs from accepted methodology",
        )

        research_source = self.api(
            f"repos/GrahamArdent/PROGRAMSTART/contents/scripts/programstart_research_admission.py?ref={methodology}"
        )
        _require(research_source.get("encoding") == "base64", "accepted research consumer unavailable")
        _require(
            base64.b64decode(research_source["content"])
            == Path(__file__).with_name("programstart_research_admission.py").read_bytes(),
            "research consumer differs from accepted methodology",
        )

    def snapshot(self, repository: str, pr: int) -> dict[str, Any]:
        try:
            from .programstart_objective_proof import merge_objective_snapshot
        except ImportError:  # pragma: no cover
            from programstart_objective_proof import merge_objective_snapshot
        base = f"repos/{repository}"
        pull = self.api(f"{base}/pulls/{pr}")
        branch = pull["base"].get("ref")
        _require(isinstance(branch, str) and bool(branch), "target branch unavailable")
        target = self.api(f"{base}/git/ref/heads/{quote(branch, safe='')}")
        parents = []
        if pull.get("merged"):
            commit = pull.get("merge_commit_sha")
            _require(isinstance(commit, str) and SHA.fullmatch(commit) is not None, "invalid merged commit identity")
            parents = [parent["sha"] for parent in self.api(f"{base}/git/commits/{commit}")["parents"]]
        return {
            "methodology_sha": self.api("repos/GrahamArdent/PROGRAMSTART/git/ref/heads/main")["object"]["sha"],
            "repository": self.api(base),
            "pull": pull,
            "target_ref": target.get("ref"),
            "target_sha": (target.get("object") or {}).get("sha"),
            "merge_parent_shas": parents,
            "reviews": self.pages(f"{base}/pulls/{pr}/reviews"),
            "comments": self.pages(f"{base}/issues/{pr}/comments"),
            "objective_proof": merge_objective_snapshot(self, repository, target["object"]["sha"], pull["head"]["sha"]),
        }


def guarded_merge(
    read: Callable[[], dict[str, Any]],
    merge: Callable[[str], dict[str, Any]],
    repository: str,
    pr: int,
    head: str,
    methodology: str,
) -> dict[str, Any]:
    """Re-read before PUT and reconcile afterwards; never claim atomic fencing.

    The remote provider has no compare-and-merge operation for a comment/review
    version. A blocker between the last GET and PUT remains a residual race.
    Post-read failure is UNKNOWN/UNACCEPTED, never permission to activate/retry.
    """
    before = admit(read(), repository, pr, head, methodology)
    confirmation = read()
    current = admit(confirmation, repository, pr, head, methodology)
    _require(current == before, "admission evidence changed; reorient before merge")
    try:
        result = merge(head)
    except (AdmissionDenied, OSError, subprocess.SubprocessError, ValueError):
        return {"status": "UNKNOWN", "activation_permitted": False, "retry_merge": False}
    if not isinstance(result, dict) or type(result.get("merged")) is not bool:
        return {"status": "UNKNOWN", "activation_permitted": False, "retry_merge": False}
    if result["merged"] is False:
        return {"status": "MERGE_REFUSED", "activation_permitted": False, "retry_merge": False}
    if not isinstance(result.get("sha"), str) or SHA.fullmatch(result["sha"]) is None:
        return {"status": "UNKNOWN", "activation_permitted": False, "retry_merge": False}
    try:
        observed = read()
        _require(observed["pull"].get("merge_commit_sha") == result.get("sha"), "merge receipt mismatch")
        after = admit(observed, repository, pr, head, methodology, after_merge=True, admitted_base=confirmation["target_sha"])
        _require(after == current, "Challenge evidence changed during merge")
    except (AdmissionDenied, KeyError, TypeError, OSError, subprocess.SubprocessError, ValueError):
        return {
            "status": "MERGED_BUT_UNACCEPTED",
            "merge_sha": result.get("sha"),
            "activation_permitted": False,
            "retry_merge": False,
        }
    # A merged result is historical effect evidence, not release acceptance.
    return {
        "status": "MERGED_REQUIRES_OWNER_RECONCILIATION",
        "merge_sha": result.get("sha"),
        "admission_snapshot_sha256": current,
        "atomic_challenge_fence": False,
        "activation_permitted": False,
        "retry_merge": False,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repository")
    parser.add_argument("pr", type=int)
    parser.add_argument("--expected-head", required=True)
    parser.add_argument("--methodology-sha", required=True)
    parser.add_argument("--merge", action="store_true", help="perform an already-authorized squash merge")
    args = parser.parse_args(argv)
    try:
        _require(REPOSITORY.fullmatch(args.repository) is not None and args.pr > 0, "invalid repository/PR")
        _require(
            SHA.fullmatch(args.expected_head) is not None and SHA.fullmatch(args.methodology_sha) is not None,
            "invalid commit identity",
        )
        github = GitHub()
        github.verify_consumer(args.methodology_sha)

        def read() -> dict[str, Any]:
            return github.snapshot(args.repository, args.pr)

        if args.merge:
            result = guarded_merge(
                read,
                lambda head: github.api(
                    f"repos/{args.repository}/pulls/{args.pr}/merge",
                    method="PUT",
                    payload={"sha": head, "merge_method": "squash"},
                ),
                args.repository,
                args.pr,
                args.expected_head,
                args.methodology_sha,
            )
        else:
            digest = admit(read(), args.repository, args.pr, args.expected_head, args.methodology_sha)
            result = {"status": "ADMISSIBLE_SNAPSHOT_ONLY", "snapshot_sha256": digest, "activation_permitted": False}
        print(json.dumps(result, sort_keys=True))
        return 0 if result["status"] == "ADMISSIBLE_SNAPSHOT_ONLY" else 1
    except (AdmissionDenied, KeyError, TypeError, OSError, subprocess.SubprocessError, ValueError) as exc:
        print(json.dumps({"status": "BLOCKED", "reason": str(exc), "activation_permitted": False}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
