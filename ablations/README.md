# Ablations

This phase evaluates three systems on held-out examples and writes final ablation artifacts.

Systems compared:

- `baseline_rules`
- `prompt_engineered_rules`
- `trained_critic`

Run:

`python ablations/run_ablations.py`

Outputs:

- `ablation_results.json`
- `held_out_traces.jsonl`

Metrics include:

- accuracy per system
- Delta A: trained critic vs baseline
- Delta B: trained critic vs prompt-engineered
- paired bootstrap CI and p-value
- cost/latency proxy table for Pareto reporting
