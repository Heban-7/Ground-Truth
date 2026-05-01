import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "submission_readiness_report.json"


REQUIRED_FILES = [
    "submission_packet.md",
    "submission_ready_order.md",
    "final_submission_checklist.md",
    "final_pdf_ready_report.md",
    "memo.md",
    "evidence_graph.json",
    "datasheet.md",
    "methodology.md",
    "methodology_rationale.md",
    "training_data/path_b/preference_pairs_train.jsonl",
    "training_data/path_b/preference_pairs_val.jsonl",
    "training/path_b/artifacts/training_run.log",
    "training/path_b/artifacts/metrics.json",
    "ablations/ablation_results.json",
    "ablations/statistical_test_output.json",
    "ablations/held_out_traces.jsonl",
    "contamination_check.json",
    "training_data_contamination_check.json",
    "inter_rater_agreement.json",
]

TODO_SCAN_FILES = [
    "submission_packet.md",
    "final_submission_checklist.md",
    "publication/publication_manifest.json",
    "final_pdf_ready_report.md",
]


def main() -> None:
    missing = []
    for rel in REQUIRED_FILES:
        if not (ROOT / rel).exists():
            missing.append(rel)

    todo_hits = []
    for rel in TODO_SCAN_FILES:
        path = ROOT / rel
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        cnt = text.count("TODO")
        if cnt > 0:
            todo_hits.append({"file": rel, "todo_count": cnt})

    report = {
        "ready_for_submission": len(missing) == 0,
        "missing_required_files": missing,
        "todo_occurrences": sum(x["todo_count"] for x in todo_hits),
        "todo_breakdown": todo_hits,
        "notes": [
            "Replace TODO URLs before final submission.",
            "Some TODOs may be intentional if public artifacts are not published yet.",
        ],
    }

    REPORT_PATH.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
