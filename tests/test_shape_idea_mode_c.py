from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_shape_idea_tracks_eight_dimension_mode_c_contract() -> None:
    text = (ROOT / ".github" / "prompts" / "shape-idea.prompt.md").read_text(encoding="utf-8")

    assert "Eight-Dimension" in text
    assert "NEEDS_UI" in text
    assert "KILL_SIGNAL_*" in text
    assert "Mode C" in text
    assert "Do not advance from Stage 0 merely because a freshly adopted PROGRAMBUILD state starts there." in text
    assert "existing project's actual next incomplete executable slice" in text

    stale_fragments = (
        "7-question",
        "7 interview questions",
        "For each of the 7 questions",
        "After all 7 questions",
    )
    for fragment in stale_fragments:
        assert fragment not in text


def test_mode_c_does_not_promote_legacy_repository_evidence_to_product_intent() -> None:
    text = (ROOT / ".github" / "prompts" / "shape-idea.prompt.md").read_text(encoding="utf-8")

    required_fragments = (
        "Repository state is authoritative for **what currently exists and behaves**",
        "it is not automatically authoritative for **what the product has been decided to become**",
        "current explicit operator/user decisions",
        "designated execution spine or canonical strategic authority",
        "descriptive documentation such as `README.md`",
        "legacy code, historical frameworks, archived artifacts, and obsolete dependencies",
        "MUST NOT by itself become a rebuild requirement or strategic direction",
        "reconcile apparent repository behavior with current product authority",
    )
    for fragment in required_fragments:
        assert fragment in text


def test_idea_intake_uses_validator_compatible_stop_signal_fields() -> None:
    text = (ROOT / "PROGRAMBUILD" / "PROGRAMBUILD_IDEA_INTAKE.md").read_text(encoding="utf-8")

    for index in range(1, 4):
        assert f"KILL_SIGNAL_{index}:" in text
        assert f"KILL_OR_STOP_SIGNAL_{index}:" not in text

    assert "NEEDS_UI:" in text
    assert "all 8 dimensions" in text
