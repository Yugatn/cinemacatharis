import unittest
from cinema_catharsis.policy import Finding, evaluate, analyze_document

def finding(**kwargs):
    base = dict(category="alcohol", context="promotion", start_ms=0, end_ms=1000,
                confidence=0.95, evidence="Explicit paid endorsement",
                commercial_signal=True, verified=True)
    base.update(kwargs)
    return Finding(**base)

class PolicyTests(unittest.TestCase):
    def test_verified_promotion(self):
        result = evaluate([finding()])
        self.assertEqual(result["monetization"], "ineligible")
        self.assertEqual(result["publication"], "not_restricted_by_this_policy")

    def test_documentary_not_penalized(self):
        self.assertEqual(evaluate([finding(context="documentary")])["monetization"], "eligible_under_this_policy")

    def test_unverified_requires_review(self):
        self.assertEqual(evaluate([finding(verified=False)])["monetization"], "pending_review")

    def test_unknown_requires_review(self):
        self.assertEqual(evaluate([finding(context="unknown")])["monetization"], "pending_review")

    def test_invalid_interval(self):
        with self.assertRaises(ValueError):
            finding(end_ms=0)

    def test_contract(self):
        doc = {"schema_version":"1.0", "asset_id":"x", "findings":[]}
        self.assertEqual(analyze_document(doc)["asset_id"], "x")

if __name__ == "__main__":
    unittest.main()
