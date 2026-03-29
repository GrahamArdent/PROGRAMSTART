from __future__ import annotations

import argparse
import re

try:
    from .programstart_common import warn_direct_script_invocation, workspace_path
except ImportError:  # pragma: no cover - standalone script execution fallback
    from programstart_common import warn_direct_script_invocation, workspace_path


CHECKBOX_RE = re.compile(r"^- \[(?P<mark>[ xX])\]\s+")


def summarize_checklist(text: str) -> tuple[list[tuple[str, int, int]], int, int]:
    current_section = "Unsectioned"
    sections: list[tuple[str, int, int]] = []
    checked = 0
    total = 0
    section_checked = 0
    section_total = 0

    def flush() -> None:
        nonlocal section_checked, section_total
        if section_total:
            sections.append((current_section, section_checked, section_total))
        section_checked = 0
        section_total = 0

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if line.startswith("## "):
            flush()
            current_section = line[3:]
            continue
        match = CHECKBOX_RE.match(line)
        if not match:
            continue
        total += 1
        section_total += 1
        if match.group("mark").lower() == "x":
            checked += 1
            section_checked += 1

    flush()
    return sections, checked, total


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize PROGRAMBUILD checklist completion.")
    parser.add_argument("--file", default="PROGRAMBUILD/PROGRAMBUILD_CHECKLIST.md", help="Checklist file to summarize.")
    args = parser.parse_args()

    checklist_path = workspace_path(args.file)
    text = checklist_path.read_text(encoding="utf-8")
    sections, checked, total = summarize_checklist(text)

    print(f"Checklist: {args.file}")
    print(f"Overall: {checked}/{total} completed")
    for title, section_checked, section_total in sections:
        print(f"- {title}: {section_checked}/{section_total}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    warn_direct_script_invocation("'uv run programstart progress' or 'pb progress'")
    raise SystemExit(main())
