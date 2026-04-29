import json
import re
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
DATASET_DIR = ROOT / "tenacious_bench_v0.1"
REPORT_PATH = ROOT / "contamination_check.json"

NGRAM_N = 8
SIMILARITY_THRESHOLD = 0.85


def load_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def normalize_tokens(text: str) -> list[str]:
    return re.findall(r"[a-z0-9$]+", text.lower())


def ngrams(tokens: list[str], n: int) -> set[tuple[str, ...]]:
    if len(tokens) < n:
        return set()
    return {tuple(tokens[i : i + n]) for i in range(len(tokens) - n + 1)}


def has_any_shared_ngram(a_text: str, b_text: str, n: int) -> bool:
    a_ngrams = ngrams(normalize_tokens(a_text), n)
    b_ngrams = ngrams(normalize_tokens(b_text), n)
    return len(a_ngrams.intersection(b_ngrams)) > 0


def jaccard_similarity(a_tokens: Iterable[str], b_tokens: Iterable[str]) -> float:
    a = set(a_tokens)
    b = set(b_tokens)
    union = a.union(b)
    if not union:
        return 0.0
    return len(a.intersection(b)) / len(union)


def lexical_similarity(a_text: str, b_text: str) -> float:
    return jaccard_similarity(normalize_tokens(a_text), normalize_tokens(b_text))


def has_time_anchor(text: str) -> bool:
    # Minimal proxy for "time-shift verification": month name or 4-digit year.
    month_pattern = (
        r"\b(january|february|march|april|may|june|july|august|"
        r"september|october|november|december)\b"
    )
    year_pattern = r"\b(19|20)\d{2}\b"
    return bool(re.search(month_pattern, text.lower()) or re.search(year_pattern, text))


def check_contamination(train_tasks: list[dict], held_out_tasks: list[dict]) -> dict:
    ngram_violations = []
    similarity_violations = []
    time_anchor_warnings = []

    for h in held_out_tasks:
        held_signal = h["input"]["signal_brief"]

        if not has_time_anchor(held_signal):
            time_anchor_warnings.append(
                {
                    "held_out_id": h["id"],
                    "reason": "No explicit month/year found in signal_brief.",
                }
            )

        for t in train_tasks:
            train_signal = t["input"]["signal_brief"]

            if has_any_shared_ngram(train_signal, held_signal, NGRAM_N):
                ngram_violations.append(
                    {
                        "train_id": t["id"],
                        "held_out_id": h["id"],
                        "n": NGRAM_N,
                    }
                )

            sim = lexical_similarity(train_signal, held_signal)
            if sim >= SIMILARITY_THRESHOLD:
                similarity_violations.append(
                    {
                        "train_id": t["id"],
                        "held_out_id": h["id"],
                        "similarity": round(sim, 4),
                        "threshold": SIMILARITY_THRESHOLD,
                    }
                )

    report = {
        "policy": {
            "n_gram_rule": f"No shared {NGRAM_N}-gram between train and held_out signal_brief.",
            "similarity_rule": f"Lexical similarity < {SIMILARITY_THRESHOLD} (proxy for embedding check).",
            "time_shift_rule": "Each held_out signal_brief should include an explicit time anchor.",
        },
        "counts": {
            "train_tasks": len(train_tasks),
            "held_out_tasks": len(held_out_tasks),
            "ngram_violations": len(ngram_violations),
            "similarity_violations": len(similarity_violations),
            "time_anchor_warnings": len(time_anchor_warnings),
        },
        "violations": {
            "ngram": ngram_violations,
            "similarity": similarity_violations,
            "time_anchor_warnings": time_anchor_warnings,
        },
        "pass": len(ngram_violations) == 0 and len(similarity_violations) == 0,
        "notes": [
            "Similarity uses lexical Jaccard proxy for now.",
            "Replace lexical proxy with real embedding model in a later step.",
        ],
    }
    return report


def main() -> None:
    train_tasks = load_jsonl(DATASET_DIR / "train" / "tasks.jsonl")
    held_out_tasks = load_jsonl(DATASET_DIR / "held_out" / "tasks.jsonl")
    report = check_contamination(train_tasks, held_out_tasks)

    with REPORT_PATH.open("w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print(f"Wrote contamination report to: {REPORT_PATH.name}")
    print(json.dumps(report["counts"], indent=2))


if __name__ == "__main__":
    main()
