# Collected perceived-clarity ratings

The author confirmed that this dataset contains actual responses from 30 participants with generative-AI production experience; this was reconfirmed on November 11, 2026. Earlier synthetic/persona descriptions were erroneous metadata according to the author. This provenance statement is not an independent audit of recruitment or data collection.

- `responses.csv`: 60 responses, two scenes per participant. IDs, assignments, presentation order and Q1–Q4 scores have not been changed during this repository preparation.
- `participants.csv`: participant metadata. Legacy `SIM-POS-*` identifiers are retained to preserve links between files; the prefix does not indicate synthetic observations. Background and experience statements reflect the author's confirmation.
- `summary.csv`: means and sample standard deviations recomputed from response records. The legacy `simulated_n` field was previously corrected to `n`.
- `analysis.json`: distributions, allocation strata, source hashes, Q1 differences and participant-level stratified bootstrap intervals. Its earlier provenance timestamp is retained as part of the imported record.

From the repository root, run:

```sh
python3 evaluation/perceived-clarity-study/analyze_collected_data.py
```

The implementation uses the Python standard library, resampling participants within eight condition-combination/order strata and retaining both scene responses together. It uses 20,000 bootstrap resamples, seed 20260922 and percentile 95% intervals. These settings are documented analysis choices, not a claim of preregistration.

Recruitment records, compensation, consent documentation and institutional ethics records are not included here. Protocol descriptions alone do not independently verify implementation. Human participant ratings should not be confused with model-assisted production observations elsewhere in the project.
