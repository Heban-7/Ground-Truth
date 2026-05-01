# Synthesis Memo: Preference Leakage (Path B)

## Paper focus

*Preference Leakage: A Contamination Problem in LLM-as-a-Judge* (Li et al.)

## Practical takeaway

When generation and judging share model-family artifacts, the judge can reward style familiarity rather than true quality.

## What we applied

- enforced explicit separation policy in metadata (`chosen_model_family` vs `judge_model_family`)
- documented route policy in authoring logs
- added contamination checks between training prompts and dev/held signal space

## Remaining risk

Current implementation is still a baseline proxy pipeline. True leakage resilience must be re-tested after real API judge integration.

## Actionable rule

Never let the same model family generate and evaluate the same sample in final scoring loops.
