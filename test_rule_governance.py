import yaml

from engine.feedback.approval import rule_candidate_to_yaml_rule
from engine.feedback.models import RuleCandidate
from engine.rules.governance import validate_rule_governance


RULES_PATH = "engine/rules/rules.yaml"

with open(RULES_PATH, "r", encoding="utf-8") as file:
    existing_data = yaml.safe_load(file) or {}

existing_rules = existing_data.get("rules", [])

candidate = RuleCandidate(
    id="candidate_test_governance",
    name="Rule candidate from memory: Generic failure rule",
    description="This candidate should be reviewed by governance.",
    event_type="flow.failed",
    source="prefect",
    symptoms=["error"],
    recommended_action="Review the failure.",
    confidence="high",
    success_count=10,
)

new_rule = rule_candidate_to_yaml_rule(candidate)

result = validate_rule_governance(
    new_rule=new_rule,
    existing_rules=existing_rules,
)

print("Approved:", result.approved)

print("\nErrors:")
for error in result.errors:
    print("-", error)

print("\nWarnings:")
for warning in result.warnings:
    print("-", warning)