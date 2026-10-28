"""Generate four review views and supporting inventories from the one derived register."""

import csv
import json
from pathlib import Path

from validate_register import validate

ROOT = Path(__file__).parent


def views(d):
    js = {x["id"]: x for x in d["journeys"]}
    v = {}
    v["01_components"] = (
        [
            "Component ID",
            "Name",
            "Purpose",
            "Owner",
            "Runtime observation",
            "Installed identity",
            "Next observation",
            "Source refs",
        ],
        [
            [
                x["id"],
                x["name"],
                x["purpose"],
                x["owner"],
                x["runtime_state"],
                x["installed_identity"] or "UNKNOWN",
                x["next_observation"],
                ", ".join(x["source_refs"]),
            ]
            for x in d["components"]
        ],
    )
    v["02_outcomes"] = (
        [
            "Case ID",
            "Journey",
            "Type",
            "Stimulus",
            "Expected independent observation",
            "Existing test links",
            "Environment",
            "Run status",
            "Binding gap",
            "Owner",
            "Source refs",
        ],
        [
            [
                x["id"],
                js[x["journey_id"]]["name"],
                x["kind"],
                x["stimulus"],
                x["expected"],
                ", ".join(x["existing_test_ids"]) or "UNMAPPED",
                x["initial_environment_id"],
                x["run_status"],
                x["prerequisite"],
                ", ".join(js[x["journey_id"]]["owners"]),
                ", ".join(x["source_refs"]),
            ]
            for x in d["cases"]
        ],
    )
    v["03_adoption"] = (
        [
            "Finding ID",
            "Finding",
            "Journey",
            "Owner",
            "Disposition",
            "Source stage",
            "Runtime stage",
            "Next action",
            "Evidence refs",
        ],
        [
            [
                x["id"],
                x["title"],
                ", ".join(x["journey_ids"]),
                x["owner"],
                x["status"],
                x["source_stage"],
                x["runtime_stage"],
                x["next_action"],
                ", ".join(x["evidence_refs"]),
            ]
            for x in d["adoption"]
        ],
    )
    v["04_lean"] = (
        [
            "Control ID",
            "Subject",
            "Measurement",
            "Protection to retain",
            "Journey",
            "Baseline",
            "Savings",
            "Disposition",
            "Retirement",
        ],
        [
            [
                x["id"],
                x["subject"],
                x["measurement"],
                x["protection"],
                ", ".join(x["journey_ids"]),
                "NOT_MEASURED" if x["baseline"] is None else x["baseline"],
                "NOT_MEASURED" if x["savings"] is None else x["savings"],
                x["status"],
                x["retirement_decision"],
            ]
            for x in d["lean"]
        ],
    )
    v["existing_tests"] = (
        [
            "Test ID",
            "Repository",
            "Path",
            "Symbol",
            "Commit",
            "Blob",
            "Source state",
            "This packet execution",
            "Historical scope",
            "Source / pilot refs",
        ],
        [
            [
                x["id"],
                x["repository"],
                x["path"],
                x["symbol"],
                x["source_commit"],
                x["git_blob"],
                x["source_state"],
                x["execution_this_packet"],
                x["historical_evidence_scope"],
                ", ".join(filter(None, [x["source_ref"], x.get("execution_evidence_ref")])),
            ]
            for x in d["existing_tests"]
        ],
    )
    v["boundaries"] = (
        ["Boundary ID", "Producer", "Consumer", "Meaning", "Journeys", "Coverage"],
        [[x["id"], x["producer"], x["consumer"], x["name"], ", ".join(x["journey_ids"]), x["coverage"]] for x in d["boundaries"]],
    )
    v["sources"] = (
        ["Source ID", "Title", "Kind", "Source URL", "Git blob", "Observed date", "Retrieved text SHA256"],
        [
            [x["id"], x["title"], x["kind"], x["url"], x.get("git_blob", ""), x["observed_on"], x["retrieved_text_sha256"]]
            for x in d["sources"]
        ],
    )
    return v


def main():
    d = json.loads((ROOT / "data/register.json").read_text())
    errs = validate(d, ROOT)
    if errs:
        raise ValueError(errs)
    data = views(d)
    (ROOT / "views").mkdir(exist_ok=True)
    for name, (cols, rows) in data.items():
        with (ROOT / "views" / f"{name}.csv").open("w", newline="") as f:
            w = csv.writer(f)
            w.writerow(cols)
            w.writerows(rows)
    (ROOT / "views/workbook_data.json").write_text(
        json.dumps({k: dict(columns=c, rows=r) for k, (c, r) in data.items()}, indent=2) + "\n"
    )
    print(json.dumps({k: len(v[1]) for k, v in data.items()}))


if __name__ == "__main__":
    main()
