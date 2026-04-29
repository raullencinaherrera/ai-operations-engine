from typing import Any, Dict, List

from engine.rules.models import Rule, RuleMatch


def get_field_value(event: Dict[str, Any], field: str) -> Any:
    return event.get(field)


def evaluate_condition(event: Dict[str, Any], condition: Dict[str, Any]) -> bool:
    field = condition["field"]
    operator = condition["operator"]
    expected_value = condition["value"]

    actual_value = get_field_value(event, field)

    if actual_value is None:
        return False

    actual_text = str(actual_value).lower()

    if operator == "equals":
        return actual_value == expected_value

    if operator == "contains":
        return str(expected_value).lower() in actual_text

    if operator == "contains_any":
        return any(str(item).lower() in actual_text for item in expected_value)

    if operator == "contains_all":
        return all(str(item).lower() in actual_text for item in expected_value)

    raise ValueError(f"Unsupported operator: {operator}")


def rule_matches_event(rule: Rule, event: Dict[str, Any]) -> bool:
    if not rule.enabled:
        return False

    if rule.event_type != event.get("event_type"):
        return False

    conditions = rule.conditions

    if "all" in conditions:
        return all(evaluate_condition(event, condition) for condition in conditions["all"])

    if "any" in conditions:
        return any(evaluate_condition(event, condition) for condition in conditions["any"])

    return False


def evaluate_rules(rules: List[Rule], event: Dict[str, Any]) -> List[RuleMatch]:
    matches: List[RuleMatch] = []

    for rule in rules:
        if rule_matches_event(rule, event):
            matches.append(
                RuleMatch(
                    rule_id=rule.id,
                    rule_name=rule.name,
                    action_type=rule.action.type,
                    message=rule.action.message,
                    confidence=rule.action.confidence,
                    priority=rule.priority,
                )
            )

    return matches