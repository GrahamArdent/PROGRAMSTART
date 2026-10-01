from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_reasoning_locality_requires_escalation_step_down_and_reescalation():
    text = (ROOT / "docs/PROGRAMSTART_COST_GOVERNANCE.md").read_text()
    assert "decision-boundary properties, not objective-wide inheritance" in text
    assert "Escalate to premium reasoning only when" in text
    assert "step down" in text
    assert "Re-escalate only when new material uncertainty appears" in text

def test_reasoning_locality_preserves_stronger_constraints_and_avoids_registry():
    text = (ROOT / "docs/PROGRAMSTART_COST_GOVERNANCE.md").read_text()
    assert "MUST NOT become a model registry" in text
    assert "never trade those constraints for token savings" in text
    assert "Missing telemetry is `unknown`, never estimated as fact" in text

def test_codex_usage_counterexample_is_durable_and_truthful():
    text = (ROOT / "docs/acceptance/observations/2026-10-01-reasoning-locality-codex-usage.md").read_text()
    assert "976,937 input tokens" in text
    assert "876,416 cached input" in text
    assert "100,521 derived uncached input" in text
    assert "43 command executions" in text
    assert "exact final token accounting is unavailable" in text
    assert "usage-limit" in text

def test_learning_ledger_tracks_candidate_and_real_retest():
    text = (ROOT / "docs/PROGRAMSTART_ACCEPTANCE_LEARNING_LEDGER.md").read_text()
    assert "`PSL-025`" in text
    assert "cheaper mechanical execution" in text
    assert "materially reducing unnecessary premium consumption" in text
