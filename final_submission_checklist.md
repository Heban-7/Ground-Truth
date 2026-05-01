# Final Submission Checklist

## Repository artifacts

- [x] `audit_memo.md`
- [x] `schema.json`
- [x] `scoring_evaluator.py`
- [x] `tenacious_bench_v0.1/train/tasks.jsonl`
- [x] `tenacious_bench_v0.1/dev/tasks.jsonl`
- [x] `tenacious_bench_v0.1/held_out/tasks.jsonl`
- [x] `datasheet.md`
- [x] `methodology.md`
- [x] `methodology_rationale.md`
- [x] `training_data/path_b/preference_pairs_train.jsonl`
- [x] `training_data/path_b/preference_pairs_val.jsonl`
- [x] `training/path_b/train_critic.py`
- [x] `training/path_b/artifacts/training_run.log`
- [x] `ablations/ablation_results.json`
- [x] `ablations/held_out_traces.jsonl`
- [x] `evidence_graph.json`
- [x] `memo.md`
- [x] `ablations/statistical_test_output.json`
- [x] `final_pdf_ready_report.md`

## Public artifacts (fill before final)

- [ ] HuggingFace dataset URL: `TODO`
- [ ] HuggingFace model/judge URL (if publishing): `TODO`
- [ ] Blog post URL: `TODO`
- [ ] Community engagement URL (issue/submission/PR): `TODO`
- [ ] Publication manifest URLs updated: `publication/publication_manifest.json`

## Demo package

- [x] Demo structure script: `demo_video_checklist.md`
- [ ] Recorded demo video URL (no-login): `TODO`

## Integrity checks

- [x] Benchmark contamination check pass (`contamination_check.json`)
- [x] Training-data contamination check pass (`training_data_contamination_check.json`)
- [x] Inter-rater agreement pass (`inter_rater_agreement.json`)
- [x] Claims mapped in `evidence_graph.json`

## Known constraints (declare openly)

- Week 10 artifacts unavailable; proxy trace/probe IDs used with explicit disclosure.
- Delta C (vs tau-squared Week 10 score) not reported because no Week 10 score available in repo.

## Synthesis memo completeness

- [x] 4 common memos completed (`01`-`04`)
- [x] 3 Path B memos completed (`05`-`07`)
