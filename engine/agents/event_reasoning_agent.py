from engine.agents.models import ContextRequest
from engine.events.normalizer import normalize_event
from engine.memory.store import load_memory
from engine.orchestrator.decision import build_decision
from engine.reasoning.reasoner import analyze_event
from engine.reasoning.models import ReasoningRequest
from engine.rules.loader import load_rules


class EventReasoningAgent:
    def __init__(self, rules_path: str, memory_path: str):
        self.rules = load_rules(rules_path)
        self.memory = load_memory(memory_path)

    def process_event(self, source: str, raw_event: dict, documentation_agent):
        event = normalize_event(source, raw_event)

        decision = build_decision(
            event.to_dict(),
            self.rules,
            self.memory,
        )

        if not decision.requires_llm:
            return {
                "type": "deterministic",
                "decision": decision,
            }

        # 🔥 aquí entra el otro agente
        context_request = ContextRequest(
            event_type=event.event_type,
            source=event.source,
            summary=event.summary,
            query=event.logs or event.message or event.reason or "",
        )

        context_response = documentation_agent.retrieve_context(context_request)

        enriched_context = f"""
Event context:
{context_request.query}

Documentation context:
{chr(10).join(context_response.snippets)}
""".strip()

        reasoning_request = ReasoningRequest(
            event_type=event.event_type,
            source=event.source,
            summary=event.summary,
            context=enriched_context,
            known_rule_matches=len(decision.rule_matches),
            known_memory_matches=len(decision.memory_matches),
        )

        reasoning_result = analyze_event(reasoning_request)

        return {
            "type": "ai_reasoning",
            "decision": decision,
            "context_sources": context_response.sources,
            "reasoning": reasoning_result,
        }