# Cinema Catharsis — release quality gates

The product must distinguish a transparent informational aid from a proven child-safety control.

## Evidence contract
Every detection should carry category, modality, original timestamp or text offset, source reference, method version, confidence calibration status, coverage status, and human verification state. Absence of detections is never evidence of absence without adequate coverage.

## Acceptance criteria
1. The same content gives equivalent annotations on desktop and mobile when using the same detector version and settings.
2. Cross-language false positives, sarcasm, negation, quoted criticism and educational contexts are tested separately.
3. Promotion is not inferred solely from the presence of alcohol, nicotine, violence or gambling.
4. Every displayed percentage states its denominator and unknown fraction.
5. Parents can inspect why a category was assigned; adult users can opt out without blocking access.
6. Child data remains local by default, with clear retention and deletion controls.
7. Browser extension permissions are minimal; no silent browsing history capture.
8. Accessibility, battery impact, crash recovery and offline use are tested on supported devices.
9. Model performance is reported using independent annotated media, per category and platform.
10. Security review and passing automated tests are required before any family-safety claim.

## Planned product packages
- Shared analysis library with versioned output schema.
- Browser extension for desktop, explicitly invoked.
- Mobile-friendly web interface.
- Optional native desktop and mobile browsers with navigation and media permissions independently reviewed.

## Release status
The existing prototypes are not certified parental-control tools. Automated testing and independent detector validation have not yet been demonstrated.
