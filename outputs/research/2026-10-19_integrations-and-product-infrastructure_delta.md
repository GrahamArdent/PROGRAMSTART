# Research Delta - Integrations and product infrastructure

Review date: 2026-10-19
Owner: integrations-platform
Outcome: recommendation changed
Confidence: high

## Source changes

- Reviewed Stripe's API changelog and versioning process: <https://stripe.com/blog/changelog> and <https://stripe.com/blog/introducing-stripes-new-api-release-process>.
- Reviewed Resend's official changelog: <https://resend.com/changelog/>.

## Decision

Keep integrations version-pinned and webhook-idempotent. Stripe's versioned upgrade guidance remains the safe adoption surface. Resend's expanded OAuth, suppression, metrics, webhook, and account-usage APIs justify capability detection and least-privilege scopes, not automatic enablement.

## Follow-up

- Update individual provider profiles only when a project selects the corresponding new capability.
