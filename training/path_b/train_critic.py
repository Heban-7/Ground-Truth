import json
import random
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = Path(__file__).resolve().parent / "config.json"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def tokenize(text: str, min_len: int) -> list[str]:
    toks = re.findall(r"[a-z0-9_:-]+", text.lower())
    return [t for t in toks if len(t) >= min_len]


def pair_to_text(pair: dict, side: str) -> str:
    block = pair[side]
    return f"{block['subject']} {block['body']}"


def build_vocab(pairs: list[dict], min_len: int, max_vocab: int) -> set[str]:
    counts = Counter()
    for p in pairs:
        counts.update(tokenize(pair_to_text(p, "chosen"), min_len))
        counts.update(tokenize(pair_to_text(p, "rejected"), min_len))
    return {tok for tok, _ in counts.most_common(max_vocab)}


def vectorize(text: str, vocab: set[str], min_len: int) -> Counter:
    c = Counter(tokenize(text, min_len))
    return Counter({k: v for k, v in c.items() if k in vocab})


def score(vec: Counter, weights: dict[str, float]) -> float:
    return sum(weights.get(tok, 0.0) * val for tok, val in vec.items())


def eval_pairs(
    pairs: list[dict], weights: dict[str, float], vocab: set[str], min_len: int
) -> dict:
    correct = 0
    margins = []
    for p in pairs:
        chosen_vec = vectorize(pair_to_text(p, "chosen"), vocab, min_len)
        rejected_vec = vectorize(pair_to_text(p, "rejected"), vocab, min_len)
        s_pos = score(chosen_vec, weights)
        s_neg = score(rejected_vec, weights)
        margin = s_pos - s_neg
        margins.append(margin)
        if margin > 0:
            correct += 1
    total = len(pairs)
    return {
        "total": total,
        "correct": correct,
        "accuracy": round((correct / total) * 100, 2) if total else 0.0,
        "avg_margin": round(sum(margins) / total, 4) if total else 0.0,
        "min_margin": round(min(margins), 4) if margins else 0.0,
    }


def train() -> None:
    cfg = load_json(CONFIG_PATH)
    rng = random.Random(cfg["seed"])

    train_pairs = load_jsonl(ROOT / cfg["train_pairs_path"])
    val_pairs = load_jsonl(ROOT / cfg["val_pairs_path"])
    vocab = build_vocab(train_pairs, cfg["min_token_length"], cfg["max_vocab_size"])

    weights = defaultdict(float)
    history = []

    for epoch in range(1, cfg["epochs"] + 1):
        rng.shuffle(train_pairs)
        updates = 0

        for p in train_pairs:
            chosen_vec = vectorize(pair_to_text(p, "chosen"), vocab, cfg["min_token_length"])
            rejected_vec = vectorize(pair_to_text(p, "rejected"), vocab, cfg["min_token_length"])

            s_pos = score(chosen_vec, weights)
            s_neg = score(rejected_vec, weights)
            if s_pos <= s_neg:
                # Ranking perceptron-style update.
                for tok, val in chosen_vec.items():
                    weights[tok] += cfg["learning_rate"] * val
                for tok, val in rejected_vec.items():
                    weights[tok] -= cfg["learning_rate"] * val
                updates += 1

        tr = eval_pairs(train_pairs, weights, vocab, cfg["min_token_length"])
        va = eval_pairs(val_pairs, weights, vocab, cfg["min_token_length"])
        epoch_row = {
            "epoch": epoch,
            "updates": updates,
            "train_accuracy": tr["accuracy"],
            "val_accuracy": va["accuracy"],
            "train_avg_margin": tr["avg_margin"],
            "val_avg_margin": va["avg_margin"],
        }
        history.append(epoch_row)

    artifacts_dir = ROOT / cfg["artifacts_dir"]
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    sorted_w = sorted(weights.items(), key=lambda x: x[1], reverse=True)
    model = {
        "model_type": "path_b_linear_preference_critic",
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "config": cfg,
        "vocab_size": len(vocab),
        "weights": dict(weights),
        "top_positive_tokens": sorted_w[:40],
        "top_negative_tokens": sorted_w[-40:],
    }
    (artifacts_dir / "critic_model.json").write_text(
        json.dumps(model, indent=2), encoding="utf-8"
    )

    final_train = eval_pairs(train_pairs, weights, vocab, cfg["min_token_length"])
    final_val = eval_pairs(val_pairs, weights, vocab, cfg["min_token_length"])
    metrics = {
        "final_train": final_train,
        "final_val": final_val,
        "history": history,
    }
    (artifacts_dir / "metrics.json").write_text(
        json.dumps(metrics, indent=2), encoding="utf-8"
    )

    log_lines = []
    log_lines.append("Path B training run (linear preference critic)")
    log_lines.append(f"seed={cfg['seed']}")
    log_lines.append(f"epochs={cfg['epochs']}")
    log_lines.append(f"learning_rate={cfg['learning_rate']}")
    log_lines.append(f"train_pairs={len(train_pairs)} val_pairs={len(val_pairs)}")
    log_lines.append(f"vocab_size={len(vocab)}")
    log_lines.append("")
    for row in history:
        log_lines.append(
            "epoch={epoch} updates={updates} train_acc={train_accuracy}% val_acc={val_accuracy}% train_margin={train_avg_margin} val_margin={val_avg_margin}".format(
                **row
            )
        )
    log_lines.append("")
    log_lines.append(
        f"final_train_acc={final_train['accuracy']}% final_val_acc={final_val['accuracy']}%"
    )

    (artifacts_dir / "training_run.log").write_text(
        "\n".join(log_lines) + "\n", encoding="utf-8"
    )

    print(
        json.dumps(
            {
                "train_accuracy": final_train["accuracy"],
                "val_accuracy": final_val["accuracy"],
                "artifacts_dir": str(artifacts_dir),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    train()
