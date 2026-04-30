# Methodology Rationale (Path B)

## Decision

Chosen method: **Path B (preference-tuned judge/critic)**.

## Why this path fits observed failures

Our interim evidence shows the bottleneck is reliability gating, not text fluency:

- `TRC-007`: unsupported capacity commitment risk
- `TRC-011`: condescending framing risk
- `TRC-015`: passive-aggressive follow-up risk

These are cases where generation may look fluent but should be rejected. A critic model provides an operational control point for rejection sampling or rollback before send.

## Paper-grounded rationale

1. **DPO (Rafailov et al.)** motivates optimizing preferences directly on chosen/rejected pairs, matching our training data format.
2. **LLM-as-a-Judge Survey (Gu et al.)** supports strict interface contracts and calibration; we already enforce structured judge schema and agreement checks.
3. **Preference Leakage (Li et al., 2025)** warns against same-family generate-and-judge loops; our metadata and routing policy keep model-family separation explicit.

## Data preparation strategy

Training data is built from train partition tasks only:

- prompt is structured and metadata-rich
- chosen sample is policy-aligned candidate output
- rejected sample is a controlled failure mutation (banned phrase, fake urgency, overcommitment, fabricated signal, etc.)

This creates dense reliability supervision targeted to the specific errors we need the critic to catch.

## Contamination safety

We run dedicated contamination checks against **both** `dev` and `held_out`:

- source-task ID overlap must be zero
- no shared 8-gram between training prompts and eval signal briefs
- lexical similarity threshold must stay below 0.85

Current status is recorded in `training_data_contamination_check.json`.

## Expected training behavior

A successful Path B critic should:

- assign higher preference to policy-safe outputs (`chosen`)
- assign lower preference to high-risk outputs (`rejected`)
- improve consistency on honesty/professionalism dimensions with minimal latency overhead

This methodology is aligned with Week 11 goals: measured reliability lift on Tenacious-Bench with explicit evidence and contamination controls.
