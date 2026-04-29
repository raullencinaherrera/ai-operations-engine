from typing import Any, Dict

from engine.events.models import OperationalEvent


def normalize_prefect_event(raw_event: Dict[str, Any]) -> OperationalEvent:
    flow_name = raw_event.get("flow_name", "unknown_flow")
    state = str(raw_event.get("state", "")).lower()
    logs = raw_event.get("logs", "")
    error = raw_event.get("error")

    if state == "failed":
        event_type = "flow.failed"
        summary = f"Prefect flow '{flow_name}' failed"
        tags = ["prefect", "automation", "failure"]
    else:
        event_type = "flow.event"
        summary = f"Prefect flow '{flow_name}' reported state '{state}'"
        tags = ["prefect", "automation"]

    return OperationalEvent(
        event_type=event_type,
        source="prefect",
        summary=summary,
        logs=logs,
        error=error,
        tags=tags,
        raw_event=raw_event,
    )


def normalize_rundeck_event(raw_event: Dict[str, Any]) -> OperationalEvent:
    job_name = raw_event.get("job_name", "unknown_job")
    status = str(raw_event.get("status", "")).lower()
    logs = raw_event.get("logs", "")
    error = raw_event.get("error")

    if status in ["failed", "failure"]:
        event_type = "job.failed"
        summary = f"Rundeck job '{job_name}' failed"
        tags = ["rundeck", "automation", "failure"]
    else:
        event_type = "job.event"
        summary = f"Rundeck job '{job_name}' reported status '{status}'"
        tags = ["rundeck", "automation"]

    return OperationalEvent(
        event_type=event_type,
        source="rundeck",
        summary=summary,
        logs=logs,
        error=error,
        tags=tags,
        raw_event=raw_event,
    )


def normalize_onboarding_event(raw_event: Dict[str, Any]) -> OperationalEvent:
    task_name = raw_event.get("task_name", "unknown_task")
    status = str(raw_event.get("status", "")).lower()
    reason = raw_event.get("reason", "")

    if status == "blocked":
        event_type = "onboarding.task.blocked"
        summary = f"Onboarding task '{task_name}' is blocked"
        tags = ["onboarding", "workflow", "blocked"]
    else:
        event_type = "onboarding.task.event"
        summary = f"Onboarding task '{task_name}' reported status '{status}'"
        tags = ["onboarding", "workflow"]

    return OperationalEvent(
        event_type=event_type,
        source="onboarding-engine",
        summary=summary,
        reason=reason,
        tags=tags,
        raw_event=raw_event,
    )


def normalize_event(source: str, raw_event: Dict[str, Any]) -> OperationalEvent:
    normalized_source = source.lower()

    if normalized_source == "prefect":
        return normalize_prefect_event(raw_event)

    if normalized_source == "rundeck":
        return normalize_rundeck_event(raw_event)

    if normalized_source == "onboarding":
        return normalize_onboarding_event(raw_event)

    return OperationalEvent(
        event_type="unknown.event",
        source=normalized_source,
        summary="Unknown event source",
        message=str(raw_event),
        tags=["unknown"],
        raw_event=raw_event,
    )