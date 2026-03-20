# Integration Prompt C — review + validation

Implement only the integration tests for:
- `workflows/review_orchestrator.py`
- `validation/handoff_validator.py`
- `validation/agent_governance.py`

## Required assertions
- independent reviewer path is enforced for non-trivial outputs
- reviewable handoff cannot bypass finding/validation requirements
- review path can escalate to findings/issues
- invalid review handoff is blocked
