# Tenacious-Bench v0.1 (Dataset Card Draft)

## Dataset summary

Tenacious-Bench v0.1 is a domain-focused evaluation benchmark for B2B sales outreach reliability. It measures policy-safe and tone-aligned behavior under constrained hiring-signal contexts.

## Task structure

Each task includes:

- input signal brief and confidence metadata
- candidate subject/body output
- machine-checkable constraints (word limit, banned phrases, one-ask)
- rubric dimensions (direct, grounded, honest, professional, non-condescending)

## Composition

- total accepted tasks: 209
- split: train 104 / dev 63 / held_out 42
- source modes: trace-derived, programmatic, multi-LLM synthesis, hand-authored

## Quality controls

- contamination checks pass (`contamination_check.json`)
- inter-rater agreement pass (`inter_rater_agreement.json`)
- evidence traceability in `evidence_graph.json`

## Intended use

- benchmarking model/agent reliability on Tenacious-specific outreach behavior
- filtering preference/judge training data
- evaluating rule+critic pipeline variants

## Limitations

- Week 10 originals unavailable; proxy trace/probe IDs used with explicit disclosure
- similarity contamination currently uses lexical proxy (embedding check planned in v0.2)

## Citation

Add final citation after public release URL is available.
