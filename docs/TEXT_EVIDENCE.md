# Browser text to common evidence schema

The `from_lexical_report` adapter converts `lexical-composition-1.1` character-offset matches into the common `evidence-1.0` observation schema. It does not assign a safety verdict or infer promotional intent.

**Limitation:** current lexical browser engine reports only token positions (lexical-composition-1.0), so it does not yet produce character offsets. Those older matches are explicitly skipped, rather than fabricating positions. To activate end-to-end integration, upgrade the shared browser and extension lexical engines to include `start`, `end` and optional excerpt in every example.

Next: a shared read-only report UI with source evidence and human verification. No child browsing data is uploaded automatically.
