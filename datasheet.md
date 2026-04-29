# Datasheet: Tenacious-Bench v0.1 (Interim)

## 1) Motivation

Tenacious-Bench v0.1 evaluates sales-agent outreach quality for Tenacious-style B2B delivery workflows. The benchmark exists because general-purpose benchmarks and retail-centric suites do not measure key business risks in this domain: unsupported capacity commitments, fabricated signal claims, condescending language toward engineering leaders, and policy-unsafe pricing statements.

Primary goals:

- measure trust-preserving outreach behavior under realistic hiring-signal inputs
- provide machine-verifiable scoring for iteration speed
- enable low-cost, contamination-aware evaluation before model training

Intended users:

- training participants building judge/critic or generation adapters
- reliability engineers maintaining outbound communication policy controls
- benchmark researchers studying domain-specific LLM evaluation

## 2) Composition

Each task is a JSON object with:

- metadata (`id`, `source_mode`, `partition`, `difficulty`)
- input context (`signal_brief`, confidence, AI maturity score)
- candidate output (`subject`, `body`)
- ground-truth policy constraints (word limit, banned phrases, one-ask rule)
- rubric scores for five tone dimensions

Current interim composition:

- total accepted tasks: 209 (from 210 raw, 1 deduplicated)
- partition ratio: train 50%, dev 30%, held_out 20%
- source-mode mix:
  - trace-derived ~30%
  - programmatic ~30%
  - multi-LLM synthesis ~25%
  - hand-authored adversarial ~15%

Data format:

- storage: JSONL (`tasks.jsonl`) per partition
- schema: `schema.json`

## 3) Collection process

Because Week 10 artifacts are missing in this repo, v0.1 uses controlled synthetic reconstruction:

1. template-driven generation with deterministic seed (`author_benchmark.py`)
2. deduplication by normalized subject/body key
3. judge-style filtering with deterministic policy checks
4. partitioning into train/dev/held_out

Routing policy metadata is recorded in `generation_scripts/logs/model_routes.json` to document intended model-family separation between generation and judging.

## 4) Preprocessing / cleaning / labeling

Preprocessing:

- normalize and deduplicate near-identical candidates
- enforce hard checks:
  - max body length
  - banned phrase exclusion
  - single ask constraint
  - minimal signal overlap

Labeling:

- rubric dimensions: direct, grounded, honest, professional, non-condescending
- two-round label comparison workflow implemented in `inter_rater_agreement.py`
- interim pilot labels stored in `tenacious_bench_v0.1/labeling/`

Quality controls:

- contamination checks (`contamination_check.py`)
  - 8-gram overlap rule
  - lexical similarity proxy threshold
  - held-out time-anchor warning

## 5) Uses

Supported uses:

- benchmark evaluation for sales-outreach quality
- training-data filtering for Path B judge/critic experiments
- rule-and-judge hybrid scoring ablations

Out-of-scope uses:

- legal/compliance automation without human review
- direct prospect contact without deployment guardrails
- high-stakes pricing/contract generation

## 6) Distribution

Repository distribution (interim):

- benchmark data under `tenacious_bench_v0.1/`
- generation and evaluation scripts under `generation_scripts/`
- reports at repo root (`contamination_check.json`, `inter_rater_agreement.*`)

Planned public release:

- HuggingFace dataset after sealed held-out protocol and publication checklist review
- recommended license: CC-BY-4.0 (subject to final staff sign-off)

## 7) Maintenance

Versioning:

- semantic-style versions (`v0.1`, `v0.2`, ...)
- each update must include updated contamination report and changelog summary

Monitoring:

- regression checks via `scoring_evaluator.py --mode rules`
- optional hybrid judge scaffold via `--mode hybrid`

Known limitations (interim):

- synthetic traces are proxy replacements for missing Week 10 logs
- similarity check currently uses lexical proxy, not embedding cosine
- held-out is partitioned but not yet externally sealed/released protocol

## Data Card Layering (Pushkarna extension)

### Telescopic (at-a-glance)

- domain: B2B sales outreach reliability
- size: 209 tasks
- objective: policy-safe + tone-aligned evaluation
- key risks: synthetic bias, label drift, contamination leakage

### Periscopic (workflow details)

- authoring modes mixed by fixed target percentages
- deterministic generation seed for reproducibility
- rule-based filtering before judge integration
- inter-rater threshold: 80% per dimension

### Microscopic (field-level)

- `input.signal_brief`: primary grounding source
- `ground_truth.forbidden_phrases`: hard lexical policy list
- `rubric.pass_threshold_per_dimension`: minimum score gate
- `metadata.route_model` and `metadata.judge_model`: provenance traceability
