import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from cinema_catharsis.acoustic import acoustic_fingerprint, exact_acoustic_match

class AcousticTests(unittest.TestCase):
    def test_extract_parses_fpcalc_json(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"audio.wav"
            p.write_bytes(b"sample")
            class Result:
                returncode=0
                stdout=json.dumps({"fingerprint":"abc","duration":12})
            with patch("cinema_catharsis.acoustic.shutil.which",return_value="/usr/bin/fpcalc"), patch(
                "cinema_catharsis.acoustic.subprocess.run",return_value=Result()) as runner:
                r=acoustic_fingerprint(p)
            self.assertEqual(r["fingerprint"],"abc")
            self.assertFalse(r["match_verified"])
            self.assertIn("-json",runner.call_args.args[0])

    def test_requires_fpcalc(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"a.wav"
            p.write_bytes(b"sample")
            with patch("cinema_catharsis.acoustic.shutil.which",return_value=None):
                with self.assertRaises(RuntimeError):
                    acoustic_fingerprint(p)

    def test_exact_match_not_similarity(self):
        a={"algorithm":"chromaprint-fpcalc","fingerprint":"abc","duration_seconds":5}
        self.assertTrue(exact_acoustic_match(a,dict(a)))
        self.assertFalse(exact_acoustic_match(a,{**a,"fingerprint":"abd"}))
