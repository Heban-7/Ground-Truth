# Final Submission Report (PDF-ready)

## 1) GitHub Repo Deliverables (Final)

### Training data and rationale

- `training_data/path_b/preference_pairs_train.jsonl` and `training_data/path_b/preference_pairs_val.jsonl` are included as the formatted training partition for Path B.
- `methodology_rationale.md` cites path-specific literature and at least three proxy Week 10 trace IDs (`TRC-007`, `TRC-011`, `TRC-015`).

### Training artifacts

- `training/path_b/train_critic.py` includes the training run implementation.
- `training/path_b/config.json` captures hyperparameters.
- `training/path_b/artifacts/training_run.log` and `training/path_b/artifacts/metrics.json` capture run outputs.

### Ablation artifacts

- `ablations/ablation_results.json` present.
- `ablations/held_out_traces.jsonl` present.
- `ablations/statistical_test_output.json` present.

### Evidence mapping

- `evidence_graph.json` maps numeric claims to artifact file sources.

### Synthesis memos

All required memos are included:

- Common readings (4): `01`–`04` in `synthesis_memos/`
- Path B readings (3): `05`–`07` in `synthesis_memos/`

## 2) Public Artifacts (Fill URLs Before Submission)

- HuggingFace dataset URL: `TODO`
- HuggingFace model URL (Path A/C only): `N/A for Path B baseline` (or `TODO` if publishing critic artifact)
- Blog post URL: `TODO`
- Community engagement URL (issue/submission/PR): `TODO`

## 3) PDF Memo (Two-page Content)

### Page 1 - The decision

#### Executive summary (3 sentences)

Tenacious-Bench v0.1 was built as a reliability-focused benchmark for B2B outreach, with 209 accepted tasks and contamination-safe partitions. On current held-out ablations, the trained critic matches baseline rules on Delta A (0.00 pp, 95% CI [-13.10, 13.10], p=0.5225) while outperforming a prompt-engineered comparator on Delta B (+20.24 pp, 95% CI [5.95, 34.52], p=0.004). Recommendation: **deploy with caveat** as a shadow/guardrail component, then promote only after positive Delta A separation in the next iteration.

#### Headline lift and confidence interval

- Baseline rules accuracy: 69.05%
- Trained critic accuracy: 69.05%
- **Delta A:** 0.00 pp, 95% CI [-13.10, 13.10], p=0.5225

#### Delta B (reported honestly)

- Prompt-engineered rules accuracy: 48.81%
- **Delta B:** +20.24 pp, 95% CI [5.95, 34.52], p=0.004

#### Cost per task

- Baseline rules: $0.00/example, ~4 ms
- Prompt-engineered rules: $0.00/example, ~7 ms
- Trained critic proxy: ~$0.00005/example, ~12 ms

#### Deployment recommendation

Deploy with caveat:

1. keep critic in shadow mode initially
2. enforce daily Delta A monitoring
3. require embedding-based contamination checks before broad rollout

### Page 2 - Skeptic's appendix

#### Four failure modes v0.1 does not yet capture

1. long multi-turn thread memory and context carryover effects
2. realistic contract/pricing negotiation behavior under constraints
3. channel-transition behavior (email -> LinkedIn -> voice scheduling)
4. account-specific tolerance variation beyond static rubric bins

#### Public-signal lossiness

Ground truth relies on public signals and proxy trace reconstruction due to unavailable Week 10 originals. This creates fidelity gaps between benchmark signals and full production context.

#### One unresolved failure

The current critic did not produce positive Delta A over baseline rules. This indicates pipeline correctness but insufficient model lift for deployment-grade replacement.

#### Kill-switch trigger

Disable critic gating if any condition occurs:

- negative Delta A for 3 consecutive evaluation windows
- >1% increase in policy-unsafe sends in audited sample
- reproducibility drift causing >0.5% metric instability across repeated runs

## 4) References to Repo Evidence

- `generation_scripts/logs/seed_counts.json`
- `contamination_check.json`
- `inter_rater_agreement.json`
- `training_data_contamination_check.json`
- `training/path_b/artifacts/metrics.json`
- `ablations/ablation_results.json`
- `ablations/statistical_test_output.json`
- `evidence_graph.json`
