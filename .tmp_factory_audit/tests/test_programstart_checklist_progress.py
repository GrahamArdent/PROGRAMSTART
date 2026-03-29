from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.programstart_checklist_progress import main, summarize_checklist


def test_summarize_checklist_counts_items() -> None:
    text = """\
## Section A
- [x] Done task
- [ ] Open task
- [x] Another done

## Section B
- [ ] Open one
- [ ] Open two
"""
    sections, checked, total = summarize_checklist(text)
    assert checked == 2
    assert total == 5
    assert len(sections) == 2
    assert sections[0] == ("Section A", 2, 3)
    assert sections[1] == ("Section B", 0, 2)


def test_summarize_checklist_empty() -> None:
    sections, checked, total = summarize_checklist("No checkboxes here.")
    assert checked == 0
    assert total == 0
    assert sections == []


def test_summarize_checklist_case_insensitive_marks() -> None:
    text = """\
## Items
- [X] Capital X
- [x] Lower x
- [ ] Not done
"""
    sections, checked, total = summarize_checklist(text)
    assert checked == 2
    assert total == 3


def test_main_runs_on_checklist(capsys, monkeypatch) -> None:
    monkeypatch.setattr("sys.argv", ["programstart_checklist_progress.py"])
    result = main()
    assert result == 0
    out = capsys.readouterr().out
    assert "Checklist:" in out
    assert "Overall:" in out


def test_summarize_checklist_no_section_header() -> None:
    text = """\
- [x] Top-level done
- [ ] Top-level open
"""
    sections, checked, total = summarize_checklist(text)
    assert checked == 1
    assert total == 2
    assert sections[0][0] == "Unsectioned"
