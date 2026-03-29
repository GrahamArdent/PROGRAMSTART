# LEGAL_REVIEW_NOTES.md

Purpose: Centralize legal review checklist items, concerns, and follow-ups for onboarding and consent work.
Owner: Solo operator
Last updated: 2026-03-27
Depends on: TERMS_OF_SERVICE_DRAFT.md, PRIVACY_POLICY_DRAFT.md, LEGAL_AND_CONSENT.md
Authority: Canonical legal review workspace for USERJOURNEY

---

## Review Status

Current status: Draft pending counsel review.

## Review Checklist

| Item | Status | Notes |
|---|---|---|
| Terms covers no-employment-guarantee language | Drafted | verify jurisdiction-specific wording |
| Terms covers AI output disclaimer | Drafted | confirm adequacy for employment-related use |
| Terms covers user responsibility for truthfulness | Drafted | review for scope and enforceability |
| Privacy covers resume and JD data categories | Drafted | align with actual stored fields |
| Privacy covers AI-provider processing | Drafted | current repo evidence supports Supabase, OpenAI, optional Anthropic fallback, and optional Helicone-style logging when enabled |
| Privacy covers retention | Triaged | planning default: deleted-account data within 30 days, backups up to 90 days; no numeric public promise until operationally verified |
| Privacy covers deletion/export rights | Partial | repo supports profile/resume/context deletion paths and backup/export scripts, but no confirmed self-serve account deletion path |
| Governing law and dispute section | Triaged | defer to counsel; planning assumption is US (Delaware) until confirmed |
| Contact channels | Triaged | planning default: support@[domain] and privacy@[domain]; real addresses set before launch |

## High-Risk Legal Gaps

1. Data retention language cannot be finalized until operational retention behavior is defined.
2. AI-provider disclosure may need tightening once actual provider configuration and retention posture are confirmed.
3. Account deletion language should not promise self-serve deletion until the product truly supports it.
4. Skip-onboarding behavior must not weaken required legal acceptance or data-use disclosure for upload and generation entry points.

## Product-Legal Alignment Notes

1. Product copy must not imply that uploaded data is transient if it is actually persisted.
2. Product copy must not imply AI output is verified or authoritative.
3. Product copy and policy text must align on whether user content trains internal models.
4. Product copy and policy text must align on export and deletion capability.

## Follow-Up Questions For Counsel

1. Is the current no-guarantee language strong enough for employment outcome disclaimers?
2. Are additional disclosures needed because the tool helps generate job-application materials?
3. What exact dispute and governing law structure should be used?
4. What additional notice is needed if AI providers operate across jurisdictions?

## Review Packet

Use `EXTERNAL_REVIEW_PACKET.md` when you need to hand the remaining open items to counsel or operations in a compact, decision-ready format.

## Operational Dependencies

The following must be known before legal text is finalized:

1. actual retention behavior
2. actual deletion path
3. actual data export path
4. actual provider list used in production
5. actual support or privacy contact path

## Repo-Evidenced Provider Posture

Based on current repository evidence, the planning-safe provider posture is:

1. Supabase is the canonical auth and durable persistence layer.
2. OpenAI is the primary AI provider.
3. Anthropic may be used as an optional fallback provider where configured.
4. Helicone-style request logging may be enabled for AI cost and usage monitoring when configured.

Public policy text should still describe these as configured providers or provider categories until production configuration is finalized.
