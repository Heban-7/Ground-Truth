# Submission Ready Order (Copy/Paste Flow)

Use this exact order when filling the final submission form.

## Step 1: Repository link

1. Paste your GitHub repository URL.
2. Confirm the repo contains all files indexed in `submission_packet.md`.

## Step 2: Public artifacts

Paste these URLs:

1. HuggingFace dataset URL
2. HuggingFace model/judge URL (if publishing one)
3. Blog post URL
4. Community engagement URL
5. Demo video URL

Then update the same URLs in:

- `publication/publication_manifest.json`
- `final_submission_checklist.md`
- `submission_packet.md`

## Step 3: PDF artifacts

Upload:

1. Final two-page memo PDF (from `memo.md` content)
2. Final report PDF (from `final_pdf_ready_report.md`)

## Step 4: Quick integrity checks

Before submit, verify these files exist and are up to date:

- `evidence_graph.json`
- `ablations/ablation_results.json`
- `ablations/statistical_test_output.json`
- `ablations/held_out_traces.jsonl`
- `training/path_b/artifacts/training_run.log`
- `contamination_check.json`
- `training_data_contamination_check.json`
- `inter_rater_agreement.json`

## Step 5: Run readiness validator

Run:

`python generation_scripts/validate_submission_readiness.py`

Submit only when:

- missing_required_files is empty
- todo_occurrences is 0 (or only intentional placeholders you accept)
