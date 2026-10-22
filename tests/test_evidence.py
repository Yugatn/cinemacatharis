import unittest
from cinema_catharsis.evidence import evidence_report, from_scan_capture

class EvidenceTests(unittest.TestCase):
    def test_mixed_channels_preserve_time_bases(self):
        r=evidence_report([
            {"category":"alcohol","channel":"image","timing_basis":"source_media","start":100,"end":200},
            {"category":"alcohol","channel":"text","timing_basis":"text_offsets","start":3,"end":10},
        ],source="sample.mp4",coverage="partial")
        self.assertEqual(r["observation_count"],2)
        self.assertIsNone(r["content_safe"])
        self.assertNotEqual(r["observations"][0]["timing_basis"],r["observations"][1]["timing_basis"])

    def test_invalid_confidence(self):
        with self.assertRaises(ValueError):
            evidence_report([{"category":"x","channel":"audio","confidence":float("nan")}],source="test")

    def test_scan_adapter(self):
        r=from_scan_capture({"schema_version":"scan-1.0","frames_examined":2,
            "findings":[{"category":"tobacco_nicotine","channel":"image","start_ms":500,"end_ms":501,"confidence":0.6}]})
        self.assertEqual(r["coverage"],"sampled")
        self.assertEqual(r["observations"][0]["timing_basis"],"capture_wall_clock")
        self.assertFalse(r["observations"][0]["verified"])

    def test_no_false_negative(self):
        r=evidence_report([],source="empty",coverage="unknown")
        self.assertIsNone(r["content_safe"])
        self.assertIsNone(r["promotion_detected"])
