from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PLANNING = ROOT / "PROGRAMBUILD" / "PROGRAMBUILD_PLANNING_OPERATING_MODEL.md"
CHALLENGE = ROOT / "PROGRAMBUILD" / "PROGRAMBUILD_CHALLENGE_GATE.md"
FILE_INDEX = ROOT / "PROGRAMBUILD" / "PROGRAMBUILD_FILE_INDEX.md"
PROMPT = ROOT / ".github" / "prompts" / "programstart-convergence-packet.prompt.md"
PROMPT_REGISTRY = ROOT / "config" / "registry" / "prompting.json"
WORKSPACE_REGISTRY = ROOT / "config" / "registry" / "workspace.json"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_convergence_prompt_is_registered_distributed_and_owner_bound() -> None:
    registry = json.loads(_read(PROMPT_REGISTRY))
    prompts = registry["prompt_registry"]["workflow_prompt_files"]
    assert ".github/prompts/programstart-convergence-packet.prompt.md" in prompts

    workspace = json.loads(_read(WORKSPACE_REGISTRY))
    assets = workspace["workspace"]["bootstrap_assets"]
    assert ".github/prompts/programstart-convergence-packet.prompt.md" in assets

    prompt = _read(PROMPT)
    assert "PROGRAMBUILD/PROGRAMBUILD_PLANNING_OPERATING_MODEL.md" in prompt
    assert "PROGRAMBUILD/PROGRAMBUILD_CHALLENGE_GATE.md" in prompt
    assert "A Convergence Packet is derived evidence/reference" in prompt
    assert "GO / NO-GO" in prompt
    assert "OWNER_RECONCILIATION_REQUIRED" in prompt
    assert "owner unclear" in prompt.lower()


def test_convergence_semantics_have_single_existing_owners() -> None:
    planning = _read(PLANNING)
    challenge = _read(CHALLENGE)
    index = _read(FILE_INDEX)

    assert "### 9.9 Convergence Output And Durable Packet Routing" in planning
    assert "Route a durable packet by semantic ownership" in planning
    assert "### 2.2 Material-Delta Re-Challenge Convergence" in challenge
    assert "The Challenge that changes a candidate cannot simultaneously be the final clear result" in challenge
    assert "programstart-convergence-packet.prompt.md" in index


def test_convergence_contract_rejects_shadow_authority_and_ceremonial_repeats() -> None:
    planning = _read(PLANNING)
    challenge = _read(CHALLENGE)
    prompt = _read(PROMPT)

    assert "not project authority merely because it is complete" in planning
    assert "not a queue, backlog, priority source, currentness source, or execution authority" in planning
    assert "Do not repeat identical clear passes merely to accumulate review count" in challenge
    assert "Do not create a new repository, queue, global packet registry, lifecycle state, or second Challenge Gate" in prompt
