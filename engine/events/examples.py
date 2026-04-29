PREFECT_FAILED_EVENT = {
    "flow_name": "sync_inventory",
    "state": "FAILED",
    "logs": "Request failed with 401 Unauthorized: invalid token",
}

RUNDECK_FAILED_EVENT = {
    "job_name": "create_customer_onboarding_tasks",
    "status": "failed",
    "logs": "Execution failed because required parameter customer_id was not provided",
}

ONBOARDING_BLOCKED_EVENT = {
    "task_name": "Create Mission Control subscription",
    "status": "blocked",
    "reason": "missing parameter: customer_id",
}