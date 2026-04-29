import argparse
import json
import re
from pathlib import Path

from generation_scripts.judge_scaffold import build_judge_prompt, parse_judge_response


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


def evaluate_task_rules(task: dict) -> dict:
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

    return {"passed": all(checks.values()), "checks": checks}


def _mock_judge_raw_response(task: dict, rule_passed: bool) -> str:
    """
    Placeholder judge output for local development.
    Swap this function with a real API call in a future step.
    """
    reasoning = (
        "Draft matches core style constraints and references the provided signal."
        if rule_passed
        else "Draft violates one or more hard policy checks."
    )
    high = 5 if rule_passed else 3
    low = 4 if rule_passed else 2
    payload = {
        "direct": high,
        "grounded": high,
        "honest": low,
        "professional": high,
        "non_condescending": high,
        "reasoning": reasoning,
    }
    return json.dumps(payload, ensure_ascii=True)


def evaluate_task(task: dict, mode: str) -> dict:
    rule_eval = evaluate_task_rules(task)
    result = {
        "id": task["id"],
        "mode": mode,
        "passed": rule_eval["passed"],
        "checks": rule_eval["checks"],
    }

    if mode == "hybrid":
        # We still build the prompt now so this evaluator can be wired to API quickly later.
        judge_prompt = build_judge_prompt(task)
        raw = _mock_judge_raw_response(task, rule_eval["passed"])
        judge_scores = parse_judge_response(raw)
        judge_passed = all(
            judge_scores[k] >= task["rubric"]["pass_threshold_per_dimension"]
            for k in ["direct", "grounded", "honest", "professional", "non_condescending"]
        )
        result["judge"] = {
            "passed": judge_passed,
            "scores": judge_scores,
            "prompt_preview": judge_prompt[:240] + "...",
        }
        result["passed"] = result["passed"] and judge_passed

    return result


def load_tasks_jsonl(path: Path) -> list[dict]:
    tasks = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                tasks.append(json.loads(line))
    return tasks


def evaluate_file(tasks_path: Path, mode: str) -> dict:
    tasks = load_tasks_jsonl(tasks_path)
    results = [evaluate_task(t, mode=mode) for t in tasks]
    return {
        "mode": mode,
        "input_file": str(tasks_path),
        "summary": summarize(results),
        "results": results,
    }


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


def evaluate_partition(partition: str, mode: str) -> dict:
    tasks_path = Path(f"tenacious_bench_v0.1/{partition}/tasks.jsonl")
    tasks = load_tasks_jsonl(tasks_path)
    results = [evaluate_task(t, mode=mode) for t in tasks]
    return {
        "partition": partition,
        "mode": mode,
        "summary": summarize(results),
        "results": results,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate Tenacious benchmark tasks.")
    parser.add_argument(
        "--mode",
        choices=["rules", "hybrid"],
        default="rules",
        help="rules=deterministic checks only, hybrid=rules + judge scaffold",
    )
    parser.add_argument(
        "--tasks-path",
        default="",
        help="Optional JSONL file path. If provided, evaluates only that file.",
    )
    args = parser.parse_args()

    if args.tasks_path:
        output = evaluate_file(Path(args.tasks_path), mode=args.mode)
        print(json.dumps(output, indent=2))
        raise SystemExit(0)

    partition_reports = [
        evaluate_partition("train", mode=args.mode),
        evaluate_partition("dev", mode=args.mode),
        evaluate_partition("held_out", mode=args.mode),
    ]

    overall_results = []
    for report in partition_reports:
        overall_results.extend(report["results"])

    output = {
        "mode": args.mode,
        "partitions": partition_reports,
        "overall_summary": summarize(overall_results),
    }
    print(json.dumps(output, indent=2))
