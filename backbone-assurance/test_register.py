import copy
import json
import tempfile
import unittest
from pathlib import Path

from validate_register import validate

ROOT = Path(__file__).parent


class RegisterChecks(unittest.TestCase):
    def setUp(self):
        self.d = json.loads((ROOT / "data/register.json").read_text())

    def rejects(self, fn):
        fn(self.d)
        self.assertTrue(validate(self.d))

    def test_baseline(self):
        self.assertEqual(validate(self.d, ROOT), [])

    def test_duplicate_case(self):
        self.rejects(lambda d: d["cases"].append(copy.deepcopy(d["cases"][0])))

    def test_missing_retention(self):
        self.rejects(lambda d: d["retention"].pop())

    def test_unknown_source(self):
        self.rejects(lambda d: d["cases"][0]["source_refs"].append("NOT_A_SOURCE"))

    def test_invented_test_symbol(self):
        self.rejects(lambda d: d["cases"][0]["existing_test_ids"].append("FAKE_TEST"))

    def test_fake_case_pass(self):
        self.rejects(lambda d: d["cases"][0].update(run_status="PASS"))

    def test_no_positive_path(self):
        self.rejects(
            lambda d: d.update(cases=[c for c in d["cases"] if not (c["journey_id"] == "J01" and c["kind"] == "positive")])
        )

    def test_missing_observable_oracle(self):
        self.rejects(lambda d: d["cases"][0].update(oracle=""))

    def test_unobserved_savings(self):
        self.rejects(lambda d: d["lean"][0].update(savings=0))

    def test_retirement_without_owner(self):
        self.rejects(lambda d: d["lean"][0].update(retirement_decision="RETIRE"))

    def test_source_test_credit_promotion(self):
        self.rejects(lambda d: d["existing_tests"][0].update(execution_this_packet="PASS"))

    def test_local_observation_without_pilot(self):
        self.rejects(
            lambda d: d["existing_tests"][0].update(
                execution_this_packet="LOCAL_FIXTURE_RUN_OBSERVED", execution_evidence_ref="MISSING"
            )
        )

    def test_pilot_scope_promotion(self):
        self.rejects(lambda d: d["pilot_observations"][0].update(scope="E2E"))

    def test_forged_positive_without_binding(self):
        self.rejects(lambda d: d["runs"].append({"id": "RUN1", "case_id": "J01-S01", "result": "PASS_REPORTED"}))

    def test_orphan_component(self):
        self.rejects(lambda d: d["components"].append(dict(d["components"][0], id="C99")))

    def test_legacy_journey_lost(self):
        self.rejects(lambda d: d["journeys"][0].update(legacy_id=None))

    def test_altered_baseline(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / self.d["retained_baseline"]["path"]
            p.parent.mkdir()
            p.write_text("changed")
            self.assertIn("baseline altered", validate(self.d, td))

    def test_reordering_does_not_break_keys(self):
        for k in ["cases", "journeys", "components", "existing_tests", "retention"]:
            self.d[k].reverse()
        self.assertEqual(validate(self.d, ROOT), [])

    def test_unaccepted_run_needs_evidence(self):
        self.rejects(lambda d: d["cases"][0].update(run_status="RECORDED_UNACCEPTED"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
