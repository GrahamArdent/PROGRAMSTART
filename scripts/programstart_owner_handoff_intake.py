#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from collections.abc import Mapping
from pathlib import Path
from typing import Any

TARGET_REPOSITORY = "GrahamArdent/PROGRAMSTART"
PACKET_SCHEMA = "programstart.compiled-work-packet.v0.1"
COMPILER_VERSION = "programstart-intent-compiler.v0.1"
ALLOWED_DISPOSITIONS = {
    "accepted",
    "already_covered",
    "reconciled",
    "rejected",
    "superseded",
    "needs_gate",
}
SHA_RE = re.compile(r"^[0-9a-f]{40}$")
DIGEST_RE = re.compile(r"^[0-9a-f]{64}$")
PACKET_ID_RE = re.compile(r"^WPK-[0-9a-f]{16}$")
HANDOFF_ID_RE = re.compile(r"^handoff-[0-9a-f]{24}$")
REPOSITORY_RE = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
MAX_INPUT_BYTES = 32 * 1024


class IntakeError(RuntimeError):
    pass


def _canonical(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _bounded_text(value: Any, field: str, *, maximum: int = 512) -> str:
    if not isinstance(value, str) or not value.strip() or len(value) > maximum or "\x00" in value:
        raise IntakeError(f"{field} must be bounded non-empty text")
    return value.strip()


def _repo(value: Any, field: str) -> str:
    value = _bounded_text(value, field, maximum=200)
    if REPOSITORY_RE.fullmatch(value) is None:
        raise IntakeError(f"{field} must be an exact owner/repository identity")
    return value


def _safe_authority_path(repo_root: Path, raw: Any) -> str:
    text = _bounded_text(raw, "authority path", maximum=240)
    path = Path(text)
    if path.is_absolute() or not path.parts or any(part in {"", ".", ".."} for part in path.parts):
        raise IntakeError("authority path is not a safe repository-relative path")
    target = repo_root.joinpath(*path.parts)
    root = repo_root.resolve(strict=True)
    try:
        resolved = target.resolve(strict=True)
    except OSError as exc:
        raise IntakeError(f"authority path is missing: {text}") from exc
    if root != resolved and root not in resolved.parents:
        raise IntakeError("authority path escapes the target repository")
    if not resolved.is_file() or resolved.is_symlink():
        raise IntakeError(f"authority path is not a regular file: {text}")
    return text


def _packet_integrity(packet: Any) -> tuple[str, str, str, str]:
    if not isinstance(packet, dict):
        raise IntakeError("handoff packet must be an object")
    if packet.get("schema_version") != PACKET_SCHEMA:
        raise IntakeError("handoff packet schema is not admitted")
    if packet.get("compiler_version") != COMPILER_VERSION:
        raise IntakeError("handoff packet compiler version is not admitted")
    specification_id = packet.get("specification_id")
    semantic_digest = packet.get("semantic_digest")
    if not isinstance(specification_id, str) or PACKET_ID_RE.fullmatch(specification_id) is None:
        raise IntakeError("handoff packet specification_id is invalid")
    if not isinstance(semantic_digest, str) or DIGEST_RE.fullmatch(semantic_digest) is None:
        raise IntakeError("handoff packet semantic_digest is invalid")
    target_repository = _repo(packet.get("owning_repository"), "packet owning_repository")
    authority = packet.get("authority")
    if not isinstance(authority, dict) or authority.get("owning_repository") != target_repository:
        raise IntakeError("handoff packet authority owner does not match target repository")

    body = dict(packet)
    body.pop("specification_id", None)
    body.pop("semantic_digest", None)
    observed = hashlib.sha256(_canonical(body).encode("utf-8")).hexdigest()
    if semantic_digest != observed or specification_id != f"WPK-{observed[:16]}":
        raise IntakeError("handoff packet semantic integrity verification failed")
    packet_json = _canonical(packet)
    packet_sha256 = hashlib.sha256(packet_json.encode("utf-8")).hexdigest()
    return specification_id, semantic_digest, target_repository, packet_sha256


def _handoff_identity(handoff: Mapping[str, Any]) -> str:
    identity = {
        "source_repository": handoff["source_repository"],
        "source_context_ref": handoff["source_context_ref"],
        "target_repository": handoff["target_repository"],
        "specification_id": handoff["specification_id"],
        "semantic_digest": handoff["semantic_digest"],
    }
    digest = hashlib.sha256(_canonical(identity).encode("utf-8")).hexdigest()
    return f"handoff-{digest[:24]}"


def _git_head(repo_root: Path) -> str:
    proc = subprocess.run(
        ["/usr/bin/git", "-C", str(repo_root), "rev-parse", "HEAD"],
        stdin=subprocess.DEVNULL,
        capture_output=True,
        text=True,
        timeout=10,
        check=False,
        env={"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8"},
    )
    head = proc.stdout.strip()
    if proc.returncode != 0 or SHA_RE.fullmatch(head) is None:
        raise IntakeError("target repository HEAD is unavailable")
    return head


def evaluate(payload: Any, *, repo_root: Path, observed_head: str | None = None) -> dict[str, Any]:
    required_payload_fields = {"schema_version", "target_repository", "target_sha", "handoff"}
    if not isinstance(payload, dict) or set(payload) != required_payload_fields:
        raise IntakeError("intake payload fields do not match the fixed contract")
    if payload.get("schema_version") != 1:
        raise IntakeError("unsupported intake schema_version")
    if payload.get("target_repository") != TARGET_REPOSITORY:
        raise IntakeError("intake target repository is not PROGRAMSTART")
    target_sha = payload.get("target_sha")
    if not isinstance(target_sha, str) or SHA_RE.fullmatch(target_sha) is None:
        raise IntakeError("target_sha must be an exact lowercase 40-character Git SHA")
    head = observed_head or _git_head(repo_root)
    if head != target_sha:
        raise IntakeError("target repository HEAD is stale relative to admitted target_sha")

    handoff = payload.get("handoff")
    required = {
        "handoff_id",
        "source_repository",
        "source_context_ref",
        "target_repository",
        "specification_id",
        "semantic_digest",
        "packet_sha256",
        "packet",
    }
    if not isinstance(handoff, dict) or set(handoff) != required:
        raise IntakeError("handoff fields do not match the fixed contract")
    if not isinstance(handoff.get("handoff_id"), str) or HANDOFF_ID_RE.fullmatch(handoff["handoff_id"]) is None:
        raise IntakeError("handoff_id is invalid")
    source_repository = _repo(handoff.get("source_repository"), "source_repository")
    if source_repository == TARGET_REPOSITORY:
        raise IntakeError("owner handoff source and target must differ")
    _bounded_text(handoff.get("source_context_ref"), "source_context_ref")
    if handoff.get("target_repository") != TARGET_REPOSITORY:
        raise IntakeError("handoff target repository changed")

    specification_id, semantic_digest, packet_owner, packet_sha256 = _packet_integrity(handoff.get("packet"))
    if packet_owner != TARGET_REPOSITORY:
        raise IntakeError("packet owner does not match intake target")
    if handoff.get("specification_id") != specification_id:
        raise IntakeError("handoff specification_id does not match packet")
    if handoff.get("semantic_digest") != semantic_digest:
        raise IntakeError("handoff semantic_digest does not match packet")
    if handoff.get("packet_sha256") != packet_sha256:
        raise IntakeError("handoff packet_sha256 does not match packet")
    if _handoff_identity(handoff) != handoff["handoff_id"]:
        raise IntakeError("handoff identity verification failed")

    packet = handoff["packet"]
    authority = packet.get("authority")
    if not isinstance(authority, dict):
        raise IntakeError("packet authority snapshot is missing")
    if authority.get("owning_repository") != TARGET_REPOSITORY:
        raise IntakeError("packet authority owner is ambiguous")
    if authority.get("authority_commit") != target_sha:
        raise IntakeError("packet authority commit is stale relative to current target HEAD")
    paths = authority.get("authority_paths")
    if not isinstance(paths, list) or not paths or len(paths) > 16:
        raise IntakeError("packet authority_paths must be a bounded non-empty list")
    verified_paths = [_safe_authority_path(repo_root, item) for item in paths]
    if len(set(verified_paths)) != len(verified_paths):
        raise IntakeError("packet authority_paths contain duplicates")

    disposition = "needs_gate"
    if disposition not in ALLOWED_DISPOSITIONS:
        raise IntakeError("internal disposition is outside the AC-09 bounded set")
    replay_material = {
        "handoff_id": handoff["handoff_id"],
        "target_repository": TARGET_REPOSITORY,
        "target_sha": target_sha,
        "packet_sha256": packet_sha256,
        "disposition": disposition,
    }
    replay_key = hashlib.sha256(_canonical(replay_material).encode("utf-8")).hexdigest()
    disposition_reason = (
        "current PROGRAMSTART authority was re-read; semantic consequence remains gated because this fixed intake helper "
        "does not manufacture target-owner admission"
    )
    return {
        "schema_version": 1,
        "target_repository": TARGET_REPOSITORY,
        "target_sha": target_sha,
        "handoff_id": handoff["handoff_id"],
        "specification_id": specification_id,
        "semantic_digest": semantic_digest,
        "packet_sha256": packet_sha256,
        "authority_paths_verified": verified_paths,
        "disposition": disposition,
        "disposition_reason": disposition_reason,
        "replay_key": replay_key,
        "delivery_is_acceptance": False,
        "mutation_performed": False,
        "secret_values_exported": False,
        "identity_material_exported": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="PROGRAMSTART fixed owner-handoff current-authority intake")
    parser.add_argument("--repo-root", default=".")
    args = parser.parse_args()
    raw = sys.stdin.buffer.read(MAX_INPUT_BYTES + 1)
    if len(raw) > MAX_INPUT_BYTES:
        print(json.dumps({"status": "FAILED", "error": "intake payload exceeds maximum size"}, sort_keys=True))
        return 1
    try:
        payload = json.loads(raw.decode("utf-8"))
        result = evaluate(payload, repo_root=Path(args.repo_root).resolve(strict=True))
    except (UnicodeDecodeError, json.JSONDecodeError, IntakeError, OSError, subprocess.SubprocessError) as exc:
        print(json.dumps({"status": "FAILED", "error": str(exc)[:1000]}, sort_keys=True))
        return 1
    print(json.dumps({"status": "SUCCEEDED", "evidence": result}, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
