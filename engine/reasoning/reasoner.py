import os

from engine.reasoning.gemini_reasoner import analyze_with_gemini
from engine.reasoning.mock_reasoner import analyze_with_mock_reasoner
from engine.reasoning.models import ReasoningRequest, ReasoningResult


def analyze_event(request: ReasoningRequest) -> ReasoningResult:
    provider = os.getenv("LLM_PROVIDER", "mock").lower()

    if provider == "gemini":
        return analyze_with_gemini(request)

    return analyze_with_mock_reasoner(request)