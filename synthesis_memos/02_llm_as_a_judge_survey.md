# Synthesis Memo: LLM-as-a-Judge Survey (Gu et al.)

## Core takeaway

Judge systems fail when prompt format, calibration, and leakage controls are weak. A judge should be treated like a model component with explicit interface contracts and audit traces.

## What we adopted

- strict JSON-only judge schema in `judge_scaffold.py`
- parser-side validation for required keys and score ranges
- hybrid evaluation mode combining deterministic checks + judge scores
- policy to avoid same-family self-judging in routing metadata

## What we disagree with (for this project stage)

The survey highlights pairwise and preference judgments as high-performing, but for interim milestone we prioritize pointwise score stability and parser robustness first. Given missing Week 10 artifacts, the immediate bottleneck is reliable data intake and filtering, not sophisticated comparative judging.

## Evidence from our implementation

- evaluator can run `rules` and `hybrid` modes with consistent output schema
- judge response parsing is resilient to fenced-json outputs
- inter-rater workflow is in place to test rubric clarity independently of judge outputs

## Actionable rule

Before scaling judge calls, lock the judge I/O contract and monitoring artifacts; otherwise debugging becomes guesswork.
