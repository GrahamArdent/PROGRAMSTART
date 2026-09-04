from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUTONOMY_PATH = ROOT / "docs" / "PROGRAMSTART_EFFECTIVE_AUTONOMY.md"
CHECKLIST_PATH = ROOT / "PROGRAMBUILD" / "PROGRAMBUILD_CHECKLIST.md"
OBSERVATIONS_DIR = ROOT / "docs" / "acceptance" / "observations"
OBSERVATION_PATH = OBSERVATIONS_DIR / "2026-09-03-manual-boundary-origin-retest.md"
BELL_RETEST_PATH = OBSERVATIONS_DIR / "2026-09-04-court-evidence-alternative-actuation-retest.md"


def test_manual_boundary_origin_is_explicit():
    autonomy = AUTONOMY_PATH.read_text(encoding="utf-8")
    checklist = CHECKLIST_PATH.read_text(encoding="utf-8")
    observation = OBSERVATION_PATH.read_text(encoding="utf-8")
    bell_retest = BELL_RETEST_PATH.read_text(encoding="utf-8")

    assert "genuine_human_gate" in autonomy
    assert "temporary_automation_gap" in autonomy
    assert "Current-environment inability alone is never evidence of a genuine human gate" in autonomy
    assert "removable implementation debt" in autonomy
    assert "alternative-actuation search" in autonomy
    assert "Tool creativity is mandatory before human transport" in autonomy
    assert "creative in mechanism and conservative in authority" in autonomy
    assert "connected APIs/connectors" in autonomy
    assert "custom/bounded API composition" in autonomy
    assert "before escalating an already-authorized mechanical action to operator transport" in checklist
    assert "tool creativity was applied before any operator transport claim" in checklist
    assert "GrahamArdent/whats" in observation
    assert "GrahamArdent/resume_creator_v5" in observation
    assert "Compute Spine issue #36" in observation
    assert "whats PR #42" in bell_retest
    assert "PSL-021" in bell_retest
