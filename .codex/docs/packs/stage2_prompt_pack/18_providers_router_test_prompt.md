# Tests only: `src/gdc_adk/providers/router.py`

## Required assertions
- `generate_with_failover` executes providers in supplied order only
- success on first provider returns normalized response and stops chain
- first-provider failure preserves failure record and falls through to next provider
- if all providers fail, structured ordered failure chain is returned
- intermediate failures are not dropped
- provider order is not mutated by router
- router does not decide policy
