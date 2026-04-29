from typing import Any, Dict, List

from engine.memory.models import MemoryMatch, MemoryRecord
from engine.memory.search import search_memory
from engine.orchestrator.models import OperationalDecision
from engine.rules.evaluator import evaluate_rules
from engine.rules.models import Rule, RuleMatch


def choose_best_rule(rule_matches: List[RuleMatch]) -> RuleMatch | None:
    if not rule_matches:
        return None

    return sorted(rule_matches, key=lambda match: match.priority, reverse=True)[0]


def choose_best_memory(memory_matches: List[MemoryMatch]) -> MemoryMatch | None:
    if not memory_matches:
        return None

    return sorted(memory_matches, key=lambda match: match.score, reverse=True)[0]


def build_decision(
    event: Dict[str, Any],
    rules: List[Rule],
    memory_records: List[MemoryRecord],
) -> OperationalDecision:
    rule_matches = evaluate_rules(rules, event)
    memory_matches = search_memory(memory_records, event)

    best_rule = choose_best_rule(rule_matches)
    best_memory = choose_best_memory(memory_matches)

    if best_rule and best_rule.confidence == "high":
        return OperationalDecision(
            decision="deterministic_rule_matched",
            recommended_action=best_rule.message,
            confidence=best_rule.confidence,
            requires_llm=False,
            rule_matches=rule_matches,
            memory_matches=memory_matches,
            reason=f"High-confidence deterministic rule matched: {best_rule.rule_id}",
        )

    if best_memory and best_memory.score >= 80:
        return OperationalDecision(
            decision="known_issue_detected",
            recommended_action=best_memory.record.resolution,
            confidence=best_memory.record.confidence,
            requires_llm=False,
            rule_matches=rule_matches,
            memory_matches=memory_matches,
            reason=f"Similar past case found in operational memory: {best_memory.record.id}",
        )

    if best_rule:
        return OperationalDecision(
            decision="rule_matched_low_or_medium_confidence",
            recommended_action=best_rule.message,
            confidence=best_rule.confidence,
            requires_llm=True,
            rule_matches=rule_matches,
            memory_matches=memory_matches,
            reason=f"Rule matched but additional reasoning is recommended: {best_rule.rule_id}",
        )

    if best_memory:
        return OperationalDecision(
            decision="possible_known_issue",
            recommended_action=best_memory.record.resolution,
            confidence=best_memory.record.confidence,
            requires_llm=True,
            rule_matches=rule_matches,
            memory_matches=memory_matches,
            reason=f"Possible similar memory found, but score is not high enough: {best_memory.record.id}",
        )

    return OperationalDecision(
        decision="unknown_issue",
        recommended_action="No deterministic rule or reliable memory found. Send event to reasoning engine.",
        confidence="low",
        requires_llm=True,
        rule_matches=[],
        memory_matches=[],
        reason="No matching rule or operational memory was found.",
    )