import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from cinema_catharsis.scan_capture import scan_capture

class ScanTests(unittest.TestCase):
    def test_empty_scan_is_not_approval(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "capture_manifest.json"
            p.write_text(json.dumps({"schema_version":"capture-1.0", "frames":[]}))
            report = scan_capture(str(p))
            self.assertEqual(report["assessment"]["monetization"], "not_assessed")

    @patch("cinema_catharsis.scan_capture.inspect_frames")
    def test_detected_sample_requires_review(self, detector):
        detector.return_value = [{"category":"alcohol", "context":"unknown",
            "start_ms":0, "end_ms":1000, "confidence":0.8, "evidence":"CLIP",
            "channel":"visual", "commercial_signal":False, "verified":False}]
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "capture_manifest.json"
            p.write_text(json.dumps({"schema_version":"capture-1.0",
                "frames":[{"file":"frame_00000.jpg", "wall_ms":12345}]}))
            report = scan_capture(str(p), vision=True)
            self.assertEqual(report["findings"][0]["start_ms"], 12345)
            self.assertEqual(report["assessment"]["monetization"], "pending_review")

    def test_reject_path_traversal(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "capture_manifest.json"
            p.write_text(json.dumps({"schema_version":"capture-1.0",
                "frames":[{"file":"../private.jpg", "wall_ms":0}]}))
            with self.assertRaises(ValueError):
                scan_capture(str(p))
