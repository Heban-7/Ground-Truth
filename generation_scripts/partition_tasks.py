import argparse
import json
import random
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATASET_DIR = ROOT / "tenacious_bench_v0.1"


def load_jsonl(path: Path) -> list[dict]:
    rows = []
    if not path.exists():
        return rows
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


def target_counts(total: int, train_ratio: float, dev_ratio: float, held_ratio: float) -> tuple[int, int, int]:
    train_n = round(total * train_ratio)
    dev_n = round(total * dev_ratio)
    held_n = total - train_n - dev_n

    # Small correction in case rounding pushes held_n negative on tiny datasets.
    if held_n < 0:
        held_n = 0
        overflow = (train_n + dev_n) - total
        if dev_n >= overflow:
            dev_n -= overflow
        else:
            train_n -= (overflow - dev_n)
            dev_n = 0

    return train_n, dev_n, held_n


def repartition(seed: int, train_ratio: float, dev_ratio: float, held_ratio: float) -> dict:
    train_path = DATASET_DIR / "train" / "tasks.jsonl"
    dev_path = DATASET_DIR / "dev" / "tasks.jsonl"
    held_path = DATASET_DIR / "held_out" / "tasks.jsonl"

    all_tasks = load_jsonl(train_path) + load_jsonl(dev_path) + load_jsonl(held_path)
    if not all_tasks:
        raise ValueError("No tasks found across train/dev/held_out.")

    rng = random.Random(seed)
    rng.shuffle(all_tasks)

    train_n, dev_n, held_n = target_counts(len(all_tasks), train_ratio, dev_ratio, held_ratio)

    train_tasks = all_tasks[:train_n]
    dev_tasks = all_tasks[train_n : train_n + dev_n]
    held_tasks = all_tasks[train_n + dev_n : train_n + dev_n + held_n]

    for t in train_tasks:
        t["partition"] = "train"
    for t in dev_tasks:
        t["partition"] = "dev"
    for t in held_tasks:
        t["partition"] = "held_out"

    write_jsonl(train_path, train_tasks)
    write_jsonl(dev_path, dev_tasks)
    write_jsonl(held_path, held_tasks)

    return {
        "seed": seed,
        "ratios": {"train": train_ratio, "dev": dev_ratio, "held_out": held_ratio},
        "counts": {
            "total": len(all_tasks),
            "train": len(train_tasks),
            "dev": len(dev_tasks),
            "held_out": len(held_tasks),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Repartition tasks into train/dev/held_out.")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--train-ratio", type=float, default=0.5)
    parser.add_argument("--dev-ratio", type=float, default=0.3)
    parser.add_argument("--held-ratio", type=float, default=0.2)
    args = parser.parse_args()

    ratio_sum = args.train_ratio + args.dev_ratio + args.held_ratio
    if abs(ratio_sum - 1.0) > 1e-9:
        raise ValueError("Ratios must sum to 1.0")

    report = repartition(args.seed, args.train_ratio, args.dev_ratio, args.held_ratio)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
