# Film-shot-informed storyboard study

Private working repository for reproducibility materials and reviewer-response evidence. Public release is not yet complete.

## Contents

- [Supplement S: production records](supplementary/README.md)
- [Proposed manuscript addition and reviewer response](supplementary/manuscript-and-response.md)
- [Image metadata verification](supplementary/image-metadata/report.json)
- [N/S production comparison: 78 cuts](supplementary/S4-NS-production-comparison.md)

All explanatory documentation is provided in English. Original Korean source descriptions, prompts and historical records are retained verbatim as evidence; they are not translations or newly reconstructed inputs.

## Participant data

The dataset contains 60 scene responses from 30 actual participants with generative-AI production experience, as reconfirmed by the author on November 11, 2026. Legacy SIM/sims identifiers and synthetic/persona descriptions were erroneous metadata according to the author. Participant identifiers, assignments, presentation order and Q1–Q4 scores are unchanged. This provenance statement does not constitute an independent audit of data collection.

## Reproduce the analysis

Python 3 standard library only:

```sh
python3 evaluation/perceived-clarity-study/analyze_collected_data.py
python3 scripts/extract_image_metadata.py /path/to/downloaded/image-archives
```

The image archives are kept outside Git. The extractor records archive and image hashes, preserves embedded prompt graphs, selects the image-generation node matching each cut ID, and compares its prompt with the archived catalog and prompt file.

## Provenance

Production records were selected from the existing local copy of `research-data-and-analysis.zip`. The eight image archives were downloaded directly from the supplied Google Drive folder during this verification. All 157 embedded target-node prompts exactly match the catalog. All images are stored under `novel-continuity-v2`; no first-generation image prompt has been located in the examined materials. Metadata corroborates archived inputs but does not independently authenticate backend execution.

`source-manifest.json` preserves initial imported-file hashes. `supplementary/manifest.json` records current supplementary-file hashes. Historical files retain their original wording and may describe checks not repeated in this repository.
