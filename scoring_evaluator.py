import json
import re
from pathlib import Path


def word_count(text: str) -> int:
    return len(re.findall(r"\b\w+\b", text))


def count_question_marks(text: str) -> int:
    return text.count("?")


def contains_any_phrase(text: str, phrases: list[str]) -> bool:
    lowered = text.lower()
    return any(p.lower() in lowered for p in phrases)


def has_signal_overlap(signal_brief: str, body: str) -> bool:
    brief_tokens = set(re.findall(r"[a-zA-Z0-9$]+", signal_brief.lower()))
    body_tokens = set(re.findall(r"[a-zA-Z0-9$]+", body.lower()))
    # Ignore tiny tokens to reduce noise.
    brief_tokens = {t for t in brief_tokens if len(t) >= 3}
    overlap = brief_tokens.intersection(body_tokens)
    return len(overlap) >= 3


def evaluate_task(task: dict) -> dict:
    body = task["candidate_output"]["body"]
    subject = task["candidate_output"]["subject"]
    gt = task["ground_truth"]
    signal_brief = task["input"]["signal_brief"]

    checks = {}
    checks["max_body_words"] = word_count(body) <= gt["max_body_words"]
    checks["banned_phrases"] = not contains_any_phrase(
        f"{subject} {body}", gt["forbidden_phrases"]
    )
    checks["single_ask_required"] = (
        count_question_marks(body) <= 1 if gt["single_ask_required"] else True
    )
    checks["signal_grounding"] = has_signal_overlap(signal_brief, body)

    passed = all(checks.values())
    return {"id": task["id"], "passed": passed, "checks": checks}


def load_tasks_jsonl(path: Path) -> list[dict]:
    tasks = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                tasks.append(json.loads(line))
    return tasks


def summarize(results: list[dict]) -> dict:
    total = len(results)
    passed = sum(1 for r in results if r["passed"])
    failed = total - passed
    return {
        "total": total,
        "passed": passed,
        "failed": failed,
        "pass_rate": round((passed / total) * 100, 2) if total else 0.0,
    }


def evaluate_partition(partition: str) -> dict:
    tasks_path = Path(f"tenacious_bench_v0.1/{partition}/tasks.jsonl")
    tasks = load_tasks_jsonl(tasks_path)
    results = [evaluate_task(t) for t in tasks]
    return {
        "partition": partition,
        "summary": summarize(results),
        "results": results,
    }


if __name__ == "__main__":
    partition_reports = [
        evaluate_partition("train"),
        evaluate_partition("dev"),
        evaluate_partition("held_out"),
    ]

    overall_results = []
    for report in partition_reports:
        overall_results.extend(report["results"])

    output = {
        "partitions": partition_reports,
        "overall_summary": summarize(overall_results),
    }
    print(json.dumps(output, indent=2))
