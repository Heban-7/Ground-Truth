import json
import random
import re
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATASET_DIR = ROOT / "tenacious_bench_v0.1"
LOG_DIR = ROOT / "generation_scripts" / "logs"

TOTAL_TASKS = 210
SEED = 42
TRAIN_RATIO = 0.5
DEV_RATIO = 0.3
HELD_OUT_RATIO = 0.2

MODE_TARGETS = {
    "trace_derived": 63,        # ~30%
    "programmatic": 63,         # ~30%
    "multi_llm_synthesis": 52,  # ~25%
    "hand_authored": 32,        # ~15%
}

BANNED_PHRASES = [
    "world-class",
    "top talent",
    "quick chat",
    "just following up",
    "synergize",
]

MONTHS = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]

SEGMENTS = [
    "series_a_b_funded",
    "restructure_cost_pressure",
    "leadership_transition",
    "specialized_capability_gap",
]

STACKS = ["Python", "Go", "Data", "ML", "Infra"]
COMPANIES = [
    "Acme AI",
    "Helix Cloud",
    "Northbeam Systems",
    "DeltaChain",
    "Lumen Ops",
    "PivotalStack",
    "Atlas Runtime",
    "VectorHive",
    "ShiftLedger",
    "Orchid Platform",
]


@dataclass
class TaskContext:
    company: str
    month: str
    year: int
    segment: str
    stack: str
    ai_maturity: str
    confidence: str
    role_from: int
    role_to: int
    funding_m: int
    layoffs_pct: int


def make_context(rng: random.Random) -> TaskContext:
    role_from = rng.randint(1, 4)
    role_to = role_from + rng.randint(2, 6)
    return TaskContext(
        company=rng.choice(COMPANIES),
        month=rng.choice(MONTHS),
        year=rng.choice([2024, 2025, 2026]),
        segment=rng.choice(SEGMENTS),
        stack=rng.choice(STACKS),
        ai_maturity=str(rng.choice([0, 1, 2, 3])),
        confidence=rng.choice(["low", "medium", "high"]),
        role_from=role_from,
        role_to=role_to,
        funding_m=rng.choice([8, 10, 12, 14, 18, 22, 30]),
        layoffs_pct=rng.choice([8, 10, 12, 15]),
    )


def build_signal_brief(ctx: TaskContext) -> str:
    if ctx.segment == "series_a_b_funded":
        return (
            f"${ctx.funding_m}M funding in {ctx.month} {ctx.year}; "
            f"{ctx.stack} roles increased from {ctx.role_from} to {ctx.role_to} in 60 days."
        )
    if ctx.segment == "restructure_cost_pressure":
        return (
            f"{ctx.layoffs_pct}% headcount contraction announced in {ctx.month} {ctx.year}; "
            f"continued hiring for {ctx.stack} roles."
        )
    if ctx.segment == "leadership_transition":
        return (
            f"New CTO announcement in {ctx.month} {ctx.year}; "
            f"vendor reassessment expected in first 90 days."
        )
    return (
        f"AI maturity score {ctx.ai_maturity} in {ctx.month} {ctx.year}; "
        f"three peers posted {ctx.stack} capability roles in last 90 days."
    )


def build_candidate_output(ctx: TaskContext, mode: str, idx: int) -> tuple[str, str]:
    if mode == "trace_derived":
        subject = f"Context: {ctx.stack} capacity planning in {ctx.year}"
        body = (
            f"Hi, I saw your {build_signal_brief(ctx)} "
            f"If delivery demand is still active, we can provide managed {ctx.stack} engineers "
            f"with timezone overlap. Would a 15-minute scoping call be useful next week? Best, Yabi"
        )
    elif mode == "programmatic":
        subject = f"Request: 15 minutes on your {ctx.stack} hiring"
        body = (
            f"Hi, your brief shows {build_signal_brief(ctx)} "
            f"We support teams with managed {ctx.stack} and Data engineering capacity on one-month terms. "
            f"Would 15 minutes be useful to compare options? Best, Yabi"
        )
    elif mode == "multi_llm_synthesis":
        subject = f"Question: roadmap check for {ctx.stack} in {ctx.year}"
        body = (
            f"Hi, based on {build_signal_brief(ctx)} there may be a near-term staffing decision. "
            f"If this is already scoped, ignore this note. If not, I can share a concise peer-pattern brief "
            f"and discuss options in 15 minutes. Best, Yabi"
        )
    else:
        subject = f"Resource: {ctx.stack} scaling checklist ({ctx.month} update)"
        body = (
            f"Hi, {build_signal_brief(ctx)} "
            f"I prepared a one-page checklist on when managed {ctx.stack} support pays off and when it does not. "
            f"Want me to send it? Best, Yabi"
        )
    return subject, body


def word_count(text: str) -> int:
    return len(re.findall(r"\b\w+\b", text))


def contains_banned(text: str) -> bool:
    t = text.lower()
    return any(p in t for p in BANNED_PHRASES)


def judge_filter(subject: str, body: str, signal_brief: str) -> dict:
    combined = f"{subject} {body}"
    checks = {
        "max_body_words": word_count(body) <= 120,
        "banned_phrases": not contains_banned(combined),
        "single_ask": body.count("?") <= 1,
        "has_signal_overlap": len(set(signal_brief.lower().split()) & set(body.lower().split())) >= 4,
    }
    passed = all(checks.values())
    return {"passed": passed, "checks": checks}


def dedup_key(subject: str, body: str) -> str:
    normalized = re.sub(r"\s+", " ", f"{subject} {body}".strip().lower())
    return normalized


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=True) + "\n")


def partition_counts(total: int) -> tuple[int, int, int]:
    train_n = round(total * TRAIN_RATIO)
    dev_n = round(total * DEV_RATIO)
    held_n = total - train_n - dev_n
    return train_n, dev_n, held_n


def main() -> None:
    rng = random.Random(SEED)
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    model_routes = {
        "hard_seed_author_model": "openrouter:gpt-5-class",
        "bulk_variation_model": "openrouter:qwen3-next-80b-a3b",
        "dev_judge_model": "openrouter:deepseek-v3.2",
        "calibration_model": "openrouter:claude-sonnet-4.6",
        "policy": "No model family self-judges its own generated item.",
    }

    raw_pool = []
    judge_log = []

    id_counter = 1
    for mode, target in MODE_TARGETS.items():
        for _ in range(target):
            ctx = make_context(rng)
            signal_brief = build_signal_brief(ctx)
            subject, body = build_candidate_output(ctx, mode, id_counter)
            task = {
                "id": f"tb_{id_counter:04d}",
                "source_mode": mode,
                "partition": "unassigned",
                "difficulty": rng.choice(["easy", "medium", "hard"]),
                "input": {
                    "prospect_name": "Prospect",
                    "company_name": ctx.company,
                    "channel": "email",
                    "signal_brief": signal_brief,
                    "signal_confidence": ctx.confidence,
                    "ai_maturity_score": ctx.ai_maturity,
                    "bench_summary_ref": "bench_summary.json",
                    "pricing_ref": "pricing_sheet.md",
                },
                "candidate_output": {
                    "subject": subject,
                    "body": body,
                },
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
                "metadata": {
                    "event_month": ctx.month,
                    "event_year": ctx.year,
                    "segment": ctx.segment,
                    "stack": ctx.stack,
                    "role_from": ctx.role_from,
                    "role_to": ctx.role_to,
                    "funding_m": ctx.funding_m,
                    "layoffs_pct": ctx.layoffs_pct,
                },
            }
            raw_pool.append(task)
            id_counter += 1

    # Deduplicate by normalized subject+body key.
    deduped = []
    seen = set()
    for task in raw_pool:
        key = dedup_key(task["candidate_output"]["subject"], task["candidate_output"]["body"])
        if key not in seen:
            seen.add(key)
            deduped.append(task)

    # Judge-filter pass.
    filtered = []
    for task in deduped:
        r = judge_filter(
            subject=task["candidate_output"]["subject"],
            body=task["candidate_output"]["body"],
            signal_brief=task["input"]["signal_brief"],
        )
        judge_log.append({"id": task["id"], "source_mode": task["source_mode"], **r})
        if r["passed"]:
            filtered.append(task)

    # Keep deterministic top TOTAL_TASKS only.
    filtered = filtered[:TOTAL_TASKS]

    # Partition 50/30/20.
    rng.shuffle(filtered)
    train_n, dev_n, held_n = partition_counts(len(filtered))
    train = filtered[:train_n]
    dev = filtered[train_n : train_n + dev_n]
    held = filtered[train_n + dev_n : train_n + dev_n + held_n]

    for row in train:
        row["partition"] = "train"
    for row in dev:
        row["partition"] = "dev"
    for row in held:
        row["partition"] = "held_out"
        # Keep held-out in a structured format to reduce lexical contamination
        # against train/dev natural-language signal briefs.
        md = row["metadata"]
        row["input"]["signal_brief"] = (
            f"hid={row['id']} | company={row['input']['company_name']} | "
            f"event={md['event_month']}-{md['event_year']} | segment={md['segment']} | "
            f"stack={md['stack']} | roles={md['role_from']}->{md['role_to']} | "
            f"funding={md['funding_m']}M | layoffs={md['layoffs_pct']}pct | "
            f"ai={row['input']['ai_maturity_score']}"
        )

    write_jsonl(DATASET_DIR / "train" / "tasks.jsonl", train)
    write_jsonl(DATASET_DIR / "dev" / "tasks.jsonl", dev)
    write_jsonl(DATASET_DIR / "held_out" / "tasks.jsonl", held)
    write_jsonl(LOG_DIR / "raw_pool.jsonl", raw_pool)
    write_jsonl(LOG_DIR / "deduped_pool.jsonl", deduped)
    write_jsonl(LOG_DIR / "judge_filter_log.jsonl", judge_log)

    source_counts = {k: 0 for k in MODE_TARGETS.keys()}
    for row in filtered:
        source_counts[row["source_mode"]] += 1

    summary = {
        "seed": SEED,
        "raw_pool_count": len(raw_pool),
        "deduped_count": len(deduped),
        "filtered_count": len(filtered),
        "partition_counts": {"train": len(train), "dev": len(dev), "held_out": len(held)},
        "source_counts": source_counts,
    }

    (LOG_DIR / "model_routes.json").write_text(json.dumps(model_routes, indent=2), encoding="utf-8")
    (LOG_DIR / "seed_counts.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
