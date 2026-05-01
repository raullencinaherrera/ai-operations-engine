from engine.context.builder import build_context_bundle
from engine.context.sources.local_docs import load_local_markdown_documents
from engine.events.normalizer import normalize_event


raw_event = {
    "flow_name": "update_customer_inventory",
    "state": "FAILED",
    "logs": "Request failed with 403 Forbidden. Service account does not have permission.",
}

event = normalize_event("prefect", raw_event)

documents = load_local_markdown_documents("docs/operational_knowledge.md")
context_bundle = build_context_bundle(event.to_dict(), documents)

print("Event:")
print(event.to_dict())
print("---")

print("Context sources:")
for source in context_bundle.sources:
    print("-", source)

print("---")

print("Context snippets:")
for snippet in context_bundle.snippets:
    print(snippet)
    print("---")

print("Matches:")
for match in context_bundle.matches:
    print(match.document.title, "score:", match.score, "matched:", match.matched_terms)