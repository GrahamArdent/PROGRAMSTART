from __future__ import annotations

from pathlib import Path

from scripts.programstart_intent_compile import DependencySpec

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "docs" / "PROGRAMSTART_MATRIX_COORDINATION.md"
WORK_PACKET = ROOT / "PROGRAMBUILD" / "PROGRAMBUILD_WORK_PACKET.md"


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_matrix_coordination_is_mandatory_but_non_authoritative() -> None:
    text = _text(CONTRACT)
    assert "No consequential autonomous mutation may cross the mutation boundary" in text
    assert "does not create any of those truths" in text
    assert "No new Matrix repository, state database, queue, scheduler, or orchestration layer" in text


def test_existing_compiled_write_set_is_the_only_semantic_claim_declaration() -> None:
    text = _text(CONTRACT)
    dependency = DependencySpec()
    assert "dependencies.expected_write_set" in text
    assert "Do not create a parallel Matrix resource-declaration channel" in text
    assert "Controller admission owns leases/fencing" in dependency.serialization_policy


def test_shared_mutation_claims_are_not_blind_ttl_locks() -> None:
    text = _text(CONTRACT)
    assert "time passage alone is not permission" in text
    assert "blind TTL expiry is not sufficient proof" in text
    assert "multi-resource acquisition is atomic as a bundle" in text
    assert "monotonic fencing identity" in text


def test_fail_closed_and_recovery_do_not_create_bypass() -> None:
    text = _text(CONTRACT)
    assert "consequential autonomous mutation is blocked" in text
    assert "ordinary autonomous work may not bypass" in text
    assert "Recovery restores the same coordination authority" in text


def test_matrix_projection_remains_read_only_derived_state() -> None:
    text = _text(CONTRACT)
    assert "The projection is not the mutation claim itself" in text
    assert "Neither becomes the live claim store" in text
    assert "Composition does not collapse ownership" in text


def test_work_packet_methodology_already_requires_single_shared_mutation_owner() -> None:
    text = _text(WORK_PACKET)
    assert "SHARED_MUTATION_RESOURCE:" in text
    assert "MUTATION_OWNER:" in text
    assert "RELEASE_OR_TRANSFER_CONDITION:" in text
    assert "at most one lane may own mutation of that resource at a time" in text
