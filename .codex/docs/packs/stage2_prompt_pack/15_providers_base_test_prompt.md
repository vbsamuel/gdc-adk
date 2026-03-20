# Tests only: `src/gdc_adk/providers/base.py`

## Required assertions
- `LLMRequest` can be instantiated with valid normalized fields
- `LLMResponse` can be instantiated with normalized provider and model attribution
- provider interface contract can be implemented by adapters
- missing provider attribution rejects or fails contract validation
- missing model attribution rejects or fails contract validation
- non-normalized response shape is not accepted
