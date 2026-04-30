import json
import random
import re
import sys
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scoring_evaluator import evaluate_task_rules


HELD_PATH = ROOT / "tenacious_bench_v0.1" / "held_out" / "tasks.jsonl"
MODEL_PATH = ROOT / "training" / "path_b" / "artifacts" / "critic_model.json"
RESULTS_PATH = ROOT / "ablations" / "ablation_results.json"
TRACES_PATH = ROOT / "ablations" / "held_out_traces.jsonl"

SEED = 42
BOOTSTRAP_SAMPLES = 4000


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


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=True) + "\n")


def tokenize(text: str, min_len: int) -> list[str]:
    return [t for t in re.findall(r"[a-z0-9_:-]+", text.lower()) if len(t) >= min_len]


def vectorize(text: str, vocab: set[str], min_len: int) -> dict[str, int]:
    out = {}
    for t in tokenize(text, min_len):
        if t in vocab:
            out[t] = out.get(t, 0) + 1
    return out


def dot(vec: dict[str, int], weights: dict[str, float]) -> float:
    return sum(weights.get(tok, 0.0) * cnt for tok, cnt in vec.items())


def critic_score(task: dict, model: dict) -> float:
    cfg = model["config"]
    weights = model["weights"]
    vocab = set(weights.keys())
    text = task["candidate_output"]["subject"] + " " + task["candidate_output"]["body"]
    vec = vectorize(text, vocab, cfg["min_token_length"])
    return dot(vec, weights)


def prompt_engineer(task: dict) -> dict:
    out = deepcopy(task)
    subj = out["candidate_output"]["subject"]
    body = out["candidate_output"]["body"]
    banned = out["ground_truth"]["forbidden_phrases"]

    # Light cleanup policy to mimic prompt-only intervention.
    for phrase in banned:
        subj = re.sub(re.escape(phrase), "", subj, flags=re.IGNORECASE)
        body = re.sub(re.escape(phrase), "", body, flags=re.IGNORECASE)
    body = re.sub(r"\s+", " ", body).strip()
    if body.count("?") > 1:
        # Keep only first ask sentence.
        parts = body.split("?")
        body = parts[0] + "?"
    out["candidate_output"]["subject"] = subj.strip()
    out["candidate_output"]["body"] = body
    return out


def mutate_negative(task: dict, idx: int) -> dict:
    out = deepcopy(task)
    body = out["candidate_output"]["body"]
    subject = out["candidate_output"]["subject"]
    patterns = [
        ("banned_phrase", " We have world-class top talent."),
        ("multi_ask", " Can we do 15 minutes? Also send your roadmap and budget?"),
        ("condescending_subtle", " Your leadership is behind peers on this decision."),
        ("fabricated_signal_subtle", " Congrats on your $40M Series C last month."),
        ("overcommit_subtle", " We can commit 15 engineers in two weeks with no risk."),
        ("fake_urgency", " This is your last slot, sign by Friday."),
    ]
    kind, suffix = patterns[idx % len(patterns)]
    if kind in {"banned_phrase", "multi_ask", "fake_urgency"}:
        out["candidate_output"]["subject"] = f"Quick chat: {subject}"
    else:
        out["candidate_output"]["subject"] = subject
    out["candidate_output"]["body"] = body + suffix
    out["metadata"] = {**out.get("metadata", {}), "negative_mutation": kind}
    return out


def baseline_decision(task: dict) -> dict:
    r = evaluate_task_rules(task)
    return {"pass": bool(r["passed"]), "checks": r["checks"], "score": 1.0 if r["passed"] else 0.0}


def prompt_decision(task: dict) -> dict:
    patched = prompt_engineer(task)
    r = evaluate_task_rules(patched)
    return {"pass": bool(r["passed"]), "checks": r["checks"], "score": 1.0 if r["passed"] else 0.0}


def critic_decision(task: dict, model: dict, threshold: float = -5.0) -> dict:
    r = evaluate_task_rules(task)
    s = critic_score(task, model)
    # Critic-only decision boundary for ablation contrast.
    passed = s >= threshold
    return {"pass": passed, "checks": r["checks"], "score": round(s, 4)}


def paired_bootstrap_ci(diffs: list[int], samples: int, rng: random.Random) -> dict:
    n = len(diffs)
    stats = []
    for _ in range(samples):
        draw = [diffs[rng.randrange(n)] for _ in range(n)]
        stats.append(sum(draw) / n)
    stats.sort()
    lo = stats[int(0.025 * samples)]
    hi = stats[int(0.975 * samples)]
    # one-sided p: probability delta <= 0
    p = sum(1 for x in stats if x <= 0) / samples
    return {"ci95_low": round(lo * 100, 2), "ci95_high": round(hi * 100, 2), "p_value": round(p, 4)}


def main() -> None:
    rng = random.Random(SEED)
    held_tasks = load_jsonl(HELD_PATH)
    model = load_json(MODEL_PATH)

    examples = []
    for i, t in enumerate(held_tasks):
        pos = deepcopy(t)
        pos["label"] = 1
        pos["example_id"] = f"{t['id']}:pos"
        neg = mutate_negative(t, i)
        neg["label"] = 0
        neg["example_id"] = f"{t['id']}:neg"
        examples.extend([pos, neg])

    traces = []
    baseline_correct = []
    prompt_correct = []
    critic_correct = []

    for ex in examples:
        b = baseline_decision(ex)
        p = prompt_decision(ex)
        c = critic_decision(ex, model=model, threshold=-5.0)

        b_ok = int((1 if b["pass"] else 0) == ex["label"])
        p_ok = int((1 if p["pass"] else 0) == ex["label"])
        c_ok = int((1 if c["pass"] else 0) == ex["label"])

        baseline_correct.append(b_ok)
        prompt_correct.append(p_ok)
        critic_correct.append(c_ok)

        traces.append(
            {
                "example_id": ex["example_id"],
                "source_task_id": ex["id"],
                "label": ex["label"],
                "source_mode": ex["source_mode"],
                "difficulty": ex["difficulty"],
                "systems": {
                    "baseline_rules": {"pass": b["pass"], "score": b["score"], "correct": b_ok},
                    "prompt_engineered_rules": {"pass": p["pass"], "score": p["score"], "correct": p_ok},
                    "trained_critic": {"pass": c["pass"], "score": c["score"], "correct": c_ok},
                },
            }
        )

    n = len(examples)
    baseline_acc = sum(baseline_correct) / n
    prompt_acc = sum(prompt_correct) / n
    critic_acc = sum(critic_correct) / n

    delta_a = critic_acc - baseline_acc
    delta_b = critic_acc - prompt_acc

    diffs_a = [c - b for c, b in zip(critic_correct, baseline_correct)]
    diffs_b = [c - p for c, p in zip(critic_correct, prompt_correct)]
    ci_a = paired_bootstrap_ci(diffs_a, BOOTSTRAP_SAMPLES, rng)
    ci_b = paired_bootstrap_ci(diffs_b, BOOTSTRAP_SAMPLES, rng)

    # Proxy latency/cost estimates per example for Pareto reporting.
    costs = {
        "baseline_rules": {"cost_usd_per_example": 0.0, "latency_ms_per_example": 4},
        "prompt_engineered_rules": {"cost_usd_per_example": 0.0, "latency_ms_per_example": 7},
        "trained_critic": {"cost_usd_per_example": 0.00005, "latency_ms_per_example": 12},
    }

    results = {
        "meta": {
            "seed": SEED,
            "bootstrap_samples": BOOTSTRAP_SAMPLES,
            "held_out_tasks": len(held_tasks),
            "evaluated_examples": n,
            "protocol": "Each held-out task expanded into positive+negative example.",
        },
        "systems": {
            "baseline_rules": {"accuracy_percent": round(baseline_acc * 100, 2)},
            "prompt_engineered_rules": {"accuracy_percent": round(prompt_acc * 100, 2)},
            "trained_critic": {"accuracy_percent": round(critic_acc * 100, 2)},
        },
        "deltas": {
            "delta_a_trained_vs_baseline": {
                "delta_percent_points": round(delta_a * 100, 2),
                **ci_a,
            },
            "delta_b_trained_vs_prompt_engineered": {
                "delta_percent_points": round(delta_b * 100, 2),
                **ci_b,
            },
        },
        "cost_latency_pareto": costs,
        "notes": [
            "Delta C against tau-squared retail is not included (Week 10 score unavailable).",
            "Current critic is a deterministic baseline proxy for pipeline validation.",
        ],
    }

    RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULTS_PATH.write_text(json.dumps(results, indent=2), encoding="utf-8")
    write_jsonl(TRACES_PATH, traces)
    print(json.dumps(results["systems"], indent=2))
    print(json.dumps(results["deltas"], indent=2))


if __name__ == "__main__":
    main()
