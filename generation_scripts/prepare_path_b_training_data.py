import json
import random
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATASET_DIR = ROOT / "tenacious_bench_v0.1"
OUTPUT_DIR = ROOT / "training_data" / "path_b"

SEED = 42
NEGATIVES_PER_TASK = 10
TRAIN_SPLIT = 0.9


def load_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=True) + "\n")


def one_line(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def build_prompt(task: dict) -> str:
    md = task.get("metadata", {})
    inp = task["input"]
    # Structured prompt reduces accidental lexical overlap with dev/held narratives.
    return (
        f"task_id={task['id']} | company={inp['company_name']} | "
        f"segment={md.get('segment','unknown')} | event={md.get('event_month','NA')}-{md.get('event_year','NA')} | "
        f"stack={md.get('stack','NA')} | signal_confidence={inp['signal_confidence']} | "
        f"ai_maturity={inp['ai_maturity_score']} | channel={inp['channel']}"
    )


def mutate_subject(subject: str, rejection_type: str) -> str:
    if rejection_type == "banned_phrase":
        return f"Quick chat: {subject}"
    if rejection_type == "fake_urgency":
        return f"URGENT: {subject}"
    if rejection_type == "condescending_frame":
        return f"{subject} (you are behind the curve)"
    return subject


def mutate_body(task: dict, rejection_type: str) -> str:
    body = one_line(task["candidate_output"]["body"])
    signal_conf = task["input"]["signal_confidence"]
    company = task["input"]["company_name"]

    if rejection_type == "banned_phrase":
        return body + " We have world-class top talent ready now."
    if rejection_type == "fake_urgency":
        return body + " This is the last slot and you must sign by Friday."
    if rejection_type == "multi_ask":
        return body + " Can we schedule 15 minutes? Also send your roadmap and budget?"
    if rejection_type == "bench_overcommit":
        return body + " We can commit 15 engineers in two weeks with no risk."
    if rejection_type == "fabricated_signal":
        return (
            f"Congrats on your $40M Series C last month at {company}. "
            + body
        )
    if rejection_type == "passive_aggressive":
        return body + " Per my last email, I need a reply by end of day."
    if rejection_type == "condescending_frame":
        return body + " Your leadership is behind peers on this decision."
    if rejection_type == "confidence_mismatch":
        if signal_conf == "low":
            return body + " You are clearly scaling aggressively right now."
        return body + " You might not be growing at all."
    if rejection_type == "pricing_fabrication":
        return body + " The total 12-month contract is exactly $1.2M, sign now."
    # default: style drift
    return body + " We can synergize your ecosystem and 10x outcomes quickly."


def build_preference_pair(task: dict, rejection_type: str, pair_idx: int) -> dict:
    chosen = {
        "subject": one_line(task["candidate_output"]["subject"]),
        "body": one_line(task["candidate_output"]["body"]),
    }
    rejected = {
        "subject": mutate_subject(chosen["subject"], rejection_type),
        "body": mutate_body(task, rejection_type),
    }
    return {
        "pair_id": f"{task['id']}_neg_{pair_idx:02d}",
        "source_task_id": task["id"],
        "source_mode": task["source_mode"],
        "prompt": build_prompt(task),
        "chosen": chosen,
        "rejected": rejected,
        "rejection_type": rejection_type,
        "partition": "train",
        "metadata": {
            "builder": "prepare_path_b_training_data.py",
            "leakage_safe_note": "chosen and rejected generated from train partition only",
            "chosen_model_family": "manual+proxy-fix",
            "judge_model_family": "separate_judge_family_required",
        },
    }


def dedup_pairs(rows: list[dict]) -> list[dict]:
    seen = set()
    out = []
    for row in rows:
        key = (
            row["prompt"],
            row["chosen"]["subject"],
            row["chosen"]["body"],
            row["rejected"]["subject"],
            row["rejected"]["body"],
        )
        if key in seen:
            continue
        seen.add(key)
        out.append(row)
    return out


def main() -> None:
    rng = random.Random(SEED)
    train_tasks = load_jsonl(DATASET_DIR / "train" / "tasks.jsonl")

    rejection_types = [
        "banned_phrase",
        "fake_urgency",
        "multi_ask",
        "bench_overcommit",
        "fabricated_signal",
        "passive_aggressive",
        "condescending_frame",
        "confidence_mismatch",
        "pricing_fabrication",
        "style_drift",
    ]

    all_pairs = []
    for task in train_tasks:
        for i in range(NEGATIVES_PER_TASK):
            rt = rejection_types[i % len(rejection_types)]
            all_pairs.append(build_preference_pair(task, rt, i + 1))

    all_pairs = dedup_pairs(all_pairs)
    rng.shuffle(all_pairs)

    train_n = int(len(all_pairs) * TRAIN_SPLIT)
    train_pairs = all_pairs[:train_n]
    val_pairs = all_pairs[train_n:]

    write_jsonl(OUTPUT_DIR / "preference_pairs_train.jsonl", train_pairs)
    write_jsonl(OUTPUT_DIR / "preference_pairs_val.jsonl", val_pairs)
    (OUTPUT_DIR / "summary.json").write_text(
        json.dumps(
            {
                "seed": SEED,
                "source_train_tasks": len(train_tasks),
                "negatives_per_task": NEGATIVES_PER_TASK,
                "total_pairs": len(all_pairs),
                "train_pairs": len(train_pairs),
                "val_pairs": len(val_pairs),
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "total_pairs": len(all_pairs),
                "train_pairs": len(train_pairs),
                "val_pairs": len(val_pairs),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
