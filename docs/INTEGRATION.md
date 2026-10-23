# Cinema Catharsis — pre-upload integration v0.2

## Philosophy and scope
The viewer has a right to interpret; the creator has a right to depict difficult realities; a platform can transparently set advertising eligibility standards. **Depiction is not endorsement, exposure is not proof of harm, and monetization is distinct from publication.** No score is a judgment of a person. A flagged creator can inspect timestamps, correct annotations, and appeal to a human reviewer.

## Architecture
1. Client optionally runs preflight locally before publishing.
2. An upstream detector or human annotator emits timecoded findings from image, speech, subtitles, audio and metadata.
3. Normalize findings into JSON contract (example in `examples/preupload.json`).
4. Policy engine evaluates evidence and returns separate publication and monetization fields, reasons and timecodes.
5. Platform displays preview and appeal channel. The platform—not this package—implements final enforcement, consent, access control and audit trails.

## Run without external dependencies (Python 3.10+)
```sh
PYTHONPATH=src python -m unittest discover -s tests
PYTHONPATH=src python -m cinema_catharsis.cli examples/preupload.json
PYTHONPATH=src python -m cinema_catharsis.server
curl -X POST http://127.0.0.1:8765/v1/analyze -H 'Content-Type: application/json' --data-binary @examples/preupload.json
```

## JSON contract
Input: `schema_version: "1.0"`, optional `asset_id`, `findings: []`, optional `policy: {"min_confidence":0.85,"restricted_categories":["alcohol","tobacco","nicotine"]}`.
Each finding: `category`, `context`, `start_ms`, `end_ms`, `confidence`, `evidence`, `channel`, `commercial_signal`, `verified`.
Output: `publication`, `monetization` (`eligible_under_this_policy` / `pending_review` / `ineligible`), `flags`, `appeal_available`, `policy_version`.

## Rule semantics
Verified, high-confidence explicit commercial promotion in a configured restricted category is monetization-ineligible under the example policy. Suspected promotion or unknown context requires human review. Critical, educational, documentary, fictional and neutral depictions are not restricted merely for showing an object. Platform must independently determine compliance with law, contractual advertising rules and local jurisdiction.

## Not implemented
This release **does not read or classify raw video**, run speech recognition, detect brands, establish sponsorship, identify psychological influence, authenticate reviewers, host uploads, or securely serve the public internet. The HTTP server binds to localhost and is for local testing only. A production integration requires robust detectors, calibrated validation datasets, human review, privacy/security review, audit logs, queueing, TLS/auth, rate limits, regional policy and appeal procedures. Automated detector output should default to `verified:false` until independently reviewed.

## Suggested next work
Media decoding and frame sampling via FFmpeg; pluggable object detection, OCR and ASR; multilingual context classification with human adjudication; inter-annotator agreement; adversarial tests; accessibility and multilingual explanations; signed policy versions; appeal and override ledger; containerized API with authentication and observability. Publish error rates by language, genre and region before enforcement.
