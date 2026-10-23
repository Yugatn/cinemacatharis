"""Versioned, provenance-aware observations. No automatic safety verdicts."""
from math import isfinite

SCHEMA = "evidence-1.0"
CHANNELS = frozenset({"text", "image", "video", "audio", "ocr"})
TIMING = frozenset({"source_media", "capture_wall_clock", "text_offsets", "unknown"})

def normalize_observation(item):
    if not isinstance(item, dict):
        raise ValueError("Observation must be an object")
    category = item.get("category")
    channel = item.get("channel")
    if not isinstance(category, str) or not category.strip() or len(category) > 100:
        raise ValueError("Invalid category")
    if channel not in CHANNELS:
        raise ValueError("Unsupported channel")
    basis = item.get("timing_basis", "unknown")
    if basis not in TIMING:
        raise ValueError("Unsupported timing basis")
    confidence = item.get("confidence")
    if confidence is not None and (isinstance(confidence, bool) or
            not isinstance(confidence, (int, float)) or not isfinite(confidence) or
            not 0 <= confidence <= 1):
        raise ValueError("Invalid confidence")
    start, end = item.get("start"), item.get("end")
    if (start is None) != (end is None):
        raise ValueError("Both boundaries are required")
    if start is not None and (type(start) is not int or type(end) is not int or
            start < 0 or end <= start):
        raise ValueError("Invalid boundaries")
    if basis == "text_offsets" and channel != "text":
        raise ValueError("Text offsets require text channel")
    if basis == "text_offsets" and start is None:
        raise ValueError("Text offsets required")
    if basis == "unknown" and start is not None:
        raise ValueError("Unknown timeline cannot carry boundaries")
    return {
        "category": category.strip(), "channel": channel,
        "timing_basis": basis, "start": start, "end": end,
        "confidence": confidence, "confidence_calibrated": item.get("confidence_calibrated") is True,
        "verified": item.get("verified") is True,
        "method": str(item.get("method", "unspecified"))[:120],
        "evidence": str(item.get("evidence", ""))[:500],
        "interpretation": "observed_candidate_not_intent_or_harm",
    }

def evidence_report(observations, *, source, coverage="unknown"):
    if not isinstance(source, str) or not source.strip():
        raise ValueError("Source required")
    if coverage not in ("unknown", "sampled", "partial", "continuous_review"):
        raise ValueError("Invalid coverage")
    rows = [normalize_observation(item) for item in observations]
    return {
        "schema_version": SCHEMA, "source": source, "coverage": coverage,
        "observations": rows, "observation_count": len(rows),
        "content_safe": None, "promotion_detected": None,
        "limitations": [
            "Detected presence does not establish endorsement, promotion or harm",
            "No observations is not proof of absence",
            "Confidence scores are not probabilities unless calibrated",
            "Do not combine capture-clock times with source-media times",
        ],
    }

def from_scan_capture(report):
    if not isinstance(report, dict) or report.get("schema_version") != "scan-1.0":
        raise ValueError("Expected scan-1.0")
    rows = []
    for finding in report.get("findings", []):
        if not isinstance(finding, dict):
            raise ValueError("Invalid finding")
        start, end = finding.get("start_ms"), finding.get("end_ms")
        rows.append({
            "category": finding.get("category"),
            "channel": {"visual": "image"}.get(finding.get("channel", "image"), finding.get("channel", "image")),
            "timing_basis": "capture_wall_clock",
            "start": start, "end": end,
            "confidence": finding.get("confidence"),
            "verified": finding.get("verified") is True,
            "method": "scan_capture",
            "evidence": finding.get("evidence", ""),
        })
    transcript = report.get("transcript")
    if transcript is not None:
        if not isinstance(transcript, dict) or not isinstance(transcript.get("segments"), list):
            raise ValueError("Invalid transcript")
        for segment in transcript["segments"]:
            if not isinstance(segment, dict):
                raise ValueError("Invalid transcript segment")
            start, end = segment.get("start_ms"), segment.get("end_ms")
            if type(start) is not int or type(end) is not int or start < 0 or end <= start:
                raise ValueError("Invalid transcript timing")
            rows.append({
                "category": "speech_transcription", "channel": "audio",
                "timing_basis": "unknown", "confidence": None,
                "method": "faster_whisper_unverified",
                "evidence": segment.get("text", ""),
            })
    result = evidence_report(rows, source="screen_capture", coverage="sampled")
    if transcript is not None:
        result["limitations"].append("Speech transcription timestamps refer to the separate audio recording; alignment with capture wall clock is unknown")
    result["frames_examined"] = report.get("frames_examined", 0)
    return result
