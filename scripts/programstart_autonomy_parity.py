from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "config" / "autonomy-parity-contract.json"
RENDERED = ROOT / "docs" / "AUTONOMY_PARITY_MATRIX.md"
STATES = {"implemented", "partial", "missing", "prompt_only", "semantic", "human_gate"}
MODES = {"deterministic", "semantic", "hybrid", "human"}
CLOSURES = {"proven", "partial", "unproven", "pending_methodology"}
EXACT_FILE_PROOF_RE = re.compile(r"^GrahamArdent/[A-Za-z0-9_.-]+@[0-9a-f]{40}:[A-Za-z0-9_./-]+$")
EXACT_LIVE_PROOF_RE = re.compile(r"^GrahamArdent/[A-Za-z0-9_.-]+#[0-9]+$")
FIELDS = {
    "id",
    "title",
    "owner",
    "covers",
    "trigger",
    "expected_behavior",
    "must_not",
    "jit_inputs",
    "invalidation",
    "machinery_state",
    "execution_mode",
    "current_proof",
    "acceptance_scenarios",
    "closure_status",
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_contract():
    return json.loads(CONTRACT.read_text(encoding="utf-8"))


def validate_contract(c):
    e = []
    if c.get("schema_version") != 1:
        e.append("schema_version must be 1")
    if c.get("contract_id") != "programstart.autonomy-parity.v1":
        e.append("invalid contract_id")
    ru = c.get("runtime_usage", {})
    if ru.get("authority_role") != "derived_acceptance_evidence":
        e.append("matrix must remain derived acceptance evidence")
    if ru.get("retrieval_policy") != "jit_by_trigger" or ru.get("load_entire_contract_per_effect") is not False:
        e.append("matrix runtime usage must remain JIT, never load-all")

    paths = set()
    for s in c.get("source_files", []):
        p = s.get("path")
        if not p or p in paths:
            e.append("source file paths must be unique and non-empty")
            continue
        paths.add(p)
        fp = ROOT / p
        if not fp.is_file():
            e.append(f"source missing: {p}")
        else:
            expected = str(s.get("sha256", "")).replace("-", "")
            if sha(fp) != expected:
                e.append(f"source fingerprint drift: {p}")

    oids = set()
    for o in c.get("source_obligations", []):
        oid, p, anchor = o.get("id"), o.get("source_path"), o.get("anchor")
        if not oid or oid in oids:
            e.append("source obligation ids must be unique/non-empty")
            continue
        oids.add(oid)
        if o.get("required") is not True:
            e.append(f"obligation not marked required: {oid}")
        if p not in paths:
            e.append(f"obligation has unknown source: {oid}")
        elif not anchor or anchor not in (ROOT / p).read_text(encoding="utf-8"):
            e.append(f"obligation anchor drift: {oid}")

    bids, coverage = set(), defaultdict(list)
    state_counts, closure_counts = Counter(), Counter()
    for b in c.get("behaviors", []):
        bid = b.get("id")
        if not bid or bid in bids:
            e.append("behavior ids must be unique/non-empty")
            continue
        bids.add(bid)
        missing = FIELDS - set(b)
        if missing:
            e.append(f"{bid} missing fields: {sorted(missing)}")
        for oid in b.get("covers", []):
            if oid not in oids:
                e.append(f"{bid} covers unknown obligation: {oid}")
            else:
                coverage[oid].append(bid)
        if not b.get("covers") and not b.get("methodology_delta_refs"):
            e.append(f"{bid} covers no obligations")
        if b.get("methodology_delta_refs") and b.get("covers"):
            e.append(f"{bid} pending methodology behavior must not claim canonical source coverage")
        state = b.get("machinery_state")
        mode = b.get("execution_mode")
        closure = b.get("closure_status")
        if state not in STATES:
            e.append(f"{bid} invalid machinery state")
        else:
            state_counts[state] += 1
        if mode not in MODES:
            e.append(f"{bid} invalid execution mode")
        if closure not in CLOSURES:
            e.append(f"{bid} invalid closure state")
        else:
            closure_counts[closure] += 1
        for f in (
            "trigger",
            "expected_behavior",
            "must_not",
            "jit_inputs",
            "invalidation",
            "current_proof",
            "acceptance_scenarios",
        ):
            if not isinstance(b.get(f), list) or not b[f]:
                e.append(f"{bid}.{f} must be non-empty list")
        if state == "implemented":
            proofs = [x for x in b.get("current_proof", []) if isinstance(x, dict)]
            kinds = {x.get("kind") for x in proofs}
            if "code" not in kinds or not ({"test", "live"} & kinds):
                e.append(f"{bid} implemented claim lacks code plus test/live proof")
            for item in proofs:
                kind, ref = item.get("kind"), item.get("ref")
                if kind in {"code", "test"} and (not isinstance(ref, str) or EXACT_FILE_PROOF_RE.fullmatch(ref) is None):
                    e.append(f"{bid} has non-exact {kind} proof reference: {ref}")
                if kind == "live" and (not isinstance(ref, str) or EXACT_LIVE_PROOF_RE.fullmatch(ref) is None):
                    e.append(f"{bid} has non-exact live proof reference: {ref}")

    for oid in sorted(oids):
        if not coverage[oid]:
            e.append(f"uncovered obligation: {oid}")

    pending = c.get("pending_methodology_deltas", [])
    deltas = {d.get("id") for d in pending if d.get("id")}
    for delta in pending:
        did = delta.get("id")
        if delta.get("authority_status") != "accepted_pending_canonicalization":
            e.append(f"pending methodology delta has invalid authority status: {did}")
        if not delta.get("durable_reference"):
            e.append(f"pending methodology delta lacks durable reference: {did}")
        if not delta.get("narrows_current_rule"):
            e.append(f"pending methodology delta lacks narrowed current rule: {did}")
        if not delta.get("canonical_effect"):
            e.append(f"pending methodology delta lacks canonical-effect statement: {did}")
    covered_deltas = {d for b in c.get("behaviors", []) for d in b.get("methodology_delta_refs", [])}
    for d in deltas - covered_deltas:
        e.append(f"pending methodology delta not represented: {d}")

    for required in (
        "jit_context_evidence_governor",
        "credential_human_enablement_leverage",
        "objective_terminality_next_effect",
    ):
        if required not in bids:
            e.append(f"required cross-cutting behavior missing: {required}")

    ch = c.get("matrix_challenge", {})
    if ch.get("status") not in {"pending", "clear", "failed"}:
        e.append("matrix challenge status invalid")
    if len(ch.get("adversarial_cases", [])) < 8:
        e.append("matrix challenge requires at least eight cases")

    c["_summary"] = {
        "source_files": len(paths),
        "source_obligations": len(oids),
        "behaviors": len(bids),
        "machinery_states": dict(sorted(state_counts.items())),
        "closure_states": dict(sorted(closure_counts.items())),
        "pending_methodology_deltas": len(deltas),
    }
    return e


def render(c):
    s = c["_summary"]
    out = [
        "# PROGRAMSTART Autonomy Parity Matrix",
        "",
        "> Derived acceptance evidence only. Canonical PROGRAMSTART sources remain authoritative.",
        "> This is not a Master, scheduler, backlog, controller, methodology database, or execution spine.",
        "",
        f"- Contract: {c['contract_id']}",
        f"- PROGRAMSTART baseline: {c['derived_at']['programstart_commit']}",
        f"- Controller observation baseline: {c['derived_at']['controller_commit']}",
        f"- Durable reference: {c['derived_at']['durable_reference']}",
        f"- Fingerprinted source files: {s['source_files']}",
        f"- Required source obligations covered: {s['source_obligations']}",
        f"- Parity behaviors: {s['behaviors']}",
        "",
        "## JIT usage invariant",
        "",
        "Query this contract by the current trigger/effect. Never load the full matrix into every objective.",
        "Reuse still-valid evidence; widen only on declared invalidation or convergence boundaries.",
        "",
        "## Coverage summary",
        "",
    ]
    for state, count in sorted(s["machinery_states"].items()):
        out.append(f"- {state}: {count}")
    out += [
        "",
        "## Behavior matrix",
        "",
        "| Behavior | Machinery | Mode | Closure | Owner |",
        "|---|---|---|---|---|",
    ]
    for b in c["behaviors"]:
        out.append(
            f"| {b['id']} — {b['title']} | {b['machinery_state']} | {b['execution_mode']} | "
            f"{b['closure_status']} | {b['owner']} |"
        )
    out += ["", "## Priority gaps", ""]
    for b in c["behaviors"]:
        if b["machinery_state"] in {"missing", "prompt_only"}:
            out.append(f"- {b['id']}: {b['title']}")
    out += ["", "## Pending methodology deltas", ""]
    for d in c["pending_methodology_deltas"]:
        out += [f"### {d['id']}", "", d["summary"], "", f"Durable reference: {d['durable_reference']}", ""]
    out += ["## Matrix Challenge", "", f"Status: {c['matrix_challenge']['status'].upper()}", ""]
    for case in c["matrix_challenge"]["adversarial_cases"]:
        out.append(f"- {case['id']}: {case['attack']} -> {case['result']}")
    out += ["", "## Closure rule", "", c["closure_rule"], ""]
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    try:
        c = load_contract()
    except Exception as exc:
        print(f"FAIL load: {exc}", file=sys.stderr)
        return 1
    errors = validate_contract(c)
    if errors:
        for x in errors:
            print(f"FAIL: {x}", file=sys.stderr)
        return 1
    expected = render(c)
    if args.write:
        RENDERED.write_text(expected, encoding="utf-8")
    if args.check or not args.write:
        if not RENDERED.is_file() or RENDERED.read_text(encoding="utf-8") != expected:
            print("FAIL: rendered parity matrix drift; run --write", file=sys.stderr)
            return 1
    print(
        f"PASS autonomy parity: {c['_summary']['source_obligations']} obligations -> "
        f"{c['_summary']['behaviors']} behaviors; states={c['_summary']['machinery_states']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
