# Browser report viewer — no command line for report review

Open `web/report.html` in a modern browser, select a `scan-1.0` JSON report produced by `cinema-catharsis-scan`, and review findings and transcript. Export CSV for Google Sheets, HTML for Google Docs, or the original JSON. Everything runs locally in the browser; there are no network requests or credentials.

This is a **viewer/exporter**, not a model runner. It does not automatically scan video files, send files to Google, or authorize monetization. CSV downloads may require browser permission for multiple files. For native XLSX with four worksheets, use the Python exporter `cinema-catharsis-export`.

Security: user content is rendered as text, not HTML; CSV strings beginning with spreadsheet formula characters are escaped. Avoid opening untrusted generated HTML outside this tool. Report size is limited to 20 MB in the browser.

Future integration: add a local desktop wrapper or authenticated localhost service to run the optional models behind this browser UI; add Google OAuth for direct upload only with explicit user authorization.
