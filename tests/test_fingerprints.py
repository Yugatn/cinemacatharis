import tempfile
import unittest
from pathlib import Path
from cinema_catharsis.fingerprints import add_exact, identify_exact, file_digest

class FingerprintTests(unittest.TestCase):
    def test_identical_media_reuses_report(self):
        with tempfile.TemporaryDirectory() as directory:
            a=Path(directory)/"a.bin"
            b=Path(directory)/"b.bin"
            a.write_bytes(b"same media")
            b.write_bytes(b"same media")
            index=add_exact(a,"reports/a.json")
            self.assertEqual(identify_exact(b,index),["reports/a.json"])
            self.assertEqual(file_digest(a),file_digest(b))

    def test_changed_bytes_do_not_false_match(self):
        with tempfile.TemporaryDirectory() as directory:
            a=Path(directory)/"a.bin"
            a.write_bytes(b"original")
            index=add_exact(a,"report.json")
            a.write_bytes(b"modified")
            self.assertEqual(identify_exact(a,index),[])

    def test_invalid_index_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            a=Path(directory)/"a.bin"
            a.write_bytes(b"x")
            with self.assertRaises(ValueError):
                identify_exact(a,{"entries":{}})
