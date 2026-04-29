# tenacious_bench_v0.1

Dataset partitions for the Tenacious sales evaluation benchmark.

- `train/`: training partition (target 50%)
- `dev/`: public development partition (target 30%)
- `held_out/`: sealed evaluation partition (target 20%)

The folders are initialized empty and will be populated in later steps.

Current seed status:

- `train/tasks.jsonl`: 3 tasks
- `dev/tasks.jsonl`: 2 tasks
- `held_out/tasks.jsonl`: 1 task

To regenerate these starter files, run:

`python generation_scripts/build_seed_dataset.py`

To run contamination checks (train vs held_out), run:

`python generation_scripts/contamination_check.py`

This writes `contamination_check.json` at the repository root.

To repartition current tasks with deterministic shuffle (default 50/30/20), run:

`python generation_scripts/partition_tasks.py --seed 42`

To compute pilot inter-rater agreement (two labeling rounds), run:

`python generation_scripts/inter_rater_agreement.py`

This writes `inter_rater_agreement.json` and `inter_rater_agreement.md` at the repository root.

To compute pilot inter-rater agreement (two labeling rounds), run:

`python generation_scripts/inter_rater_agreement.py`

This writes `inter_rater_agreement.json` and `inter_rater_agreement.md` at the repository root.
