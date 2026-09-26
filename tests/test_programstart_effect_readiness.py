from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.programstart_intent_compile import (  # noqa: E402
    AuthoritySnapshot,
    IntentKind,
    authority_fingerprint,
    compile_work_packet,
)
from scripts.programstart_objective_continuation import (  # noqa: E402
    CompletedEffectEvidence,
    ContinuationDisposition,
    RootObjective,
    derive_effect_readiness,
    evaluate_objective_continuation,
)

PREPARE = "prepare accepted change"
APPLY = "apply accepted change"
VERIFY = "verify accepted outcome"


def _authority(**changes: object) -> AuthoritySnapshot:
    values: dict[str, object] = {
        "project_name": "Owner",
        "owning_repository": "example/owner",
        "authority_commit": "a" * 40,
        "authority_paths": ["OWNER_AUTHORITY.md"],
        "methodology_commit": "b" * 40,
        "execution_mode": "bounded",
        "allowed_effects": [PREPARE, APPLY, VERIFY],
        "prohibited_effects": ["publish release"],
        "effect_readiness_rules": [
            {"completed_effect": PREPARE, "ready_effect": APPLY},
        ],
    }
    values.update(changes)
    return AuthoritySnapshot.model_validate(values)


def _context(authority: AuthoritySnapshot):
    packet = compile_work_packet(
        "Continue the root objective.",
        authority,
        kind=IntentKind.CONTINUATION,
        interpreted_objective="Deliver the accepted root outcome.",
    )
    root = RootObjective(root_id="root-162", objective="Deliver the accepted root outcome.")
    binding = {
        "root_id": root.root_id,
        "work_packet_specification_id": packet.specification_id,
        "authority_fingerprint": authority_fingerprint(authority),
    }
    return root, packet, binding


def _completed(token: str, binding: dict[str, str], *, evidence_id: str = "completed") -> CompletedEffectEvidence:
    return CompletedEffectEvidence(
        evidence_id=evidence_id,
        status="accepted",
        semantic_effect_token=token,
        root_id=binding["root_id"],
        work_packet_specification_id=binding["work_packet_specification_id"],
        authority_fingerprint=binding["authority_fingerprint"],
    )


@pytest.mark.parametrize(
    "allowed",
    [
        [PREPARE, APPLY, VERIFY],
        [VERIFY, PREPARE, APPLY],
        [APPLY, VERIFY, PREPARE],
    ],
)
def test_owner_readiness_is_independent_of_allowed_effect_order(allowed: list[str]) -> None:
    authority = _authority(allowed_effects=allowed)
    root, packet, binding = _context(authority)

    receipt = derive_effect_readiness(root, packet, authority, [_completed(PREPARE, binding)])

    assert receipt is not None
    assert receipt.semantic_effect_token == APPLY


def test_missing_and_ambiguous_owner_semantics_fail_closed() -> None:
    no_rules = _authority(effect_readiness_rules=[])
    root, packet, binding = _context(no_rules)
    completed = _completed(PREPARE, binding)
    assert derive_effect_readiness(root, packet, no_rules, [completed]) is None

    ambiguous = _authority(
        effect_readiness_rules=[
            {"completed_effect": PREPARE, "ready_effect": APPLY},
            {"completed_effect": PREPARE, "ready_effect": VERIFY},
        ]
    )
    root, packet, binding = _context(ambiguous)
    assert derive_effect_readiness(root, packet, ambiguous, [_completed(PREPARE, binding)]) is None


def test_stale_authority_packet_and_completion_bindings_fail_closed() -> None:
    authority = _authority()
    root, packet, binding = _context(authority)
    completed = _completed(PREPARE, binding)

    changed = authority.model_copy(update={"authority_commit": "c" * 40})
    assert derive_effect_readiness(root, packet, changed, [completed]) is None
    stale = completed.model_copy(update={"authority_fingerprint": "0" * 64})
    assert derive_effect_readiness(root, packet, authority, [stale]) is None
    corrupt = packet.model_copy(update={"semantic_digest": "0" * 64})
    assert derive_effect_readiness(root, corrupt, authority, [completed]) is None


def test_replayed_completion_and_already_completed_target_fail_closed() -> None:
    authority = _authority()
    root, packet, binding = _context(authority)
    completed = _completed(PREPARE, binding)
    replay = completed.model_copy(update={"evidence_id": "completed-replay"})

    assert derive_effect_readiness(root, packet, authority, [completed, replay]) is None
    assert (
        derive_effect_readiness(
            root,
            packet,
            authority,
            [completed, _completed(APPLY, binding, evidence_id="completed-apply")],
        )
        is None
    )


@pytest.mark.parametrize(
    ("ready_effect", "allowed_effects", "prohibited_effects"),
    [
        ("invented effect", [PREPARE, APPLY, VERIFY], []),
        (APPLY, [PREPARE, APPLY, VERIFY], [APPLY]),
        ("git push origin main", [PREPARE, "git push origin main"], []),
    ],
)
def test_out_of_scope_prohibited_and_executor_material_fail_closed(
    ready_effect: str,
    allowed_effects: list[str],
    prohibited_effects: list[str],
) -> None:
    authority = _authority(
        allowed_effects=allowed_effects,
        prohibited_effects=prohibited_effects,
        effect_readiness_rules=[
            {"completed_effect": PREPARE, "ready_effect": ready_effect},
        ],
    )
    root, packet, binding = _context(authority)
    assert derive_effect_readiness(root, packet, authority, [_completed(PREPARE, binding)]) is None


def test_prepare_readiness_receipt_contains_no_executor_material_and_feeds_existing_oracle() -> None:
    authority = _authority()
    root, packet, binding = _context(authority)
    completed = _completed(PREPARE, binding)

    receipt = derive_effect_readiness(root, packet, authority, [completed])

    assert receipt is not None
    assert set(receipt.model_dump()) == {
        "evidence_id",
        "status",
        "root_id",
        "work_packet_specification_id",
        "authority_fingerprint",
        "kind",
        "semantic_effect_token",
        "preconditions_proven",
    }
    assert evaluate_objective_continuation(
        root,
        packet,
        authority,
        [completed, receipt],
    ).model_dump() == {
        "disposition": ContinuationDisposition.EFFECT,
        "semantic_effect_token": APPLY,
    }
