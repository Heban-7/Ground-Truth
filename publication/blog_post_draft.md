# What Existing Benchmarks Miss in B2B Sales Agent Reliability

## 1) The gap

Generic benchmarks reward fluent text but under-measure trust-critical failures in B2B outreach: fabricated signals, unsupported commitments, condescending framing, and policy-unsafe urgency.

## 2) The audit method

- built proxy evidence from style-guide failure taxonomy and structured trace reconstruction
- translated risks into measurable rubric + hard policy checks
- documented gap handling because Week 10 originals were unavailable

## 3) Dataset construction choices

- 4 authoring modes mixed by target proportions
- deterministic seed and reproducible generation scripts
- dedup + judge filtering + contamination checks before sealing held_out
- inter-rater agreement threshold gate at 80%

## 4) Training experiment (Path B)

- prepared 1040 preference pairs
- trained a lightweight critic baseline
- evaluated on held-out positive/negative challenge protocol

## 5) Honest result

- Delta A (trained vs baseline): 0.00 pp
- Delta B (trained vs prompt-engineered): +20.24 pp
- interpretation: current critic validates pipeline but does not yet outperform strong rules baseline

## 6) What is next

- replace lexical contamination proxy with embeddings
- run stronger preference model architecture
- improve hard-negative generation diversity
- package benchmark + artifacts publicly and invite external replication
