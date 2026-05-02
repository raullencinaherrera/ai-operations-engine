from typing import Dict


def build_markdown_report(metrics: Dict) -> str:
    lines = [
        "# AI Operations Engine Control Report",
        "",
        "## Summary",
        "",
        f"- Total events processed: {metrics['total_events']}",
        f"- Rule match rate: {metrics['rule_match_rate']}",
        f"- Memory match rate: {metrics['memory_match_rate']}",
        f"- Documentation found rate: {metrics['documentation_found_rate']}",
        f"- LLM usage rate: {metrics['llm_usage_rate']}",
        f"- Promotion rate: {metrics['promotion_rate']}",
        f"- Unresolved rate: {metrics['unresolved_rate']}",
        f"- Execution success rate: {metrics['execution_success_rate']}",
        "",
        "## Top Event Types",
        "",
    ]

    for event_type, count in metrics["top_event_types"]:
        lines.append(f"- {event_type}: {count}")

    lines.extend(["", "## Top Rules", ""])

    for rule_id, count in metrics["top_rules"]:
        lines.append(f"- {rule_id}: {count}")

    lines.extend(["", "## Top Memories", ""])

    for memory_id, count in metrics["top_memories"]:
        lines.append(f"- {memory_id}: {count}")

    lines.extend(["", "## Documentation Gaps", ""])

    for event_type, count in metrics["documentation_gaps"]:
        lines.append(f"- {event_type}: {count}")

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- High rule match rate means the deterministic reflex layer is effective.",
            "- High LLM usage may indicate missing rules, weak memory, or documentation gaps.",
            "- Documentation gaps identify areas where operational knowledge should be improved.",
            "- Promotion rate shows how often repeated successful solutions become rule candidates.",
        ]
    )

    return "\n".join(lines)