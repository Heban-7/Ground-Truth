# Synthesis Memo: Prometheus 2 and Judge Design (Path B)

## Paper focus

*Prometheus 2* (Kim et al.)

## Practical takeaway

Judge models need strict schema contracts, calibration routines, and domain-grounded criteria. Free-form judging is hard to audit and harder to reproduce.

## What we applied

- strict judge output contract in `generation_scripts/judge_scaffold.py`
- parser validation for required keys and score ranges
- hybrid evaluator mode that preserves deterministic checks while integrating judge scores

## Adaptation

Our interim critic is intentionally lightweight. The infrastructure mirrors judge-specialized design principles so the same contract can be reused with a stronger model later.

## Actionable rule

Judge model quality must be measured as a first-class component, not treated as a hidden helper.
