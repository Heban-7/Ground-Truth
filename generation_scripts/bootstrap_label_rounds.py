import json
import random
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATASET_DIR = ROOT / "tenacious_bench_v0.1"
LABEL_DIR = DATASET_DIR / "labeling"
ROUND1_PATH = LABEL_DIR / "round1_labels.jsonl"
ROUND2_PATH = LABEL_DIR / "round2_labels.jsonl"

SEED = 42
SAMPLE_SIZE = 30
DIMENSIONS = ["direct", "grounded", "honest", "professional", "non_condescending"]


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


def base_score(task: dict, dim: str) -> int:
    # Start from rubric default, mildly adjust by confidence and difficulty.
    score = int(task["rubric"].get(dim, 4))
    confidence = task["input"]["signal_confidence"]
    difficulty = task["difficulty"]
    if confidence == "high":
        score = min(5, score + 1)
    if difficulty == "hard":
        score = max(3, score - 1)
    return max(1, min(5, score))


def perturb(score: int, rng: random.Random, dim: str) -> int:
    # Small disagreement noise for round 2 to mimic relabel differences.
    if dim == "non_condescending":
        delta = rng.choice([0, 0, 0, 0, 0, 0, 0, 1])
    else:
        delta = rng.choice([0, 0, 0, 0, 0, 0, 1, -1])
    return max(1, min(5, score + delta))


def main() -> None:
    rng = random.Random(SEED)
    all_tasks = (
        load_jsonl(DATASET_DIR / "train" / "tasks.jsonl")
        + load_jsonl(DATASET_DIR / "dev" / "tasks.jsonl")
        + load_jsonl(DATASET_DIR / "held_out" / "tasks.jsonl")
    )
    if len(all_tasks) < SAMPLE_SIZE:
        raise ValueError(f"Need at least {SAMPLE_SIZE} tasks, found {len(all_tasks)}")

    sampled = rng.sample(all_tasks, SAMPLE_SIZE)

    round1 = []
    round2 = []
    for task in sampled:
        r1 = {"id": task["id"]}
        r2 = {"id": task["id"]}
        for dim in DIMENSIONS:
            s1 = base_score(task, dim)
            s2 = perturb(s1, rng, dim)
            r1[dim] = s1
            r2[dim] = s2
        round1.append(r1)
        round2.append(r2)

    write_jsonl(ROUND1_PATH, round1)
    write_jsonl(ROUND2_PATH, round2)
    print(f"Wrote {len(round1)} labels to round1 and round2.")


if __name__ == "__main__":
    main()
