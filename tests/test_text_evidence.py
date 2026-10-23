import unittest
from cinema_catharsis.text_evidence import from_lexical_report

class TextEvidenceTests(unittest.TestCase):
    def test_offsets(self):
        result = from_lexical_report({"schema_version":"lexical-composition-1.1",
            "categories":{"alcohol":{"examples":[{"start":4,"end":8,"term":"вино","excerpt":"про вино"}]}}})
        item=result["observations"][0]
        self.assertEqual(item["timing_basis"],"text_offsets")
        self.assertEqual((item["start"],item["end"]),(4,8))
        self.assertIsNone(result["content_safe"])

    def test_old_format_skipped(self):
        result=from_lexical_report({"schema_version":"lexical-composition-1.0",
            "categories":{"alcohol":{"examples":[{"token_index":1,"term":"вино"}]}}})
        self.assertEqual(result["observation_count"],0)

    def test_bad_schema(self):
        with self.assertRaises(ValueError):
            from_lexical_report({"schema_version":"unknown"})
