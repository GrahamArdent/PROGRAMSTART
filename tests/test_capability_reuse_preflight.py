import pytest

from scripts.programstart_capability_discovery_gate import DiscoverySearchReceipt, ReusePreflight, validate_reuse_preflight

OWNER = "GrahamArdent/execution-node-control"


def receipts(found=False):
    pairs = [("GrahamArdent/paths", k) for k in ("registry", "blueprint", "composition")]
    pairs += [(OWNER, k) for k in ("issues", "merged_prs", "code")]
    return tuple(
        DiscoverySearchReceipt.model_validate(
            {
                "repository": repo,
                "source_kind": kind,
                "source_commit_sha": "a" * 40,
                "query": "codex_usage_diagnostic rate_limits usageLimitExceeded",
                "observed_at": "2026-10-08T20:00:00Z",
                "coverage": "complete",
                "result_ref": f"evidence/{kind}.json",
                "result_sha256": "b" * 64,
                "matched_capability_refs": ("GrahamArdent/execution-node-control#362",) if found and kind == "merged_prs" else (),
            }
        )
        for repo, kind in pairs
    )


def preflight(searches=None, decision="NEW"):
    return ReusePreflight.model_validate(
        {
            "material_reusable_delta": True,
            "required_owner_repositories": (OWNER,),
            "searches": receipts() if searches is None else searches,
            "decision": decision,
            "rationale": "compare existing source capabilities",
        }
    )


def test_registry_miss_does_not_hide_merged_en362():
    with pytest.raises(ValueError, match="EXISTING_CAPABILITY_FOUND"):
        validate_reuse_preflight(preflight(receipts(found=True)))
    validate_reuse_preflight(preflight(receipts(found=True), "COMPOSE"))


@pytest.mark.parametrize("kind", ["registry", "blueprint", "composition", "issues", "merged_prs", "code"])
def test_each_required_source_must_be_covered(kind):
    with pytest.raises(ValueError, match="DISCOVERY_INCOMPLETE"):
        validate_reuse_preflight(preflight(tuple(s for s in receipts() if s.source_kind != kind)))


@pytest.mark.parametrize("coverage", ["failed", "truncated"])
def test_failed_or_partial_search_cannot_establish_absence(coverage):
    rows = list(receipts())
    rows[-1] = rows[-1].model_copy(update={"coverage": coverage})
    with pytest.raises(ValueError, match="DISCOVERY_INCOMPLETE"):
        validate_reuse_preflight(preflight(tuple(rows)))


def test_owner_currentness_mismatch_fails_closed():
    rows = list(receipts())
    rows[-1] = rows[-1].model_copy(update={"source_commit_sha": "c" * 40})
    with pytest.raises(ValueError, match="currentness differs"):
        validate_reuse_preflight(preflight(tuple(rows)))


def test_genuinely_novel_effect_can_pass():
    validate_reuse_preflight(preflight())


def test_nonmaterial_change_needs_no_corpus_search():
    validate_reuse_preflight(
        ReusePreflight(material_reusable_delta=False, decision="NONMATERIAL", rationale="routine status only")
    )
