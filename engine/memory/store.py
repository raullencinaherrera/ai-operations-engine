import json
from pathlib import Path
from typing import List

from engine.memory.models import MemoryRecord


def load_memory(path: str | Path) -> List[MemoryRecord]:
    memory_path = Path(path)

    if not memory_path.exists():
        raise FileNotFoundError(f"Memory file not found: {memory_path}")

    records: List[MemoryRecord] = []

    with memory_path.open("r", encoding="utf-8") as file:
        for line in file:
            clean_line = line.strip()

            if not clean_line:
                continue

            raw_record = json.loads(clean_line)

            records.append(
                MemoryRecord(
                    id=raw_record["id"],
                    event_type=raw_record["event_type"],
                    source=raw_record.get("source", ""),
                    summary=raw_record["summary"],
                    symptoms=raw_record.get("symptoms", []),
                    root_cause=raw_record.get("root_cause", ""),
                    resolution=raw_record.get("resolution", ""),
                    success_count=raw_record.get("success_count", 0),
                    failure_count=raw_record.get("failure_count", 0),
                    confidence=raw_record.get("confidence", "medium"),
                    tags=raw_record.get("tags", []),
                )
            )

    return records