# Research Delta - Web and platform delivery

Review date: 2026-10-19
Owner: product-platform
Outcome: recommendation changed
Confidence: high

## Source changes

- Reviewed Next.js 16.2 release guidance: <https://nextjs.org/blog/next-16-2>.
- Reviewed the React Server Components security advisory and patched release lines: <https://react.dev/blog/2025/12/03/critical-security-vulnerability-in-react-server-components>.

## Decision

Retain Next.js as a contextual full-stack option, but require supported patched release lines and treat framework security advisories as upgrade triggers. Turbopack and agent-facing tooling improvements do not remove the need for framework/runtime pinning, server/client boundary review, and regression verification.

## Follow-up

- Recheck affected release lines whenever a React Server Components advisory changes.
