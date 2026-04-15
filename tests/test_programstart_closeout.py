from __future__ import annotations

import json
from pathlib import Path

from scripts import programstart_closeout as closeout


def test_closeout_writes_evidence_and_passes_with_drift_notes(tmp_path: Path, monkeypatch, capsys) -> None:
    monkeypatch.setattr(closeout, "load_registry", lambda: {})
    monkeypatch.setattr(closeout, "git_changed_files", lambda: ["scripts/programstart_closeout.py"])
    monkeypatch.setattr(closeout, "validate_adr_coverage", lambda _registry: [])
    monkeypatch.setattr(closeout, "validate_adr_coherence", lambda _registry: [])
    monkeypatch.setattr(closeout, "validate_authority_sync", lambda _registry: [])
    monkeypatch.setattr(closeout, "evaluate_drift", lambda _registry, _changed: ([], ["note-only drift"]))
    monkeypatch.setattr(closeout, "generated_outputs_root", lambda: tmp_path / "outputs")

    result = closeout.main(["--label", "phase-k1", "--adr-result", "not-required"])
    out = capsys.readouterr().out

    assert result == 0
    assert "passed_with_notes" in out
    evidence_files = list((tmp_path / "outputs" / "governance").glob("*.json"))
    assert len(evidence_files) == 1
    payload = json.loads(evidence_files[0].read_text(encoding="utf-8"))
    assert payload["label"] == "phase-k1"
    assert payload["status"] == "passed_with_notes"
    assert payload["checks"]["drift"]["notes"] == ["note-only drift"]


def test_closeout_rejects_missing_adr_id_for_created_result(capsys) -> None:
    result = closeout.main(["--label", "phase-k1", "--adr-result", "created"])
    out = capsys.readouterr().out

    assert result == 1
    assert "--adr-id is required" in out


def test_closeout_fails_when_adr_coverage_warns(tmp_path: Path, monkeypatch) -> None:
    output_path = tmp_path / "evidence.json"
    monkeypatch.setattr(closeout, "load_registry", lambda: {})
    monkeypatch.setattr(closeout, "git_changed_files", lambda: ["scripts/programstart_closeout.py"])
    monkeypatch.setattr(closeout, "validate_adr_coverage", lambda _registry: ["DEC-011 missing ADR"])
    monkeypatch.setattr(closeout, "validate_adr_coherence", lambda _registry: [])
    monkeypatch.setattr(closeout, "validate_authority_sync", lambda _registry: [])
    monkeypatch.setattr(closeout, "evaluate_drift", lambda _registry, _changed: ([], []))

    result = closeout.main(
        [
            "--label",
            "phase-k1",
            "--adr-result",
            "updated",
            "--adr-id",
            "ADR-0013",
            "--output",
            str(output_path),
        ]
    )

    assert result == 1
    payload = json.loads(output_path.read_text(encoding="utf-8"))
    assert payload["status"] == "failed"
    assert payload["checks"]["adr_coverage"]["warnings"] == ["DEC-011 missing ADR"]