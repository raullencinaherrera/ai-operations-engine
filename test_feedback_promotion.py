from engine.feedback.models import FeedbackResult
from engine.feedback.promotion import build_rule_candidate, should_promote_memory
from engine.feedback.recorder import record_feedback


MEMORY_PATH = "engine/memory/memory_store.jsonl"

feedback = FeedbackResult(
    memory_id="mem_001",
    worked=True,
    notes="Applied token refresh recommendation and the flow recovered successfully.",
)

updated_record = record_feedback(MEMORY_PATH, feedback)

print("Updated memory:")
print("ID:", updated_record["id"])
print("Success count:", updated_record.get("success_count"))
print("Failure count:", updated_record.get("failure_count"))
print("---")

if should_promote_memory(updated_record, threshold=5):
    candidate = build_rule_candidate(updated_record)

    print("Promotion candidate created:")
    print("ID:", candidate.id)
    print("Name:", candidate.name)
    print("Event type:", candidate.event_type)
    print("Symptoms:", candidate.symptoms)
    print("Recommended action:", candidate.recommended_action)
    print("Success count:", candidate.success_count)
else:
    print("Not ready for promotion yet.")