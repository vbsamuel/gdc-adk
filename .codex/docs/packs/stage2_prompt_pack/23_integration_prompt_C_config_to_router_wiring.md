# Integration Prompt C — config to router wiring

Implement only the integration tests for:
- `config/settings.py`
- `control_plane/policy.py`
- `control_plane/router.py`
- `providers/router.py`

## Required assertions
- failover order from config is used by control plane
- control-plane chain is passed unchanged into providers router
- unknown provider in config fails explicitly
- cloud is not reachable for local-only task even if configured globally
