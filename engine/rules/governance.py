from dataclasses import dataclass, field
from typing import Dict, List


DANGEROUS_ACTION_TYPES = {
    "execute",
    "delete",
    "restart",
    "modify",
    "deploy",
}

GENERIC_TERMS = {
    "error",
    "failed",
    "failure",
    "exception",
    "unknown",
    "issue",
    "problem",
}


@dataclass
class RuleGovernanceResult:
    approved: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)


def validate_rule_governance(
    new_rule: Dict,
    existing_rules: List[Dict],
) -> RuleGovernanceResult:
    result = RuleGovernanceResult(approved=True)

    existing_ids = {rule.get("id") for rule in existing_rules}

    rule_id = new_rule.get("id")
    if not rule_id:
        result.errors.append("Rule must have an id.")
    elif rule_id in existing_ids:
        result.errors.append(f"Duplicated rule id: {rule_id}")

    if not new_rule.get("name"):
        result.errors.append("Rule must have a name.")

    if not new_rule.get("event_type"):
        result.errors.append("Rule must have an event_type.")

    priority = new_rule.get("priority", 0)
    if not isinstance(priority, int):
        result.errors.append("Rule priority must be an integer.")
    elif priority < 1 or priority > 100:
        result.errors.append("Rule priority must be between 1 and 100.")

    conditions = new_rule.get("conditions", {})
    condition_items = []

    if "all" in conditions:
        condition_items.extend(conditions["all"])

    if "any" in conditions:
        condition_items.extend(conditions["any"])

    if not condition_items:
        result.errors.append("Rule must have at least one condition.")

    if len(condition_items) > 5:
        result.warnings.append("Rule has more than 5 conditions. Consider simplifying it.")

    for condition in condition_items:
        field = condition.get("field")
        operator = condition.get("operator")
        value = condition.get("value")

        if not field:
            result.errors.append("Every condition must define a field.")

        if operator not in {"equals", "contains", "contains_any", "contains_all"}:
            result.errors.append(f"Unsupported operator: {operator}")

        if value in [None, "", []]:
            result.errors.append("Every condition must define a non-empty value.")

        if isinstance(value, str) and value.lower() in GENERIC_TERMS:
            result.errors.append(
                f"Condition value '{value}' is too generic and may cause noisy matches."
            )

    action = new_rule.get("action", {})
    action_type = action.get("type")

    if not action_type:
        result.errors.append("Rule action must define a type.")

    if action_type in DANGEROUS_ACTION_TYPES:
        result.errors.append(
            f"Action type '{action_type}' is not allowed for promoted rules."
        )

    if not action.get("message"):
        result.errors.append("Rule action must include a message.")

    if action.get("confidence") not in {"low", "medium", "high"}:
        result.errors.append("Rule confidence must be low, medium or high.")

    detect_potential_conflicts(new_rule, existing_rules, result)

    if result.errors:
        result.approved = False

    return result


def detect_potential_conflicts(
    new_rule: Dict,
    existing_rules: List[Dict],
    result: RuleGovernanceResult,
) -> None:
    new_event_type = new_rule.get("event_type")
    new_conditions = extract_condition_signature(new_rule)

    for existing_rule in existing_rules:
        if existing_rule.get("event_type") != new_event_type:
            continue

        existing_conditions = extract_condition_signature(existing_rule)

        overlap = new_conditions.intersection(existing_conditions)

        if overlap:
            result.warnings.append(
                f"Potential overlap with rule '{existing_rule.get('id')}' on conditions: {sorted(overlap)}"
            )


def extract_condition_signature(rule: Dict) -> set[str]:
    conditions = rule.get("conditions", {})
    condition_items = []

    if "all" in conditions:
        condition_items.extend(conditions["all"])

    if "any" in conditions:
        condition_items.extend(conditions["any"])

    signature = set()

    for condition in condition_items:
        field = condition.get("field", "")
        operator = condition.get("operator", "")
        value = condition.get("value", "")

        if isinstance(value, list):
            for item in value:
                signature.add(f"{field}:{operator}:{str(item).lower()}")
        else:
            signature.add(f"{field}:{operator}:{str(value).lower()}")

    return signature