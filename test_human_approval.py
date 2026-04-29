from engine.feedback.approval import append_rule_to_rules_file, request_human_approval
from engine.feedback.models import FeedbackResult
from engine.feedback.promotion import build_rule_candidate, should_promote_memory
from engine.feedback.recorder import record_feedback


MEMORY_PATH = "engine/memory/memory_store.jsonl"
RULES_PATH = "engine/rules/rules.yaml"

feedback = FeedbackResult(
    memory_id="mem_001",
    worked=True,
    notes="Human confirmed that the token refresh resolution worked.",
)

updated_record = record_feedback(MEMORY_PATH, feedback)

print("Updated memory:")
print("ID:", updated_record["id"])
print("Success count:", updated_record.get("success_count"))
print("Failure count:", updated_record.get("failure_count"))

if should_promote_memory(updated_record, threshold=5):
    candidate = build_rule_candidate(updated_record)

    approved = request_human_approval(candidate)

    if approved:
        append_rule_to_rules_file(RULES_PATH, candidate)
        print("Rule approved and added to rules.yaml")
    else:
        print("Rule candidate rejected by human reviewer.")
else:
    print("Not ready for promotion yet.")