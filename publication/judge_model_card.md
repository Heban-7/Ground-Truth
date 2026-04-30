# Path B Critic Card (Draft)

## Model summary

This artifact is a lightweight preference critic baseline trained on synthetic chosen/rejected pairs derived from Tenacious-Bench train partition tasks.

## Training data

- source file: `training_data/path_b/preference_pairs_train.jsonl`
- validation file: `training_data/path_b/preference_pairs_val.jsonl`
- total pairs: 1040 (train 936 / val 104)

## Objective

Learn to prefer policy-safe outreach variants over policy-violating variants.

## Configuration snapshot

- seed: 42
- epochs: 6
- optimizer style: perceptron-like ranking updates
- representation: token-weight linear scorer

## Evaluation snapshot

- train pairwise accuracy: 100.0%
- validation pairwise accuracy: 100.0%
- held-out ablation:
  - baseline rules: 69.05%
  - trained critic: 69.05%
  - delta A: 0.00 pp
  - delta B vs prompt-engineered: +20.24 pp

## Intended use

- reliability gating experiments
- rejection-sampling policy checks
- ablation baselines before larger LLM judge training

## Limitations

- baseline linear model; not a final production critic
- synthetic preference pairs may overfit lexical artifacts
- requires stronger model and embedding-based contamination checks in next iteration
