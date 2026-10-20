# Research Delta - Developer tooling and monorepo delivery

Review date: 2026-10-19
Owner: developer-platform
Outcome: recommendation changed
Confidence: high

## Source changes

- Reviewed pnpm 12.14 and current release notes: <https://pnpm.io/blog/releases/12.14.0> and <https://pnpm.io/blog/>.
- Reviewed the Nx 23.3/current platform feed: <https://nx.dev/blog>.

## Decision

Retain locked package-manager versions and fail-closed integrity controls. pnpm's cache exclusion, registry-token scoping, permissions, and remote-cache changes are meaningful but require deliberate workspace migration. Nx remains optional orchestration for repositories that benefit from its graph/caching model; agent features do not justify adding it to small projects.

## Follow-up

- Reassess only in repositories already using pnpm/Nx or when monorepo scale earns orchestration overhead.
