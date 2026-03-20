# Tests only: `src/gdc_adk/validation/handoff_validator.py`

## Required assertions
- valid handoff artifact references can validate
- missing artifact reference rejects explicitly
- missing workflow linkage rejects explicitly
- issue and finding references validate when present
- unresolved continuity reference rejects or declares gap explicitly
- review requirements are enforced for reviewable artifacts
- validation output is structured and serializable
