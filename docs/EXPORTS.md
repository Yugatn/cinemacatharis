# Export results to Excel, Google Sheets and Google Docs

Run `cinema-catharsis-export report.json --output-dir exported`.

The exporter produces:
- `cinema_catharsis.xlsx`: Excel workbook with Summary, Findings, Transcript and Limitations tabs.
- `summary.csv`, `findings.csv`, `transcript.csv`, `limitations.csv`: UTF-8 BOM files for Google Sheets import (**File → Import → Upload**), or Excel.
- `cinema_catharsis.html`: formatted report to open in a browser, then copy into Google Docs or upload via Google Drive as a document.

**No automatic cloud upload is performed.** Direct writing into a user's Google Drive, Sheets or Docs requires separate Google OAuth consent and a connected API integration. The files are generated locally, without sending private video/transcripts to third parties.

The XLSX exporter is a minimal Office Open XML implementation using the Python standard library; cells are stored as text to preserve annotations and avoid spreadsheet formula execution. This means numeric columns may need conversion in Excel/Sheets before statistical analysis. Untrusted text is prefixed to reduce formula injection risks in CSV/Excel. Exports do not establish accuracy or verification of AI findings.
