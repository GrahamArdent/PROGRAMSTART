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


# ---------------------------------------------------------------------------
# Phase C: boundary consolidation — closeout.py → ≥95%
# ---------------------------------------------------------------------------


def test_closeout_rejects_adr_id_with_not_required(capsys) -> None:
    """--adr-id cannot be used with --adr-result not-required (line 51)."""
    result = closeout.main(["--label", "x", "--adr-result", "not-required", "--adr-id", "ADR-0001"])
    out = capsys.readouterr().out
    assert result == 1
    assert "cannot be used" in out


def test_closeout_rejects_invalid_adr_id_format(capsys) -> None:
    """Invalid ADR id format is rejected (line 56)."""
    result = closeout.main(["--label", "x", "--adr-result", "created", "--adr-id", "INVALID"])
    out = capsys.readouterr().out
    assert result == 1
    assert "ADR-0000 format" in out


def test_closeout_json_flag_prints_evidence(tmp_path: Path, monkeypatch, capsys) -> None:
    """--json flag prints evidence payload (line 152)."""
    monkeypatch.setattr(closeout, "load_registry", lambda: {})
    monkeypatch.setattr(closeout, "git_changed_files", lambda: [])
    monkeypatch.setattr(closeout, "validate_adr_coverage", lambda _r: [])
    monkeypatch.setattr(closeout, "validate_adr_coherence", lambda _r: [])
    monkeypatch.setattr(closeout, "validate_authority_sync", lambda _r: [])
    monkeypatch.setattr(closeout, "evaluate_drift", lambda _r, _c: ([], []))
    monkeypatch.setattr(closeout, "generated_outputs_root", lambda: tmp_path / "outputs")

    result = closeout.main(["--label", "test", "--adr-result", "not-required", "--json"])
    out = capsys.readouterr().out
    assert result == 0
    parsed = json.loads(out)
    assert parsed["label"] == "test"


def test_closeout_summary_prints_warnings_and_notes(tmp_path: Path, monkeypatch, capsys) -> None:
    """Summary prints warnings and notes (lines 114, 118)."""
    monkeypatch.setattr(closeout, "load_registry", lambda: {})
    monkeypatch.setattr(closeout, "git_changed_files", lambda: [])
    monkeypatch.setattr(closeout, "validate_adr_coverage", lambda _r: ["warn1"])
    monkeypatch.setattr(closeout, "validate_adr_coherence", lambda _r: [])
    monkeypatch.setattr(closeout, "validate_authority_sync", lambda _r: [])
    monkeypatch.setattr(closeout, "evaluate_drift", lambda _r, _c: ([], ["drift-note-1"]))
    monkeypatch.setattr(closeout, "generated_outputs_root", lambda: tmp_path / "outputs")

    result = closeout.main(["--label", "z", "--adr-result", "not-required"])
    out = capsys.readouterr().out
    assert result == 1  # adr_coverage warning → failed
    assert "warning: warn1" in out
    assert "note: drift-note-1" in out
