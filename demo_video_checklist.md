# Demo Video Checklist (<= 6 minutes)

## 1) Dataset walkthrough (HuggingFace-ready structure in repo)

- Open `tenacious_bench_v0.1/README.md`
- Show partition files:
  - `tenacious_bench_v0.1/train/tasks.jsonl`
  - `tenacious_bench_v0.1/dev/tasks.jsonl`
  - `tenacious_bench_v0.1/held_out/tasks.jsonl`
- Show `datasheet.md`

## 2) Score one task end-to-end

- Run: `python scoring_evaluator.py --mode rules --tasks-path dummy_tasks.jsonl`
- Explain one output row and pass/fail checks

## 3) Show one ablation result with traces

- Open `ablations/ablation_results.json`
- Highlight Delta A and Delta B fields
- Open `ablations/held_out_traces.jsonl`
- Trace one claim to source entries

## 4) Show evidence graph linkage

- Open `evidence_graph.json`
- Demonstrate one claim mapping to source file/path

## 5) Show publication placeholders

- Open `final_submission_checklist.md`
- Point out fields still requiring public URLs:
  - HuggingFace dataset URL
  - blog URL
  - community engagement URL

## Recording notes

- Keep terminal font zoomed in
- Narrate only key files/metrics
- Avoid scrolling long JSON quickly
