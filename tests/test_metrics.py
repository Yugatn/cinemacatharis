import unittest
from cinema_catharsis.metrics import Exposure, summarize, wilson_interval

class MetricsTests(unittest.TestCase):
    def test_overlap(self):
        events = [Exposure(0, 30, 30, category="tobacco"),
                  Exposure(15, 45, 30, category="tobacco")]
        result = summarize(events)["tobacco"][0]
        self.assertAlmostEqual(result["unique_exposure_seconds"], 1.5)
        self.assertEqual(result["event_count"], 2)

    def test_fractional_fps(self):
        self.assertAlmostEqual(Exposure(0, 30000, 30000, 1001).duration_seconds, 1001)

    def test_validation(self):
        with self.assertRaises(ValueError):
            Exposure(4, 4, 30)
        with self.assertRaises(ValueError):
            wilson_interval(2, 1)

    def test_wilson(self):
        low, high = wilson_interval(5, 10)
        self.assertLess(low, 0.5)
        self.assertGreater(high, 0.5)

if __name__ == "__main__":
    unittest.main()
