import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATASET_DIR = ROOT / "tenacious_bench_v0.1"

BANNED_PHRASES = [
    "world-class",
    "top talent",
    "quick chat",
    "just following up",
]


def make_task(
    task_id: str,
    partition: str,
    source_mode: str,
    difficulty: str,
    signal_brief: str,
    subject: str,
    body: str,
    signal_confidence: str = "high",
    ai_maturity_score: str = "2",
) -> dict:
    return {
        "id": task_id,
        "source_mode": source_mode,
        "partition": partition,
        "difficulty": difficulty,
        "input": {
            "prospect_name": "Prospect",
            "company_name": "SampleCo",
            "channel": "email",
            "signal_brief": signal_brief,
            "signal_confidence": signal_confidence,
            "ai_maturity_score": ai_maturity_score,
            "bench_summary_ref": "bench_summary.json",
            "pricing_ref": "pricing_sheet.md",
        },
        "candidate_output": {"subject": subject, "body": body},
        "ground_truth": {
            "required_elements": [
                "at_least_one_specific_signal",
                "one_clear_ask",
                "no_external_bench_term",
            ],
            "forbidden_phrases": BANNED_PHRASES,
            "max_body_words": 120,
            "single_ask_required": True,
        },
        "rubric": {
            "direct": 4,
            "grounded": 4,
            "honest": 4,
            "professional": 4,
            "non_condescending": 4,
            "pass_threshold_per_dimension": 4,
        },
    }


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=True) + "\n")


def main() -> None:
    train_tasks = [
        make_task(
            task_id="task_1001",
            partition="train",
            source_mode="programmatic",
            difficulty="easy",
            signal_brief="$9M Series A in March and backend roles increased from 1 to 4.",
            subject="Request: 15 minutes on your backend hiring",
            body=(
                "Hi team, I saw your $9M Series A in March and backend roles moving from 1 to 4. "
                "We place managed backend and data engineers with timezone overlap. "
                "Would 15 minutes next week be useful to compare options? Best, Yabi"
            ),
        ),
        make_task(
            task_id="task_1002",
            partition="train",
            source_mode="trace_derived",
            difficulty="medium",
            signal_brief="12% contraction in March with continued data hiring.",
            subject="Context: cost-aware data capacity after restructure",
            body=(
                "Hi team, I saw the 12% contraction in March and continued data hiring. "
                "If delivery needs are still active, we can provide managed data engineering capacity "
                "with one-month minimum terms. Would a short scoping call help this week? Best, Yabi"
            ),
        ),
        make_task(
            task_id="task_1003",
            partition="train",
            source_mode="hand_authored",
            difficulty="hard",
            signal_brief="New CTO announced on April 14 and vendor review expected in first 90 days.",
            subject="Context: vendor model brief for new CTO",
            body=(
                "Hi, welcome to the new CTO role announced on April 14. "
                "Many teams review vendor mix in the first 90 days, so I can share a one-page brief "
                "on common offshore models and trade-offs. Want me to send the brief? Best, Yabi"
            ),
        ),
    ]

    dev_tasks = [
        make_task(
            task_id="task_2001",
            partition="dev",
            source_mode="hand_authored",
            difficulty="easy",
            signal_brief="$14M Series A in February and Python roles increased from 2 to 7 in 60 days.",
            subject="Request: 15 minutes on your Q3 Python hiring",
            body=(
                "Hi Maya, You closed your $14M Series A in February and your open Python roles moved "
                "from 2 to 7 in the last 60 days. We place managed Python and data engineers with "
                "at least three hours of timezone overlap. Would 15 minutes next week be useful to "
                "compare options? Best, Yabi"
            ),
        ),
        make_task(
            task_id="task_2002",
            partition="dev",
            source_mode="multi_llm_synthesis",
            difficulty="medium",
            signal_brief="Two open data engineer roles, signal confidence low.",
            subject="Question: are your data hires keeping pace?",
            body=(
                "Hi, I noticed two open data engineer roles. I cannot tell from public signal whether "
                "that matches demand or if the queue is longer. If the queue is longer, we can provide "
                "managed data capacity quickly. Would 15 minutes be useful? Best, Yabi"
            ),
            signal_confidence="low",
            ai_maturity_score="1",
        ),
    ]

    held_out_tasks = [
        make_task(
            task_id="task_3001",
            partition="held_out",
            source_mode="hand_authored",
            difficulty="hard",
            signal_brief="AI maturity score 2 with three named peers hiring MLOps in last 90 days.",
            subject="Question: your MLOps roadmap for 2026",
            body=(
                "Hi, three named peers posted senior MLOps roles in the last 90 days while your team "
                "has not publicly posted one. That may be intentional, or not yet scoped. "
                "If useful, I can share a concise peer pattern brief and discuss options in 15 minutes. "
                "Best, Yabi"
            ),
        ),
    ]

    write_jsonl(DATASET_DIR / "train" / "tasks.jsonl", train_tasks)
    write_jsonl(DATASET_DIR / "dev" / "tasks.jsonl", dev_tasks)
    write_jsonl(DATASET_DIR / "held_out" / "tasks.jsonl", held_out_tasks)
    print("Seed dataset written to train/dev/held_out.")


if __name__ == "__main__":
    main()
