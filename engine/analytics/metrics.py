from collections import Counter
from typing import Dict, List


def safe_rate(numerator: int, denominator: int) -> float:
    if denominator == 0:
        return 0.0

    return round(numerator / denominator, 2)


def calculate_metrics(events: List[dict]) -> Dict:
    total_events = len(events)

    rule_matched_count = sum(1 for event in events if event.get("rule_matched"))
    memory_matched_count = sum(1 for event in events if event.get("memory_matched"))
    documentation_found_count = sum(1 for event in events if event.get("documentation_found"))
    llm_used_count = sum(1 for event in events if event.get("llm_used"))
    promoted_to_rule_count = sum(1 for event in events if event.get("promoted_to_rule"))
    unresolved_count = sum(1 for event in events if event.get("unresolved"))

    execution_success_count = sum(
        1 for event in events if event.get("execution_status") == "success"
    )
    execution_failed_count = sum(
        1 for event in events if event.get("execution_status") == "failed"
    )

    event_type_counter = Counter(event.get("event_type", "unknown") for event in events)

    rule_counter = Counter()
    memory_counter = Counter()
    documentation_gap_counter = Counter()

    for event in events:
        for rule_id in event.get("rule_ids", []):
            rule_counter[rule_id] += 1

        for memory_id in event.get("memory_ids", []):
            memory_counter[memory_id] += 1

        if not event.get("documentation_found"):
            documentation_gap_counter[event.get("event_type", "unknown")] += 1

    return {
        "total_events": total_events,
        "rule_match_rate": safe_rate(rule_matched_count, total_events),
        "memory_match_rate": safe_rate(memory_matched_count, total_events),
        "documentation_found_rate": safe_rate(documentation_found_count, total_events),
        "llm_usage_rate": safe_rate(llm_used_count, total_events),
        "promotion_rate": safe_rate(promoted_to_rule_count, total_events),
        "unresolved_rate": safe_rate(unresolved_count, total_events),
        "execution_success_rate": safe_rate(
            execution_success_count,
            execution_success_count + execution_failed_count,
        ),
        "top_event_types": event_type_counter.most_common(5),
        "top_rules": rule_counter.most_common(5),
        "top_memories": memory_counter.most_common(5),
        "documentation_gaps": documentation_gap_counter.most_common(5),
    }