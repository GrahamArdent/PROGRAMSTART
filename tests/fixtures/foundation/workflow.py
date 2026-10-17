"""Tiny offline acceptance fixture; not a product or semantic discovery engine."""

from __future__ import annotations

import json
import sys
from pathlib import Path


def validated(payload: dict) -> dict:
    if not payload.get("id") or not payload.get("source") or payload.get("kind") != "observed":
        raise ValueError("verified identity/source/observed fact required")
    if payload.get("unit") != "items" or type(payload.get("quantity")) is not int or payload["quantity"] < 0:
        raise ValueError("nonnegative integer quantity in items required")
    if type(payload.get("version")) is not int or payload["version"] not in {1, 2}:
        raise ValueError("unsupported/stale version")
    return payload


def run(action: str, state: Path, payload: dict | None = None) -> dict:
    if action == "import":
        candidate = validated(payload or {})
        if candidate["version"] != 1:
            raise ValueError("initial observation version required")
        if state.exists() and json.loads(state.read_text()) != candidate:
            raise ValueError("conflicting import")
    else:
        current = validated(json.loads(state.read_text()))
        if action == "report":
            return current
        if action != "correct":
            raise ValueError("unsupported action")
        candidate = validated(payload or {})
        if candidate["id"] != current["id"] or candidate["version"] != 2:
            raise ValueError("correction identity/version mismatch")
        if current["version"] == 2 and current != candidate:
            raise ValueError("conflicting correction replay")
    temporary = state.with_suffix(".pending")
    temporary.write_text(json.dumps(candidate))
    temporary.replace(state)
    return candidate


if __name__ == "__main__":
    try:
        input_payload = json.loads(sys.argv[3]) if len(sys.argv) > 3 else None
        print(json.dumps(run(sys.argv[1], Path(sys.argv[2]), input_payload)))
    except (OSError, ValueError, KeyError) as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1) from exc
