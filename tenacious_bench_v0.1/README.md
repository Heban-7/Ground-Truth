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
