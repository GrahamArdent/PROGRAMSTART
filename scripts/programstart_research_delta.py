from __future__ import annotations

# ruff: noqa: I001

import argparse
import json
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path

try:
    from .programstart_common import generated_outputs_root, warn_direct_script_invocation, workspace_path
    from .programstart_models import KnowledgeBase, ResearchTrack
except ImportError:  # pragma: no cover - standalone script execution fallback
    from programstart_common import generated_outputs_root, warn_direct_script_invocation, workspace_path  # type: ignore
    from programstart_models import KnowledgeBase, ResearchTrack  # type: ignore


@dataclass(slots=True)
class ResearchDeltaTemplate:
    track: str
    review_date: str
    cadence: str
    owner: str
    scope: list[str]
    trigger_signals: list[str]
    required_outputs: list[str]
    operating_model: str
    weekly_review_day: str
    update_policy: list[str]
    output_path: str


def load_knowledge_base_model() -> KnowledgeBase:
    kb_path = workspace_path("config/knowledge-base.json")
    return KnowledgeBase.model_validate(json.loads(kb_path.read_text(encoding="utf-8")))


def find_track(knowledge_base: KnowledgeBase, track_name: str | None) -> ResearchTrack:
    tracks = knowledge_base.research_ledger.tracks
    if not tracks:
        raise SystemExit("Knowledge base does not define any research tracks.")
    if track_name is None:
        return tracks[0]

    needle = track_name.lower()
    for track in tracks:
        if needle == track.name.lower() or needle in track.name.lower():
            return track
    available = ", ".join(track.name for track in tracks)
    raise SystemExit(f"Unknown research track: {track_name}. Available tracks: {available}")


def slugify(value: str) -> str:
    chars = [ch.lower() if ch.isalnum() else "-" for ch in value]
    slug = "".join(chars)
    while "--" in slug:
        slug = slug.replace("--", "-")
    return slug.strip("-")


def default_output_path(review_date: str, track: ResearchTrack) -> Path:
    return generated_outputs_root() / "research" / f"{review_date}_{slugify(track.name)}_delta.md"


def render_markdown(template: ResearchDeltaTemplate) -> str:
    lines = [
        f"# Research Delta - {template.track}",
        "",
        f"Review date: {template.review_date}",
        f"Cadence: {template.cadence}",
        f"Owner: {template.owner or 'unassigned'}",
        f"Operating model: {template.operating_model}",
        f"Weekly review day: {template.weekly_review_day}",
        "",
        "## Scope",
        "",
        *(f"- {item}" for item in template.scope),
        "",
        "## Trigger Signals",
        "",
        *(f"- {item}" for item in template.trigger_signals),
        "",
        "## Required Outputs",
        "",
        *(f"- {item}" for item in template.required_outputs),
        "",
        "## Update Policy",
        "",
        *(f"- {item}" for item in template.update_policy),
        "",
        "## Source Changes",
        "",
        "- Changed sources:",
        "- Release notes or docs reviewed:",
        "- Breaking or notable deltas:",
        "",
        "## Recommendation Decision",
        "",
        "- Outcome: changed | unchanged | blocked pending evidence",
        "- Recommendation summary:",
        "- Confidence: high | medium | low",
        "",
        "## KB Update Surface",
        "",
        "- Stacks changed:",
        "- Decision rules changed:",
        "- Relationships changed:",
        "- Comparisons changed:",
        "",
        "## Follow-Up",
        "",
        "- Validation needed:",
        "- Open questions:",
        "- Deferred items:",
        "",
    ]
    return "\n".join(lines)


def build_template(review_date: str, track_name: str | None, output: str | None) -> ResearchDeltaTemplate:
    knowledge_base = load_knowledge_base_model()
    track = find_track(knowledge_base, track_name)
    output_path = Path(output) if output else default_output_path(review_date, track)
    if not output_path.is_absolute():
        output_path = workspace_path(str(output_path))

    return ResearchDeltaTemplate(
        track=track.name,
        review_date=review_date,
        cadence=track.cadence,
        owner=track.owner,
        scope=list(track.scope),
        trigger_signals=list(track.trigger_signals),
        required_outputs=list(track.required_outputs),
        operating_model=knowledge_base.research_ledger.operating_model,
        weekly_review_day=knowledge_base.research_ledger.weekly_review_day,
        update_policy=list(knowledge_base.research_ledger.update_policy),
        output_path=str(output_path),
    )


def write_template(template: ResearchDeltaTemplate) -> None:
    output_path = Path(template.output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_markdown(template), encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate a research delta template from the KB research ledger.")
    parser.add_argument("--track", help="Research track name. Defaults to the first configured track.")
    parser.add_argument("--date", default=str(date.today()), help="Review date in YYYY-MM-DD format.")
    parser.add_argument("--output", help="Explicit output path for the generated markdown file.")
    parser.add_argument("--json", action="store_true", help="Emit template metadata as JSON.")
    args = parser.parse_args(argv)

    template = build_template(args.date, args.track, args.output)
    write_template(template)

    if args.json:
        print(json.dumps(asdict(template), indent=2))
    else:
        print(f"Wrote research delta template to {template.output_path}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    warn_direct_script_invocation("'uv run programstart research' or 'pb research'")
    raise SystemExit(main())
