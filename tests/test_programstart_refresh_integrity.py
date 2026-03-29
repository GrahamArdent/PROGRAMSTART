from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.programstart_refresh_integrity import baseline_for, load_attachment_manifest, main, sha256


def test_sha256_produces_64_char_hex(tmp_path: Path) -> None:
    test_file = tmp_path / "test.txt"
    test_file.write_text("hello\n", encoding="utf-8")
    digest = sha256(test_file)
    assert len(digest) == 64
    assert digest == digest.upper()


def test_sha256_consistent(tmp_path: Path) -> None:
    test_file = tmp_path / "test.txt"
    test_file.write_text("deterministic content", encoding="utf-8")
    assert sha256(test_file) == sha256(test_file)


def test_sha256_differs_for_different_content(tmp_path: Path) -> None:
    a = tmp_path / "a.txt"
    b = tmp_path / "b.txt"
    a.write_text("content A", encoding="utf-8")
    b.write_text("content B", encoding="utf-8")
    assert sha256(a) != sha256(b)


def test_baseline_for_reads_registry_integrity_section() -> None:
    registry = {
        "integrity": {
            "baselines": [
                {"name": "snapshot", "root": "BACKUPS/example"},
            ]
        }
    }

    baseline = baseline_for(registry, "snapshot")

    assert baseline["root"] == "BACKUPS/example"


def test_load_attachment_manifest_reads_json(tmp_path: Path, monkeypatch) -> None:
    manifest = tmp_path / "USERJOURNEY" / "USERJOURNEY_INTEGRITY_REFERENCE.json"
    manifest.parent.mkdir(parents=True, exist_ok=True)
    manifest.write_text(
        json.dumps(
            {
                "source_workspace": "Example",
                "allowed_external_paths": ["frontend/app/page.tsx"],
            }
        ),
        encoding="utf-8",
    )
    registry = {
        "integrity": {
            "baselines": [
                {
                    "name": "userjourney_attachment_reference",
                    "manifest": "USERJOURNEY/USERJOURNEY_INTEGRITY_REFERENCE.json",
                }
            ]
        }
    }
    monkeypatch.setattr("scripts.programstart_refresh_integrity.workspace_path", lambda relative: tmp_path / relative)

    payload = load_attachment_manifest(registry, "userjourney_attachment_reference")

    assert payload == {"source_workspace": "Example", "allowed_external_paths": ["frontend/app/page.tsx"]}


def test_main_generates_manifest_and_report(capsys, monkeypatch) -> None:
    # Create a small set of fake repo files inside the workspace to avoid scanning the entire tree
    fake_file = ROOT / "_test_sentinel.md"
    output_dir = ROOT / "_test_outputs"
    fake_file.write_text("# Test sentinel", encoding="utf-8")
    try:
        monkeypatch.setattr(
            "sys.argv",
            ["programstart_refresh_integrity.py", "--date", "2099-01-01", "--output-dir", str(output_dir)],
        )
        monkeypatch.setattr(
            "scripts.programstart_refresh_integrity.collect_registry_integrity_files",
            lambda _registry: [fake_file],
        )
        result = main()
        out = capsys.readouterr().out
        assert "MANIFEST_2099-01-01.txt" in out
        assert "VERIFICATION_REPORT_2099-01-01.md" in out
        assert result == 0
        report_text = (output_dir / "VERIFICATION_REPORT_2099-01-01.md").read_text(encoding="utf-8")
        assert "USERJOURNEY integrity manifest:" in report_text
        assert "USERJOURNEY allowlisted external implementation paths:" in report_text
        assert "Temp, generated, and previously emitted integrity artifacts are excluded" in report_text
    finally:
        # Clean up generated files
        fake_file.unlink(missing_ok=True)
        shutil.rmtree(output_dir, ignore_errors=True)


def test_main_reports_backup_mismatch(capsys, monkeypatch) -> None:
    fake_file = ROOT / "_test_sentinel_two.md"
    output_dir = ROOT / "_test_outputs_two"
    fake_file.write_text("# Test sentinel", encoding="utf-8")
    original_sha256 = sha256
    try:
        monkeypatch.setattr(
            "sys.argv",
            ["programstart_refresh_integrity.py", "--date", "2099-01-02", "--output-dir", str(output_dir)],
        )
        monkeypatch.setattr(
            "scripts.programstart_refresh_integrity.collect_registry_integrity_files",
            lambda _registry: [fake_file],
        )

        def fake_sha256(path: Path) -> str:
            if "BACKUPS" in str(path):
                return "A" * 64
            if path.name == fake_file.name:
                return original_sha256(path)
            return "B" * 64

        monkeypatch.setattr("scripts.programstart_refresh_integrity.sha256", fake_sha256)
        result = main()
        report_text = (output_dir / "VERIFICATION_REPORT_2099-01-02.md").read_text(encoding="utf-8")
        assert result == 0
        assert "PROGRAMBUILD files match backup snapshot: no" in report_text
    finally:
        fake_file.unlink(missing_ok=True)
        shutil.rmtree(output_dir, ignore_errors=True)


def test_main_reports_backup_match(capsys, monkeypatch) -> None:
    fake_file = ROOT / "_test_sentinel_three.md"
    output_dir = ROOT / "_test_outputs_three"
    fake_file.write_text("# Test sentinel", encoding="utf-8")
    try:
        monkeypatch.setattr(
            "sys.argv",
            ["programstart_refresh_integrity.py", "--date", "2099-01-03", "--output-dir", str(output_dir)],
        )
        monkeypatch.setattr(
            "scripts.programstart_refresh_integrity.collect_registry_integrity_files",
            lambda _registry: [fake_file],
        )
        monkeypatch.setattr("scripts.programstart_refresh_integrity.sha256", lambda _path: "A" * 64)
        result = main()
        report_text = (output_dir / "VERIFICATION_REPORT_2099-01-03.md").read_text(encoding="utf-8")
        assert result == 0
        assert "PROGRAMBUILD files match backup snapshot: yes" in report_text
    finally:
        fake_file.unlink(missing_ok=True)
        shutil.rmtree(output_dir, ignore_errors=True)
