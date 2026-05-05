from engine.analytics.dashboard import save_dashboard
from engine.analytics.event_log import load_trace_events
from engine.analytics.metrics import calculate_metrics


ANALYTICS_PATH = "engine/analytics/analytics_store.jsonl"
DASHBOARD_PATH = "engine/analytics/dashboard.html"


events = load_trace_events(ANALYTICS_PATH)
metrics = calculate_metrics(events)

save_dashboard(metrics, DASHBOARD_PATH)

print("Dashboard generated:")
print(DASHBOARD_PATH)