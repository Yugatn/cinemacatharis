# Unified evidence contract v1

The Python module `cinema_catharsis.evidence` provides a common observation schema for text, image, video, audio and OCR. This is **normalization**, not multimodal inference.

Each observation records category, channel, timeline basis, optional integer interval, confidence, calibration status, verification state, method and a short evidence excerpt. Time boundaries must be interpreted in their own basis: original video milliseconds, screen capture wall-clock milliseconds, or text character offsets. These bases **must never be summed together**.

`evidence_report(observations, source="...", coverage="sampled")` returns a JSON-serializable report without claiming the content is safe. `from_scan_capture(scan_report)` adapts the existing `scan-1.0` frame detector results and explicitly labels them as sampled capture-clock observations.

Future integrations: normalize transcript text, browser lexical matches and OCR observations; introduce source identifiers, independent reviewer decisions and evidence redaction before enabling any remote synchronization. There is no automatic content blocking or hidden behavioral scoring.

A missing observation is not a negative finding. Uncalibrated confidence must not be interpreted as a probability.
