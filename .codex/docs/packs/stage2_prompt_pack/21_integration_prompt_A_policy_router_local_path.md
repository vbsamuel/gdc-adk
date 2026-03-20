# Integration Prompt A — policy + router + local runtime path

Implement only the integration tests for:
- `config/settings.py`
- `control_plane/policy.py`
- `control_plane/router.py`
- `runtime/local_model_manager.py`

## Required assertions
- configured default provider is local
- deterministic task type classifies to deterministic path before provider path
- local reasoning task type classifies to local_llm path
- local-only task never produces cloud chain
- runtime active-model lifecycle can be used without violating provider boundary
