# Tests only: `src/gdc_adk/validation/validator.py`

## Required assertions
- validation can create a structured ReviewFinding
- ReviewFinding includes finding type, severity, description, related artifact IDs, evidence, and status
- finding lifecycle supports open -> resolved
- finding lifecycle supports open -> rejected
- finding lifecycle supports resolved -> reopened
- reopening preserves history
- finding-to-issue escalation can be represented
- validation result is separate from authored artifact content
- review is not plain comments only
