# Cinema Catharsis Family — mobile-first concept and prototype

## Implemented
The `web/family.html` page is responsive and usable on mobile browsers. It provides a **parent-curated HTTPS link launcher** with local device storage, accessible 44px controls, safe text rendering, a clear reset action, and no telemetry or accounts. It links to the existing report viewer. Open the page via HTTPS hosting; file:// localStorage behavior may differ between browsers.

## Not yet a protected browser
This is **not** an iOS/Android browser engine, device-wide filter, safe-search enforcement, PIN-protected parental control, VPN/DNS filter or guaranteed child-safe environment. Once an external link opens, the destination can navigate elsewhere; children can also open other apps or browsers. No live website classification, blocking or remote monitoring is implemented. Parents should use Apple Screen Time / Android Family Link or equivalent device controls as additional layers.

## Proposed production roadmap
1. Mobile PWA with offline shell, explicit consent and no unnecessary trackers. Do not cache private media by default.
2. Family policy profiles: parent-controlled, age-appropriate recommendations (not medical diagnoses), per-category preferences, transparent overrides, expiry, and review.
3. Optional on-device classifier for images/text and contextual video/audio analysis. Unknown or low-confidence results must be surfaced as unknown rather than 'safe'.
4. Native Android WebView and iOS WKWebView wrappers for navigation policy enforcement, only after platform-specific security review. WebView interception is limited; device-wide protection requires OS-managed controls.
5. Google Sheets/Docs export through separately authorized OAuth integration; no automatic uploading of minors' browsing histories or transcripts.
6. Threat modeling, privacy review, accessibility tests, mobile performance and battery benchmarking, independent age-appropriate content evaluation, and child safety impact assessment.

## Safety principles
No advertising profiles for children, no sale of browsing data, no covert monitoring, minimal retention, no behavioral manipulation, parental transparency, right to delete, explainable warnings, human appeal and clear unknown classifications. Do not infer that mere depiction of alcohol or smoking equals promotion.
