from dataclasses import dataclass, field
from typing import List


@dataclass
class MemoryRecord:
    id: str
    event_type: str
    source: str
    summary: str
    symptoms: List[str]
    root_cause: str
    resolution: str
    success_count: int = 0
    failure_count: int = 0
    confidence: str = "medium"
    tags: List[str] = field(default_factory=list)


@dataclass
class MemoryMatch:
    record: MemoryRecord
    score: int
    matched_terms: List[str]