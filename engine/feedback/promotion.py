from engine.feedback.models import RuleCandidate


def should_promote_memory(record: dict, threshold: int = 5) -> bool:
    success_count = record.get("success_count", 0)
    failure_count = record.get("failure_count", 0)

    if success_count < threshold:
        return False

    if failure_count > 0 and success_count / (success_count + failure_count) < 0.8:
        return False

    return True


def build_rule_candidate(record: dict) -> RuleCandidate:
    return RuleCandidate(
        id=f"candidate_{record['id']}",
        name=f"Rule candidate from memory: {record['summary']}",
        description=(
            "This rule candidate was generated from operational memory "
            "after repeated successful resolutions."
        ),
        event_type=record["event_type"],
        source=record.get("source", ""),
        symptoms=record.get("symptoms", []),
        recommended_action=record["resolution"],
        confidence=record.get("confidence", "medium"),
        success_count=record.get("success_count", 0),
    )