import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATASET_DIR = ROOT / "tenacious_bench_v0.1"
TDIR = ROOT / "training_data" / "path_b"
REPORT_PATH = ROOT / "training_data_contamination_check.json"

NGRAM_N = 8
SIM_THRESHOLD = 0.85


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


def norm_tokens(text: str) -> list[str]:
    return re.findall(r"[a-z0-9_:-]+", text.lower())


def ngrams(tokens: list[str], n: int) -> set[tuple[str, ...]]:
    if len(tokens) < n:
        return set()
    return {tuple(tokens[i : i + n]) for i in range(len(tokens) - n + 1)}


def shared_ngram(a: str, b: str, n: int) -> bool:
    return len(ngrams(norm_tokens(a), n).intersection(ngrams(norm_tokens(b), n))) > 0


def jaccard(a: str, b: str) -> float:
    sa = set(norm_tokens(a))
    sb = set(norm_tokens(b))
    union = sa.union(sb)
    if not union:
        return 0.0
    return len(sa.intersection(sb)) / len(union)


def main() -> None:
    train_pairs = load_jsonl(TDIR / "preference_pairs_train.jsonl")
    val_pairs = load_jsonl(TDIR / "preference_pairs_val.jsonl")
    all_pairs = train_pairs + val_pairs

    dev = load_jsonl(DATASET_DIR / "dev" / "tasks.jsonl")
    held = load_jsonl(DATASET_DIR / "held_out" / "tasks.jsonl")
    eval_tasks = dev + held

    eval_ids = {t["id"] for t in eval_tasks}

    source_id_overlap = []
    ngram_violations = []
    similarity_violations = []

    eval_signals = {t["id"]: t["input"]["signal_brief"] for t in eval_tasks}
    eval_sources = {t["id"]: f"dev_or_held:{t['partition']}" for t in eval_tasks}

    for p in all_pairs:
        sid = p["source_task_id"]
        if sid in eval_ids:
            source_id_overlap.append({"pair_id": p["pair_id"], "source_task_id": sid})

        prompt = p["prompt"]
        for tid, signal in eval_signals.items():
            if shared_ngram(prompt, signal, NGRAM_N):
                ngram_violations.append({"pair_id": p["pair_id"], "eval_task_id": tid, "n": NGRAM_N})
            sim = jaccard(prompt, signal)
            if sim >= SIM_THRESHOLD:
                similarity_violations.append(
                    {
                        "pair_id": p["pair_id"],
                        "eval_task_id": tid,
                        "similarity": round(sim, 4),
                        "threshold": SIM_THRESHOLD,
                    }
                )

    report = {
        "policy": {
            "id_overlap_rule": "No training-data source_task_id can be in dev/held_out IDs",
            "ngram_rule": f"No shared {NGRAM_N}-gram between training prompt and dev/held signal brief",
            "similarity_rule": f"Jaccard(prompt, eval_signal) < {SIM_THRESHOLD}",
        },
        "counts": {
            "train_pairs": len(train_pairs),
            "val_pairs": len(val_pairs),
            "total_pairs": len(all_pairs),
            "eval_tasks_checked": len(eval_tasks),
            "source_id_overlap": len(source_id_overlap),
            "ngram_violations": len(ngram_violations),
            "similarity_violations": len(similarity_violations),
        },
        "violations": {
            "source_id_overlap": source_id_overlap[:50],
            "ngram": ngram_violations[:50],
            "similarity": similarity_violations[:50],
        },
        "pass": (
            len(source_id_overlap) == 0
            and len(ngram_violations) == 0
            and len(similarity_violations) == 0
        ),
        "notes": [
            "This check compares training-data prompts against both dev and held_out.",
            "Similarity uses lexical Jaccard proxy; replace with embeddings in later phase.",
            f"Eval task index keys: {sorted(eval_sources.keys())[:5]} ...",
        ],
    }

    REPORT_PATH.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report["counts"], indent=2))


if __name__ == "__main__":
    main()
