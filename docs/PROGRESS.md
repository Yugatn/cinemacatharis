# Cinema Catharsis — development progress

**Measurement date:** 2026-10-23. **Status:** prototype, not production-ready.

## How percentages are calculated
These are **engineering planning estimates**, not measured reliability or AI classification accuracy. Each workstream has a fixed share of the release scope. The completed fraction within each workstream is a conservative qualitative estimate based on code present in the branch. The total is the sum of weighted completion. Do not treat an implemented feature as verified until CI, manual tests, security review and user trials are complete.

| Workstream | Weight | Estimated completion | Contribution |
|---|---:|---:|---:|
| Transparent taxonomy, composition and uncertainty metrics | 20% | 65% | 13% |
| Text and browser extension prototype | 15% | 70% | 10.5% |
| Image, audio and video pipeline integration | 20% | 73% | 14.6% |
| Desktop and mobile application distribution | 15% | 15% | 2.25% |
| Parent preferences, privacy and family experience | 15% | 20% | 3% |
| Testing, security, calibration and accessibility | 15% | 35% | 5.25% |
| **Overall estimated readiness** | **100%** | | **48.6%** |

## Milestones
- [x] Content composition with coverage and unknown intervals (research implementation).
- [x] Browser-based manual text composition tool.
- [x] Desktop Chromium extension prototype with on-demand active-tab text extraction.
- [x] Local source-media timestamp sampler and calibration formulas.
- [x] Family link launcher prototype.
- [x] Initial lexical-engine unit tests and CI workflow committed.
- [x] Verify GitHub Actions browser lexical and Python test workflows passed on commit d53d266a6511d163ed252f4694ac6120610172fe.
- [x] Verify browser and Python workflows passed for commit 0510b3e2b349d960ded886748cd82b84abde6208.
- [x] Verify CI passed on report-viewer commit b056bdbac1d040fe713f12c159de3c799eb50957.
- [x] Verify CI passed on commit 786795f7abf67d4575818a78cc6bbffe1f88a202.
- [x] Verify Python and browser workflows passed on commit ff66d3170cf3ff0f8c20d128bdd9954d5591049f.
- [x] Verify both workflows passed on commit 9bdfc8489c1b6352493dc45e23360920066394da.
- [ ] Verify CI for acoustic catalog changes.
- [x] Add common evidence normalization schema and screen-capture adapter (integration foundation only).
- [x] Add lexical-to-evidence adapter for reports with explicit character offsets.
- [x] Upgrade web and Chromium lexical engines to lexical-composition-1.1 with text offsets and excerpts; tests committed.
- [x] Show source excerpts and character offsets in the responsive browser text report.
- [x] Integrate browser lexical output with local evidence-1.0 conversion and JSON export.
- [x] Enable local report viewer to open evidence-1.0 observations from any channel (read-only display).
- [x] Normalize visual detector channel and preserve unaligned speech transcription as audio evidence in capture adapter.
- [x] Add --evidence-output to capture CLI to export combined image and audio evidence-1.0 for local report viewer.
- [x] Implement privacy-preserving exact-byte media fingerprint index and unit tests (not robust audio matching).
- [x] Implement optional offline Chromaprint fingerprint extraction and strict equality baseline; unit tests added.
- [x] Prototype offset-aware raw Chromaprint bit-agreement comparison and synthetic unit tests (uncalibrated).
- [x] Add local acoustic candidate catalog linking similarity rankings to report references without automatic identity claims.
- [ ] Validate acoustic matching on transformed real recordings and calibrate thresholds.
- [ ] Integrate live OCR and video classification; capture export currently requires optional local ML dependencies.
- [ ] Independently validate classifiers with representative annotated data.
- [ ] Build installable desktop and mobile browser applications.
- [ ] Complete security, accessibility, performance and child-privacy audits.

**Important:** 48.6% is an estimated share of a defined MVP scope, not a promise of safety, an accuracy percentage, or a guarantee of delivery.
