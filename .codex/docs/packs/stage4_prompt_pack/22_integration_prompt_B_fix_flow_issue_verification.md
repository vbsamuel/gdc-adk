# Integration Prompt B — fix flow + issue linkage + verification

Implement only the integration tests for:
- `workflows/engine.py`
- `workflows/fix_flow.py`
- `validation/validator.py`

## Required assertions
- fix-flow binds to issue ID in workflow run
- remediation evidence artifact IDs are preserved
- verification result is structured
- closure without evidence rejects
- closure without verification rejects
- failed verification can lead to reopen
- validation gate can influence closure readiness for non-trivial outputs
