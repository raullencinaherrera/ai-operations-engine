# AI Operations Engine Control Report

## Summary

- Total events processed: 3
- Rule match rate: 0.67
- Memory match rate: 1.0
- Documentation found rate: 0.67
- LLM usage rate: 0.33
- Promotion rate: 0.33
- Unresolved rate: 0.33
- Execution success rate: 0.67

## Top Event Types

- flow.failed: 2
- onboarding.task.blocked: 1

## Top Rules

- prefect_failed_authentication: 1
- onboarding_missing_required_parameters: 1

## Top Memories

- mem_001: 1
- mem_002: 1
- mem_003: 1

## Documentation Gaps

- flow.failed: 1

## Interpretation

- High rule match rate means the deterministic reflex layer is effective.
- High LLM usage may indicate missing rules, weak memory, or documentation gaps.
- Documentation gaps identify areas where operational knowledge should be improved.
- Promotion rate shows how often repeated successful solutions become rule candidates.