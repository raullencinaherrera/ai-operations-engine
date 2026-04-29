from engine.memory.store import load_memory
from engine.memory.search import search_memory


event = {
    "event_type": "flow.failed",
    "source": "prefect",
    "flow_name": "sync_inventory",
    "logs": "Request failed with 401 Unauthorized: invalid token",
    "tags": ["prefect", "authentication"],
}

records = load_memory("engine/memory/memory_store.jsonl")
matches = search_memory(records, event)

for match in matches:
    print("Score:", match.score)
    print("Memory:", match.record.summary)
    print("Root cause:", match.record.root_cause)
    print("Resolution:", match.record.resolution)
    print("Matched terms:", match.matched_terms)
    print("---")