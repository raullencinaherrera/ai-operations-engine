from pathlib import Path
from typing import Dict

import yaml

from engine.feedback.models import RuleCandidate


def rule_candidate_to_yaml_rule(candidate: RuleCandidate) -> Dict:
    return {
        "id": candidate.id.replace("candidate_", "promoted_"),
        "name": candidate.name.replace("Rule candidate from memory: ", ""),
        "description": candidate.description,
        "enabled": True,
        "priority": 70,
        "event_type": candidate.event_type,
        "conditions": {
            "any": [
                {
                    "field": "logs",
                    "operator": "contains",
                    "value": symptom,
                }
                for symptom in candidate.symptoms
            ]
        },
        "action": {
            "type": "recommend",
            "message": candidate.recommended_action,
            "confidence": candidate.confidence,
        },
    }


def append_rule_to_rules_file(rules_path: str | Path, candidate: RuleCandidate) -> None:
    from engine.rules.governance import validate_rule_governance

    path = Path(rules_path)

    if path.exists():
        with path.open("r", encoding="utf-8") as file:
            data = yaml.safe_load(file) or {}
    else:
        data = {"rules": []}

    data.setdefault("rules", [])

    new_rule = rule_candidate_to_yaml_rule(candidate)

    governance_result = validate_rule_governance(
        new_rule=new_rule,
        existing_rules=data["rules"],
    )

    if governance_result.warnings:
        print("\nGovernance warnings:")
        for warning in governance_result.warnings:
            print(f"- {warning}")

    if not governance_result.approved:
        print("\nGovernance errors:")
        for error in governance_result.errors:
            print(f"- {error}")

        raise ValueError("Rule candidate rejected by governance validation.")

    data["rules"].append(new_rule)

    with path.open("w", encoding="utf-8") as file:
        yaml.safe_dump(data, file, sort_keys=False, allow_unicode=True)


def request_human_approval(candidate: RuleCandidate) -> bool:
    print("\nRule candidate requires human approval")
    print("--------------------------------------")
    print(f"ID: {candidate.id}")
    print(f"Name: {candidate.name}")
    print(f"Event type: {candidate.event_type}")
    print(f"Source: {candidate.source}")
    print(f"Symptoms: {candidate.symptoms}")
    print(f"Recommended action: {candidate.recommended_action}")
    print(f"Confidence: {candidate.confidence}")
    print(f"Success count: {candidate.success_count}")
    print("--------------------------------------")

    answer = input("Approve promotion to deterministic rule? (yes/no): ").strip().lower()

    return answer in ["yes", "y"]