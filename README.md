# Ground-Truth (Week 11 Interim)

Building the Sales Evaluation Bench and Aligning the Conversion Engine for Tenacious-style B2B outreach reliability.

## Current status

Interim scope (Acts I + II) is implemented:

- audit memo and benchmark schema
- dataset authoring pipeline with 209 accepted tasks (from 210 raw)
- train/dev/held_out partitions (50/30/20)
- contamination checks and inter-rater agreement workflow
- rule-based + hybrid judge-scaffold evaluator
- datasheet, methodology, synthesis memos, and cost log

## Repository map

- `audit_memo.md`: gap analysis and benchmark rationale
- `schema.json`: machine-readable task schema with 3 examples
- `methodology.md`: path decision, fallback policy, reproducible protocol
- `datasheet.md`: dataset documentation (Gebru + Data Card layering)
- `scoring_evaluator.py`: rules/hybrid evaluation runner
- `tenacious_bench_v0.1/`: dataset partitions and labeling rounds
- `generation_scripts/`: authoring, partitioning, contamination, and agreement scripts
- `synthesis_memos/`: common-reading synthesis notes
- `cost_log.md`: budget and spend tracking

## Setup

Use Python 3.11+.

Install dependencies (stdlib-only scripts currently, no external package required):

`python -V`

## Reproduce interim artifacts

Run in order:

1. `python generation_scripts/author_benchmark.py`
2. `python generation_scripts/bootstrap_label_rounds.py`
3. `python generation_scripts/contamination_check.py`
4. `python scoring_evaluator.py --mode rules`
5. `python scoring_evaluator.py --mode hybrid`
6. `python generation_scripts/inter_rater_agreement.py`

Dummy-task evaluator check (Act I requirement):

- `python scoring_evaluator.py --mode rules --tasks-path dummy_tasks.jsonl`

## What is next

- replace lexical similarity proxy with embedding cosine checks
- connect hybrid judge scaffold to real OpenRouter calls
- prepare training_data for Path B preference/judge tuning
- run held-out ablations and package interim PDF/report visuals

## Phase III (implemented)

Path B training-data preparation is now implemented:

1. `python generation_scripts/prepare_path_b_training_data.py`
2. `python generation_scripts/check_training_data_contamination.py`

Artifacts:

- `training_data/path_b/preference_pairs_train.jsonl`
- `training_data/path_b/preference_pairs_val.jsonl`
- `training_data/path_b/summary.json`
- `training_data_contamination_check.json`
- `methodology_rationale.md`
