from engine.memory.store import load_memory
from engine.orchestrator.decision import build_decision
from engine.rules.loader import load_rules


event = {
    "event_type": "flow.failed",
    "source": "prefect",
    "flow_name": "sync_inventory",
    "logs": "Request failed with 401 Unauthorized: invalid token",
    "tags": ["prefect", "authentication"],
}

rules = load_rules("engine/rules/rules.yaml")
memory_records = load_memory("engine/memory/memory_store.jsonl")

decision = build_decision(event, rules, memory_records)

print("Decision:", decision.decision)
print("Recommended action:", decision.recommended_action)
print("Confidence:", decision.confidence)
print("Requires LLM:", decision.requires_llm)
print("Reason:", decision.reason)
print("Rule matches:", len(decision.rule_matches))
print("Memory matches:", len(decision.memory_matches))