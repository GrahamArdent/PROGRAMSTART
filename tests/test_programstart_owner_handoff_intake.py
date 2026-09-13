from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

MODULE_PATH = Path(__file__).parents[1] / "scripts" / "programstart_owner_handoff_intake.py"
SPEC = importlib.util.spec_from_file_location("owner_intake", MODULE_PATH)
mod = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(mod)

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
        packet = payload["handoff"]["packet"]
        packet["authority"]["authority_commit"] = "b" * 40
        body = dict(packet)
        body.pop("specification_id")
        body.pop("semantic_digest")
        semantic = hashlib.sha256(canonical(body).encode()).hexdigest()
        packet["specification_id"] = f"WPK-{semantic[:16]}"
        packet["semantic_digest"] = semantic
        payload["handoff"]["specification_id"] = packet["specification_id"]
        payload["handoff"]["semantic_digest"] = semantic
        payload["handoff"]["packet_sha256"] = hashlib.sha256(canonical(packet).encode()).hexdigest()
        identity = {k: payload["handoff"][k] for k in ("source_repository", "source_context_ref", "target_repository", "specification_id", "semantic_digest")}
        payload["handoff"]["handoff_id"] = "handoff-" + hashlib.sha256(canonical(identity).encode()).hexdigest()[:24]
        with self.assertRaisesRegex(mod.IntakeError, "authority commit is stale"):
            mod.evaluate(payload, repo_root=self.root, observed_head=TARGET_SHA)

    def test_tampered_packet_digest_fails_closed(self):
        payload = make_payload()
        payload["handoff"]["packet"]["objective"]["text"] = "tampered"
        with self.assertRaisesRegex(mod.IntakeError, "semantic integrity"):
            mod.evaluate(payload, repo_root=self.root, observed_head=TARGET_SHA)

    def test_missing_or_unsafe_authority_path_fails_closed(self):
        payload = make_payload()
        packet = payload["handoff"]["packet"]
        packet["authority"]["authority_paths"] = ["../outside"]
        body = dict(packet)
        body.pop("specification_id")
        body.pop("semantic_digest")
        semantic = hashlib.sha256(canonical(body).encode()).hexdigest()
        packet["specification_id"] = f"WPK-{semantic[:16]}"
        packet["semantic_digest"] = semantic
        payload["handoff"]["specification_id"] = packet["specification_id"]
        payload["handoff"]["semantic_digest"] = semantic
        payload["handoff"]["packet_sha256"] = hashlib.sha256(canonical(packet).encode()).hexdigest()
        identity = {k: payload["handoff"][k] for k in ("source_repository", "source_context_ref", "target_repository", "specification_id", "semantic_digest")}
        payload["handoff"]["handoff_id"] = "handoff-" + hashlib.sha256(canonical(identity).encode()).hexdigest()[:24]
        with self.assertRaisesRegex(mod.IntakeError, "safe repository-relative"):
            mod.evaluate(payload, repo_root=self.root, observed_head=TARGET_SHA)


if __name__ == "__main__":
    unittest.main()
