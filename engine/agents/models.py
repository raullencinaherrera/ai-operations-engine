from dataclasses import dataclass
from typing import List


@dataclass
class ContextRequest:
    event_type: str
    source: str
    summary: str
    query: str


@dataclass
class ContextResponse:
    snippets: List[str]
    sources: List[str]