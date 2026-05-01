from engine.context.builder import build_context_bundle
from engine.context.sources.local_docs import load_local_markdown_documents
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
documents = load_local_markdown_documents("docs/operational_knowledge.md")

decision = build_decision(event.to_dict(), rules, memory_records)

print("Decision:", decision.decision)
print("Requires LLM:", decision.requires_llm)
print("Reason:", decision.reason)
print("---")

if decision.requires_llm:
    context_bundle = build_context_bundle(event.to_dict(), documents)

    operational_context = event.logs or event.message or event.reason or event.error or ""

    documentation_context = "\n\n".join(context_bundle.snippets)

    enriched_context = f"""
Operational event context:
{operational_context}

Relevant documentation context:
{documentation_context}
""".strip()

    request = ReasoningRequest(
        event_type=event.event_type,
        source=event.source,
        summary=event.summary,
        context=enriched_context,
        known_rule_matches=len(decision.rule_matches),
        known_memory_matches=len(decision.memory_matches),
    )

    result = analyze_with_mock_reasoner(request)

    print("Context sources:")
    for source in context_bundle.sources:
        print("-", source)

    print("---")
    print("Probable cause:", result.probable_cause)
    print("Recommended action:", result.recommended_action)
    print("Confidence:", result.confidence)
    print("Rule candidate:", result.rule_candidate)
    print("Notes:")
    for note in result.reasoning_notes:
        print("-", note)
else:
    print("No reasoning needed.")