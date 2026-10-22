"""Descriptive exposure metrics; no causal or clinical claims."""
from dataclasses import dataclass
from math import sqrt
from typing import Iterable

@dataclass(frozen=True)
class Exposure:
    start_frame: int
    end_frame: int
    fps_num: int
    fps_den: int = 1
    category: str = "unspecified"
    prominence: float = 1.0

    def __post_init__(self):
        if self.start_frame < 0 or self.end_frame <= self.start_frame:
            raise ValueError("Require nonnegative start and end > start")
        if self.fps_num <= 0 or self.fps_den <= 0:
            raise ValueError("Frame rate must be positive")
        if not 0 <= self.prominence <= 1:
            raise ValueError("Prominence must be between 0 and 1")

    @property
    def duration_seconds(self) -> float:
        return (self.end_frame - self.start_frame) * self.fps_den / self.fps_num

def summarize(events: Iterable[Exposure]) -> dict:
    """Aggregate overlapping intervals by category without double-counting time.
    A prominence-weighted sum is a descriptive annotation, not an effect score.
    """
    groups = {}
    for e in events:
        key = (e.category, e.fps_num, e.fps_den)
        groups.setdefault(key, []).append(e)
    output = {}
    for (category, num, den), rows in groups.items():
        intervals = sorted((e.start_frame, e.end_frame) for e in rows)
        merged = []
        for start, end in intervals:
            if merged and start <= merged[-1][1]:
                merged[-1] = (merged[-1][0], max(end, merged[-1][1]))
            else:
                merged.append((start, end))
        unique = sum(b-a for a,b in merged) * den / num
        weighted = sum(e.duration_seconds * e.prominence for e in rows)
        output.setdefault(category, []).append({
            "fps_num": num, "fps_den": den, "event_count": len(rows),
            "unique_exposure_seconds": unique,
            "annotation_weighted_seconds": weighted,
            "note": "Weighted seconds may double-count overlaps; not a behavioral effect."
        })
    return output

def wilson_interval(successes: int, trials: int, z: float = 1.96) -> tuple[float,float]:
    """Wilson score interval for an observed binary response proportion."""
    if trials <= 0 or not 0 <= successes <= trials or z <= 0:
        raise ValueError("Invalid successes, trials, or z")
    p = successes / trials
    d = 1 + z*z/trials
    c = (p + z*z/(2*trials)) / d
    h = z * sqrt(p*(1-p)/trials + z*z/(4*trials*trials)) / d
    return max(0.,c-h), min(1.,c+h)
