from dataclasses import dataclass, field
from typing import List


@dataclass
class ReasoningRequest:
    event_type: str
    source: str
    summary: str
    context: str
    known_rule_matches: int = 0
    known_memory_matches: int = 0


@dataclass
class ReasoningResult:
    probable_cause: str
    recommended_action: str
    confidence: str
    reasoning_notes: List[str] = field(default_factory=list)
    rule_candidate: bool = False