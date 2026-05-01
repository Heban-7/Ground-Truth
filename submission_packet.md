# Week 11 Submission Packet

Use this file as the single handoff index for final submission.

## 1) GitHub Repo Deliverables

- `README.md`
- `audit_memo.md`
- `schema.json`
- `scoring_evaluator.py`
- `datasheet.md`
- `methodology.md`
- `methodology_rationale.md`
- `cost_log.md`
- `evidence_graph.json`

### Dataset partitions

- `tenacious_bench_v0.1/train/tasks.jsonl`
- `tenacious_bench_v0.1/dev/tasks.jsonl`
- `tenacious_bench_v0.1/held_out/tasks.jsonl`

### Generation + validation

- `generation_scripts/author_benchmark.py`
- `generation_scripts/contamination_check.py`
- `contamination_check.json`
- `inter_rater_agreement.json`
- `inter_rater_agreement.md`

### Training data + rationale

- `training_data/path_b/preference_pairs_train.jsonl`
- `training_data/path_b/preference_pairs_val.jsonl`
- `training_data/path_b/summary.json`
- `training_data_contamination_check.json`
- `methodology_rationale.md`

### Training run artifacts

- `training/path_b/train_critic.py`
- `training/path_b/config.json`
- `training/path_b/artifacts/critic_model.json`
- `training/path_b/artifacts/metrics.json`
- `training/path_b/artifacts/training_run.log`

### Ablation artifacts

- `ablations/ablation_results.json`
- `ablations/held_out_traces.jsonl`
- `ablations/statistical_test_output.json`

### Synthesis memos

- `synthesis_memos/01_synthetic_data_best_practices.md`
- `synthesis_memos/02_llm_as_a_judge_survey.md`
- `synthesis_memos/03_datasheets_and_data_cards.md`
- `synthesis_memos/04_contamination_survey.md`
- `synthesis_memos/05_dpo_foundations.md`
- `synthesis_memos/06_preference_leakage.md`
- `synthesis_memos/07_prometheus2_judge_design.md`

## 2) Public Artifact URLs (fill before submit)

- HuggingFace dataset URL: `TODO`
- HuggingFace model URL (if applicable): `N/A for Path B baseline` (or `TODO` if publishing critic artifact)
- Blog post URL: `TODO`
- Community engagement URL: `TODO`

## 3) PDF Memo and Report

- Two-page memo draft: `memo.md`
- Final report (PDF-ready): `final_pdf_ready_report.md`
- Interim report (PDF-ready): `interim_pdf_ready_report.md`

## 4) Demo Package

- Demo checklist: `demo_video_checklist.md`
- Demo video URL: `TODO`

## 5) Final Checks

- Final checklist tracker: `final_submission_checklist.md`
- Publication bundle index: `publication/README.md`
- Publication manifest: `publication/publication_manifest.json`

---

Last-mile note: once URLs are available, update:

1. `final_submission_checklist.md`
2. `publication/publication_manifest.json`
3. this file (`submission_packet.md`)
