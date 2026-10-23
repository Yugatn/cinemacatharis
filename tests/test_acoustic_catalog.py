import unittest
from cinema_catharsis.acoustic_catalog import new_catalog,add_record,find_candidates

def fp(values):
    return {"schema_version":"acoustic-raw-1.0","values":values}

class AcousticCatalogTests(unittest.TestCase):
    def test_rank_and_link_reports(self):
        pattern=[(i*1234567)&0xffffffff for i in range(32)]
        catalog=new_catalog()
        add_record(catalog,work_id="work-a",report_ref="reports/a.json",fingerprint=fp(pattern))
        add_record(catalog,work_id="work-b",report_ref="reports/b.json",fingerprint=fp([0xffffffff]*32))
        result=find_candidates(fp([0]*5+pattern),catalog,min_overlap=20,max_shift=8)
        self.assertEqual(result["candidates"][0]["work_id"],"work-a")
        self.assertEqual(result["candidates"][0]["report_ref"],"reports/a.json")
        self.assertFalse(result["candidates"][0]["verified"])
        self.assertEqual(result["candidates"][0]["status"],"candidate_requires_review")

    def test_duplicate_work_id_rejected(self):
        catalog=new_catalog()
        add_record(catalog,work_id="a",report_ref="a.json",fingerprint=fp([1]*20))
        with self.assertRaises(ValueError):
            add_record(catalog,work_id="a",report_ref="b.json",fingerprint=fp([2]*20))

    def test_no_short_matches(self):
        catalog=new_catalog()
        add_record(catalog,work_id="a",report_ref="a.json",fingerprint=fp([1,2]))
        self.assertEqual(find_candidates(fp([1,2]),catalog)["candidates"],[])
