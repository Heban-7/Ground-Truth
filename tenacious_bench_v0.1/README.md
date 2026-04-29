# tenacious_bench_v0.1

Dataset partitions for the Tenacious sales evaluation benchmark.

- `train/`: training partition (target 50%)
- `dev/`: public development partition (target 30%)
- `held_out/`: sealed evaluation partition (target 20%)

Current interim build (seed 42):

- total accepted tasks: 209
- `train/tasks.jsonl`: 104 tasks
- `dev/tasks.jsonl`: 63 tasks
- `held_out/tasks.jsonl`: 42 tasks

Generate and validate:

1. `python generation_scripts/author_benchmark.py`
2. `python generation_scripts/contamination_check.py`
3. `python generation_scripts/bootstrap_label_rounds.py`
4. `python generation_scripts/inter_rater_agreement.py`
5. `python scoring_evaluator.py --mode rules`
6. `python scoring_evaluator.py --mode hybrid`

Artifacts at repo root:

- `contamination_check.json`
- `inter_rater_agreement.json`
- `inter_rater_agreement.md`

Generation logs:

- `generation_scripts/logs/raw_pool.jsonl`
- `generation_scripts/logs/deduped_pool.jsonl`
- `generation_scripts/logs/judge_filter_log.jsonl`
- `generation_scripts/logs/model_routes.json`
- `generation_scripts/logs/seed_counts.json`
