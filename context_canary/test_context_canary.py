import json
import unittest
import context_canary as cc

class ContextCanaryTests(unittest.TestCase):
    def payload_with_expected_answers(self, seed=cc.DEFAULT_SEED):
        payload = cc.emit_payload(seed)
        expected = {t.id: t.expected for t in cc.build_suite(seed)}
        for item in payload["tests"]:
            value = expected[item["id"]]
            if isinstance(value, dict):
                item["response"] = json.dumps(value, separators=(",", ":"))
            elif item["id"] == "RT-02":
                item["response"] = "0.05"
            elif isinstance(value, (list, tuple)):
                item["response"] = " ".join(value)
            else:
                item["response"] = str(value)
        return payload

    def test_perfect_run_is_green(self):
        run = cc.score_payload(self.payload_with_expected_answers(), "test-model")
        self.assertEqual(run["status"], "GREEN")
        self.assertEqual(run["score"]["percent"], 100.0)

    def test_single_failure_is_not_red(self):
        payload = self.payload_with_expected_answers()
        payload["tests"][0]["response"] = "CANARY_OK extra"
        run = cc.score_payload(payload, "test-model")
        self.assertNotEqual(run["status"], "RED")
        self.assertFalse(run["results"][0]["passed"])

    def test_baseline_delta(self):
        baseline = cc.score_payload(self.payload_with_expected_answers(), "test-model")
        current_payload = self.payload_with_expected_answers()
        for item in current_payload["tests"][:8]:
            item["response"] = "WRONG"
        current = cc.score_payload(current_payload, "test-model")
        cc.apply_baseline(current, baseline)
        self.assertLess(current["delta_vs_baseline"], 0)

    def test_handoff_requires_two_red_and_baseline_drop(self):
        baseline = cc.score_payload(self.payload_with_expected_answers(), "test-model")
        bad_payload = self.payload_with_expected_answers()
        for item in bad_payload["tests"][:12]:
            item["response"] = "WRONG"
        red1 = cc.score_payload(bad_payload, "test-model")
        cc.apply_baseline(red1, baseline)
        red2 = cc.score_payload(bad_payload, "test-model")
        cc.apply_baseline(red2, baseline)
        self.assertEqual(red1["status"], "RED")
        self.assertFalse(cc.decide_handoff(red1, [])["recommend_handoff"])
        self.assertTrue(cc.decide_handoff(red2, [red1])["recommend_handoff"])

    def test_seed_replays_matrioshka_exactly(self):
        self.assertEqual(cc.build_suite(12345), cc.build_suite(12345))

    def test_different_seed_changes_only_matrioshka_case(self):
        a = {t.id: t for t in cc.build_suite(1)}
        b = {t.id: t for t in cc.build_suite(2)}
        changed = [k for k in a if a[k] != b[k]]
        self.assertEqual(changed, ["MX-01"])

    def test_suite_mismatch_stops(self):
        payload = self.payload_with_expected_answers()
        payload["tests"].pop()
        with self.assertRaises(RuntimeError):
            cc.score_payload(payload, "test-model")

    def test_baseline_model_mismatch_stops(self):
        base = cc.score_payload(self.payload_with_expected_answers(), "model-a")
        run = cc.score_payload(self.payload_with_expected_answers(), "model-b")
        with self.assertRaises(RuntimeError):
            cc.apply_baseline(run, base)

if __name__ == "__main__":
    unittest.main()
