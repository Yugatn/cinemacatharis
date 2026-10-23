"""Time-resolved content composition with explicit unknown coverage.

All intervals use the original media timeline in milliseconds. A sample-only
screen capture must not be passed off as full-duration coverage.
"""
from collections import defaultdict
from dataclasses import dataclass
from math import isfinite

@dataclass(frozen=True)
class Segment:
    start_ms: int
    end_ms: int
    labels: tuple[str, ...]
    confidence: float = 1.0
    prominence: float = 1.0

    def __post_init__(self):
        if type(self.start_ms) is not int or type(self.end_ms) is not int:
            raise ValueError("Intervals must use integer milliseconds")
        if self.start_ms < 0 or self.end_ms <= self.start_ms:
            raise ValueError("Invalid interval")
        if not isinstance(self.labels, tuple) or not self.labels or any(
                not isinstance(label, str) or not label.strip() for label in self.labels):
            raise ValueError("Expected nonempty label tuple")
        for value in (self.confidence, self.prominence):
            if isinstance(value, bool) or not isinstance(value, (int, float)) or not isfinite(value) or not 0 <= value <= 1:
                raise ValueError("Confidence and prominence must be finite within [0,1]")

def _union_ms(intervals):
    intervals = sorted(intervals)
    if not intervals:
        return 0
    start, end = intervals[0]
    total = 0
    for a, b in intervals[1:]:
        if a <= end:
            end = max(end, b)
        else:
            total += end - start
            start, end = a, b
    return total + end - start

def _intersections(a, b):
    return [(max(x, y), min(u, v)) for x, u in a for y, v in b if max(x, y) < min(u, v)]

def compose(duration_ms: int, coverage: list[tuple[int, int]], segments: list[Segment]) -> dict:
    """Measure multi-label composition without falsely treating unseen time as negative.

    Coverage means intervals examined *continuously* by an adequate detector
    or reviewer; sampled frames do not justify extending coverage between them.
    """
    if type(duration_ms) is not int or duration_ms <= 0:
        raise ValueError("duration_ms must be positive integer")
    for start, end in coverage:
        if type(start) is not int or type(end) is not int or not 0 <= start < end <= duration_ms:
            raise ValueError("Invalid coverage interval")
    for segment in segments:
        if segment.end_ms > duration_ms:
            raise ValueError("Segment exceeds media duration")
    coverage_ms = _union_ms(coverage)
    categories = defaultdict(list)
    for segment in segments:
        for label in set(segment.labels):
            categories[label].append((segment.start_ms, segment.end_ms))
    output = {}
    for label, intervals in sorted(categories.items()):
        observed_ms = _union_ms(_intersections(intervals, coverage))
        # Upper bound is conservative: anything outside coverage could contain this label.
        upper_ms = min(duration_ms, observed_ms + duration_ms - coverage_ms)
        output[label] = {
            "observed_ms": observed_ms,
            "observed_fraction_of_total": observed_ms / duration_ms,
            "observed_fraction_of_covered": observed_ms / coverage_ms if coverage_ms else None,
            "possible_fraction_range": [observed_ms / duration_ms, upper_ms / duration_ms],
            "interpretation": "Observed label duration; bounds assume no false detections inside coverage."
        }
    return {
        "duration_ms": duration_ms,
        "coverage_ms": coverage_ms,
        "coverage_fraction": coverage_ms / duration_ms,
        "unknown_ms": duration_ms - coverage_ms,
        "categories": output,
        "multi_label": True,
        "note": "Category fractions may sum above 1. Confidence scores are not calibrated probabilities. Unseen time is unknown, not negative."
    }

def exclusive_timeline(duration_ms: int, coverage: list[tuple[int,int]],
                       segments: list[Segment], priority: list[str]) -> dict:
    """Optional exclusive breakdown: one priority label per instant, plus other/unknown."""
    if len(priority) != len(set(priority)):
        raise ValueError("Priority labels must be unique")
    base = compose(duration_ms, coverage, segments)
    points = {0, duration_ms}
    for a,b in coverage:
        points.update((a,b))
    for s in segments:
        points.update((s.start_ms,s.end_ms))
    ordered = sorted(points)
    durations = defaultdict(int)
    for a,b in zip(ordered,ordered[1:]):
        if not any(x <= a and b <= y for x,y in coverage):
            # Union of adjacent/overlapping coverage intervals is checked by midpoint.
            mid = (a+b)/2
            if not any(x <= mid < y for x,y in coverage):
                durations["unknown"] += b-a
                continue
        active = {label for s in segments if s.start_ms < b and s.end_ms > a for label in s.labels}
        label = next((label for label in priority if label in active), "other")
        durations[label] += b-a
    base["exclusive_ms"] = dict(durations)
    base["priority"] = priority
    return base
