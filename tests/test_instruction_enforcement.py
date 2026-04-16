from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.programstart_common import load_registry as load_composed_registry


def load_registry() -> dict:
    return load_composed_registry()


def test_sync_rule_authority_files_exist() -> None:
    registry = load_registry()

    for rule in registry["sync_rules"]:
        for relative_path in rule.get("authority_files", []):
            assert (ROOT / relative_path).exists(), f"Missing authority file in sync rule {rule['name']}: {relative_path}"


def test_sync_rule_dependent_files_exist() -> None:
    registry = load_registry()

    for rule in registry["sync_rules"]:
        for relative_path in rule.get("dependent_files", []):
            assert (ROOT / relative_path).exists(), f"Missing dependent file in sync rule {rule['name']}: {relative_path}"


def test_workflow_guidance_steps_reference_active_step_files() -> None:
    registry = load_registry()
    workflow_state = registry["workflow_state"]
    workflow_guidance = registry["workflow_guidance"]

    for system in ("programbuild", "userjourney"):
        step_files = workflow_state[system]["step_files"]
        guidance = workflow_guidance[system]
        for step_name, step_guidance in guidance.items():
            if step_name not in step_files:
                continue
            guided_files = set(step_guidance.get("files", []))
            assert guided_files & set(step_files[step_name]), (
                f"workflow_guidance.{system}.{step_name} does not reference any active step files"
            )


def test_copilot_instructions_reference_registry() -> None:
    text = (ROOT / ".github" / "copilot-instructions.md").read_text(encoding="utf-8")

    assert "config/process-registry.json" in text


def test_source_of_truth_instructions_require_drift_check() -> None:
    text = (ROOT / ".github" / "instructions" / "source-of-truth.instructions.md").read_text(encoding="utf-8")

    assert "programstart drift" in text


def test_prompt_registry_class_files_exist_and_are_disjoint() -> None:
    registry = load_registry()
    prompt_registry = registry["prompt_registry"]

    class_sets = {
        name: set(prompt_registry[name]) for name in ("workflow_prompt_files", "operator_prompt_files", "internal_prompt_files")
    }

    for class_name, prompt_paths in class_sets.items():
        for relative_path in prompt_paths:
            assert (ROOT / relative_path).exists(), f"Missing {class_name} prompt file: {relative_path}"

    assert class_sets["workflow_prompt_files"].isdisjoint(class_sets["operator_prompt_files"])
    assert class_sets["workflow_prompt_files"].isdisjoint(class_sets["internal_prompt_files"])
    assert class_sets["operator_prompt_files"].isdisjoint(class_sets["internal_prompt_files"])


def test_workflow_guidance_prompts_are_workflow_classed() -> None:
    registry = load_registry()
    workflow_prompts = set(registry["prompt_registry"]["workflow_prompt_files"])
    guidance = registry["workflow_guidance"]

    kickoff_prompts = set(guidance.get("kickoff", {}).get("prompts", []))
    assert kickoff_prompts <= workflow_prompts

    cross_cutting = set(guidance.get("cross_cutting_workflow_prompts", []))
    assert cross_cutting <= workflow_prompts

    for system in ("programbuild", "userjourney"):
        for step_name, step_guidance in guidance.get(system, {}).items():
            prompts = set(step_guidance.get("prompts", []))
            assert prompts <= workflow_prompts, (
                f"workflow_guidance.{system}.{step_name} contains non-workflow prompt(s): {sorted(prompts - workflow_prompts)}"
            )


def test_operator_discoverability_prompts_are_operator_classed() -> None:
    registry = load_registry()
    operator_prompts = set(registry["prompt_registry"]["operator_prompt_files"])

    for section_name, section in registry["workflow_guidance"].get("operator", {}).items():
        prompts = set(section.get("prompts", []))
        assert prompts <= operator_prompts, (
            f"workflow_guidance.operator.{section_name} contains non-operator prompt(s): {sorted(prompts - operator_prompts)}"
        )


def test_prompt_authority_metadata_references_existing_files() -> None:
    registry = load_registry()
    prompt_authority = registry.get("prompt_authority", {})
    public_prompts = set(registry["prompt_registry"]["workflow_prompt_files"]) | set(
        registry["prompt_registry"]["operator_prompt_files"]
    )

    for prompt_path, payload in prompt_authority.items():
        assert prompt_path in public_prompts, f"prompt_authority references prompt outside public prompt registry: {prompt_path}"
        assert (ROOT / prompt_path).exists(), f"Missing prompt_authority prompt file: {prompt_path}"
        authority_files = payload.get("authority_files", [])
        assert authority_files, f"prompt_authority entry has no authority_files: {prompt_path}"
        for relative_path in authority_files:
            assert (ROOT / relative_path).exists(), f"Missing prompt_authority authority file: {relative_path}"
