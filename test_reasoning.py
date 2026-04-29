from engine.events.normalizer import normalize_event
from engine.memory.store import load_memory
from engine.orchestrator.decision import build_decision
from engine.reasoning.mock_reasoner import analyze_with_mock_reasoner
from engine.reasoning.models import ReasoningRequest
from engine.rules.loader import load_rules


raw_event = {
    "flow_name": "update_customer_inventory",
    "state": "FAILED",
    "logs": "Request failed with 403 Forbidden. Service account does not have permission.",
}

event = normalize_event("prefect", raw_event)

rules = load_rules("engine/rules/rules.yaml")
memory_records = load_memory("engine/memory/memory_store.jsonl")

decision = build_decision(event.to_dict(), rules, memory_records)

print("Decision:", decision.decision)
print("Requires LLM:", decision.requires_llm)
print("Reason:", decision.reason)
print("---")

if decision.requires_llm:
    request = ReasoningRequest(
        event_type=event.event_type,
        source=event.source,
        summary=event.summary,
        context=event.logs or event.message or event.reason or event.error or "",
        known_rule_matches=len(decision.rule_matches),
        known_memory_matches=len(decision.memory_matches),
    )

    result = analyze_with_mock_reasoner(request)

    print("Probable cause:", result.probable_cause)
    print("Recommended action:", result.recommended_action)
    print("Confidence:", result.confidence)
    print("Rule candidate:", result.rule_candidate)
    print("Notes:")
    for note in result.reasoning_notes:
        print("-", note)
else:
    print("No reasoning needed.")