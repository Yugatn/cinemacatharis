# Composition model v0.7: measured content vs unknown

A *precise composition* requires an operational definition of each label, original-media timecodes, near-complete temporal coverage, calibrated detectors and independent human annotation. No single percentage can accurately describe an incompletely scanned film.

## Formulae

Let total duration be **T**, union of continuously inspected intervals **C**, and union of intervals assigned label **k** be **A_k**.

- Coverage: **q = |C| / T**.
- Observed category duration: **d_k = |A_k ∩ C|** (overlaps merged).
- Observed fraction of full media: **p_k,observed = d_k / T**.
- Fraction of inspected time: **p_k,covered = d_k / |C|**, if |C| > 0.
- With no assumptions about unseen time, possible full-media share lies in **[d_k/T, (d_k + T - |C|)/T]**, *conditional on correct labels inside coverage*.
- Unknown time: **U = T - |C|**.

**Multi-label categories overlap.** A scene may contain dialogue, alcohol, humor and violence simultaneously, so category shares need not sum to 100%. If a 100% breakdown is required, use an explicitly disclosed priority rule to assign one label per instant; this is an *editorial convention*, not a scientific discovery.

## Confidence, uncertainty and sampling

CLIP zero-shot similarity scores are not calibrated probabilities. They should not be averaged as if they were a physical percentage of content. Calibration requires a held-out labeled dataset, reliability diagrams, Brier score and per-category precision/recall. Frame sampling every second or at ×10 does **not** establish continuous coverage; single frames should be represented as samples with unknown intervals between them.

For a frame-based estimate, report number of frames actually analyzed, sample selection design, source-media timestamps, intervals missed, and confidence intervals that account for temporal correlation. A bootstrap over contiguous scene blocks may be preferable to an independent-frame binomial interval.

Audio, visual, speech and OCR findings should remain separate evidence channels until aligned on the original timeline. Classify observed presence separately from intent (promotion, criticism, documentary). Monetization decisions require human review and a transparent appeal process.

## Example

Film duration 100 s; continuously reviewed 60 s; label observed for 18 s within reviewed time. Observed share of full film is 18%, share of reviewed material is 30%, and the unconstrained whole-film share lies between 18% and 58%. Reporting only 30% as the precise whole-film composition would be misleading.

## Integration

`compose(duration_ms, coverage, segments)` returns the coverage-aware multi-label metrics. `exclusive_timeline(..., priority)` provides an optional non-overlapping allocation. **Do not** pass frame sample timestamps as if they were continuously reviewed intervals.
