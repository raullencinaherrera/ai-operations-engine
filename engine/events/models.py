from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class OperationalEvent:
    event_type: str
    source: str
    summary: str
    raw_event: Dict[str, Any] = field(default_factory=dict)
    logs: Optional[str] = None
    message: Optional[str] = None
    reason: Optional[str] = None
    error: Optional[str] = None
    tags: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_type": self.event_type,
            "source": self.source,
            "summary": self.summary,
            "logs": self.logs,
            "message": self.message,
            "reason": self.reason,
            "error": self.error,
            "tags": self.tags,
            "raw_event": self.raw_event,
        }