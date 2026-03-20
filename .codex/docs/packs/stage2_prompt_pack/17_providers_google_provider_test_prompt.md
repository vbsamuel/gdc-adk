# Tests only: `src/gdc_adk/providers/google_provider.py`

## Required assertions
- valid secret-backed invocation returns normalized `LLMResponse`
- missing secret fails explicitly
- invalid configured model fails explicitly
- provider failure surfaces explicitly
- provider does not implement local-first override logic
