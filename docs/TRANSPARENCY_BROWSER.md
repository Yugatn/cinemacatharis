# Cinema Catharsis — transparent content browser architecture

## Product contract
The project is a **content transparency layer**, not a censor or a tool for assigning psychological diagnoses. Its job is to show **what was observed**, by channel (text, visual, audio, video, OCR), with timestamps, provenance, confidence/validation, coverage and unknown intervals. Parents may set family preferences; adult users retain choice and can inspect and challenge findings. Presence of a substance, conflict or political viewpoint does not imply endorsement or intent to manipulate.

## Working prototypes
- `web/composition.html`: mobile/desktop responsive, local pasted-text lexical analysis.
- `extension/`: optional Chromium Manifest V3 extension, user-initiated analysis of visible text in the current tab. No broad host permissions, network calls, monitoring, blocking or browsing history storage.
- `web/family.html`: family link launcher; not an enforceable browser sandbox.
- Existing local video-analysis modules and report exports are separate.

Install desktop Chromium prototype: visit `chrome://extensions`, enable Developer mode, select Load unpacked, choose `extension/`. Chrome internal pages, browser stores and other protected pages cannot be analyzed. This prototype is not published in an extension store. It has not undergone independent security review.

## Cross-platform strategy
**Desktop (Windows, macOS, Linux):** Chromium/Firefox extensions, then optional dedicated browser shell after security review. An extension cannot guarantee observation of all content or prevent bypass.
**Android:** responsive web app first; a browser shell or Android extension-capable browser later, with permissions and platform-specific testing.
**iOS/iPadOS:** responsive web app first; Safari Web Extension or WKWebView app later, subject to platform restrictions. A desktop Chromium extension is not an iOS extension.
**Family controls:** explicit opt-in, parent-managed preferences and OS-level parental controls when needed; never imply a web page can enforce device-wide restrictions.

## Composition engine roadmap
1. Separate observed presence from interpretation (promotion, criticism, documentary, fiction, persuasion).
2. Define a transparent, versioned multilingual taxonomy; include positive and neutral categories, not just risk.
3. Align original-media timestamps across visual, OCR, ASR and text channels; preserve unknown regions.
4. Train and calibrate on diverse consented annotated datasets. Measure per-category precision, recall, calibration, false positives and disparities.
5. Explain individual evidence snippets with review/appeal, configurable thresholds and user-owned local export.
6. Default to no remote transmission of children's browsing or transcripts. Never monetize user behavioral profiles.

## Important limits
The current lexical detector counts **dictionary occurrences**, not content duration or semantic meaning. Its counts are not percentages of harmful content. It cannot establish a site's overall composition, infer psychological effects, or expose hidden motivations. Browser extension and web app are not a fully secure browser; automatic all-media analysis is a future goal.
