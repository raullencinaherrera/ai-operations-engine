from dataclasses import dataclass
from typing import Optional


@dataclass
class ExecutionFeedback:
    event_id: str
    plan_id: str
    execution_id: str
    status: str
    logs: str
    applied_resolution: str
    memory_id: Optional[str] = None


@dataclass
class FeedbackClassification:
    status: str
    worked: bool
    ambiguous: bool
    reason: str