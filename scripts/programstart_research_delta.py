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


@dataclass(slots=True)
class ResearchTrackStatus:
    track: str
    owner: str
    cadence: str
    linked_domains: list[str]
    last_review_date: str
    freshness_days: int
    days_since_review: int | None
    days_until_due: int | None
    status: str


@dataclass(slots=True)
class CoverageDomainStatus:
    name: str
    status: str
    priority: str
    summary: str
    current_gaps: list[str]
    linked_tracks: list[str]


@dataclass(slots=True)
class ResearchStatusReport:
    review_date: str
    weekly_review_day: str
    operating_model: str
    total_tracks: int
    due_tracks: int
    partial_or_seed_domains: int
    tracks: list[ResearchTrackStatus]
    domains: list[CoverageDomainStatus]


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


def parse_iso_date(value: str) -> date | None:
    if not value.strip():
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


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


def build_status(review_date: str | None = None) -> ResearchStatusReport:
    knowledge_base = load_knowledge_base_model()
    ledger = knowledge_base.research_ledger
    current_date = parse_iso_date(review_date or "") or date.today()

    tracks: list[ResearchTrackStatus] = []
    for track in ledger.tracks:
        last_review = parse_iso_date(track.last_review_date)
        days_since_review = (current_date - last_review).days if last_review else None
        days_until_due = track.freshness_days - days_since_review if days_since_review is not None else None
        if days_since_review is None:
            status = "missing_review_date"
        elif days_since_review > track.freshness_days:
            status = "due"
        elif days_since_review == track.freshness_days:
            status = "due_today"
        else:
            status = "fresh"

        tracks.append(
            ResearchTrackStatus(
                track=track.name,
                owner=track.owner,
                cadence=track.cadence,
                linked_domains=list(track.linked_domains),
                last_review_date=track.last_review_date,
                freshness_days=track.freshness_days,
                days_since_review=days_since_review,
                days_until_due=days_until_due,
                status=status,
            )
        )

    domains = [
        CoverageDomainStatus(
            name=domain.name,
            status=domain.status,
            priority=domain.priority,
            summary=domain.summary,
            current_gaps=list(domain.current_gaps),
            linked_tracks=list(domain.linked_tracks),
        )
        for domain in knowledge_base.coverage_domains
    ]

    partial_or_seed_domains = sum(1 for domain in domains if domain.status in {"seed", "partial"})
    due_tracks = sum(1 for track in tracks if track.status in {"due", "due_today", "missing_review_date"})
    return ResearchStatusReport(
        review_date=str(current_date),
        weekly_review_day=ledger.weekly_review_day,
        operating_model=ledger.operating_model,
        total_tracks=len(tracks),
        due_tracks=due_tracks,
        partial_or_seed_domains=partial_or_seed_domains,
        tracks=tracks,
        domains=domains,
    )


def render_status(report: ResearchStatusReport) -> str:
    lines = [
        "PROGRAMSTART Knowledge Status",
        f"- review date: {report.review_date}",
        f"- weekly review day: {report.weekly_review_day or 'unset'}",
        f"- research tracks: {report.total_tracks}",
        f"- due tracks: {report.due_tracks}",
        f"- partial or seed domains: {report.partial_or_seed_domains}",
        "",
        "Research Tracks",
    ]
    if not report.tracks:
        lines.append("- none configured")
    else:
        for track in report.tracks:
            timing = (
                f"last review {track.last_review_date}, due in {track.days_until_due} day(s)"
                if track.days_until_due is not None
                else "last review missing"
            )
            lines.append(
                f"- {track.track}: {track.status} | owner={track.owner or 'unassigned'} | freshness={track.freshness_days}d | {timing}"
            )

    lines.extend(["", "Coverage Domains"])
    if not report.domains:
        lines.append("- none configured")
    else:
        for domain in report.domains:
            gap_text = "; ".join(domain.current_gaps[:2]) if domain.current_gaps else "no explicit gaps"
            lines.append(f"- {domain.name}: {domain.status} | priority={domain.priority or 'unset'} | {gap_text}")
    return "\n".join(lines)


def has_due_tracks(report: ResearchStatusReport) -> bool:
    return any(track.status in {"due", "due_today", "missing_review_date"} for track in report.tracks)


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
    parser.add_argument(
        "--status", action="store_true", help="Print KB coverage and research freshness status instead of generating a template."
    )
    parser.add_argument(
        "--fail-on-due",
        action="store_true",
        help="Return exit code 1 when any research track is due, due today, or missing a review date.",
    )
    parser.add_argument("--json", action="store_true", help="Emit template metadata as JSON.")
    args = parser.parse_args(argv)

    if args.status:
        report = build_status(args.date)
        if args.json:
            print(json.dumps(asdict(report), indent=2))
        else:
            print(render_status(report))
        return 1 if args.fail_on_due and has_due_tracks(report) else 0

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
