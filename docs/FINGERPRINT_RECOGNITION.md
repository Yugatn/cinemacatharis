# Shazam-inspired recognition architecture

## Separate identification from interpretation

1. **Exact recognition (implemented):** SHA-256 of a local file identifies identical bytes. `fingerprints.py` stores only a digest and explicit report references in a caller-managed index. It does not upload media or infer content. Transcoding, trimming or recording a soundtrack again will change the digest.
2. **Robust audio recognition (research, not implemented):** optional Chromaprint/AcoustID-compatible acoustic fingerprints, local comparison, and explicit thresholds. Chromaprint is designed for audio identification, but it is not a complete Shazam service and cannot determine psychological impact or commercial intent. Check third-party licenses and data-sharing consent before integrating external databases.
3. **Visual recognition (research):** perceptual image hashes for sampled frames, with collision checks and human verification. A similar frame does not prove that the same complete work was viewed.
4. **Analysis (partially implemented):** lexical evidence, sampled image detections, optional speech transcription, and future OCR. Store separate timing bases and coverage; never silently combine source-media and capture clocks.
5. **Report reuse (planned):** show previously reviewed evidence with its model version, provenance, coverage and date; clearly label stale or incomplete analyses. Never reuse a content safety verdict based solely on a fingerprint.

## Privacy and misuse boundaries

Prefer local indexing, opt-in sharing, no microphone or screen capture without user consent, no automatic surveillance, and no automatic blocking. Do not collect or upload recordings merely to identify media. Exact matching is not robust fingerprinting.

## Example (Python)

```python
from cinema_catharsis.fingerprints import add_exact, identify_exact
index = add_exact("sample.mp4", "reports/sample-evidence.json")
print(identify_exact("sample.mp4", index))
```

The matching reference is an index pointer, not a verified fact about the media.
