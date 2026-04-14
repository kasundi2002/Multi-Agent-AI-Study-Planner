import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

LOG_PATH = Path("logs.jsonl")


def log_event(
    *,
    agent: str,
    event_type: str,
    trace_id: str,
    input_data: Any = None,
    tool_name: str = "",
    tool_args: Dict[str, Any] | None = None,
    output_data: Any = None,
    state_delta: Dict[str, Any] | None = None,
) -> None:
    """
    Append one structured observability event into logs.jsonl.

    Args:
        agent: Agent name emitting the event.
        event_type: Category such as task_start, tool_call, task_end.
        trace_id: End-to-end execution id for one user run.
        input_data: Optional event input payload.
        tool_name: Optional tool name for tool-related events.
        tool_args: Optional tool argument dictionary.
        output_data: Optional event output payload.
        state_delta: Optional changed state fragment after event.
    """
    payload = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "agent": agent,
        "event_type": event_type,
        "trace_id": trace_id,
        "input": input_data,
        "tool_name": tool_name,
        "tool_args": tool_args or {},
        "output": output_data,
        "state_delta": state_delta or {},
    }
    with LOG_PATH.open("a", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=True)
        handle.write("\n")