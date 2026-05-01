import json
import os
import re

from google import genai

from engine.reasoning.models import ReasoningRequest, ReasoningResult
from engine.reasoning.prompt_builder import build_reasoning_prompt


def extract_json_from_response(raw_text: str) -> dict:
    cleaned = raw_text.strip()

    # Remove Markdown code fences if Gemini returns ```json ... ```
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?", "", cleaned, flags=re.IGNORECASE).strip()
        cleaned = re.sub(r"```$", "", cleaned).strip()

    # Fallback: extract first JSON object from the response
    if not cleaned.startswith("{"):
        match = re.search(r"\{.*\}", cleaned, flags=re.DOTALL)
        if not match:
            raise ValueError(f"No JSON object found in Gemini response: {raw_text}")
        cleaned = match.group(0)

    return json.loads(cleaned)


def analyze_with_gemini(request: ReasoningRequest) -> ReasoningResult:
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("GEMINI_API_KEY is not configured.")

    model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

    client = genai.Client(api_key=api_key)

    prompt = build_reasoning_prompt(request)

    json_instruction = """
Return only valid JSON. Do not wrap it in Markdown fences.

Use this exact structure:
{
  "probable_cause": "string",
  "recommended_action": "string",
  "confidence": "low|medium|high",
  "reasoning_notes": ["string"],
  "rule_candidate": true
}
""".strip()

    response = client.models.generate_content(
        model=model,
        contents=f"{prompt}\n\n{json_instruction}",
    )

    raw_text = response.text.strip()
    data = extract_json_from_response(raw_text)

    return ReasoningResult(
        probable_cause=data.get("probable_cause", "Unknown"),
        recommended_action=data.get("recommended_action", "Escalate to an engineer."),
        confidence=data.get("confidence", "low"),
        reasoning_notes=data.get("reasoning_notes", []),
        rule_candidate=bool(data.get("rule_candidate", False)),
    )