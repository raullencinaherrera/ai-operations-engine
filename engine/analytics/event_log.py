import json
from dataclasses import asdict
from pathlib import Path
from typing import List

from engine.analytics.models import EngineTraceEvent


def append_trace_event(path: str, trace_event: EngineTraceEvent) -> None:
    log_path = Path(path)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    with log_path.open("a", encoding="utf-8") as file:
        file.write(json.dumps(asdict(trace_event), ensure_ascii=False) + "\n")


def load_trace_events(path: str) -> List[dict]:
    log_path = Path(path)

    if not log_path.exists():
        return []

    events = []

    with log_path.open("r", encoding="utf-8") as file:
        for line in file:
            clean_line = line.strip()

            if clean_line:
                events.append(json.loads(clean_line))

    return events