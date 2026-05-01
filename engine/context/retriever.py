from typing import List

from engine.context.models import ContextDocument, ContextMatch


STOPWORDS = {
    "the",
    "and",
    "or",
    "to",
    "a",
    "an",
    "of",
    "in",
    "with",
    "by",
    "for",
    "is",
    "was",
    "were",
    "be",
    "from",
    "this",
    "that",
}


def tokenize(text: str) -> List[str]:
    cleaned = (
        text.lower()
        .replace(".", " ")
        .replace(",", " ")
        .replace(":", " ")
        .replace(";", " ")
        .replace("(", " ")
        .replace(")", " ")
        .replace("-", " ")
        .replace("_", " ")
    )

    return [
        token.strip()
        for token in cleaned.split()
        if token.strip() and token.strip() not in STOPWORDS and len(token.strip()) > 2
    ]


def score_document(query: str, document: ContextDocument) -> ContextMatch:
    query_terms = tokenize(query)
    document_text = f"{document.title}\n{document.content}".lower()

    score = 0
    matched_terms = []

    for term in query_terms:
        if term in document_text:
            score += 10
            matched_terms.append(term)

    return ContextMatch(
        document=document,
        score=score,
        matched_terms=matched_terms,
    )


def retrieve_context(
    query: str,
    documents: List[ContextDocument],
    minimum_score: int = 10,
    limit: int = 3,
) -> List[ContextMatch]:
    matches = []

    for document in documents:
        match = score_document(query, document)

        if match.score >= minimum_score:
            matches.append(match)

    return sorted(matches, key=lambda item: item.score, reverse=True)[:limit]