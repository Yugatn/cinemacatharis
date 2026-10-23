import unittest
from cinema_catharsis.calibration import calibration_report

class CalibrationTests(unittest.TestCase):
    def test_perfect(self):
        r=calibration_report([{"score":1.0,"truth":True},{"score":0.0,"truth":False}])
        self.assertEqual(r["precision"],1.0)
        self.assertEqual(r["recall"],1.0)
        self.assertEqual(r["brier"],0.0)
        self.assertEqual(r["ece"],0.0)

    def test_empty(self):
        self.assertEqual(calibration_report([])["status"],"insufficient_data")

    def test_reject_unverified_truth(self):
        with self.assertRaises(ValueError):
            calibration_report([{"score":0.7,"truth":1}])
