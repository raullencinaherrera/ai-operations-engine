from pathlib import Path

from engine.analytics.event_log import append_trace_event, load_trace_events
from engine.analytics.metrics import calculate_metrics
from engine.analytics.models import EngineTraceEvent
from engine.analytics.reports import build_markdown_report


ANALYTICS_PATH = "engine/analytics/analytics_store.jsonl"
REPORT_PATH = "engine/analytics/control_report.md"


sample_events = [
    EngineTraceEvent(
        event_id="evt_001",
        event_type="flow.failed",
        source="prefect",
        decision="deterministic_rule_matched",
        rule_matched=True,
        rule_ids=["prefect_failed_authentication"],
        memory_matched=True,
        memory_ids=["mem_001"],
        documentation_found=False,
        llm_used=False,
        execution_status="success",
        promoted_to_rule=False,
    ),
    EngineTraceEvent(
        event_id="evt_002",
        event_type="flow.failed",
        source="prefect",
        decision="ai_reasoning",
        rule_matched=False,
        memory_matched=True,
        memory_ids=["mem_002"],
        documentation_found=True,
        documentation_sources=["Permission Issues"],
        llm_used=True,
        execution_status="failed",
        unresolved=True,
    ),
    EngineTraceEvent(
        event_id="evt_003",
        event_type="onboarding.task.blocked",
        source="onboarding-engine",
        decision="deterministic_rule_matched",
        rule_matched=True,
        rule_ids=["onboarding_missing_required_parameters"],
        memory_matched=True,
        memory_ids=["mem_003"],
        documentation_found=True,
        documentation_sources=["Onboarding Workflow Blockers"],
        llm_used=False,
        execution_status="success",
        promoted_to_rule=True,
    ),
]

for event in sample_events:
    append_trace_event(ANALYTICS_PATH, event)

events = load_trace_events(ANALYTICS_PATH)
metrics = calculate_metrics(events)
report = build_markdown_report(metrics)

Path(REPORT_PATH).write_text(report, encoding="utf-8")

print("Analytics report generated:")
print(REPORT_PATH)
print("---")
print(report)