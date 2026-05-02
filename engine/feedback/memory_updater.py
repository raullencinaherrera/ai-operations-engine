from typing import Dict

from engine.feedback.execution_feedback import ExecutionFeedback, FeedbackClassification
from engine.feedback.models import FeedbackResult
from engine.feedback.recorder import record_feedback


def update_memory_from_execution_feedback(
    memory_path: str,
    feedback: ExecutionFeedback,
    classification: FeedbackClassification,
) -> Dict:
    if not feedback.memory_id:
        raise ValueError("Execution feedback does not include memory_id. Cannot update memory.")

    feedback_result = FeedbackResult(
        memory_id=feedback.memory_id,
        worked=classification.worked,
        notes=(
            f"Execution feedback from {feedback.execution_id}. "
            f"Plan: {feedback.plan_id}. "
            f"Applied resolution: {feedback.applied_resolution}. "
            f"Classification: {classification.status}. "
            f"Reason: {classification.reason}"
        ),
    )

    return record_feedback(memory_path, feedback_result)