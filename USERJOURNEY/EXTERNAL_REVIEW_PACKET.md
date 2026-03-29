# EXTERNAL_REVIEW_PACKET.md

Purpose: Review-ready packet for the remaining legal and operational approvals that block USERJOURNEY finalization.
Owner: Solo operator
Last updated: 2026-03-27
Depends on: OPEN_QUESTIONS.md, LEGAL_REVIEW_NOTES.md, LEGAL_AND_CONSENT.md, TERMS_OF_SERVICE_DRAFT.md, PRIVACY_POLICY_DRAFT.md
Authority: Derived review packet only; source of truth remains the linked authority docs

---

## Goal

Package the remaining blocked decisions so counsel or operations can answer them directly without needing to reconstruct the product context from scratch.

This file is not the source of truth. It is a decision-ready summary layer for external review.

## Current Product Context

The product is a resume workflow platform that:

1. requires account creation before upload
2. stores resume and related profile data in authenticated user context
3. uses AI-assisted features for content improvement and tailoring
4. treats `first_value_achieved` as the canonical activation event
5. should not publish legal or operational promises that exceed verified capability

## Decisions Needed

### 1. Governing Law And Jurisdiction

Decision needed:

- Which governing law and dispute forum should Terms use for the intended launch market?

Why this matters:

- `TERMS_OF_SERVICE_DRAFT.md` cannot finalize section 16 without it.
- public legal text should not guess a jurisdiction.

Current recommendation:

- pick one primary launch jurisdiction now and align the initial Terms to that jurisdiction instead of writing pseudo-global dispute language.

Blocked files:

- `TERMS_OF_SERVICE_DRAFT.md`
- `LEGAL_REVIEW_NOTES.md`

Response format requested:

- jurisdiction
- governing law
- dispute forum or arbitration posture
- any required consumer-law carve-outs

### 2. Limitation Of Liability Wording

Decision needed:

- What limitation of liability wording is appropriate for the intended market and product risk profile?

Why this matters:

- employment-related tooling increases sensitivity around outcomes and disclaimers.
- the current draft is directionally useful but not jurisdiction-tuned.

Current recommendation:

- keep the no-employment-guarantee language strong and pair it with a jurisdiction-appropriate liability cap and excluded-damages clause.

Blocked files:

- `TERMS_OF_SERVICE_DRAFT.md`
- `LEGAL_REVIEW_NOTES.md`

Response format requested:

- approved limitation clause text or fallback language
- any prohibited phrases for the target jurisdiction

### 3. Additional Employment-Tool Disclosures

Decision needed:

- Are additional disclosures required because the product helps create or tailor job-application materials?

Why this matters:

- policy text should not under-disclose the employment-related context if counsel believes extra warnings are needed.

Current recommendation:

- assume the existing no-guarantee and AI-output disclaimers are the baseline, then add only disclosures counsel says are specifically required for the target market.

Blocked files:

- `TERMS_OF_SERVICE_DRAFT.md`
- `PRIVACY_POLICY_DRAFT.md`
- `LEGAL_REVIEW_NOTES.md`
- `UX_COPY_DRAFT.md`

Response format requested:

- required disclosures
- preferred placement: signup, policy text, inline notice, or all three

### 4. Retention And Backup Behavior

Decision needed:

- What retention behavior is actually supportable for deleted user data and backups?

Why this matters:

- privacy language is currently intentionally non-numeric because operations are not yet frozen.
- implementation and support copy must not overpromise deletion timing.

Current recommendation:

- do not publish numeric deletion or backup-retention promises until operations are explicitly verified.
- if a number must be published, tie it to an operational process that is already supportable.

Blocked files:

- `PRIVACY_POLICY_DRAFT.md`
- `LEGAL_REVIEW_NOTES.md`
- `OPEN_QUESTIONS.md`

Response format requested:

- active-data deletion behavior
- backup retention behavior
- any legal-compliance retention exceptions
- wording constraints for public policy text

### 5. Published Contact Path

Decision needed:

- What production contact path should Terms and Privacy publish for support and privacy requests?

Why this matters:

- policies should not ship with placeholder or personal-only contact details if a more durable route is intended.

Current recommendation:

- define one support contact path and one privacy contact path now, even if they initially route to the same monitored inbox.

Blocked files:

- `TERMS_OF_SERVICE_DRAFT.md`
- `PRIVACY_POLICY_DRAFT.md`
- `LEGAL_REVIEW_NOTES.md`

Response format requested:

- support contact
- privacy contact
- whether they are public aliases or a shared inbox

## What Should Not Be Invented Before Review

Do not guess or publish:

1. numeric retention periods
2. self-serve account deletion promises
3. jurisdiction-specific legal language without counsel review
4. extra employment-related disclosures unless counsel requires them
5. contact paths that are not actually monitored

## Recommended Review Order

1. governing law and liability posture
2. employment-tool disclosure requirements
3. retention and backup behavior
4. published support and privacy contacts

## Suggested Review Ask

Please answer each decision in the requested response format and note any wording that must be changed in Terms, Privacy, signup copy, or inline AI/data notice copy.

---

## Phase 1 Triage Status

Status recorded 2026-03-27. Planning defaults set for items that can safely proceed; counsel involvement required before publishing policy text for items marked "defer to counsel."

| # | Item | Disposition | Planning Default / Action |
|---|---|---|---|
| 1 | Governing law and jurisdiction | Defer to counsel | US (Delaware) planning assumption; do not publish jurisdiction until confirmed |
| 2 | Limitation of liability wording | Defer to counsel | Mutual exclusion + fee-based cap planning posture; no final text without jurisdiction decision |
| 3 | Additional employment-tool disclosures | Planning default set | Existing no-guarantee + AI-output disclaimers are the baseline; add only disclosures counsel specifically requires |
| 4 | Retention and backup behavior | Planning default set | Deleted-account data: within 30 days; backups: up to 90 days; no numeric promise in public copy until operationally verified |
| 5 | Published contact path | Planning default set | support@[domain] and privacy@[domain]; replace placeholders with real addresses before launch |

Items 1 and 2 require counsel decision before TERMS_OF_SERVICE_DRAFT.md can be finalized. Items 3–5 may proceed in drafts with planning defaults clearly marked as pre-launch placeholders.
