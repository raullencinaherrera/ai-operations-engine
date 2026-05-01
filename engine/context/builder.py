from typing import Any, Dict, List

from engine.context.models import ContextBundle, ContextDocument
from engine.context.retriever import retrieve_context


def build_event_query(event: Dict[str, Any]) -> str:
    parts = []

    for key in ["summary", "logs", "message", "reason", "error"]:
        value = event.get(key)

        if value:
            parts.append(str(value))

    tags = event.get("tags", [])
    if tags:
        parts.extend(tags)

    return " ".join(parts)


def build_context_bundle(
    event: Dict[str, Any],
    documents: List[ContextDocument],
    limit: int = 3,
) -> ContextBundle:
    query = build_event_query(event)

    matches = retrieve_context(
        query=query,
        documents=documents,
        limit=limit,
    )

    snippets = [
        f"Source: {match.document.title}\n{match.document.content[:700]}"
        for match in matches
    ]

    sources = [
        match.document.title
        for match in matches
    ]

    return ContextBundle(
        snippets=snippets,
        sources=sources,
        matches=matches,
    )