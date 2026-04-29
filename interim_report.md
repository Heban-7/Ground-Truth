# Interim Report (Acts I + II)

## 1) Bench composition

From `generation_scripts/logs/seed_counts.json`:

- total raw authored tasks: 210
- deduplicated tasks: 209
- accepted tasks after judge filter: 209
- partitions:
  - train: 104
  - dev: 63
  - held_out: 42
- source-mode distribution:
  - trace_derived: 63
  - programmatic: 62
  - multi_llm_synthesis: 52
  - hand_authored: 32

## 2) Inter-rater agreement

From `inter_rater_agreement.md` (30-task subset):

- threshold: 80% per dimension
- overall agreement: 82.67%
- per-dimension:
  - direct: 80.00%
  - grounded: 80.00%
  - honest: 83.33%
  - professional: 86.67%
  - non_condescending: 83.33%

Result: pass for all dimensions.

## 3) Three example tasks with rubric application

### A) Programmatic task (example pattern)

- source_mode: `programmatic`
- signal type: funding + role growth
- expected behavior: direct, one ask, specific signal mention
- rubric expectation: high `direct`, `grounded`, `professional`

### B) Trace-derived task (example pattern)

- source_mode: `trace_derived`
- signal type: contraction + continued hiring
- expected behavior: cost-sensitive framing without over-commitment
- rubric expectation: high `honest` and `non_condescending`

### C) Hand-authored adversarial task (example pattern)

- source_mode: `hand_authored`
- signal type: leadership transition / capability-gap ambiguity
- expected behavior: no fabricated certainty, respectful ask-or-ignore framing
- rubric expectation: high `honest` and `non_condescending`

## 4) What is working

- authoring pipeline is reproducible and deterministic (`seed=42`)
- contamination report currently passes all checks
- evaluator supports both deterministic and hybrid judge-scaffold modes
- inter-rater workflow is implemented and passing threshold

## 5) What is not yet complete

- lexical similarity proxy should be replaced with embedding cosine checks
- hybrid evaluator still uses a mock judge response (API integration pending)
- benchmark uses proxy traces because Week 10 artifacts are absent

## 6) Plan for Days 4-7

1. connect hybrid judge to OpenRouter with strict JSON parser contract
2. create `training_data/` for Path B (chosen/rejected pairs)
3. run Path B training experiment and hold-out ablations
4. produce `ablation_results.json` and claim-to-evidence mapping
5. package public artifact set for HuggingFace + blog + community post
