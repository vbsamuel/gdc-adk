# Integration Prompt D — validation spine

Implement only the integration tests for:
- `validation/validator.py`
- `validation/drift_checker.py`
- `validation/traceability_auditor.py`
- `validation/grounding_checker.py`

## Required assertions
- validation outputs become structured findings
- drift failures become structured findings
- traceability gaps become structured findings
- grounding failures become structured findings
- finding lifecycle transitions are explicit
- outputs are independent from authored artifact generation path
