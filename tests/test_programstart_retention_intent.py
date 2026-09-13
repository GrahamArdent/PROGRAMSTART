from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROMPT = ROOT / ".github" / "prompts" / "start-programstart-project.prompt.md"


def _prompt() -> str:
    return PROMPT.read_text(encoding="utf-8")


def test_retention_intent_needs_no_magic_phrase_and_does_not_execute() -> None:
    prompt = _prompt()

    assert "Natural-language **retention intent** is also a valid orchestration input" in prompt
    assert "Do not require a magic phrase, exact command" in prompt
    assert "Interpret the operator's meaning semantically from context" in prompt
    assert "Retention intent is not execution authorization" in prompt
    assert "full conversation context actually available" in prompt
    assert "save the good stuff from this chat" in prompt
    assert "do not infer execution, priority, sequencing, budget, or architecture" in prompt


def test_retention_then_proceed_keeps_authority_separate() -> None:
    prompt = _prompt()

    assert "save the good stuff, then proceed" in prompt
    assert "complete the retention/reconciliation pass first" in prompt
    assert "then independently resolve `proceed`" in prompt
    assert "Retention itself never upgrades the later `proceed` into broader authority" in prompt


def test_retention_uses_available_context_and_existing_surfaces() -> None:
    prompt = _prompt()

    assert "use the full conversation context actually available" in prompt
    assert "search plausible owning/reference surfaces before creating duplicates" in prompt
    assert "use an existing workspace resurfacing/detection mechanism when one exists" in prompt
    assert "return a concise retention receipt" in prompt


def test_retention_preserves_meaning_instead_of_raw_transcript() -> None:
    prompt = _prompt()

    assert "smallest useful durable meaning" in prompt
    assert "Do not archive or copy the raw conversation" in prompt
