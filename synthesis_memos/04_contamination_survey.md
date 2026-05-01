# Synthesis Memo: Contamination Prevention Survey

## Paper focus

*Recent Advances in LLM Benchmarks against Data Contamination* (Chen et al.)

## Practical takeaway

Held-out quality requires explicit anti-overlap protocols, not just random splitting. Static random partitions are vulnerable to lexical and semantic leakage.

## What we applied

- enforced partition protocol (train/dev/held_out)
- implemented 8-gram overlap checks
- implemented similarity threshold checks
- required time-anchor structure for held-out signal briefs
- added separate contamination checks for training pairs vs dev/held_out

## Limitation acknowledged

Current similarity check is lexical proxy (Jaccard), not embedding cosine. This is documented as a v0.2 upgrade requirement.

## Actionable rule

No new benchmark release without a fresh contamination report committed with it.
