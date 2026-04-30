# Tenacious CEO/CFO Memo (Draft)

## Page 1 - Decision

### Executive summary (3 sentences)

We built Tenacious-Bench v0.1, a 209-task domain benchmark that scores reliability-critical outreach behavior using machine-checkable rules and judge-aligned rubric dimensions. On the current held-out ablation protocol, the trained critic baseline matches the rules baseline (Delta A = 0.00 pp, 95% CI [-13.10, 13.10], p=0.5225), but outperforms a prompt-engineered comparator (Delta B = +20.24 pp, 95% CI [5.95, 34.52], p=0.004). Recommendation: **deploy with caveat** as a guardrail layer for controlled traffic, while prioritizing embedding-based contamination checks and a stronger critic model in v0.2.

### Headline metrics

- Benchmark size: 209 tasks (train/dev/held_out = 104/63/42)
- Inter-rater agreement: 82.67% overall (all dimensions >= 80%)
- Delta A (trained critic vs baseline rules): 0.00 pp
- Delta B (trained critic vs prompt-engineered): +20.24 pp

### Cost and latency

- Baseline rules: $0.00/example, ~4 ms
- Prompt-engineered rules: $0.00/example, ~7 ms
- Trained critic proxy: ~$0.00005/example, ~12 ms

### Deployment recommendation

Deploy the critic as a **non-blocking shadow gate** first, then move to blocking mode only after:

1. at least one improved Delta A run with positive CI separation
2. embedding-based contamination check replacement
3. calibration on live traffic slices with human overrides

---

## Page 2 - Skeptic's Appendix

### Four failure modes v0.1 still does not capture

1. **Context-window mismatch** across long multi-touch threads (current tasks are mostly single-message).
2. **True pricing negotiation dynamics** with nuanced concessions and legal constraints.
3. **Cross-channel transition behavior** (email -> LinkedIn -> voice) under evolving user intent.
4. **Prospect-specific tolerance variance** for tone and urgency beyond static rubric bins.

### Public-signal lossiness

Ground truth relies on public hiring/funding/leadership signals and synthetic proxies where Week 10 traces were missing. This introduces approximation error between benchmark signal fidelity and real-world account context.

### One unresolved training failure

Current trained critic did not beat baseline rules on Delta A (0.00 pp). This indicates the present linear preference model is not yet adding measurable held-out reliability lift beyond deterministic policy checks.

### Kill-switch trigger condition

Disable critic gating immediately if any of the following occurs in production:

- >3 consecutive days of negative Delta A relative to baseline rules
- >1% increase in policy-unsafe sends in audited outbound sample
- parsing or scoring instability that causes >0.5% drop in evaluation reproducibility

### Evidence references

All numeric claims above are mapped in `evidence_graph.json`.
