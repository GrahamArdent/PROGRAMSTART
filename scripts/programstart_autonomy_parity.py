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
CONVERSATION_DECISION_STATUSES = {
    "accepted_reconciled",
    "accepted_pending_methodology",
    "accepted_execution_sequence",
}
HOP_CLASSES = {
    "objective_ingress",
    "semantic_pipeline",
    "execution_fabric",
    "async_continuation",
    "control_plane",
    "owner_instance",
}
HOP_STATUSES = {"proven", "partial", "unproven", "human_gate"}
HOP_ID_RE = re.compile(r"^HOP-\d{3}$")
HOP_FIELDS = {
    "id",
    "class",
    "source",
    "target",
    "purpose",
    "general_mechanism",
    "required_behavior_refs",
    "instance_status",
    "evidence_refs",
    "invalidation",
    "path_authority_ref",
}
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

    conversation = c.get("conversation_decisions")
    conversation_ids = set()
    if not isinstance(conversation, list) or not conversation:
        e.append("conversation_decisions must be a non-empty list")
        conversation = []
    for decision in conversation:
        if not isinstance(decision, dict):
            e.append("conversation decision entries must be objects")
            continue
        did = decision.get("id")
        if not isinstance(did, str) or not did or did in conversation_ids:
            e.append("conversation decision ids must be unique/non-empty")
            continue
        conversation_ids.add(did)
        if decision.get("status") not in CONVERSATION_DECISION_STATUSES:
            e.append(f"conversation decision has invalid status: {did}")
        if not decision.get("durable_reference"):
            e.append(f"conversation decision lacks durable reference: {did}")
        if not decision.get("summary"):
            e.append(f"conversation decision lacks summary: {did}")
        behavior_refs = decision.get("behavior_refs")
        delta_refs = decision.get("methodology_delta_refs")
        if not isinstance(behavior_refs, list) or not isinstance(delta_refs, list):
            e.append(f"conversation decision mappings must be lists: {did}")
            continue
        if not behavior_refs and not delta_refs:
            e.append(f"conversation decision has no durable mapping: {did}")
        for ref in behavior_refs:
            if ref not in bids:
                e.append(f"conversation decision {did} references unknown behavior: {ref}")
        for ref in delta_refs:
            if ref not in deltas:
                e.append(f"conversation decision {did} references unknown methodology delta: {ref}")
        if decision.get("status") == "accepted_pending_methodology" and not delta_refs:
            e.append(f"pending-methodology conversation decision lacks methodology mapping: {did}")


    hop_policy = c.get("hop_policy", {})
    if hop_policy.get("authority_role") != "derived_acceptance_evidence":
        e.append("hop matrix must remain derived acceptance evidence")
    if hop_policy.get("instance_acceptance_required") is not True:
        e.append("hop policy must require concrete instance acceptance")
    if hop_policy.get("general_mechanism_implies_instance_acceptance") is not False:
        e.append("generalized hop machinery must never imply instance acceptance")
    if hop_policy.get("path_authority_role") != "referenced_not_replaced":
        e.append("hop matrix must reference, not replace, Path Authority")
    if not hop_policy.get("durable_reference"):
        e.append("hop policy lacks durable reference")

    hops = c.get("hop_instances")
    hop_ids = set()
    hop_keys = set()
    if not isinstance(hops, list) or not hops:
        e.append("hop_instances must be a non-empty list")
        hops = []
    for hop in hops:
        if not isinstance(hop, dict):
            e.append("hop entries must be objects")
            continue
        hid = hop.get("id")
        if (
            not isinstance(hid, str)
            or HOP_ID_RE.fullmatch(hid) is None
            or hid in hop_ids
        ):
            e.append("hop ids must be unique HOP-NNN values")
            continue
        hop_ids.add(hid)
        missing = HOP_FIELDS - set(hop)
        if missing:
            e.append(f"{hid} missing hop fields: {sorted(missing)}")
        hclass = hop.get("class")
        if hclass not in HOP_CLASSES:
            e.append(f"{hid} invalid hop class")
        status = hop.get("instance_status")
        if status not in HOP_STATUSES:
            e.append(f"{hid} invalid hop instance status")
        for field in (
            "source",
            "target",
            "purpose",
            "general_mechanism",
            "path_authority_ref",
        ):
            if not isinstance(hop.get(field), str) or not hop[field].strip():
                e.append(f"{hid}.{field} must be non-empty string")
        key = (hop.get("source"), hop.get("target"), hop.get("purpose"))
        if key in hop_keys:
            e.append(f"duplicate concrete hop instance: {hid}")
        hop_keys.add(key)
        behavior_refs = hop.get("required_behavior_refs")
        if not isinstance(behavior_refs, list) or not behavior_refs:
            e.append(f"{hid}.required_behavior_refs must be non-empty list")
            behavior_refs = []
        for ref in behavior_refs:
            if ref not in bids:
                e.append(f"{hid} references unknown behavior: {ref}")
        if hclass == "owner_instance":
            for required_ref in (
                "cross_repository_dependency_graph",
                "canonical_before_dependent",
                "repository_independence",
            ):
                if required_ref not in behavior_refs:
                    e.append(f"{hid} owner instance missing required behavior: {required_ref}")
        for field in ("evidence_refs", "invalidation"):
            value = hop.get(field)
            if (
                not isinstance(value, list)
                or not value
                or not all(isinstance(x, str) and x.strip() for x in value)
            ):
                e.append(f"{hid}.{field} must be non-empty string list")

    for required in (
        "jit_context_evidence_governor",
        "credential_human_enablement_leverage",
        "conversation_decision_reconciliation",
        "objective_terminality_next_effect",
    ):
        if required not in bids:
            e.append(f"required cross-cutting behavior missing: {required}")

    credential = next(
        (b for b in c.get("behaviors", []) if b.get("id") == "credential_human_enablement_leverage"),
        None,
    )
    if credential and "credential_human_enablement_v1" not in deltas:
        if "support.effective_autonomy.09" not in credential.get("covers", []):
            e.append("canonical credential human-enablement behavior must cover Effective Autonomy section 9")
        if credential.get("closure_status") == "pending_methodology":
            e.append("canonical credential human-enablement behavior cannot remain pending_methodology")
        if credential.get("machinery_state") not in {"partial", "implemented"}:
            e.append("canonical credential human-enablement behavior must remain at least partial")

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
        "conversation_decisions": len(conversation_ids),
        "hop_instances": len(hop_ids),
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
        f"- Accepted conversation decisions reconciled: {s['conversation_decisions']}",
        f"- Material hop instances: {s['hop_instances']}",
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
    out += [
        "",
        "## Material hop instance matrix",
        "",
        "> Generalized machinery may be reused, but every concrete material hop requires its own instance acceptance evidence.",
        "> Physical path inventory/health/recovery remains authoritative in Paths/Path Authority or the owning project.",
        "",
        "| Hop | Class | Source | Target | Mechanism | Status | Evidence |",
        "|---|---|---|---|---|---|---|",
    ]
    for hop in c["hop_instances"]:
        evidence = "<br>".join(hop["evidence_refs"])
        out.append(
            f"| {hop['id']} | {hop['class']} | {hop['source']} | {hop['target']} | "
            f"{hop['general_mechanism']} | {hop['instance_status']} | {evidence} |"
        )
    out += ["", "## Accepted conversation-decision reconciliation", ""]
    for decision in c["conversation_decisions"]:
        behaviors = ", ".join(decision["behavior_refs"]) or "none"
        deltas = ", ".join(decision["methodology_delta_refs"]) or "none"
        out.append(
            f"- {decision['id']} [{decision['status']}]: {decision['summary']} "
            f"(behaviors: {behaviors}; methodology deltas: {deltas}; "
            f"durable: {decision['durable_reference']})"
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


def select_behaviors(c, behavior_ids):
    errors = validate_contract(c)
    if errors:
        raise ValueError("invalid parity contract: " + "; ".join(errors))

    requested = tuple(dict.fromkeys(behavior_ids))
    if not requested:
        raise ValueError("at least one exact behavior id is required")

    behaviors = {item["id"]: item for item in c["behaviors"]}
    unknown = [behavior_id for behavior_id in requested if behavior_id not in behaviors]
    if unknown:
        raise ValueError(f"unknown parity behavior id(s): {', '.join(unknown)}")

    obligations = {item["id"]: item for item in c["source_obligations"]}
    selected = []
    for behavior_id in requested:
        behavior = behaviors[behavior_id]
        source_refs = [
            {
                "obligation_id": obligation_id,
                "source_path": obligations[obligation_id]["source_path"],
                "anchor": obligations[obligation_id]["anchor"],
                "kind": obligations[obligation_id]["kind"],
            }
            for obligation_id in behavior["covers"]
        ]
        selected.append(
            {
                "behavior": {
                    key: behavior[key]
                    for key in (
                        "id",
                        "title",
                        "owner",
                        "trigger",
                        "expected_behavior",
                        "must_not",
                        "jit_inputs",
                        "invalidation",
                        "machinery_state",
                        "execution_mode",
                        "closure_status",
                    )
                },
                "canonical_source_refs": source_refs,
            }
        )

    return {
        "schema_version": 1,
        "authority_role": c["runtime_usage"]["authority_role"],
        "retrieval_policy": c["runtime_usage"]["retrieval_policy"],
        "selection_rule": c["runtime_usage"]["selection_rule"],
        "canonical_source_required": True,
        "selected_behavior_ids": list(requested),
        "selections": selected,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--select-behavior", action="append", default=[])
    args = ap.parse_args()
    if args.select_behavior and (args.write or args.check):
        ap.error("--select-behavior cannot be combined with --write or --check")
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
    if args.select_behavior:
        try:
            selection = select_behaviors(c, args.select_behavior)
        except ValueError as exc:
            print(f"FAIL: {exc}", file=sys.stderr)
            return 1
        print(json.dumps(selection, sort_keys=True))
        return 0
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
