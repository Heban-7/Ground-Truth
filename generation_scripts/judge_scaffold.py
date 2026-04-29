import json
import re


def build_judge_prompt(task: dict) -> str:
    """
    Build a strict JSON-only judge prompt.
    This template is model-agnostic and can be sent to any LLM API later.
    """
    return (
        "You are evaluating a B2B sales outreach draft using Tenacious style policy.\n"
        "Return ONLY valid JSON with this exact schema:\n"
        '{'
        '"direct": <1-5 int>,'
        '"grounded": <1-5 int>,'
        '"honest": <1-5 int>,'
        '"professional": <1-5 int>,'
        '"non_condescending": <1-5 int>,'
        '"reasoning": "<short reason>"'
        '}\n'
        "No markdown. No extra keys.\n\n"
        f"TASK INPUT:\n{json.dumps(task['input'], ensure_ascii=True)}\n\n"
        f"CANDIDATE OUTPUT:\n{json.dumps(task['candidate_output'], ensure_ascii=True)}\n\n"
        f"GROUND TRUTH RULES:\n{json.dumps(task['ground_truth'], ensure_ascii=True)}\n"
    )


def _extract_json_blob(text: str) -> str:
    # Handle responses like ```json {...}``` or plain JSON.
    fenced = re.search(r"```(?:json)?\s*(\{.*\})\s*```", text, re.DOTALL | re.IGNORECASE)
    if fenced:
        return fenced.group(1)

    direct = re.search(r"(\{.*\})", text, re.DOTALL)
    if direct:
        return direct.group(1)

    raise ValueError("No JSON object found in judge response.")


def parse_judge_response(raw_text: str) -> dict:
    blob = _extract_json_blob(raw_text)
    data = json.loads(blob)

    required = ["direct", "grounded", "honest", "professional", "non_condescending", "reasoning"]
    missing = [k for k in required if k not in data]
    if missing:
        raise ValueError(f"Missing judge keys: {missing}")

    for k in ["direct", "grounded", "honest", "professional", "non_condescending"]:
        if not isinstance(data[k], int) or not (1 <= data[k] <= 5):
            raise ValueError(f"Judge score for '{k}' must be int in [1,5].")

    if not isinstance(data["reasoning"], str):
        raise ValueError("Judge 'reasoning' must be a string.")

    return data
