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


def test_idea_intake_uses_validator_compatible_stop_signal_fields() -> None:
    text = (ROOT / "PROGRAMBUILD" / "PROGRAMBUILD_IDEA_INTAKE.md").read_text(encoding="utf-8")

    for index in range(1, 4):
        assert f"KILL_SIGNAL_{index}:" in text
        assert f"KILL_OR_STOP_SIGNAL_{index}:" not in text

    assert "NEEDS_UI:" in text
    assert "all 8 dimensions" in text
