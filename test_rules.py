from engine.rules.loader import load_rules
from engine.rules.evaluator import evaluate_rules


event = {
    "event_type": "flow.failed",
    "source": "prefect",
    "flow_name": "sync_inventory",
    "logs": "Request failed with 401 Unauthorized: invalid token",
}

rules = load_rules("engine/rules/rules.yaml")
matches = evaluate_rules(rules, event)

for match in matches:
    print(match)