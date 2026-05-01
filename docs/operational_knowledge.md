# Operational Knowledge Base

## Prefect Authentication Troubleshooting

If a Prefect flow fails with `401 Unauthorized`, `invalid token`, or `authentication error`, the most likely cause is an expired or misconfigured API token.

Recommended actions:

- Check the secret used by the flow.
- Validate that the API token has not expired.
- Confirm that the token is available in the runtime environment.
- Retry the flow after refreshing the credentials.

---

## Permission Issues

If an automation fails with `403 Forbidden`, `permission denied`, or `access denied`, the service account may not have enough permissions.

Recommended actions:

- Review the service account permissions.
- Validate access to the target API or system.
- Confirm that the role assigned to the automation is correct.
- Escalate to the platform owner if access changes are required.

---

## Rundeck Missing Parameters

If a Rundeck job fails because a required parameter was not provided, the workflow should not continue.

Recommended actions:

- Identify the missing parameter.
- Request the required input from the owner.
- Keep dependent tasks blocked until all required values are available.
- Avoid retrying the job without correcting the input data.

---

## Onboarding Workflow Blockers

Onboarding tasks should remain blocked when mandatory data is missing.

Typical blockers:

- missing customer identifier
- missing environment
- missing credentials
- missing target platform
- missing approval

Recommended actions:

- Keep the task blocked.
- Request the missing information.
- Validate the data before unlocking dependent tasks.