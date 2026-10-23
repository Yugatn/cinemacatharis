# Accuracy validation and source-media timeline — v0.8

## Why source timestamps matter
At ×10 screen playback, a second of captured wall-clock time can represent approximately ten seconds of film, but buffering, seeking, frame drops and audio acceleration break this mapping. The source-video sampler uses FFmpeg seeking at known media timestamps. It does **not** claim continuous inspection: between extracted frames, content remains unknown.

Use `sample_source_video("movie.mp4", "samples", every_seconds=5)` from Python to extract frames with original-media timestamps. FFmpeg and ffprobe must be installed. No video is uploaded.

## Quantifying detector accuracy
The `calibration_report` function accepts pairs of `{"score":0.83,"truth":true}` from an **independent, human-verified** reference set and returns:
- Precision: TP / (TP + FP), or undefined if no positive predictions.
- Recall: TP / (TP + FN), or undefined if no ground-truth positives.
- F1: harmonic mean when defined.
- Brier score: mean squared difference between score and binary truth.
- ECE: bin-weighted absolute gap between average confidence and observed frequency.

These are descriptive evaluation statistics, **not** proof of generalization. Report per-category and per-context scores, number of videos, train/test separation by film, annotator agreement, confidence intervals and domain shift. Zero-shot CLIP similarity is not inherently calibrated probability.

## Integration status
Source frame extraction and calibration statistics are implemented as standalone modules. The screen-capture pipeline still uses wall-clock timestamps and is **not** automatically aligned to source time. No measured model accuracy is available until a representative labeled evaluation dataset is supplied.
