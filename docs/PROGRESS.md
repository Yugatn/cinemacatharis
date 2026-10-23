# Cinema Catharsis — development progress

**Measurement date:** 2026-10-23. **Status:** prototype, not production-ready.

## How percentages are calculated
These are **engineering planning estimates**, not measured reliability or AI classification accuracy. Each workstream has a fixed share of the release scope. The completed fraction within each workstream is a conservative qualitative estimate based on code present in the branch. The total is the sum of weighted completion. Do not treat an implemented feature as verified until CI, manual tests, security review and user trials are complete.

| Workstream | Weight | Estimated completion | Contribution |
|---|---:|---:|---:|
| Transparent taxonomy, composition and uncertainty metrics | 20% | 65% | 13% |
| Text and browser extension prototype | 15% | 70% | 10.5% |
| Image, audio and video pipeline integration | 20% | 50% | 10% |
| Desktop and mobile application distribution | 15% | 15% | 2.25% |
| Parent preferences, privacy and family experience | 15% | 20% | 3% |
| Testing, security, calibration and accessibility | 15% | 30% | 4.5% |
| **Overall estimated readiness** | **100%** | | **43.25%** |

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
- [ ] Verify CI after visual/audio evidence adapter changes.
- [x] Add common evidence normalization schema and screen-capture adapter (integration foundation only).
- [x] Add lexical-to-evidence adapter for reports with explicit character offsets.
- [x] Upgrade web and Chromium lexical engines to lexical-composition-1.1 with text offsets and excerpts; tests committed.
- [x] Show source excerpts and character offsets in the responsive browser text report.
- [x] Integrate browser lexical output with local evidence-1.0 conversion and JSON export.
- [x] Enable local report viewer to open evidence-1.0 observations from any channel (read-only display).
- [x] Normalize visual detector channel and preserve unaligned speech transcription as audio evidence in capture adapter.
- [ ] Connect live image, audio, OCR and video detectors to the common browser review UI.
- [ ] Independently validate classifiers with representative annotated data.
- [ ] Build installable desktop and mobile browser applications.
- [ ] Complete security, accessibility, performance and child-privacy audits.

**Important:** 43.25% is an estimated share of a defined MVP scope, not a promise of safety, an accuracy percentage, or a guarantee of delivery.
