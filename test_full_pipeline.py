from engine.events.examples import PREFECT_FAILED_EVENT
from engine.events.normalizer import normalize_event
from engine.memory.store import load_memory
from engine.orchestrator.decision import build_decision
from engine.rules.loader import load_rules


raw_event = PREFECT_FAILED_EVENT

event = normalize_event("prefect", raw_event)

rules = load_rules("engine/rules/rules.yaml")
memory_records = load_memory("engine/memory/memory_store.jsonl")

decision = build_decision(event.to_dict(), rules, memory_records)

print("Normalized event:")
print(event.to_dict())
print("---")
print("Decision:", decision.decision)
print("Recommended action:", decision.recommended_action)
print("Confidence:", decision.confidence)
print("Requires LLM:", decision.requires_llm)
print("Reason:", decision.reason)