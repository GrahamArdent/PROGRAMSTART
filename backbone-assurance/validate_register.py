"""Read-only structural checks for the audit reference. Never an authorization or test-success gate."""

import argparse
import gzip
import hashlib
import json
from pathlib import Path

GROUPS = [
    "sources",
    "components",
    "boundaries",
    "environments",
    "journeys",
    "cases",
    "existing_tests",
    "adoption",
    "lean",
    "compound_sequences",
    "retention",
    "runs",
    "execution_bindings",
    "pilot_observations",
]


def validate(d, root=None):
    errors = []

    def require(ok, msg):
        if not ok:
            errors.append(msg)

    indexes = {}
    for g in GROUPS:
        rows = d.get(g)
        require(isinstance(rows, list), f"{g}: missing list")
        rows = rows if isinstance(rows, list) else []
        ids = [x.get("id") for x in rows if isinstance(x, dict)]
        require(len(ids) == len(rows) and all(isinstance(x, str) and x for x in ids), f"{g}: invalid ID")
        require(len(ids) == len(set(ids)), f"{g}: duplicate ID")
        indexes[g] = {x["id"]: x for x in rows if isinstance(x, dict) and isinstance(x.get("id"), str)}

    def refs(vals, group, context):
        require(isinstance(vals, list), context + ": references must be a list")
        for v in vals if isinstance(vals, list) else []:
            require(v in indexes[group], context + ": unknown " + str(v))

    for g in ["components", "journeys", "cases", "lean"]:
        for x in d.get(g, []):
            refs(x.get("source_refs", []), "sources", g + "/" + x["id"])
    for x in d.get("boundaries", []):
        refs([x.get("producer"), x.get("consumer")], "components", x["id"])
        refs(x.get("journey_ids", []), "journeys", x["id"])
    for x in d.get("journeys", []):
        for f in ["outcome", "entry_boundary", "oracle_type", "prerequisite"]:
            require(bool(x.get(f)), x["id"] + ": missing " + f)
        refs(x.get("component_ids", []), "components", x["id"])
        refs(x.get("boundary_ids", []), "boundaries", x["id"])
        require(
            any(c.get("journey_id") == x["id"] and c.get("kind") == "positive" for c in d.get("cases", [])),
            x["id"] + ": no positive liveness case",
        )
        require(
            any(c.get("journey_id") == x["id"] and c.get("kind") != "positive" for c in d.get("cases", [])),
            x["id"] + ": no falsifier",
        )
    touched = set()
    for e in d.get("boundaries", []):
        touched.update([e.get("producer"), e.get("consumer")])
    for c in d.get("components", []):
        require(c["id"] in touched, c["id"] + ": no mapped boundary")
    for c in d.get("cases", []):
        refs([c.get("journey_id")], "journeys", c["id"])
        refs(c.get("boundary_ids", []), "boundaries", c["id"])
        refs([c.get("initial_environment_id")], "environments", c["id"])
        refs(c.get("existing_test_ids", []), "existing_tests", c["id"])
        for f in ["stimulus", "expected", "oracle", "prerequisite"]:
            require(bool(c.get(f)), c["id"] + ": missing " + f)
        require(bool(c.get("fault_axes")), c["id"] + ": no fault axis")
        require(c.get("run_status") in ["NOT_RUN", "RECORDED_UNACCEPTED"], c["id"] + ": invalid case result promotion")
        if c.get("run_status") != "NOT_RUN":
            require(any(r.get("case_id") == c["id"] for r in d.get("runs", [])), c["id"] + ": no run evidence")
        if c.get("existing_test_ids"):
            require(c.get("binding_status") == "PARTIAL_SOURCE_LINK", c["id"] + ": source link overclaim")
    for t in d.get("existing_tests", []):
        refs([t.get("source_ref"), t.get("historical_evidence_ref")], "sources", t["id"])
        state = t.get("execution_this_packet")
        require(state in ["NOT_RUN", "LOCAL_FIXTURE_RUN_OBSERVED"], t["id"] + ": imported execution credit")
        if state == "LOCAL_FIXTURE_RUN_OBSERVED":
            p = indexes["pilot_observations"].get(t.get("execution_evidence_ref"), {})
            require(
                p.get("scope") == "LOCAL_SOURCE_FIXTURE" and t["id"] in p.get("existing_test_ids", []),
                t["id"] + ": local observation lacks scoped pilot evidence",
            )
        require(bool(t.get("symbol")) and len(t.get("git_blob", "")) == 40, t["id"] + ": unpinned source")
    for p in d.get("pilot_observations", []):
        require(p.get("scope") == "LOCAL_SOURCE_FIXTURE", p["id"] + ": pilot scope overclaim")
        refs(p.get("existing_test_ids", []), "existing_tests", p["id"])
        require(p.get("owner_acceptance") == "NOT_ESTABLISHED", p["id"] + ": pilot owner overclaim")
        require(bool(p.get("results_path")) and len(p.get("results_sha256", "")) == 64, p["id"] + ": missing evidence identity")
        if root and p.get("results_path"):
            evidence = Path(root) / p["results_path"]
            require(evidence.is_file(), p["id"] + ": pilot evidence missing")
            if evidence.is_file():
                require(
                    hashlib.sha256(evidence.read_bytes()).hexdigest() == p.get("results_sha256"),
                    p["id"] + ": pilot evidence altered",
                )
    for x in d.get("adoption", []):
        refs(x.get("journey_ids", []), "journeys", x["id"])
        refs(x.get("evidence_refs", []), "sources", x["id"])
        require(bool(x.get("next_action")), x["id"] + ": missing next action")
    for x in d.get("lean", []):
        refs(x.get("journey_ids", []), "journeys", x["id"])
        if x.get("baseline") is None:
            require(x.get("savings") is None, x["id"] + ": invented saving without baseline")
        if x.get("retirement_decision") != "NOT_SELECTED":
            require(bool(x.get("owner_decision_ref")), x["id"] + ": retirement lacks owner decision")
    for x in d.get("compound_sequences", []):
        refs(x.get("journey_ids", []), "journeys", x["id"])
        require(len(x.get("journey_ids", [])) >= 2, x["id"] + ": compound needs interacting journeys")
    expected = set(d.get("required_retention_ids", []))
    require(expected == set(indexes["retention"]), "retention inventory mismatch")
    for x in d.get("retention", []):
        refs([x.get("source_ref")], "sources", x["id"])
        refs(x.get("targets", []), "adoption" if x.get("target_kind") == "finding" else "journeys", x["id"])
        require(bool(x.get("targets")) and bool(x.get("disposition")), x["id"] + ": missing disposition")
    legacy = {j.get("legacy_id") for j in d.get("journeys", []) if j.get("legacy_id")}
    require(legacy == set(d.get("required_legacy_journey_ids", [])), "original journey retention mismatch")
    for b in d.get("execution_bindings", []):
        refs([b.get("case_id")], "cases", b["id"])
        refs([b.get("environment_id")], "environments", b["id"])
        for k in [
            "callable_tool",
            "owner_admission_ref",
            "source_identity",
            "test_identity",
            "checker_identity",
            "isolation",
            "limits",
            "cleanup",
            "result_destination",
            "original_identity_rule",
        ]:
            require(bool(b.get(k)), b["id"] + ": missing " + k)
    for r in d.get("runs", []):
        refs([r.get("case_id")], "cases", r["id"])
        refs([r.get("execution_binding_id")], "execution_bindings", r["id"])
        require(r.get("result") in ["PASS_REPORTED", "FAIL", "INCONCLUSIVE", "BLOCKED", "SKIPPED"], "invalid run result")
        for k in [
            "source_identity",
            "test_identity",
            "environment_identity",
            "raw_log_ref",
            "raw_log_sha256",
            "started_at",
            "ended_at",
            "observed_oracle",
            "substituted_boundaries",
            "inventory_accounting",
        ]:
            require(k in r and r[k] is not None, r["id"] + ": missing " + k)
        if r.get("result") == "PASS_REPORTED":
            require(bool(r.get("independent_verifier_ref")), r["id"] + ": positive result lacks independent verifier")
        require(r.get("owner_acceptance") == "NOT_AUTOMATIC", r["id"] + ": local validation cannot grant owner acceptance")
    require(d.get("metadata", {}).get("runtime_passes_claimed") == 0, "packet must not claim runtime passes")
    require(d.get("metadata", {}).get("classification") == "NON_AUTHORITATIVE_REFERENCE", "unexpected authority promotion")
    if root:
        b = d.get("retained_baseline", {})
        p = Path(root) / b.get("path", "MISSING")
        require(p.is_file(), "baseline missing")
        if p.is_file():
            try:
                data = gzip.decompress(p.read_bytes()) if b.get("compression") == "gzip" else p.read_bytes()
            except OSError:
                data = b""
            require(len(data) == b.get("size_bytes") and hashlib.sha256(data).hexdigest() == b.get("sha256"), "baseline altered")
    return errors


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("path", nargs="?", default=str(Path(__file__).parent / "data/register.json"))
    a = ap.parse_args()
    path = Path(a.path)
    d = json.loads(path.read_text())
    errors = validate(d, path.parent.parent)
    print(
        json.dumps(
            {
                "result": "STRUCTURE_VALID_NOT_ACCEPTED" if not errors else "INVALID",
                "errors": errors,
                "limits": "No execution, owner authentication, semantic oracle or production authorization is established.",
            },
            indent=2,
        )
    )
    raise SystemExit(bool(errors))
