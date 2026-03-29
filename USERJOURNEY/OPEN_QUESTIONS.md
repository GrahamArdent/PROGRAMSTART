# OPEN_QUESTIONS.md

Purpose: Track unresolved product, legal, and UX decisions for the new-user journey.
Owner: Solo operator
Last updated: 2026-03-27
Depends on: PRODUCT_SPEC.md, LEGAL_AND_CONSENT.md
Authority: Canonical unresolved-decision list for USERJOURNEY

---

## Status

Product, UX, consent, and analytics defaults are now frozen in `DECISION_LOG.md`.

The remaining items are external legal or operational approvals that should not be guessed in product copy.

Use `EXTERNAL_REVIEW_PACKET.md` to package these items for counsel or operations review without rewriting the source-of-truth list.

## Remaining Operational And Legal Decisions

1. What jurisdiction and governing law should Terms use?
2. What exact limitation of liability wording is appropriate for the intended market?
3. Are any additional employment-tool disclosures required by counsel for the target market?
4. What exact retention behavior is operationally supportable for deleted user data and backups?
5. What production contact path should Terms and Privacy publish for support and privacy requests?

## Phase 1 Triage Dispositions

Status values: `Decide now (planning default set)` / `Defer to counsel` / `Defer to operations`

| # | Question | Triage | Planning Default |
|---|---|---|---|
| 1 | Governing law and jurisdiction | Defer to counsel | US (Delaware) assumed until counsel confirms; do not publish jurisdiction in policy until confirmed |
| 2 | Limitation of liability wording | Defer to counsel | Mutual exclusion + fee-based liability cap assumed; no final text without jurisdiction decision |
| 3 | Additional employment-tool disclosures | Decide now (planning default set) | Existing no-guarantee and AI-output disclaimers are the planning baseline; add only what counsel specifically requires |
| 4 | Retention and backup behavior | Decide now (planning default set) | Deleted-account data removed within 30 days; backups retained up to 90 days; no numeric promise in public copy until operationally verified |
| 5 | Published contact path | Decide now (planning default set) | support@[domain] and privacy@[domain] as planning defaults; actual addresses set before launch |

---

## Recommendation Bias

Default recommendation based on current product shape:

1. account before upload
2. import-first default path
3. explicit AI notice before first upload or generation
4. onboarding separate from normal workspace routing
5. versioned consent tracking from the start
6. skip guided onboarding is allowed, but activation still requires first value
7. no separate read-only explore mode in v1
8. first profile naming happens after a meaningful artifact exists
9. `first_value_achieved` is the canonical activation event
