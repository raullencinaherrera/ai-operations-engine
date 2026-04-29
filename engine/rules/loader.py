from pathlib import Path
from typing import List

import yaml

from engine.rules.models import Rule, RuleAction


def load_rules(path: str | Path) -> List[Rule]:
    rules_path = Path(path)

    if not rules_path.exists():
        raise FileNotFoundError(f"Rules file not found: {rules_path}")

    with rules_path.open("r", encoding="utf-8") as file:
        data = yaml.safe_load(file) or {}

    loaded_rules: List[Rule] = []

    for raw_rule in data.get("rules", []):
        raw_action = raw_rule["action"]

        action = RuleAction(
            type=raw_action["type"],
            message=raw_action["message"],
            confidence=raw_action.get("confidence", "medium"),
        )

        rule = Rule(
            id=raw_rule["id"],
            name=raw_rule["name"],
            description=raw_rule.get("description", ""),
            enabled=raw_rule.get("enabled", True),
            priority=raw_rule.get("priority", 0),
            event_type=raw_rule["event_type"],
            conditions=raw_rule.get("conditions", {}),
            action=action,
        )

        loaded_rules.append(rule)

    return sorted(loaded_rules, key=lambda rule: rule.priority, reverse=True)