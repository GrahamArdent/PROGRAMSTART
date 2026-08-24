from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .programstart_graph import DependencyGraph


@dataclass(frozen=True, slots=True)
class EvidenceRecord:
    """Reusable verification evidence and the surfaces that make it relevant.

    ``observed_at`` is provenance metadata only. Validity is determined by explicit
    dependency/scope invalidation, not by age alone.
    """

    evidence_id: str
    source: str = ""
    scopes: tuple[str, ...] = ()
    depends_on: tuple[str, ...] = ()
    provenance: tuple[str, ...] = ()
    observed_at: str = ""

    def __post_init__(self) -> None:
        if not self.evidence_id.strip():
            raise ValueError("evidence_id must not be empty")

    @property
    def validity_surfaces(self) -> frozenset[str]:
        return frozenset((*self.scopes, *self.depends_on))


@dataclass(frozen=True, slots=True)
class InvalidationCause:
    """One changed surface and the deterministic path by which it invalidates evidence."""

    trigger: str
    surface: str
    path: tuple[str, ...]

    @property
    def propagated(self) -> bool:
        return len(self.path) > 1


@dataclass(frozen=True, slots=True)
class EvidenceAssessment:
    """Validity result for one evidence record."""

    record: EvidenceRecord
    causes: tuple[InvalidationCause, ...] = ()

    @property
    def valid(self) -> bool:
        return not self.causes

    @property
    def invalidated_surfaces(self) -> tuple[str, ...]:
        return tuple(sorted({cause.surface for cause in self.causes}))


@dataclass(frozen=True, slots=True)
class EvidenceEvaluation:
    """Batch evidence validity result for a single change set."""

    changed_surfaces: tuple[str, ...]
    impacted_surfaces: tuple[str, ...]
    assessments: tuple[EvidenceAssessment, ...]

    @property
    def valid_evidence(self) -> tuple[EvidenceRecord, ...]:
        return tuple(item.record for item in self.assessments if item.valid)

    @property
    def invalidated_evidence(self) -> tuple[EvidenceRecord, ...]:
        return tuple(item.record for item in self.assessments if not item.valid)


def impact_causes(
    changed_surfaces: Iterable[str],
    *,
    graph: DependencyGraph | None = None,
    max_depth: int | None = None,
) -> dict[str, tuple[InvalidationCause, ...]]:
    """Map each directly or transitively affected surface to its provenance causes.

    When a graph is supplied, a changed prerequisite invalidates downstream dependents.
    The graph itself controls which relation types can propagate impact. Without a graph,
    only direct changes are considered.
    """
    changed = tuple(sorted({surface for surface in changed_surfaces if surface}))
    causes_by_surface: dict[str, list[InvalidationCause]] = {}

    def add(cause: InvalidationCause) -> None:
        bucket = causes_by_surface.setdefault(cause.surface, [])
        if cause not in bucket:
            bucket.append(cause)

    for trigger in changed:
        add(InvalidationCause(trigger=trigger, surface=trigger, path=(trigger,)))
        if graph is None:
            continue
        for path in graph.dependent_paths(trigger, max_depth=max_depth):
            add(
                InvalidationCause(
                    trigger=trigger,
                    surface=path.end,
                    path=path.nodes,
                )
            )

    return {
        surface: tuple(sorted(causes, key=lambda cause: (len(cause.path), cause.trigger, cause.path)))
        for surface, causes in sorted(causes_by_surface.items())
    }


def assess_evidence(
    record: EvidenceRecord,
    *,
    changed_surfaces: Iterable[str],
    graph: DependencyGraph | None = None,
    max_depth: int | None = None,
) -> EvidenceAssessment:
    """Assess one record against explicit changed surfaces and optional graph impact."""
    causes = impact_causes(changed_surfaces, graph=graph, max_depth=max_depth)
    matched = [cause for surface in sorted(record.validity_surfaces) for cause in causes.get(surface, ())]
    matched.sort(key=lambda cause: (cause.surface, len(cause.path), cause.trigger, cause.path))
    return EvidenceAssessment(record=record, causes=tuple(matched))


def evaluate_evidence(
    records: Iterable[EvidenceRecord],
    *,
    changed_surfaces: Iterable[str],
    graph: DependencyGraph | None = None,
    max_depth: int | None = None,
) -> EvidenceEvaluation:
    """Evaluate a group of evidence records without mutating or expiring them by age."""
    changed = tuple(sorted({surface for surface in changed_surfaces if surface}))
    causes = impact_causes(changed, graph=graph, max_depth=max_depth)
    assessments: list[EvidenceAssessment] = []

    for record in sorted(records, key=lambda item: item.evidence_id):
        matched = [cause for surface in sorted(record.validity_surfaces) for cause in causes.get(surface, ())]
        matched.sort(key=lambda cause: (cause.surface, len(cause.path), cause.trigger, cause.path))
        assessments.append(EvidenceAssessment(record=record, causes=tuple(matched)))

    return EvidenceEvaluation(
        changed_surfaces=changed,
        impacted_surfaces=tuple(causes),
        assessments=tuple(assessments),
    )
