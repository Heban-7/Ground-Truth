# Training - Path B

This phase runs a preference-critic training baseline using the generated Path B pairs.

## Files

- `config.json` - training configuration
- `train_critic.py` - training script (linear ranking critic baseline)
- `artifacts/critic_model.json` - trained token-weight critic
- `artifacts/metrics.json` - train/val metrics + epoch history
- `artifacts/training_run.log` - human-readable run log

## Run

`python training/path_b/train_critic.py`

## Expected output

The script prints final train/val accuracy and writes artifacts under:

- `training/path_b/artifacts/`

This baseline is intentionally lightweight and deterministic so the pipeline can be validated before LoRA/DPO integration.
