# Cinema Catharsis: optional local AI analysis of screen captures

This prototype can now **actually run** two optional model pipelines on an exported browser capture:
1. CLIP zero-shot image similarity for candidate alcohol/tobacco/vaping appearances.
2. Faster-Whisper automatic speech recognition on captured audio.

**Neither model is trained or calibrated for monetization decisions.** Image similarity is not a verified object detector; speech recognition is not evidence of persuasion. Findings are unverified, context is unknown, and the policy returns pending human review or not_assessed. A film with no detected candidates is **not** approved.

## Installation
Python 3.10+; capture images and manifest from `web/capture.html`. Use a local computer with adequate RAM, and allow model weights to download on first run.

```bash
python -m pip install -e '.[vision,speech]'
cinema-catharsis-scan path/to/capture_manifest.json --vision --audio path/to/captured_audio.webm --output report.json
```

For metadata-only report (no model downloads): `cinema-catharsis-scan path/to/capture_manifest.json`.

The capture manifest stores wall-clock timestamps. At ×10 playback, frame intervals are not equivalent to source video time; short scenes may be missed and ASR may fail. For reproducible results, use a controlled player with original media timestamps or scan the original file. Browser export of many frames may require multiple-download permission.

## Research and production requirements
Add a validated object detector and scene segmentation; OCR for labels; audio resampling/time-stretch and aligned ASR; multilingual contextual analysis; sampling coverage estimates; independent reviewer verification; false-positive and false-negative evaluation; audit and appeals. Never convert CLIP similarity into automatic censorship or monetization denial. Respect rights and privacy when capturing streams.
