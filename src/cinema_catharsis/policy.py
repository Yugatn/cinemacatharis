"""Explainable pre-upload policy evaluation; annotations are supplied by humans or external detectors."""
from dataclasses import dataclass, asdict
from typing import Mapping
import json

CATEGORIES = frozenset({"alcohol", "tobacco", "nicotine", "violence", "other"})
CONTEXTS = frozenset({"promotion", "neutral", "critical", "educational", "documentary", "fictional", "unknown"})
CHANNELS = frozenset({"visual", "speech", "text", "audio", "metadata"})
POLICY_VERSION = "0.2.0"

@dataclass(frozen=True)
class Finding:
    category: str
    context: str
    start_ms: int
    end_ms: int
    confidence: float
    evidence: str
    channel: str = "visual"
    commercial_signal: bool = False
    verified: bool = False

    def __post_init__(self):
        if self.category not in CATEGORIES or self.context not in CONTEXTS:
            raise ValueError("Unsupported category or context")
        if self.channel not in CHANNELS:
            raise ValueError("Unsupported channel")
        if not isinstance(self.start_ms, int) or not isinstance(self.end_ms, int) or self.start_ms < 0 or self.end_ms <= self.start_ms:
            raise ValueError("Invalid millisecond interval")
        if not isinstance(self.confidence, (int, float)) or not 0 <= self.confidence <= 1:
            raise ValueError("Invalid confidence")
        if not isinstance(self.evidence, str) or not self.evidence.strip() or len(self.evidence) > 2000:
            raise ValueError("Evidence must be nonempty and <= 2000 chars")

def evaluate(findings: list[Finding], policy: Mapping | None = None) -> dict:
    """No automatic ban. Verified explicit commercial promotion may restrict monetization."""
    settings = {"min_confidence": 0.85, "restricted_categories": ["alcohol", "tobacco", "nicotine"]}
    if policy:
        settings.update(policy)
    threshold = settings["min_confidence"]
    if not isinstance(threshold, (int,float)) or not 0 <= threshold <= 1:
        raise ValueError("Invalid threshold")
    restricted = set(settings["restricted_categories"])
    if not restricted.issubset(CATEGORIES):
        raise ValueError("Unknown restricted category")
    flags = []
    review = False
    restricted_evidence = False
    for i, f in enumerate(findings):
        if f.category not in restricted:
            continue
        if f.context == "promotion" and f.commercial_signal:
            if f.verified and f.confidence >= threshold:
                restricted_evidence = True
                status = "verified_commercial_promotion"
            else:
                review = True
                status = "needs_human_review"
        elif f.context == "unknown":
            review = True
            status = "unclear_context"
        else:
            continue
        flags.append({"finding_index": i, "category": f.category, "start_ms": f.start_ms,
                      "end_ms": f.end_ms, "status": status, "evidence": f.evidence})
    monetization = "ineligible" if restricted_evidence else ("pending_review" if review else "eligible_under_this_policy")
    return {"policy_version": POLICY_VERSION, "publication": "not_restricted_by_this_policy",
            "monetization": monetization, "appeal_available": True,
            "explanation": "Only verified commercial promotion triggers ineligibility; depiction alone does not.",
            "flags": flags}

def analyze_document(document: dict) -> dict:
    """Versioned JSON contract for host integration; does not inspect media bytes."""
    if not isinstance(document, dict) or document.get("schema_version") != "1.0":
        raise ValueError("Expected schema_version 1.0")
    items = document.get("findings")
    if not isinstance(items, list) or len(items) > 10000:
        raise ValueError("findings must be a list of at most 10000 items")
    findings = [Finding(**item) for item in items]
    result = evaluate(findings, document.get("policy"))
    result["asset_id"] = document.get("asset_id")
    result["finding_count"] = len(findings)
    return result
