# Cinema Catharsis — development progress

**Measurement date:** 2026-10-23. **Status:** prototype, not production-ready.

## How percentages are calculated
These are **engineering planning estimates**, not measured reliability or AI classification accuracy. Each workstream has a fixed share of the release scope. The completed fraction within each workstream is a conservative qualitative estimate based on code present in the branch. The total is the sum of weighted completion. Do not treat an implemented feature as verified until CI, manual tests, security review and user trials are complete.

| Workstream | Weight | Estimated completion | Contribution |
|---|---:|---:|---:|
| Transparent taxonomy, composition and uncertainty metrics | 20% | 60% | 12% |
| Text and browser extension prototype | 15% | 55% | 8.25% |
| Image, audio and video pipeline integration | 20% | 40% | 8% |
| Desktop and mobile application distribution | 15% | 15% | 2.25% |
| Parent preferences, privacy and family experience | 15% | 20% | 3% |
| Testing, security, calibration and accessibility | 15% | 15% | 2.25% |
| **Overall estimated readiness** | **100%** | | **35.75%** |

## Milestones
- [x] Content composition with coverage and unknown intervals (research implementation).
- [x] Browser-based manual text composition tool.
- [x] Desktop Chromium extension prototype with on-demand active-tab text extraction.
- [x] Local source-media timestamp sampler and calibration formulas.
- [x] Family link launcher prototype.
- [x] Initial lexical-engine unit tests and CI workflow committed.
- [ ] Verify CI runs and fix failures.
- [x] Add common evidence normalization schema and screen-capture adapter (integration foundation only).\n- [x] Add lexical-to-evidence adapter for reports with explicit character offsets.\n- [x] Upgrade web and Chromium lexical engines to lexical-composition-1.1 with text offsets and excerpts; tests committed.\n- [ ] Connect all text, image, audio, OCR and video detectors to the common schema and review UI.
- [ ] Independently validate classifiers with representative annotated data.
- [ ] Build installable desktop and mobile browser applications.
- [ ] Complete security, accessibility, performance and child-privacy audits.

**Important:** 35.75% is an estimated share of a defined MVP scope, not a promise of safety, an accuracy percentage, or a guarantee of delivery.
