import unittest
from cinema_catharsis.composition import Segment, compose, exclusive_timeline

class CompositionTests(unittest.TestCase):
    def test_overlap_multilabel_and_unknown(self):
        result = compose(10000, [(0,5000)], [
            Segment(0,3000,("alcohol",)), Segment(2000,4000,("alcohol","tobacco"))])
        self.assertEqual(result["coverage_fraction"], .5)
        self.assertEqual(result["categories"]["alcohol"]["observed_ms"], 4000)
        self.assertEqual(result["categories"]["tobacco"]["observed_ms"], 2000)
        self.assertEqual(result["categories"]["alcohol"]["possible_fraction_range"], [.4,.9])

    def test_no_coverage_not_zero_content(self):
        result = compose(1000, [], [])
        self.assertEqual(result["unknown_ms"],1000)
        self.assertEqual(result["coverage_fraction"],0)

    def test_exclusive_priority(self):
        result = exclusive_timeline(1000,[(0,500)],[
            Segment(0,400,("alcohol",)),Segment(200,500,("tobacco",))],["tobacco","alcohol"])
        self.assertEqual(result["exclusive_ms"],{"alcohol":200,"tobacco":300,"unknown":500})

    def test_reject_out_of_bounds(self):
        with self.assertRaises(ValueError):
            compose(1000,[(0,2000)],[])

    def test_reject_nan(self):
        with self.assertRaises(ValueError):
            Segment(0,10,("alcohol",),float("nan"))
