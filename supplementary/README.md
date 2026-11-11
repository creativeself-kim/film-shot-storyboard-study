# Supplement S. Production records and scope of comparison

Prepared November 11, 2026. This supplement organizes preserved records retrospectively; it is not a reconstructed contemporaneous edit log.

## S1. Production counts and available records

| Scene | N | S | S−T | S−D |
|---|---:|---:|---:|---:|
| BAR-P01 | 20 | 26 | 26 | 22 |
| RET-P01 | 17 | 15 | 16 | 15 |

Final prompts and state instructions are available for all 157 cuts. The historical production README records re-production of the 78 N/S images and first image production of the 79 ablation-condition cuts. These are production counts, not counts of prompts demonstrably changed between versions.

See the [condition summary](S1-condition-summary.csv) and [complete cut register](S2-cut-register.csv). First-generation image prompts have not been located in the examined materials. Therefore, complete before-and-after prompt pairs and verified counts of edited cuts by revision type are unavailable. This does not establish that no earlier copy exists elsewhere.

## S2. Types of production refinement

| Type | Content documented in the preserved records | Unit of application |
|---|---|---|
| Spatial arrangement and action axis | World positions, travel direction and camera side | Shared scene rules |
| Anatomical sides and contact | Grasping hand and grasped arm; attacking finger and cheek | Shared rules and cut-specific states |
| Pose and intermediate action | Prone posture, mounting, releasing a grasp, lowering a hand and walking | Cut-specific states |
| Props and event consequences | Shield position, backpack ownership, injury, dissolution and stone appearance | Shared rules and cut-specific states |
| Temporal separation | Previous/next instants supplied as context; rendering only the current instant | Final prompt structure |
| Background references | Two shared scene backgrounds intended to avoid unwanted prop carryover | Historical production account |

These categories describe the documented instructions. They are not independently coded image outcomes or measured revision frequencies. Some information was already present in the shot plans; its presence in a final prompt does not establish that it was newly added.

See the [shared production policy](../evaluation/novel-continuity-v2/production-policy.json) and [78-cut N/S comparison](S4-NS-production-comparison.md). The comparison places original shot-plan descriptions beside final state instructions. Shot plans are not first-generation image prompts.

## S3. Same-event example

The final `production_state` strings for BAR-P01 N cut 9 and S cut 12 are identical. Both specify the anatomical right hand grasping the opponent's left forearm and exclude the magic stone and dissolution traces associated with later events. The full prompts are not claimed to be identical: shot information and neighboring context may differ. This documents a shared instruction for one matched event, not equal effects of refinement across all cuts.

## S4. Execution environment and creator awareness

The eight preserved run logs date N/S plan generation to September 16, 2026 and ablation-plan generation to September 18. Executable paths indicate macOS-style and Windows environments, respectively. All request `gpt-6-astra` with `medium` reasoning; model snapshots are recorded as not exposed. See [execution records](S3-plan-execution.csv) and the original logs under `historical-records/`. CLI versions 0.154.0 and 0.155.0 stated in the manuscript are not independently established by these run JSON files, which contain no version field.

The historical production account specifies Comfy Cloud, `OpenAIGPTImageNodeV2`, `gpt-image-2.5-sunburst`, 1536 × 864, medium quality, opaque background and n=1. It records one queue-registration failure resubmitted with the same input and retention of first outputs despite content problems. These are historical-record statements, not a newly conducted service-log audit.

The creator's awareness of condition labels is disclosed in the manuscript. Shared rules do not establish equal refinement effects across conditions. Interpretation concerns fixed outputs produced through the complete workflow, including creator refinement.

## S5. Verification against image metadata

All eight Drive image archives were downloaded and inspected. All 157 PNGs contain a `prompt` metadata field. The image-generation node identified by each cut ID was extracted, and its prompt exactly matched the corresponding catalog string in all 157 cases. All 157 standalone prompt files also matched after trimming outer whitespace. PNG chunk CRCs were checked during extraction.

All archive members are under `novel-continuity-v2`. Thus this verification corroborates final-generation inputs; it does not recover first-generation prompts. Embedded metadata can be edited and does not independently prove backend execution or the causal effect of an instruction.

- [Verification report and archive hashes](image-metadata/report.json)
- [Per-image hashes and comparison results](image-metadata/verification.csv)
- [Extracted prompt graphs and text](image-metadata/)

## S6. Participant-data provenance

The author reconfirmed that these are actual responses from 30 participants. Legacy SIM/sims and synthetic/persona descriptions were erroneous metadata according to the author. Original identifiers, assignment, order and 60 response records remain unchanged. Participant ratings and model-assisted production observations are distinct evidence sources.

## Availability

This repository is currently private. Access for reviewers or public release must be arranged before claiming public availability. Original Korean evidence is preserved verbatim. Historical records may contain superseded descriptions; current verification claims are confined to the checks described above.
