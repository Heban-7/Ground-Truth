# Week 11 Interim Report (Acts I + II)

## 1) Bench Composition

Current dataset snapshot (`tenacious_bench_v0.1`):

- Total accepted tasks: **209** (from 210 raw authored tasks)
- Partition counts:
  - `train`: **104**
  - `dev`: **63**
  - `held_out`: **42**

Counts by source mode:


- `trace_derived`: **63**
- `programmatic`: **62**
- `multi_llm_synthesis`: **52**
- `hand_authored` (adversarial slice): **32**

Counts by difficulty dimension:

- `easy`: **77**
- `medium`: **59**
- `hard`: **73**

Counts by segment dimension:

- `leadership_transition`: **62**
- `series_a_b_funded`: **54**
- `restructure_cost_pressure`: **50**
- `specialized_capability_gap`: **43**

Counts by signal-confidence dimension:

- `high`: **68**
- `medium`: **75**
- `low`: **66**

## 2) Inter-rater Agreement Results

From `inter_rater_agreement.json` on a 30-task two-round labeling subset:

- Threshold: **80% agreement per dimension**
- Overall agreement: **82.67%**
- Overall pass: **True**

Per-dimension agreement:

- `direct`: **80.00%** (24/30)
- `grounded`: **80.00%** (24/30)
- `honest`: **83.33%** (25/30)
- `professional`: **86.67%** (26/30)
- `non_condescending`: **83.33%** (25/30)

## 3) Three Example Tasks with Rubric Application

### A) Programmatic example

- Task ID: `tb_0111`
- Source mode: `programmatic`
- Partition: `train`
- Difficulty: `easy`
- Input signal brief: `New CTO announcement in May 2026; vendor reassessment expected in first 90 days.`
- Candidate subject: `Request: 15 minutes on your ML hiring`
- Candidate body: `Hi, your brief shows New CTO announcement in May 2026; vendor reassessment expected in first 90 days. We support teams with managed ML and Data engineering capacity on one-month terms. Would 15 minutes be useful to compare options? Best, Yabi`

Rubric application (hybrid evaluation):

- Hard checks:
  - max body words: pass
  - banned phrase scan: pass
  - single ask: pass
  - signal grounding overlap: pass
- Judge scores:
  - direct: 5
  - grounded: 5
  - honest: 4
  - professional: 5
  - non_condescending: 5
- Final pass: **True**

### B) Trace-derived example

- Task ID: `tb_0017`
- Source mode: `trace_derived`
- Partition: `train`
- Difficulty: `easy`
- Input signal brief: `New CTO announcement in April 2024; vendor reassessment expected in first 90 days.`
- Candidate subject: `Context: Python capacity planning in 2024`
- Candidate body: `Hi, I saw your New CTO announcement in April 2024; vendor reassessment expected in first 90 days. If delivery demand is still active, we can provide managed Python engineers with timezone overlap. Would a 15-minute scoping call be useful next week? Best, Yabi`

Rubric application (hybrid evaluation):

- Hard checks: all pass
- Judge scores: direct 5, grounded 5, honest 4, professional 5, non_condescending 5
- Final pass: **True**

### C) Adversarial (hand-authored) example

- Task ID: `tb_0208`
- Source mode: `hand_authored`
- Partition: `train`
- Difficulty: `hard`
- Input signal brief: `15% headcount contraction announced in September 2026; continued hiring for ML roles.`
- Candidate subject: `Resource: ML scaling checklist (September update)`
- Candidate body: `Hi, 15% headcount contraction announced in September 2026; continued hiring for ML roles. I prepared a one-page checklist on when managed ML support pays off and when it does not. Want me to send it? Best, Yabi`

Rubric application (hybrid evaluation):

- Hard checks: all pass
- Judge scores: direct 5, grounded 5, honest 4, professional 5, non_condescending 5
- Final pass: **True**

## 4) What Is Working, What Is Not, Plan for Days 4-7

What is working:

- Reproducible authoring pipeline (`author_benchmark.py`) produces stable dataset outputs.
- Partitioning protocol is aligned with interim target ratio (50/30/20).
- Contamination checks currently pass (0 n-gram violations, 0 similarity violations, 0 time-anchor warnings).
- Inter-rater agreement passed threshold across all five rubric dimensions.
- Evaluator supports both deterministic (`rules`) and hybrid (`rules + judge scaffold`) modes.

What is not yet complete:

- Similarity contamination check uses lexical proxy; embedding-based cosine is pending.
- Hybrid judge still uses a local mock response (API call integration pending).
- Week 10 true artifacts are unavailable; interim evidence is proxy-based and explicitly disclosed.
- Full interim PDF export and figure formatting are not yet packaged.

Plan for Days 4-7:

1. Integrate real OpenRouter judge calls into hybrid evaluator with strict JSON parser contract.
2. Build `training_data/` for Path B (chosen/rejected pairs + leakage-safe generation/judge routing).
3. Run Path B training experiment and produce initial hold-out deltas.
4. Generate `ablation_results.json` and link numeric claims to source artifacts.
5. Prepare public artifact packaging path (HF dataset draft, model/judge card draft, blog outline).
