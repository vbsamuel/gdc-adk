# Tests only: `src/gdc_adk/providers/ollama_provider.py`

## Required assertions
- availability check succeeds on valid mocked local endpoint
- availability check fails explicitly on unavailable endpoint
- generate returns normalized `LLMResponse`
- bad base URL fails explicitly
- missing model fails explicitly
- non-200 response fails explicitly
- provider does not choose itself or bypass control plane
