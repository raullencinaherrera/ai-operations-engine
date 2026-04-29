from engine.reasoning.models import ReasoningRequest, ReasoningResult
from engine.reasoning.prompt_builder import build_reasoning_prompt


def analyze_with_mock_reasoner(request: ReasoningRequest) -> ReasoningResult:
    prompt = build_reasoning_prompt(request)

    context = request.context.lower()

    if "permission" in context or "forbidden" in context or "403" in context:
        return ReasoningResult(
            probable_cause="The automation failed due to insufficient permissions or access restrictions.",
            recommended_action="Review the service account permissions and validate access to the target system.",
            confidence="medium",
            reasoning_notes=[
                "The event does not match a high-confidence deterministic rule.",
                "The context contains permission-related symptoms.",
                "This may become a deterministic rule if repeated.",
            ],
            rule_candidate=True,
        )

    if "not found" in context or "404" in context:
        return ReasoningResult(
            probable_cause="The automation referenced a resource or endpoint that does not exist.",
            recommended_action="Validate the target endpoint, resource identifier, or API path used by the automation.",
            confidence="medium",
            reasoning_notes=[
                "The context suggests a missing resource.",
                "This may be caused by a wrong endpoint, deleted resource, or incorrect identifier.",
            ],
            rule_candidate=True,
        )

    return ReasoningResult(
        probable_cause="The issue could not be confidently classified by the current mock reasoning engine.",
        recommended_action="Escalate to an engineer for review and collect additional logs, metadata and execution context.",
        confidence="low",
        reasoning_notes=[
            "No deterministic rule was matched.",
            "No strong operational memory was found.",
            "The reasoning engine needs more context to classify the issue.",
            f"Prompt generated for future LLM call:\n{prompt}",
        ],
        rule_candidate=False,
    )