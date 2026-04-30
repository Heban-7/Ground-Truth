import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PUBLICATION_DIR = ROOT / "publication"
MANIFEST_PATH = PUBLICATION_DIR / "publication_manifest.json"


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    seed_counts = read_json(ROOT / "generation_scripts" / "logs" / "seed_counts.json")
    ablations = read_json(ROOT / "ablations" / "ablation_results.json")
    inter_rater = read_json(ROOT / "inter_rater_agreement.json")
    contamination = read_json(ROOT / "contamination_check.json")
    td_contamination = read_json(ROOT / "training_data_contamination_check.json")

    manifest = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "project": {
            "name": "tenacious_bench_v0.1",
            "path_declaration": "Path B (judge/critic)",
        },
        "metrics_snapshot": {
            "benchmark_tasks": seed_counts["filtered_count"],
            "partition_counts": seed_counts["partition_counts"],
            "source_counts": seed_counts["source_counts"],
            "inter_rater_overall_percent": inter_rater["overall_percent"],
            "held_out_contamination_pass": contamination["pass"],
            "training_data_contamination_pass": td_contamination["pass"],
            "delta_a_pp": ablations["deltas"]["delta_a_trained_vs_baseline"]["delta_percent_points"],
            "delta_b_pp": ablations["deltas"]["delta_b_trained_vs_prompt_engineered"][
                "delta_percent_points"
            ],
        },
        "publication_targets": {
            "huggingface_dataset_url": "TODO",
            "huggingface_model_or_judge_url": "TODO",
            "blog_post_url": "TODO",
            "community_engagement_url": "TODO",
            "demo_video_url": "TODO",
        },
        "artifact_links": {
            "datasheet": "datasheet.md",
            "methodology": "methodology.md",
            "methodology_rationale": "methodology_rationale.md",
            "evidence_graph": "evidence_graph.json",
            "ablation_results": "ablations/ablation_results.json",
            "held_out_traces": "ablations/held_out_traces.jsonl",
            "cost_log": "cost_log.md",
            "memo": "memo.md",
        },
    }

    PUBLICATION_DIR.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"Wrote {MANIFEST_PATH}")


if __name__ == "__main__":
    main()
