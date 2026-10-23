import unittest
from cinema_catharsis.acoustic_review import new_reviews,review_candidate,latest_review

class AcousticReviewTests(unittest.TestCase):
    def test_review_and_revision_preserve_history(self):
        store=new_reviews()
        review_candidate(store,work_id="work-1",report_ref="report.json",decision="uncertain")
        review_candidate(store,work_id="work-1",report_ref="report.json",decision="confirmed",note="manual comparison")
        self.assertEqual(len(store["decisions"]),2)
        self.assertEqual(latest_review(store,"work-1","report.json")["decision"],"confirmed")
        self.assertEqual(store["decisions"][0]["decision"],"uncertain")

    def test_rejection_and_no_review(self):
        store=new_reviews()
        self.assertIsNone(latest_review(store,"a","b"))
        review_candidate(store,work_id="a",report_ref="b",decision="rejected")
        self.assertEqual(latest_review(store,"a","b")["decision"],"rejected")

    def test_invalid_decision(self):
        with self.assertRaises(ValueError):
            review_candidate(new_reviews(),work_id="a",report_ref="b",decision="auto_approved")
