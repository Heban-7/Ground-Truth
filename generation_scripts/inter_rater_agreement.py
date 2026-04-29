import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LABEL_DIR = ROOT / "tenacious_bench_v0.1" / "labeling"
ROUND1_PATH = LABEL_DIR / "round1_labels.jsonl"
ROUND2_PATH = LABEL_DIR / "round2_labels.jsonl"
OUTPUT_JSON = ROOT / "inter_rater_agreement.json"
OUTPUT_MD = ROOT / "inter_rater_agreement.md"

DIMENSIONS = ["direct", "grounded", "honest", "professional", "non_condescending"]
PASS_THRESHOLD = 80.0


def load_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def to_map(rows: list[dict]) -> dict[str, dict]:
    return {row["id"]: row for row in rows}


def percent(numerator: int, denominator: int) -> float:
    if denominator == 0:
        return 0.0
    return round((numerator / denominator) * 100, 2)


def compute_agreement(round1: dict[str, dict], round2: dict[str, dict]) -> dict:
    shared_ids = sorted(set(round1.keys()).intersection(round2.keys()))
    if not shared_ids:
        raise ValueError("No overlapping task IDs between round1 and round2.")

    per_dimension = {}
    failing_dimensions = []

    for dim in DIMENSIONS:
        matches = 0
        for task_id in shared_ids:
            if round1[task_id][dim] == round2[task_id][dim]:
                matches += 1
        agreement = percent(matches, len(shared_ids))
        per_dimension[dim] = {
            "matches": matches,
            "total": len(shared_ids),
            "agreement_percent": agreement,
            "passes_threshold": agreement >= PASS_THRESHOLD,
        }
        if agreement < PASS_THRESHOLD:
            failing_dimensions.append(dim)

    overall_matches = 0
    overall_total = len(shared_ids) * len(DIMENSIONS)
    for task_id in shared_ids:
        for dim in DIMENSIONS:
            if round1[task_id][dim] == round2[task_id][dim]:
                overall_matches += 1

    overall = percent(overall_matches, overall_total)

    return {
        "shared_task_count": len(shared_ids),
        "task_ids": shared_ids,
        "pass_threshold_percent": PASS_THRESHOLD,
        "per_dimension": per_dimension,
        "overall_percent": overall,
        "overall_pass": all(v["passes_threshold"] for v in per_dimension.values()),
        "failing_dimensions": failing_dimensions,
    }


def write_markdown(report: dict) -> None:
    lines = []
    lines.append("# Inter-rater agreement (pilot)\n")
    lines.append(
        "This is a pilot run on a 30-task benchmark subset. Production protocol keeps the same structure with a strict 24-hour relabel gap.\n"
    )
    lines.append(f"- Shared tasks: {report['shared_task_count']}")
    lines.append(f"- Threshold per dimension: {report['pass_threshold_percent']}%")
    lines.append(f"- Overall agreement: {report['overall_percent']}%")
    lines.append(f"- Overall pass: {report['overall_pass']}\n")
    lines.append("## Per-dimension agreement")
    for dim in DIMENSIONS:
        d = report["per_dimension"][dim]
        lines.append(
            f"- {dim}: {d['agreement_percent']}% ({d['matches']}/{d['total']}), pass={d['passes_threshold']}"
        )

    if report["failing_dimensions"]:
        lines.append("\n## Action required")
        lines.append(
            "- Revise rubric guidance for these dimensions: "
            + ", ".join(report["failing_dimensions"])
        )
    else:
        lines.append("\n## Action required")
        lines.append("- No rubric revision required at this stage.")

    OUTPUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    round1 = to_map(load_jsonl(ROUND1_PATH))
    round2 = to_map(load_jsonl(ROUND2_PATH))
    report = compute_agreement(round1, round2)

    with OUTPUT_JSON.open("w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    write_markdown(report)
    print(f"Wrote: {OUTPUT_JSON.name} and {OUTPUT_MD.name}")
    print(json.dumps({"overall_percent": report["overall_percent"]}, indent=2))


if __name__ == "__main__":
    main()
