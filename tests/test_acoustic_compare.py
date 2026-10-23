import unittest
from cinema_catharsis.acoustic_compare import compare_raw

def record(values):
    return {"schema_version":"acoustic-raw-1.0","values":values}

class AcousticCompareTests(unittest.TestCase):
    def test_offset_recognition(self):
        pattern=[i*314159 & 0xffffffff for i in range(32)]
        a=record([0xffffffff]*8+pattern)
        b=record(pattern+[0]*5)
        result=compare_raw(a,b,min_overlap=24,max_shift=12)
        self.assertEqual(result["score"],1)
        self.assertEqual(result["shift_frames"],8)
        self.assertFalse(result["verified"])

    def test_nonmatch_is_not_verdict(self):
        result=compare_raw(record([0]*24),record([0xffffffff]*24))
        self.assertEqual(result["score"],0)
        self.assertFalse(result["verified"])

    def test_short_audio_no_match(self):
        result=compare_raw(record([1,2]),record([1,2]))
        self.assertIsNone(result["shift_frames"])

    def test_invalid_data_rejected(self):
        with self.assertRaises(ValueError):
            compare_raw(record([True]*20),record([1]*20))
