from engine.agents.documentation_context_agent import DocumentationContextAgent
from engine.agents.event_reasoning_agent import EventReasoningAgent


event_agent = EventReasoningAgent(
    rules_path="engine/rules/rules.yaml",
    memory_path="engine/memory/memory_store.jsonl",
)

doc_agent = DocumentationContextAgent(
    docs_path="docs/operational_knowledge.md"
)


raw_event = {
    "flow_name": "update_customer_inventory",
    "state": "FAILED",
    "logs": "Request failed with 403 Forbidden. Service account does not have permission.",
}


result = event_agent.process_event(
    source="prefect",
    raw_event=raw_event,
    documentation_agent=doc_agent,
)

print("Type:", result["type"])
print("---")

if result["type"] == "deterministic":
    print("Deterministic decision:")
    print(result["decision"].recommended_action)

else:
    print("Context sources:")
    
    for source in result["context_sources"]:
        print("-", source)

    print("---")
    reasoning = result["reasoning"]

    print("Probable cause:", reasoning.probable_cause)
    print("Recommended action:", reasoning.recommended_action)
    print("Confidence:", reasoning.confidence)
    print("Rule candidate:", reasoning.rule_candidate)