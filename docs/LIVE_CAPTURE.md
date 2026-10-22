# Live Capture / Accelerated Scan — experimental browser mode

Open `web/capture.html` in a browser that supports `getDisplayMedia` (preferably served from localhost or HTTPS). Select a tab/window/screen, optionally share audio, play the video, then stop and export the frame manifest, sampled JPEGs and optional audio recording. **The capture is local; no video is uploaded to Cinema Catharsis.**

## Scope and honesty
- Browser screen capture samples the **displayed** frames, not every source frame. Playback at 10× does not provide 10× semantic processing capacity.
- Wall-clock capture timestamps are not source-media timestamps. Seek, buffering, dropped frames and playback speed make a simple mapping unreliable.
- Audio capture is browser/platform dependent and can be missing or unintelligible at high speed. Do not infer absence of dialogue from an absent audio track.
- The exported manifest deliberately reports `content_classification: not_assessed`. Frames and audio are **evidence for a later detector or human review**, not proof that any particular topic is present or absent.
- Protected streams/DRM and site permissions may block recording. Respect copyright, privacy, consent and platform terms.
- Avoid scanning private conversations or personal data without permission.

## Future production architecture
Use a controlled playback source or extension with media-time events to align samples to source timestamps. Use an adaptive sampler (scene-change detection + periodic coverage), asynchronous OCR/object detection, ASR with time stretching rather than merely sped-up audio, deduplication and calibrated multilingual contextual classifiers. Attach evidence with confidence, detector version, media hash, coverage metrics and human review state. In production, send *verified* findings to the policy API, never use an empty detection list as proof of safe content.

## Known limitations
This is a browser demonstration, not a real-time semantic scanner, a single ZIP exporter or an automatically integrated host plugin. Exporting many individual files may trigger download permission prompts or browser download throttling. Limit frame count and capture only material you are entitled to process.
