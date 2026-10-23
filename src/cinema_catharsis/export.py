"""Portable scan report exports: Excel XLSX, Google Sheets CSV, Google Docs HTML."""
import csv
import html
import io
import json
from pathlib import Path
from xml.sax.saxutils import escape
from zipfile import ZipFile, ZIP_DEFLATED

SHEETS = ("Summary", "Findings", "Transcript", "Limitations")

def safe_cell(value):
    """Prevent spreadsheet formula injection in untrusted model/user text."""
    if value is None:
        return ""
    value = str(value)
    if value.lstrip().startswith(("=", "+", "-", "@")) or value.startswith(("\t", "\r", "\n")):
        return "'" + value
    return value

def report_tables(report):
    if not isinstance(report, dict):
        raise ValueError("Expected report object")
    assessment = report.get("assessment") or {}
    summary = [
        ["Field", "Value"],
        ["Schema", report.get("schema_version", "")],
        ["Source", report.get("source", "")],
        ["Timing basis", report.get("timing_basis", "")],
        ["Frames examined", report.get("frames_examined", 0)],
        ["Frames available", report.get("frames_available", 0)],
        ["Monetization", assessment.get("monetization", "not_assessed")],
        ["Publication", assessment.get("publication", "not_assessed")],
        ["Policy version", assessment.get("policy_version", "")],
        ["Explanation", assessment.get("explanation", "")],
    ]
    findings = [["Category", "Context", "Start ms", "End ms", "Confidence",
                 "Channel", "Commercial signal", "Verified", "Evidence"]]
    for f in report.get("findings", []):
        findings.append([f.get(k, "") for k in (
            "category", "context", "start_ms", "end_ms", "confidence",
            "channel", "commercial_signal", "verified", "evidence")])
    transcript = [["Start ms", "End ms", "Text"]]
    for s in (report.get("transcript") or {}).get("segments", []):
        transcript.append([s.get("start_ms", ""), s.get("end_ms", ""), s.get("text", "")])
    limitations = [["Limitation"]] + [[x] for x in report.get("limitations", [])]
    return dict(zip(SHEETS, (summary, findings, transcript, limitations)))

def export_csv(report, folder):
    """UTF-8 BOM CSV files import into Excel or Google Sheets."""
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    paths = []
    for name, rows in report_tables(report).items():
        path = folder / (name.lower() + ".csv")
        with path.open("w", encoding="utf-8-sig", newline="") as file:
            writer = csv.writer(file)
            writer.writerows([[safe_cell(v) for v in row] for row in rows])
        paths.append(path)
    return paths

def _col(index):
    name = ""
    while index:
        index, rem = divmod(index - 1, 26)
        name = chr(65 + rem) + name
    return name

def _worksheet(rows):
    lines = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
             '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">',
             '<sheetViews><sheetView workbookViewId="0"/></sheetViews><sheetData>']
    for i, row in enumerate(rows, 1):
        cells = []
        for j, value in enumerate(row, 1):
            ref = f"{_col(j)}{i}"
            value = safe_cell(value)
            cells.append(f'<c r="{ref}" t="inlineStr"><is><t xml:space="preserve">{escape(value)}</t></is></c>')
        lines.append(f'<row r="{i}">' + "".join(cells) + '</row>')
    lines.append('</sheetData></worksheet>')
    return "".join(lines)

def export_xlsx(report, output):
    """Write a dependency-free, basic Office Open XML workbook with four tabs."""
    tables = report_tables(report)
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    workbook = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets>' + "".join(
        f'<sheet name="{name}" sheetId="{i}" r:id="rId{i}"/>' for i, name in enumerate(tables, 1)) + '</sheets></workbook>'
    relationships = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">' + "".join(
        f'<Relationship Id="rId{i}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet{i}.xml"/>' for i in range(1, len(tables)+1)) + '</Relationships>'
    types = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>' + "".join(
        f'<Override PartName="/xl/worksheets/sheet{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>' for i in range(1, len(tables)+1)) + '</Types>'
    root_rels = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/></Relationships>'
    with ZipFile(output, "w", ZIP_DEFLATED) as archive:
        archive.writestr("[Content_Types].xml", types)
        archive.writestr("_rels/.rels", root_rels)
        archive.writestr("xl/workbook.xml", workbook)
        archive.writestr("xl/_rels/workbook.xml.rels", relationships)
        for i, rows in enumerate(tables.values(), 1):
            archive.writestr(f"xl/worksheets/sheet{i}.xml", _worksheet(rows))
    return output

def export_html(report, output):
    """Self-contained document readable in browsers and pasteable into Google Docs."""
    sections = []
    for name, rows in report_tables(report).items():
        head, *body = rows
        columns = "".join("<th>" + html.escape(str(x)) + "</th>" for x in head)
        cells = "".join("<tr>" + "".join("<td>" + html.escape(str(v)) + "</td>" for v in row) + "</tr>" for row in body)
        sections.append("<h2>" + html.escape(name) + "</h2><table><thead><tr>" + columns + "</tr></thead><tbody>" + cells + "</tbody></table>")
    document = '<!doctype html><html lang="ru"><meta charset="utf-8"><title>Cinema Catharsis report</title><style>body{font:14px system-ui;margin:32px}table{border-collapse:collapse;width:100%;margin-bottom:24px}td,th{border:1px solid #aaa;padding:7px;text-align:left;overflow-wrap:anywhere}th{background:#e8edf3}</style><h1>Cinema Catharsis — отчёт</h1><p>Автоматические наблюдения не являются подтверждённым решением о монетизации.</p>' + "".join(sections) + "</html>"
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(document, encoding="utf-8")
    return output

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Export scan report for Excel, Sheets and Docs")
    parser.add_argument("report", help="scan JSON report")
    parser.add_argument("--output-dir", default="cinema_report")
    args = parser.parse_args()
    report = json.loads(Path(args.report).read_text(encoding="utf-8"))
    directory = Path(args.output_dir)
    export_xlsx(report, directory / "cinema_catharsis.xlsx")
    export_csv(report, directory)
    export_html(report, directory / "cinema_catharsis.html")
    print("Exports written to", directory)
if __name__ == "__main__":
    main()
