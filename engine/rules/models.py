from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class RuleAction:
    type: str
    message: str
    confidence: str = "medium"


@dataclass
class Rule:
    id: str
    name: str
    description: str
    enabled: bool
    priority: int
    event_type: str
    conditions: Dict[str, List[Dict[str, Any]]]
    action: RuleAction


@dataclass
class RuleMatch:
    rule_id: str
    rule_name: str
    action_type: str
    message: str
    confidence: str
    priority: int