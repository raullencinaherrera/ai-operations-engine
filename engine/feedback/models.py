from dataclasses import dataclass
from typing import List


@dataclass
class FeedbackResult:
    memory_id: str
    worked: bool
    notes: str = ""


@dataclass
class RuleCandidate:
    id: str
    name: str
    description: str
    event_type: str
    source: str
    symptoms: List[str]
    recommended_action: str
    confidence: str
    success_count: int