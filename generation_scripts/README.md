# Generation Scripts

This directory contains reproducible authoring and validation scripts for Tenacious-Bench v0.1.

## Core pipeline

1. `author_benchmark.py`
   - creates 210 raw tasks across four source modes
   - outputs 209 accepted tasks after dedup/filter
   - performs deduplication and judge-style filtering
   - writes partitioned JSONL files (train/dev/held_out)
   - writes authoring logs in `generation_scripts/logs/`

2. `contamination_check.py`
   - checks n-gram overlap + lexical similarity + time anchors
   - writes `contamination_check.json`

3. `bootstrap_label_rounds.py`
   - creates two 30-task label rounds for agreement workflow

4. `inter_rater_agreement.py`
   - computes per-dimension agreement and overall agreement
   - writes `inter_rater_agreement.json` and `inter_rater_agreement.md`

## Auxiliary scripts

- `judge_scaffold.py`: strict judge prompt + parser contract
- `partition_tasks.py`: deterministic repartition utility
- `build_seed_dataset.py`: small starter dataset generator

## Logs produced

- `logs/raw_pool.jsonl`
- `logs/deduped_pool.jsonl`
- `logs/judge_filter_log.jsonl`
- `logs/model_routes.json`
- `logs/seed_counts.json`
