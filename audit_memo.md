# Audit Memo: Tenacious-Bench Gap Analysis

Public benchmarks under-measure the failures that matter most in Tenacious-style B2B outreach. They reward fluent copy but can miss high-cost reliability errors: fabricated signals, unsupported staffing claims, pricing-policy violations, and condescending framing.

Week 10 artifacts are missing in this repo, so this audit uses explicit proxy evidence.

## Critical gap

The main gap is not writing quality. It is **policy-safe reliability under uncertainty**:

1. confidence-aware grounding (ask when signal is weak)
2. safe commercial claims (no invented pricing/capacity)
3. respectful competitor-gap framing
4. one clear ask per message

## Evidence used

Proxy probe IDs:
`PRB-01`, `PRB-02`, `PRB-03`, `PRB-04`, `PRB-05`, `PRB-06`, `PRB-07`, `PRB-08`

Proxy trace IDs:
`TRC-001`, `TRC-004`, `TRC-007`, `TRC-011`, `TRC-015`

Highest-risk cluster: `PRB-02`, `PRB-03`, `PRB-06` and `TRC-007`, `TRC-011`.

## Schema implications

Tenacious-Bench v0.1 uses hard + soft scoring:

- hard checks: banned phrases, word cap, one-ask rule, signal overlap, held-out time anchor
- soft rubric (1-5): direct, grounded, honest, professional, non-condescending
- pass policy: all hard checks pass and each soft dimension >=4

This ties benchmark scores directly to send/no-send behavior in production.

## Path implication

Interim path selection is **Path B (judge/critic)** because the dominant errors are inconsistency and safety failures, not fluency failures. A critic gate is the fastest risk-control intervention for this profile.
