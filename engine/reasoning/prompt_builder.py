from engine.reasoning.models import ReasoningRequest


def build_reasoning_prompt(request: ReasoningRequest) -> str:
    return f"""
You are an AI operations assistant.

Analyze the following operational event and provide:
1. Probable cause
2. Recommended action
3. Confidence level
4. Whether this should become a deterministic rule candidate

Event type: {request.event_type}
Source: {request.source}
Summary: {request.summary}

Context:
{request.context}

Known rule matches: {request.known_rule_matches}
Known memory matches: {request.known_memory_matches}

Important principles:
- Prefer safe recommendations.
- Do not execute changes directly.
- If the issue is repetitive and easy to detect, suggest creating a deterministic rule.
""".strip()