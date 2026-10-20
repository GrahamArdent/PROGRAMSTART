# Research Delta - Data platform and analytics tooling

Review date: 2026-10-19
Owner: data-platform
Outcome: recommendation changed
Confidence: high

## Source changes

- Reviewed the DuckDB release calendar: <https://duckdb.org/release_calendar>.
- Reviewed the DuckDB 2.0 preview: <https://www.duckdb.org/2026/08/17/duckdb-20-highlights>.

## Decision

Retain DuckDB for embedded analytics, but treat the planned 2.0 boundary as a migration event because it introduces a new parser, storage format, C API, and server mode. Prefer the supported 1.4 LTS or a verified 1.5 patch for conservative deployments until 2.0 compatibility is proven.

## Follow-up

- Review final 2.0 release and storage migration notes after release; do not infer final behavior from the preview.
