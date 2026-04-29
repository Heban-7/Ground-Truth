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

## Path decision (temporary)

Temporary default path: **Path B (judge/critic)**, because it is robust when generation traces are limited and aligns with style-compliance scoring.

Final path declaration will be confirmed after we build and inspect the first 20 benchmark tasks.

## Cost guardrails

- No tau-squared reruns.
- Use cheap-tier models for authoring/filters.
- Reserve eval-tier calls for held-out scoring only.

## Reproducible protocol (current implementation)

Run commands in this order:

1. `python generation_scripts/build_seed_dataset.py`
2. `python generation_scripts/partition_tasks.py --seed 42`
3. `python generation_scripts/contamination_check.py`
4. `python scoring_evaluator.py`
5. `python generation_scripts/inter_rater_agreement.py`

Artifacts produced:

- `tenacious_bench_v0.1/train/tasks.jsonl`
- `tenacious_bench_v0.1/dev/tasks.jsonl`
- `tenacious_bench_v0.1/held_out/tasks.jsonl`
- `contamination_check.json`
- `inter_rater_agreement.json`
- `inter_rater_agreement.md`

## Inter-rater policy

- Pilot stage: two rounds over current seed tasks to validate workflow.
- Production target: 30-task subset, relabeled after ~24 hours without looking at round 1 labels.
- Decision rule: if any dimension agreement is below 80%, revise rubric guidance and relabel.
