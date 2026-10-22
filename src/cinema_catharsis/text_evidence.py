"""Convert lexical composition findings to the common evidence format."""
from .evidence import evidence_report

def from_lexical_report(report, *, source="provided_text"):
    if not isinstance(report, dict) or report.get("schema_version") not in ("lexical-composition-1.0", "lexical-composition-1.1"):
        raise ValueError("Unsupported lexical report")
    observations = []
    for category, data in report.get("categories", {}).items():
        for match in data.get("examples", []):
            start, end = match.get("start"), match.get("end")
            if type(start) is not int or type(end) is not int or start < 0 or end <= start:
                # Older reports only have token index, not character offsets.
                continue
            observations.append({
                "category": category, "channel": "text", "timing_basis": "text_offsets",
                "start": start, "end": end, "confidence": None,
                "confidence_calibrated": False, "verified": False,
                "method": "lexical_dictionary",
                "evidence": match.get("excerpt", match.get("term", "")),
            })
    result = evidence_report(observations, source=source, coverage="partial")
    result["limitations"].append("Only first ten matches per category are retained by the lexical report")
    result["limitations"].append("Lexical occurrence is not semantic interpretation")
    return result
