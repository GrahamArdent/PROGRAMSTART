# Research Delta - Python runtime and packaging

Review date: 2026-10-19
Owner: platform
Outcome: recommendation unchanged
Confidence: high

## Source changes

- Reviewed the official uv Python support and interpreter-management guidance: <https://docs.astral.sh/uv/reference/policies/python/> and <https://docs.astral.sh/uv/concepts/python-versions/>.
- uv now lists CPython 3.10-3.15 as Tier 1 and supports explicit free-threaded variants. Managed patch upgrades do not cross minor versions.

## Decision

Retain explicit project Python constraints and locked uv environments. Do not silently move projects between Python minor versions or default them to free-threaded builds; test those as an explicit compatibility lane. No canonical stack relationship changes are required.

## Follow-up

- Revisit when PROGRAMSTART deliberately adds Python 3.14/3.15 or free-threaded CI coverage.
