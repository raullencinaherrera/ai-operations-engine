from engine.feedback.execution_feedback import ExecutionFeedback
from engine.feedback.memory_updater import update_memory_from_execution_feedback
from engine.feedback.promotion import build_rule_candidate, should_promote_memory
from engine.feedback.result_classifier import classify_execution_result


MEMORY_PATH = "engine/memory/memory_store.jsonl"


feedback = ExecutionFeedback(
    event_id="evt_001",
    plan_id="resolve_authentication_issue",
    execution_id="rundeck_exec_123",
    status="success",
    logs="Token refreshed successfully. Flow retry completed.",
    applied_resolution="refresh_token",
    memory_id="mem_001",
)

classification = classify_execution_result(feedback)

print("Classification:")
print("Status:", classification.status)
print("Worked:", classification.worked)
print("Ambiguous:", classification.ambiguous)
print("Reason:", classification.reason)
print("---")

if classification.ambiguous:
    print("Result is ambiguous. Reasoning agent should review this feedback.")
else:
    updated_record = update_memory_from_execution_feedback(
        memory_path=MEMORY_PATH,
        feedback=feedback,
        classification=classification,
    )

    print("Memory updated:")
    print("ID:", updated_record["id"])
    print("Success count:", updated_record.get("success_count"))
    print("Failure count:", updated_record.get("failure_count"))
    print("---")

    if should_promote_memory(updated_record, threshold=5):
        candidate = build_rule_candidate(updated_record)
        print("Rule candidate ready for governance:")
        print("ID:", candidate.id)
        print("Recommended action:", candidate.recommended_action)
    else:
        print("Memory not ready for rule promotion yet.")