from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List, Optional


@dataclass
class EngineTraceEvent:
    event_id: str
    event_type: str
    source: str
    decision: str
    rule_matched: bool = False
    rule_ids: List[str] = field(default_factory=list)
    memory_matched: bool = False
    memory_ids: List[str] = field(default_factory=list)
    documentation_found: bool = False
    documentation_sources: List[str] = field(default_factory=list)
    llm_used: bool = False
    execution_status: Optional[str] = None
    promoted_to_rule: bool = False
    unresolved: bool = False
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())