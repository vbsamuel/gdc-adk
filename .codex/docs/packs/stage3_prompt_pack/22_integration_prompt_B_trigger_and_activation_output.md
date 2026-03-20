# Integration Prompt B — trigger routing and activation output

Implement only the integration tests for:
- `information_plane/normalization/canonicalizer.py`
- `information_plane/activation/trigger_router.py`
- `information_plane/activation/workflow_activation.py`

## Required assertions
- fix-like normalized input produces fix-flow trigger metadata
- research/spec-like normalized input produces structured activation metadata
- activation output includes related artifact references
- activation output includes next-action types
- activation output remains structured and serializable
- no workflow execution occurs
