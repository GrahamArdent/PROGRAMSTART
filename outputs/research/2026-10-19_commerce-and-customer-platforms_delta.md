# Research Delta - Commerce and customer platforms

Review date: 2026-10-19
Owner: growth-platform
Outcome: recommendation changed
Confidence: high

## Source changes

- Reviewed Shopify's 2026-07 release notes: <https://shopify.dev/changelog/release-notes/2026-07>.
- Reviewed the Events subscription query-complexity change: <https://shopify.dev/changelog/posts/events-subscription-query-complexity-limit-is-changing-to-100-points>.

## Decision

Keep commerce APIs explicitly versioned and migration-tested. Shopify 2026-07 includes action-required changes, and Events subscriptions must be shaped below the new 100-point complexity limit. Split subscriptions by handler need while preserving required fields; do not blindly truncate queries.

## Follow-up

- Audit subscription queries and inventory/customer mutations before adopting the new API version.
