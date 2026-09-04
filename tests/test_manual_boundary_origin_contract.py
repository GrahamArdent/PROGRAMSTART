from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_manual_boundary_origin_is_explicit():
    autonomy = (ROOT / "docs" / "PROGRAMSTART_EFFECTIVE_AUTONOMY.md").read_text(
        encoding="utf-8"
    )
    observation_path = ROOT.joinpath(
        "docs",
        "acceptance",
        "observations",
        "2026-09-03-manual-boundary-origin-retest.md",
    )
    observation = observation_path.read_text(encoding="utf-8")

    assert "genuine_human_gate" in autonomy
    assert "temporary_automation_gap" in autonomy
    assert (
        "Current-environment inability alone is never evidence of a genuine human gate"
        in autonomy
    )
    assert "removable implementation debt" in autonomy
    assert "GrahamArdent/whats" in observation
    assert "GrahamArdent/resume_creator_v5" in observation
    assert "Compute Spine issue #36" in observation
