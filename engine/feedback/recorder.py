import json
from pathlib import Path
from typing import Dict, List

from engine.feedback.models import FeedbackResult


def load_raw_memory_records(path: str | Path) -> List[Dict]:
    memory_path = Path(path)

    records = []

    with memory_path.open("r", encoding="utf-8") as file:
        for line in file:
            clean_line = line.strip()

            if clean_line:
                records.append(json.loads(clean_line))

    return records


def save_raw_memory_records(path: str | Path, records: List[Dict]) -> None:
    memory_path = Path(path)

    with memory_path.open("w", encoding="utf-8") as file:
        for record in records:
            file.write(json.dumps(record, ensure_ascii=False) + "\n")


def record_feedback(path: str | Path, feedback: FeedbackResult) -> Dict:
    records = load_raw_memory_records(path)

    for record in records:
        if record["id"] == feedback.memory_id:
            if feedback.worked:
                record["success_count"] = record.get("success_count", 0) + 1
            else:
                record["failure_count"] = record.get("failure_count", 0) + 1

            if feedback.notes:
                record.setdefault("feedback_notes", [])
                record["feedback_notes"].append(feedback.notes)

            save_raw_memory_records(path, records)
            return record

    raise ValueError(f"Memory record not found: {feedback.memory_id}")