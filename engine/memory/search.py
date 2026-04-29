from typing import Any, Dict, List

from engine.memory.models import MemoryMatch, MemoryRecord


def normalize_text(value: Any) -> str:
    return str(value).lower()


def extract_event_text(event: Dict[str, Any]) -> str:
    parts = []

    for key in ["summary", "message", "reason", "logs", "error"]:
        value = event.get(key)
        if value:
            parts.append(str(value))

    return " ".join(parts).lower()


def score_memory_record(record: MemoryRecord, event: Dict[str, Any]) -> MemoryMatch:
    score = 0
    matched_terms: List[str] = []

    event_text = extract_event_text(event)
    event_tags = [normalize_text(tag) for tag in event.get("tags", [])]

    if record.event_type == event.get("event_type"):
        score += 30
        matched_terms.append(f"event_type:{record.event_type}")

    if record.source and record.source == event.get("source"):
        score += 10
        matched_terms.append(f"source:{record.source}")

    for symptom in record.symptoms:
        symptom_text = normalize_text(symptom)
        if symptom_text in event_text:
            score += 20
            matched_terms.append(symptom)

    for tag in record.tags:
        tag_text = normalize_text(tag)
        if tag_text in event_tags or tag_text in event_text:
            score += 10
            matched_terms.append(f"tag:{tag}")

    score += record.success_count * 2
    score -= record.failure_count * 2

    return MemoryMatch(
        record=record,
        score=score,
        matched_terms=matched_terms,
    )


def search_memory(
    records: List[MemoryRecord],
    event: Dict[str, Any],
    minimum_score: int = 30,
) -> List[MemoryMatch]:
    matches = []

    for record in records:
        match = score_memory_record(record, event)

        if match.score >= minimum_score:
            matches.append(match)

    return sorted(matches, key=lambda item: item.score, reverse=True)