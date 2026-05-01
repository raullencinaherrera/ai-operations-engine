from dataclasses import dataclass, field
from typing import List


@dataclass
class ContextDocument:
    id: str
    title: str
    content: str
    source: str = "local"


@dataclass
class ContextMatch:
    document: ContextDocument
    score: int
    matched_terms: List[str] = field(default_factory=list)


@dataclass
class ContextBundle:
    snippets: List[str]
    sources: List[str]
    matches: List[ContextMatch] = field(default_factory=list)