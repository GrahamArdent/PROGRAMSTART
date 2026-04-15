"""Lightweight prompt lint for pre-commit.

Checks that public `.prompt.md` files have valid YAML frontmatter and satisfy
class-aware structural requirements derived from the prompt registry.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

try:
    from .programstart_common import load_registry_from_path
except ImportError:  # pragma: no cover - standalone script execution fallback
    from programstart_common import load_registry_from_path

REQUIRED_FIELDS = {"description", "name", "agent"}
OPTIONAL_FIELDS = {"argument-hint", "version", "deprecated"}
ALLOWED_FIELDS = REQUIRED_FIELDS | OPTIONAL_FIELDS

WORKFLOW_REQUIRED_SECTIONS = [
    "## Data Grounding Rule",
    "## Protocol Declaration",
    "## Pre-flight",
    "## Verification Gate",
]

OPERATOR_BASE_REQUIRED_SECTIONS = [
    "## Data Grounding Rule",
    "## Protocol Declaration",
    "## Pre-flight",
]

OPERATOR_LONGFORM_REQUIRED_SECTIONS = [
    "## Authority Loading",
    "## Scope Guard",
    "## Resumption Protocol",
    "## Verification Gate",
    "## Completion Rule",
]

WORKFLOW_ROUTING_SECTION = "## Next Steps"
WORKFLOW_ROUTING_TOKEN = "stage-transition"

ROOT = Path(__file__).resolve().parents[1]
PROMPTS_DIR = ROOT / ".github" / "prompts"
REGISTRY_PATH = ROOT / "config" / "process-registry.json"


def _extract_frontmatter(text: str) -> dict[str, str] | None:
    m = re.match(r"^---\r?\n(.*?)\r?\n---", text, re.DOTALL)
    if not m:
        return None
    fields: dict[str, str] = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            key, _, value = line.partition(":")
            fields[key.strip()] = value.strip().strip('"').strip("'")
    return fields


def _load_prompt_registry() -> dict[str, str]:
    registry = load_registry_from_path(REGISTRY_PATH)
    prompt_registry = registry.get("prompt_registry", {})
    mapping: dict[str, str] = {}

    for prompt_path in prompt_registry.get("workflow_prompt_files", []):
        mapping[prompt_path] = "workflow"
    for prompt_path in prompt_registry.get("operator_prompt_files", []):
        mapping[prompt_path] = "operator"
    for prompt_path in prompt_registry.get("internal_prompt_files", []):
        mapping[prompt_path] = "internal"

    return mapping


PROMPT_CLASS_BY_PATH = _load_prompt_registry()


def _normalize_prompt_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _prompt_class(path: Path, explicit_class: str | None = None) -> str:
    if explicit_class is not None:
        return explicit_class

    normalized = _normalize_prompt_path(path)
    if normalized in PROMPT_CLASS_BY_PATH:
        return PROMPT_CLASS_BY_PATH[normalized]
    if "internal" in path.parts:
        return "internal"
    return "workflow"


def _is_utility_operator_prompt(text: str) -> bool:
    return "UTILITY OPERATOR PROMPT" in text


def _has_execution_protocol(text: str) -> bool:
    return "## Execution Protocol" in text or "## Phase Execution Protocol" in text


def lint_prompt(path: Path, explicit_class: str | None = None) -> list[str]:
    problems: list[str] = []
    text = path.read_text(encoding="utf-8")
    fields = _extract_frontmatter(text)
    name = path.name
    prompt_class = _prompt_class(path, explicit_class)

    if fields is None:
        problems.append(f"{name}: missing YAML frontmatter (must start with ---)")
        return problems

    for req in REQUIRED_FIELDS:
        if req not in fields or not fields[req]:
            problems.append(f"{name}: missing required frontmatter field '{req}'")

    for field in fields:
        if field not in ALLOWED_FIELDS:
            problems.append(f"{name}: unrecognized frontmatter field '{field}'")

    if prompt_class == "workflow":
        for section in WORKFLOW_REQUIRED_SECTIONS:
            if section not in text:
                problems.append(f"{name}: missing mandatory section '{section}'")

    if prompt_class == "operator":
        for section in OPERATOR_BASE_REQUIRED_SECTIONS:
            if section not in text:
                problems.append(f"{name}: missing mandatory operator section '{section}'")

        if not _is_utility_operator_prompt(text):
            for section in OPERATOR_LONGFORM_REQUIRED_SECTIONS:
                if section not in text:
                    problems.append(f"{name}: missing mandatory operator section '{section}'")
            if not _has_execution_protocol(text):
                problems.append(
                    f"{name}: missing operator execution section '## Execution Protocol' or '## Phase Execution Protocol'"
                )

        if WORKFLOW_ROUTING_SECTION in text or WORKFLOW_ROUTING_TOKEN in text:
            problems.append(f"{name}: operator prompts must not include workflow routing to stage transition")

    return problems


def main(argv: list[str] | None = None) -> int:
    files = argv if argv is not None else sys.argv[1:]
    all_problems: list[str] = []
    for filepath in files:
        path = Path(filepath)
        if not path.name.endswith(".prompt.md"):
            continue
        if _prompt_class(path) == "internal":
            continue
        all_problems.extend(lint_prompt(path))

    if all_problems:
        for problem in all_problems:
            print(problem)
        return 1
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
