from engine.events.examples import (
    ONBOARDING_BLOCKED_EVENT,
    PREFECT_FAILED_EVENT,
    RUNDECK_FAILED_EVENT,
)
from engine.events.normalizer import normalize_event


for source, raw_event in [
    ("prefect", PREFECT_FAILED_EVENT),
    ("rundeck", RUNDECK_FAILED_EVENT),
    ("onboarding", ONBOARDING_BLOCKED_EVENT),
]:
    event = normalize_event(source, raw_event)

    print("Source:", source)
    print(event.to_dict())
    print("---")