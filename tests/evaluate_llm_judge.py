import json
from pathlib import Path
import sys
from urllib.error import URLError
from urllib.request import Request, urlopen

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from main import run_pipeline


def _ask_local_judge(prompt: str, model: str = "llama3:8b") -> str:
    """Call local Ollama generate endpoint for judging."""
    payload = json.dumps({"model": model, "prompt": prompt, "stream": False}).encode("utf-8")
    request = Request(
        url="http://localhost:11434/api/generate",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urlopen(request, timeout=60) as response:
        data = json.loads(response.read().decode("utf-8"))
    return str(data.get("response", "")).strip()


def evaluate() -> dict:
    """Run pipeline and ask local LLM judge for quality scoring."""
    state = run_pipeline(subject="Machine Learning", days=14)
    rubric = {
        "coverage": "Does the plan cover beginner to advanced ML topics?",
        "ordering_quality": "Are topics logically ordered for learning progression?",
        "resource_relevance": "Are resources relevant for each topic?",
        "schedule_feasibility": "Is day-wise plan feasible for 2 weeks?",
    }
    judge_prompt = (
        "You are grading a study plan. Return ONLY JSON with integer scores 1-10 "
        "for coverage, ordering_quality, resource_relevance, schedule_feasibility, "
        "and a short overall_comment.\n\n"
        f"RUBRIC: {json.dumps(rubric)}\n\n"
        f"PLAN_STATE: {json.dumps(state)}"
    )
    response = _ask_local_judge(judge_prompt)
    try:
        parsed = json.loads(response)
    except json.JSONDecodeError:
        parsed = {
            "coverage": 0,
            "ordering_quality": 0,
            "resource_relevance": 0,
            "schedule_feasibility": 0,
            "overall_comment": f"Judge returned non-JSON output: {response[:200]}",
        }
    return {"judge_result": parsed, "trace_id": state["trace_id"]}


if __name__ == "__main__":
    output_dir = Path("tests/results")
    output_dir.mkdir(parents=True, exist_ok=True)
    try:
        result = evaluate()
    except (URLError, OSError) as error:
        result = {
            "judge_result": {
                "coverage": 0,
                "ordering_quality": 0,
                "resource_relevance": 0,
                "schedule_feasibility": 0,
                "overall_comment": f"Local Ollama judge unavailable: {error}",
            },
            "trace_id": "",
        }
    output_path = output_dir / "llm_judge_result.json"
    output_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(f"Saved LLM judge result to: {output_path}")
