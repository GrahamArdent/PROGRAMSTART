from __future__ import annotations

import hashlib
import io
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import pytest

from scripts import programstart_owner_handoff_intake as mod

TARGET_SHA = "a" * 40


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def make_packet():
    packet = {
        "schema_version": mod.PACKET_SCHEMA,
        "compiler_version": mod.COMPILER_VERSION,
        "owning_repository": mod.TARGET_REPOSITORY,
        "authority": {
            "owning_repository": mod.TARGET_REPOSITORY,
            "authority_commit": TARGET_SHA,
            "authority_paths": ["AUTHORITY.md"],
        },
        "objective": {"text": "Route a reusable observation to the methodology owner."},
    }
    body = dict(packet)
    semantic = hashlib.sha256(canonical(body).encode()).hexdigest()
    packet["specification_id"] = f"WPK-{semantic[:16]}"
    packet["semantic_digest"] = semantic
    return packet


def make_payload():
    packet = make_packet()
    packet_sha = hashlib.sha256(canonical(packet).encode()).hexdigest()
    identity = {
        "source_repository": "GrahamArdent/programstart-autonomous-controller",
        "source_context_ref": "issue:53:ac09",
        "target_repository": mod.TARGET_REPOSITORY,
        "specification_id": packet["specification_id"],
        "semantic_digest": packet["semantic_digest"],
    }
    handoff_id = "handoff-" + hashlib.sha256(canonical(identity).encode()).hexdigest()[:24]
    return {
        "schema_version": 1,
        "target_repository": mod.TARGET_REPOSITORY,
        "target_sha": TARGET_SHA,
        "handoff": {
            "handoff_id": handoff_id,
            **identity,
            "packet_sha256": packet_sha,
            "packet": packet,
        },
    }


def refresh_handoff_binding(payload):
    packet = payload["handoff"]["packet"]
    body = dict(packet)
    body.pop("specification_id", None)
    body.pop("semantic_digest", None)
    semantic = hashlib.sha256(canonical(body).encode()).hexdigest()
    packet["specification_id"] = f"WPK-{semantic[:16]}"
    packet["semantic_digest"] = semantic
    payload["handoff"]["specification_id"] = packet["specification_id"]
    payload["handoff"]["semantic_digest"] = semantic
    payload["handoff"]["packet_sha256"] = hashlib.sha256(canonical(packet).encode()).hexdigest()
    identity_fields = (
        "source_repository",
        "source_context_ref",
        "target_repository",
        "specification_id",
        "semantic_digest",
    )
    identity = {key: payload["handoff"][key] for key in identity_fields}
    payload["handoff"]["handoff_id"] = "handoff-" + hashlib.sha256(canonical(identity).encode()).hexdigest()[:24]


class IntakeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "AUTHORITY.md").write_text("current authority\n", encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def test_current_exact_handoff_returns_needs_gate_without_mutation(self):
        result = mod.evaluate(make_payload(), repo_root=self.root, observed_head=TARGET_SHA)
        self.assertEqual(result["disposition"], "needs_gate")
        self.assertFalse(result["delivery_is_acceptance"])
        self.assertFalse(result["mutation_performed"])
        self.assertEqual(result["authority_paths_verified"], ["AUTHORITY.md"])

    def test_replay_is_stable(self):
        payload = make_payload()
        first = mod.evaluate(payload, repo_root=self.root, observed_head=TARGET_SHA)
        second = mod.evaluate(payload, repo_root=self.root, observed_head=TARGET_SHA)
        self.assertEqual(first["replay_key"], second["replay_key"])
        self.assertEqual(first, second)

    def test_stale_target_head_fails_closed(self):
        with self.assertRaisesRegex(mod.IntakeError, "HEAD is stale"):
            mod.evaluate(make_payload(), repo_root=self.root, observed_head="b" * 40)

    def test_stale_packet_authority_fails_closed(self):
        payload = make_payload()
        payload["handoff"]["packet"]["authority"]["authority_commit"] = "b" * 40
        refresh_handoff_binding(payload)
        with self.assertRaisesRegex(mod.IntakeError, "authority commit is stale"):
            mod.evaluate(payload, repo_root=self.root, observed_head=TARGET_SHA)

    def test_tampered_packet_digest_fails_closed(self):
        payload = make_payload()
        payload["handoff"]["packet"]["objective"]["text"] = "tampered"
        with self.assertRaisesRegex(mod.IntakeError, "semantic integrity"):
            mod.evaluate(payload, repo_root=self.root, observed_head=TARGET_SHA)

    def test_missing_or_unsafe_authority_path_fails_closed(self):
        payload = make_payload()
        payload["handoff"]["packet"]["authority"]["authority_paths"] = ["../outside"]
        refresh_handoff_binding(payload)
        with self.assertRaisesRegex(mod.IntakeError, "safe repository-relative"):
            mod.evaluate(payload, repo_root=self.root, observed_head=TARGET_SHA)


if __name__ == "__main__":
    unittest.main()


def set_field(payload: dict, path: str, value: object) -> None:
    target = payload
    parts = path.split(".")
    for part in parts[:-1]:
        target = target[part]
    target[parts[-1]] = value


@pytest.fixture
def authority_root(tmp_path: Path) -> Path:
    (tmp_path / "AUTHORITY.md").write_text("current authority\n")
    return tmp_path


@pytest.mark.parametrize("payload", [None, [], {}, {"unexpected": True}])
def test_wrong_envelope_shapes_are_rejected(authority_root, payload):
    with pytest.raises(mod.IntakeError, match="payload fields"):
        mod.evaluate(payload, repo_root=authority_root, observed_head=TARGET_SHA)


@pytest.mark.parametrize(
    "field,value,reason",
    [
        ("schema_version", 2, "unsupported intake schema_version"),
        ("schema_version", True, "unsupported intake schema_version"),
        ("schema_version", False, "unsupported intake schema_version"),
        ("target_repository", "foreign/repository", "not PROGRAMSTART"),
        ("target_sha", None, "exact lowercase 40-character"),
        ("target_sha", "B" * 40, "exact lowercase 40-character"),
        ("handoff", None, "handoff fields"),
        ("handoff", {}, "handoff fields"),
        ("handoff.handoff_id", None, "handoff_id is invalid"),
        ("handoff.handoff_id", "handoff-wrong", "handoff_id is invalid"),
        ("handoff.source_repository", mod.TARGET_REPOSITORY, "source and target must differ"),
        ("handoff.source_repository", "not-a-repository", "exact owner/repository identity"),
        ("handoff.source_context_ref", " ", "bounded non-empty text"),
        ("handoff.source_context_ref", "x" * 513, "bounded non-empty text"),
        ("handoff.source_context_ref", "bad\x00text", "bounded non-empty text"),
        ("handoff.target_repository", "foreign/target", "handoff target repository changed"),
        ("handoff.packet", None, "packet must be an object"),
        ("handoff.packet.schema_version", "wrong", "packet schema is not admitted"),
        ("handoff.packet.compiler_version", "wrong", "compiler version is not admitted"),
        ("handoff.packet.specification_id", None, "specification_id is invalid"),
        ("handoff.packet.specification_id", "wrong", "specification_id is invalid"),
        ("handoff.packet.semantic_digest", None, "semantic_digest is invalid"),
        ("handoff.packet.semantic_digest", "wrong", "semantic_digest is invalid"),
        ("handoff.packet.owning_repository", "wrong", "exact owner/repository identity"),
        ("handoff.packet.authority", None, "authority owner does not match"),
        ("handoff.packet.authority.owning_repository", "foreign/owner", "authority owner does not match"),
        ("handoff.specification_id", "WPK-" + "0" * 16, "handoff specification_id does not match"),
        ("handoff.semantic_digest", "0" * 64, "handoff semantic_digest does not match"),
        ("handoff.packet_sha256", "0" * 64, "packet_sha256 does not match"),
        ("handoff.handoff_id", "handoff-" + "0" * 24, "handoff identity verification failed"),
    ],
)
def test_malformed_or_mismatched_identity_fails_at_its_boundary(authority_root, field, value, reason):
    payload = make_payload()
    set_field(payload, field, value)
    before = (authority_root / "AUTHORITY.md").read_bytes()
    with pytest.raises(mod.IntakeError, match=reason):
        mod.evaluate(payload, repo_root=authority_root, observed_head=TARGET_SHA)
    assert (authority_root / "AUTHORITY.md").read_bytes() == before
    assert sorted(p.name for p in authority_root.iterdir()) == ["AUTHORITY.md"]


def test_self_consistent_foreign_packet_cannot_be_retargeted(authority_root):
    payload = make_payload()
    payload["handoff"]["packet"]["owning_repository"] = "foreign/owner"
    payload["handoff"]["packet"]["authority"]["owning_repository"] = "foreign/owner"
    refresh_handoff_binding(payload)
    with pytest.raises(mod.IntakeError, match="packet owner does not match intake target"):
        mod.evaluate(payload, repo_root=authority_root, observed_head=TARGET_SHA)


def test_integrity_valid_packet_cannot_select_an_accepted_disposition(authority_root):
    payload = make_payload()
    payload["handoff"]["packet"]["disposition"] = "accepted"
    refresh_handoff_binding(payload)
    result = mod.evaluate(payload, repo_root=authority_root, observed_head=TARGET_SHA)
    assert result["disposition"] == "needs_gate"
    assert result["delivery_is_acceptance"] is False and result["mutation_performed"] is False


@pytest.mark.parametrize(
    "paths,reason",
    [
        (None, "bounded non-empty list"),
        ([], "bounded non-empty list"),
        (["AUTHORITY.md"] * 17, "bounded non-empty list"),
        (["AUTHORITY.md"] * 2, "contain duplicates"),
        ([""], "bounded non-empty text"),
        ([None], "bounded non-empty text"),
        (["/absolute"], "safe repository-relative"),
        (["../escape"], "safe repository-relative"),
        (["."], "safe repository-relative"),
        (["missing.md"], "authority path is missing"),
        (["folder"], "not a regular file"),
    ],
)
def test_authority_paths_are_bounded_existing_regular_files(authority_root, paths, reason):
    (authority_root / "folder").mkdir()
    payload = make_payload()
    payload["handoff"]["packet"]["authority"]["authority_paths"] = paths
    refresh_handoff_binding(payload)
    with pytest.raises(mod.IntakeError, match=reason):
        mod.evaluate(payload, repo_root=authority_root, observed_head=TARGET_SHA)


def test_parent_link_cannot_escape_authority_root(authority_root, tmp_path):
    outside = tmp_path.parent / (tmp_path.name + "-outside")
    outside.mkdir()
    (outside / "secret.md").write_text("external authority is not admitted")
    (authority_root / "linked").symlink_to(outside, target_is_directory=True)
    payload = make_payload()
    payload["handoff"]["packet"]["authority"]["authority_paths"] = ["linked/secret.md"]
    refresh_handoff_binding(payload)
    with pytest.raises(mod.IntakeError, match="escapes the target repository"):
        mod.evaluate(payload, repo_root=authority_root, observed_head=TARGET_SHA)


def test_final_symlink_is_not_a_regular_authority_reference(authority_root):
    (authority_root / "alias.md").symlink_to(authority_root / "AUTHORITY.md")
    payload = make_payload()
    payload["handoff"]["packet"]["authority"]["authority_paths"] = ["alias.md"]
    refresh_handoff_binding(payload)
    with pytest.raises(mod.IntakeError, match="not a regular file"):
        mod.evaluate(payload, repo_root=authority_root, observed_head=TARGET_SHA)


def real_repository(root: Path, *, sha256: bool = False) -> str:
    commands = [
        ["init", "-q", "--object-format=sha256"] if sha256 else ["init", "-q"],
        ["add", "AUTHORITY.md"],
        ["-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "commit", "-qm", "authority"],
    ]
    for args in commands:
        subprocess.run(["git", "-C", str(root), *args], check=True, capture_output=True)
    return subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip()


def current_payload(head: str) -> dict:
    payload = make_payload()
    payload["target_sha"] = head
    payload["handoff"]["packet"]["authority"]["authority_commit"] = head
    refresh_handoff_binding(payload)
    return payload


def test_real_git_head_replay_is_observe_only(authority_root):
    head = real_repository(authority_root)
    payload = current_payload(head)
    before = subprocess.check_output(["git", "-C", str(authority_root), "status", "--porcelain"])
    result = mod.evaluate(payload, repo_root=authority_root)
    assert result["target_sha"] == head
    assert result["disposition"] == "needs_gate"
    assert result["delivery_is_acceptance"] is False and result["mutation_performed"] is False
    assert mod.evaluate(payload, repo_root=authority_root) == result
    assert subprocess.check_output(["git", "-C", str(authority_root), "status", "--porcelain"]) == before


def test_real_non_repository_and_non_admitted_hash_format_fail_closed(authority_root):
    with pytest.raises(mod.IntakeError, match="HEAD is unavailable"):
        mod.evaluate(make_payload(), repo_root=authority_root)
    head = real_repository(authority_root, sha256=True)
    assert len(head) == 64
    with pytest.raises(mod.IntakeError, match="HEAD is unavailable"):
        mod._git_head(authority_root)


@pytest.mark.parametrize(
    "raw,reason",
    [
        (b"x" * (mod.MAX_INPUT_BYTES + 1), "exceeds maximum size"),
        (b"\xff", "codec"),
        (b"{", "Expecting property name"),
        (b"null", "payload fields"),
        (b"[]", "payload fields"),
    ],
)
def test_cli_rejects_invalid_bytes_as_bounded_json(authority_root, monkeypatch, capsys, raw, reason):
    monkeypatch.setattr(sys, "argv", ["intake", "--repo-root", str(authority_root)])
    monkeypatch.setattr(sys, "stdin", io.TextIOWrapper(io.BytesIO(raw)))
    assert mod.main() == 1
    output = json.loads(capsys.readouterr().out)
    assert output["status"] == "FAILED" and reason in output["error"]
    assert len(output["error"]) <= 1000


def test_cli_real_git_success_and_missing_target_are_json(authority_root, monkeypatch, capsys):
    head = real_repository(authority_root)
    raw = json.dumps(current_payload(head)).encode()
    monkeypatch.setattr(sys, "argv", ["intake", "--repo-root", str(authority_root)])
    monkeypatch.setattr(sys, "stdin", io.TextIOWrapper(io.BytesIO(raw)))
    assert mod.main() == 0
    output = json.loads(capsys.readouterr().out)
    assert output["status"] == "SUCCEEDED"
    assert output["evidence"]["disposition"] == "needs_gate"
    monkeypatch.setattr(sys, "argv", ["intake", "--repo-root", str(authority_root / "absent")])
    monkeypatch.setattr(sys, "stdin", io.TextIOWrapper(io.BytesIO(raw)))
    assert mod.main() == 1
    assert json.loads(capsys.readouterr().out)["status"] == "FAILED"


@pytest.mark.parametrize("valid", [True, False])
def test_actual_cli_process_returns_bounded_json_without_mutation(authority_root, tmp_path, valid):
    # Trace the actual child process when the parent suite is collecting coverage.
    # Merge only its real coverage.py data; no synthetic hits or exclusions.
    from coverage import Coverage

    head = real_repository(authority_root)
    active = Coverage.current()
    command = [sys.executable]
    data_file = tmp_path.parent / (tmp_path.name + ".coverage")
    if active is not None:
        command += [
            "-m",
            "coverage",
            "run",
            "--branch",
            "--source=scripts.programstart_owner_handoff_intake",
            "--data-file",
            str(data_file),
        ]
    command += ["-m", "scripts.programstart_owner_handoff_intake", "--repo-root", str(authority_root)]
    raw = json.dumps(current_payload(head)) if valid else "{"
    result = subprocess.run(command, input=raw, capture_output=True, text=True, check=False)
    assert result.returncode == (0 if valid else 1), result.stderr
    assert not result.stderr
    output = json.loads(result.stdout)
    if valid:
        evidence = output["evidence"]
        assert evidence["target_sha"] == head and evidence["disposition"] == "needs_gate"
        assert evidence["mutation_performed"] is False and evidence["delivery_is_acceptance"] is False
    else:
        assert output["status"] == "FAILED" and len(output["error"]) <= 1000
    assert subprocess.check_output(["git", "-C", str(authority_root), "status", "--porcelain"]) == b""
    if active is not None:
        child = Coverage(data_file=str(data_file))
        child.load()
        active.get_data().update(child.get_data())


@pytest.mark.parametrize("loop_root", [False, True])
def test_cli_symlink_loop_returns_bounded_failure(authority_root, monkeypatch, capsys, loop_root):
    head = real_repository(authority_root)
    (authority_root / "loop").symlink_to("loop", target_is_directory=True)
    payload = current_payload(head)
    if not loop_root:
        payload["handoff"]["packet"]["authority"]["authority_paths"] = ["loop/file.md"]
        refresh_handoff_binding(payload)
    root = authority_root / "loop" if loop_root else authority_root
    monkeypatch.setattr(sys, "argv", ["intake", "--repo-root", str(root)])
    monkeypatch.setattr(sys, "stdin", io.TextIOWrapper(io.BytesIO(json.dumps(payload).encode())))
    assert mod.main() == 1
    output = json.loads(capsys.readouterr().out)
    assert output["status"] == "FAILED" and len(output["error"]) <= 1000


def test_cli_exact_byte_limit_and_real_owner_head_drift(authority_root, monkeypatch, capsys):
    head = real_repository(authority_root)
    payload = current_payload(head)
    raw = json.dumps(payload).encode()
    raw += b" " * (mod.MAX_INPUT_BYTES - len(raw))
    assert len(raw) == mod.MAX_INPUT_BYTES
    monkeypatch.setattr(sys, "argv", ["intake", "--repo-root", str(authority_root)])
    monkeypatch.setattr(sys, "stdin", io.TextIOWrapper(io.BytesIO(raw)))
    assert mod.main() == 0
    assert json.loads(capsys.readouterr().out)["evidence"]["disposition"] == "needs_gate"
    subprocess.run(
        [
            "git",
            "-C",
            str(authority_root),
            "-c",
            "user.name=Fixture",
            "-c",
            "user.email=fixture@example.invalid",
            "commit",
            "--allow-empty",
            "-qm",
            "advanced",
        ],
        check=True,
    )
    monkeypatch.setattr(sys, "stdin", io.TextIOWrapper(io.BytesIO(raw)))
    assert mod.main() == 1
    output = json.loads(capsys.readouterr().out)
    assert output["status"] == "FAILED" and "HEAD is stale" in output["error"]
