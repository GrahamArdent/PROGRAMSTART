"""check_commit_msg.py — Validate a git commit message against Conventional Commits.

Usage (pre-commit commit-msg hook):
    python scripts/check_commit_msg.py .git/COMMIT_EDITMSG

Exits 0 on success, 1 with a helpful error on failure.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Conventional Commits pattern
# type(optional scope)!: description
# ---------------------------------------------------------------------------
VALID_TYPES = ("feat", "fix", "docs", "chore", "ci", "refactor", "test")
SUBJECT_MAX = 100
BODY_LINE_MAX = 120

# Matches: type[!][(scope)][!]: description
_SUBJECT_RE = re.compile(
    r"^(?P<type>" + "|".join(VALID_TYPES) + r")"
    r"(?:\((?P<scope>[^)]+)\))?"
    r"(?P<breaking>!)?"
    r":\s+.+"
    r"$"
)

# Commits exempt from subject validation
_EXEMPT_RE = re.compile(r"^(Merge |WIP:|Revert |chore\(release\))", re.IGNORECASE)


def validate(message: str) -> list[str]:
    lines = message.strip().splitlines()
    if not lines:
        return ["Commit message is empty."]

    subject = lines[0].strip()

    # Exempt patterns (merges, WIP, etc.)
    if _EXEMPT_RE.match(subject):
        return []

    errors: list[str] = []

    if not _SUBJECT_RE.match(subject):
        errors.append(
            f"Subject does not match Conventional Commits format.\n"
            f"  Got:      {subject!r}\n"
            f"  Expected: <type>[optional scope]: <description>\n"
            f"  Valid types: {', '.join(VALID_TYPES)}\n"
            f"  Example:  feat(schema): add commit_hash to signoff"
        )

    if len(subject) > SUBJECT_MAX:
        errors.append(f"Subject line is too long ({len(subject)} chars, max {SUBJECT_MAX}).")

    for i, line in enumerate(lines[2:], start=3):
        if len(line) > BODY_LINE_MAX:
            errors.append(f"Body line {i} is too long ({len(line)} chars, max {BODY_LINE_MAX}).")

    return errors


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: check_commit_msg.py <commit-message-file>", file=sys.stderr)
        return 1

    msg_file = Path(sys.argv[1])
    if not msg_file.exists():
        print(f"Commit message file not found: {msg_file}", file=sys.stderr)
        return 1

    message = msg_file.read_text(encoding="utf-8")
    errors = validate(message)
    if errors:
        print("Conventional Commits violation:", file=sys.stderr)
        for err in errors:
            print(f"  {err}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
