# Path B Training Data

This directory contains preference-pair training data for Path B (judge/critic).

## Files

- `preference_pairs_train.jsonl`
- `preference_pairs_val.jsonl`
- `summary.json`

Each row contains:

- `pair_id`
- `source_task_id`
- `source_mode`
- `prompt`
- `chosen` (`subject`, `body`)
- `rejected` (`subject`, `body`)
- `rejection_type`
- metadata for leakage-safe generation/judge separation policy

## Build commands

1. `python generation_scripts/prepare_path_b_training_data.py`
2. `python generation_scripts/check_training_data_contamination.py`

Contamination report is written to:

- `training_data_contamination_check.json`
