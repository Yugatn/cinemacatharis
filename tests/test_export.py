import csv
import json
import tempfile
import unittest
from pathlib import Path
from xml.etree import ElementTree
from zipfile import ZipFile
from cinema_catharsis.export import export_csv, export_xlsx, export_html, safe_cell

REPORT = {"schema_version":"scan-1.0", "source":"screen_capture",
          "frames_examined":2, "frames_available":3,
          "assessment":{"monetization":"pending_review"},
          "findings":[{"category":"alcohol", "context":"unknown",
                       "evidence":"=HYPERLINK(\"https://example.test\")"}],
          "transcript":{"segments":[{"start_ms":0,"end_ms":100,"text":"Привет"}]},
          "limitations":["Short scenes may be missed"]}

class ExportTests(unittest.TestCase):
    def test_formula_injection(self):
        self.assertTrue(safe_cell("=1+1").startswith("'"))
        self.assertEqual(safe_cell("normal"), "normal")

    def test_csv(self):
        with tempfile.TemporaryDirectory() as directory:
            paths = export_csv(REPORT, directory)
            self.assertEqual(len(paths), 4)
            with (Path(directory)/"findings.csv").open(encoding="utf-8-sig",newline="") as file:
                rows = list(csv.reader(file))
            self.assertTrue(rows[1][-1].startswith("'="))

    def test_xlsx_structure(self):
        with tempfile.TemporaryDirectory() as directory:
            path = export_xlsx(REPORT, Path(directory)/"report.xlsx")
            with ZipFile(path) as archive:
                self.assertIsNone(archive.testzip())
                ElementTree.fromstring(archive.read("xl/workbook.xml"))
                xml = archive.read("xl/worksheets/sheet3.xml")
                self.assertIn("Привет".encode(), xml)

    def test_html_escaped(self):
        with tempfile.TemporaryDirectory() as directory:
            path = export_html({"findings":[{"evidence":"<script>"}]}, Path(directory)/"report.html")
            self.assertNotIn("<script>", path.read_text())

if __name__ == "__main__":
    unittest.main()
