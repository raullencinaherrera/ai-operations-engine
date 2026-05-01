from engine.agents.models import ContextRequest, ContextResponse
from engine.context.builder import build_context_bundle
from engine.context.sources.local_docs import load_local_markdown_documents


class DocumentationContextAgent:
    def __init__(self, docs_path: str):
        self.documents = load_local_markdown_documents(docs_path)

    def retrieve_context(self, request: ContextRequest) -> ContextResponse:
        context_bundle = build_context_bundle(
            {
                "summary": request.summary,
                "logs": request.query,
                "tags": [request.source, request.event_type],
            },
            self.documents,
        )

        return ContextResponse(
            snippets=context_bundle.snippets,
            sources=context_bundle.sources,
        )