# Synthesis Memo: Best Practices on Synthetic Data (Liu et al.)

## Core takeaway

Synthetic data is most useful when treated as an engineering system, not a one-shot prompt. Quality filtering, diversity controls, and explicit failure targeting matter more than raw volume.

## What we adopted

- multi-mode authoring instead of single-template generation
- deterministic generation seed for reproducibility
- dedup + judge filtering before partitioning
- explicit source-mode metadata for every task

## What we disagree with (for this project stage)

The paper emphasizes broad synthetic scaling, but for this week we prioritize controllable, policy-dense data over scale. In this domain, one fabricated funding claim is more damaging than many bland samples. So we intentionally bias toward high-precision filtering even if it reduces throughput.

## Evidence from our implementation

- judge filtering removed policy-unsafe candidates before partitioning
- contamination checks were integrated as a first-class gate
- source mix was constrained (~30/30/25/15) to reduce mode collapse

## Actionable rule

For Tenacious-Bench, "generate fewer, verify harder" is the right interim default.
