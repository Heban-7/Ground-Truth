# Synthesis Memo: DPO Foundations (Path B)

## Paper focus

*Direct Preference Optimization* (Rafailov et al.)

## Practical takeaway

Preference learning can optimize ranking behavior directly from chosen/rejected pairs without building a separate reward model first.

## What we applied

- formatted Path B data as explicit chosen/rejected pairs
- made each pair traceable to source benchmark task ID
- encoded controlled rejection types (banned phrase, over-commitment, fabricated signal, etc.)

## Adaptation in this repo

For reproducibility and budget control, we used a deterministic linear ranking baseline before full LLM DPO. This validates data and evaluation plumbing first, then allows model-scale upgrades later.

## Actionable rule

Treat pair quality as the main lever. A larger optimizer on noisy pairs will not improve reliable gating.
