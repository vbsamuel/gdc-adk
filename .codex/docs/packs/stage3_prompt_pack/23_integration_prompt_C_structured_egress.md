# Integration Prompt C — structured egress

Implement only the integration tests for:
- `information_plane/activation/workflow_activation.py`
- `information_plane/egress/artifact_emitter.py`

## Required assertions
- activation output can feed a direct-answer emission
- activation output can feed a generated-artifact emission
- emission preserves artifact references
- emission preserves provenance notes
- emission preserves workflow linkage when applicable
- emission is not plain chat text only
