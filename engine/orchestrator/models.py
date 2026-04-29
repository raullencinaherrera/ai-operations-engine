from dataclasses import dataclass, field
from typing import List, Optional

from engine.memory.models import MemoryMatch
from engine.rules.models import RuleMatch


@dataclass
class OperationalDecision:
    decision: str
    recommended_action: str
    confidence: str
    requires_llm: bool
    rule_matches: List[RuleMatch] = field(default_factory=list)
    memory_matches: List[MemoryMatch] = field(default_factory=list)
    reason: Optional[str] = None