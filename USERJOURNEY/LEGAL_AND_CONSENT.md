# LEGAL_AND_CONSENT.md

Purpose: Define required legal surfaces and consent requirements for signup and onboarding.
Owner: Solo operator
Last updated: 2026-03-27
Depends on: PRODUCT_SPEC.md
Authority: Canonical consent and policy requirements for the new-user journey

---

## Objective

Ensure the product captures explicit, versioned, and context-appropriate consent before a user enters normal product use.

## Required Legal Surfaces

1. Terms of Service
2. Privacy Policy
3. AI and data-processing notice

## Required Consent Events

### Required At Signup

The user must explicitly accept:

1. Terms of Service
2. Privacy Policy

This should be a required affirmative action, not implied consent.

### Required Before First Upload Or Generation

The user must be shown a plain-language AI and data-processing notice before first resume upload, first job-description submission, or first AI-assisted generation event.

This notice is not a substitute for Terms or Privacy acceptance. It is a contextual disclosure.

Recommended default:

1. block the first upload or generation trigger until acknowledged
2. do not repeatedly block later use unless a material policy change requires renewed acceptance

### Optional Consent

Keep separate from legal acceptance:

1. product updates
2. marketing communications

## Terms Of Service Requirements

The Terms should cover at minimum:

1. service description
2. eligibility and account responsibilities
3. user responsibility for content truthfulness and rights
4. AI-generated output disclaimer
5. no guarantee of interview, hiring, or ATS outcomes
6. limited license to process user content for service delivery
7. prohibited conduct
8. suspension and termination rights
9. third-party provider usage
10. limitation of liability and warranty disclaimer
11. data deletion / account closure pathway
12. policy update handling

## Privacy Policy Requirements

The Privacy Policy should cover at minimum:

1. what account data is collected
2. what resume and profile data is collected
3. what job-description and generated-content data is collected
4. why the data is collected
5. what third-party providers may process the data
6. how long data is retained
7. how users can export, update, or delete data
8. whether data is used to train internal models
9. what AI providers may process content under their own terms
10. how users contact support for privacy requests

## AI Notice Requirements

The plain-language AI notice should communicate:

1. resume and job-description content may be processed by AI-backed features
2. generated suggestions may be inaccurate or incomplete
3. users must review and approve output before using it
4. uploaded and generated content may be stored with the account

## Versioning Requirements

The product should conceptually record:

1. terms version accepted
2. privacy version accepted
3. accepted timestamp
4. AI notice acknowledged timestamp
5. onboarding completion timestamp
6. optional marketing consent timestamp if applicable

Policy refresh default:

1. force re-acceptance only after material Terms or Privacy changes
2. allow non-material updates to be communicated without blocking workspace access

## UX Rules

1. Do not combine mandatory legal acceptance with optional marketing consent.
2. Do not rely on footer links alone.
3. Do not phrase required legal acceptance as pre-checked boxes.
4. Do not bury AI disclosure only in policy documents.
5. Do not over-claim legal or data security guarantees in UI copy.

## Example Plain-Language Notice

Example direction for product copy:

"Your resume and job description content may be stored in your account and processed by AI-powered features to analyze, improve, or tailor your documents. AI suggestions can be wrong, incomplete, or misleading, so you should review all output before using it."

## Legal Review Notes

This document is a product requirement outline, not legal advice. Before release, actual Terms and Privacy text should be reviewed by qualified counsel for jurisdiction, limitation language, and disclosure sufficiency.

## Phase 0 Contribution Status

This document satisfies the Phase 0 requirement to capture consent semantics before route and implementation planning proceeds.
It does not need to be finalized for Phase 0 exit — Phase 1 is explicitly scoped to harden the legal model.

| Phase 0 Contribution | Status | Notes |
|---|---|---|
| Required legal surfaces defined (Terms, Privacy, AI notice) | Complete | Section: Required Legal Surfaces |
| Required consent events defined (signup + pre-upload) | Complete | Section: Required Consent Events |
| Optional vs mandatory consent separation documented | Complete | Optional Consent section |
| Consent versioning requirements defined | Complete | Versioning Requirements section |
| UX rules for consent presentation defined | Complete | UX Rules section |
| Terms minimum coverage defined | Complete | 12 required items |
| Privacy minimum coverage defined | Complete | 10 required items |
| AI notice requirements defined | Complete | AI Notice Requirements section |
| Remaining legal items flagged for external review | Complete | `LEGAL_REVIEW_NOTES.md` and `OPEN_QUESTIONS.md` |

Last updated: 2026-03-27
