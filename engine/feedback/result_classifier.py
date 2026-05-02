from engine.feedback.execution_feedback import ExecutionFeedback, FeedbackClassification


SUCCESS_TERMS = [
    "success",
    "completed successfully",
    "recovered",
    "resolved",
    "token refreshed successfully",
    "flow retry completed",
]

FAILURE_TERMS = [
    "failed",
    "error",
    "exception",
    "traceback",
    "permission denied",
    "still failing",
]


def classify_execution_result(feedback: ExecutionFeedback) -> FeedbackClassification:
    status = feedback.status.lower()
    logs = feedback.logs.lower()

    if status in ["success", "succeeded", "completed"]:
        return FeedbackClassification(
            status="success",
            worked=True,
            ambiguous=False,
            reason="Execution status indicates success.",
        )

    if status in ["failed", "failure", "error"]:
        return FeedbackClassification(
            status="failed",
            worked=False,
            ambiguous=False,
            reason="Execution status indicates failure.",
        )

    if any(term in logs for term in SUCCESS_TERMS):
        return FeedbackClassification(
            status="success",
            worked=True,
            ambiguous=False,
            reason="Execution logs contain success indicators.",
        )

    if any(term in logs for term in FAILURE_TERMS):
        return FeedbackClassification(
            status="failed",
            worked=False,
            ambiguous=False,
            reason="Execution logs contain failure indicators.",
        )

    return FeedbackClassification(
        status="unknown",
        worked=False,
        ambiguous=True,
        reason="Execution result could not be classified deterministically.",
    )