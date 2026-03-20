# Integration Prompt B — provider contract + local/cloud failover

Implement only the integration tests for:
- `providers/base.py`
- `providers/ollama_provider.py`
- `providers/google_provider.py`
- `providers/router.py`

## Required assertions
- local provider is attempted first
- local failure is preserved in failure chain
- cloud provider is attempted only when policy-approved chain includes it
- successful fallback returns normalized response with provider and model attribution
- all-provider failure returns ordered structured failure chain
