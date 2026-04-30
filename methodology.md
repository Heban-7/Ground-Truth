# Methodology (Draft v0)

## Project scope

Build a Tenacious-specific sales evaluation benchmark and improve one component of a sales agent using a small, cost-disciplined training run.

## Baseline policy

This project does **not** depend on rerunning tau-squared retail benchmarks.

- If a Week 10 tau-squared score exists, use it only as a historical reference.
- If no Week 10 score/artifacts exist, the baseline is the first run of this Week 11 Tenacious-Bench on the untrained baseline system.

For this repo, we assume **no usable Week 10 artifacts are available** and proceed with a Week 11-native baseline.

## Week 10 gap handling plan

Because Week 10 outputs are missing, we replace each expected input with a controlled fallback:

- Missing `trace_log.jsonl` -> generate a small synthetic trace pool from the Tenacious style guide examples and public-signal templates.
- Missing `probe_library.md` -> derive an initial failure taxonomy from the 12 "bad" outreach examples.
- Missing `failure_taxonomy.md` -> draft v0 taxonomy directly from tone markers and pre-flight checks.

This keeps the workflow valid while preserving evaluation rigor.

## Path declaration (interim)

Declared path: **Path B (judge/critic)**.

Rationale:

- Failure concentration is reliability-oriented (detection + rejection), not pure fluency generation.
- Proxy trace failures `TRC-007` (capacity over-commitment), `TRC-011` (condescending framing), and `TRC-015` (aggressive follow-up) are better addressed by a critic gate.
- Probe failures `PRB-02`, `PRB-03`, `PRB-06` indicate policy violations where a judge layer provides faster risk reduction than full generator retraining.
- Judge interface and calibration choices follow guidance from *A Survey on LLM-as-a-Judge* (Gu et al.).
- Model-family rotation policy follows leakage constraints from *Preference Leakage* (Li et al., 2025).

## Cost guardrails

- No tau-squared reruns.
- Use cheap-tier models for authoring/filters.
- Reserve eval-tier calls for held-out scoring only.

## Reproducible protocol (current implementation)

Run commands in this order:

1. `python generation_scripts/author_benchmark.py`
2. `python generation_scripts/bootstrap_label_rounds.py`
3. `python generation_scripts/contamination_check.py`
4. `python scoring_evaluator.py --mode rules`
5. `python scoring_evaluator.py --mode hybrid`
6. `python generation_scripts/inter_rater_agreement.py`

Interim artifacts produced:

- `tenacious_bench_v0.1/train/tasks.jsonl`
- `tenacious_bench_v0.1/dev/tasks.jsonl`
- `tenacious_bench_v0.1/held_out/tasks.jsonl`
- `contamination_check.json`
- `inter_rater_agreement.json`
- `inter_rater_agreement.md`
- `generation_scripts/logs/model_routes.json`
- `generation_scripts/logs/seed_counts.json`
- `generation_scripts/logs/judge_filter_log.jsonl`

Phase III artifacts:

- `training_data/path_b/preference_pairs_train.jsonl`
- `training_data/path_b/preference_pairs_val.jsonl`
- `training_data/path_b/summary.json`
- `training_data_contamination_check.json`
- `methodology_rationale.md`

Phase IV artifacts:

- `training/path_b/config.json`
- `training/path_b/artifacts/critic_model.json`
- `training/path_b/artifacts/metrics.json`
- `training/path_b/artifacts/training_run.log`

## Inter-rater policy

- Pilot stage: two rounds over current seed tasks to validate workflow.
- Production target: 30-task subset, relabeled after ~24 hours without looking at round 1 labels.
- Decision rule: if any dimension agreement is below 80%, revise rubric guidance and relabel.

## Partitioning protocol

- Target split: 50% train, 30% dev, 20% held_out.
- Assignment is deterministic from seed `42` in authoring pipeline.
- Held-out is evaluated only; no training scripts should read it.

## Contamination protocol (interim)

Checks run before accepting held_out:

- 8-gram overlap check between train and held_out signal briefs
- lexical similarity proxy threshold (< 0.85)
- explicit time-anchor requirement in held_out signal briefs

Current result: pass on overlap + similarity; time-anchor warnings resolved.

## Week 10 artifact gap handling

This repository does not contain Week 10 files. To keep momentum and preserve evidence integrity:

- `trace_log.jsonl` replaced by structured proxy traces (`TRC-*`) documented in `audit_memo.md`
- `probe_library.md` replaced by explicit probe IDs (`PRB-*`) from style-guide failure patterns
- all claims in interim report are tagged as proxy-derived where applicable
