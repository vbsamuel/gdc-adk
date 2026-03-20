# Tests only: `src/gdc_adk/memory/cache.py`

## Required assertions
- result can be stored by stable key
- stored result can be retrieved by stable key
- missing key returns explicit miss behavior
- invalidation works explicitly
- exported cache bundle is serializable
- cache record includes required fields
- cache does not require opaque runtime-only pointers
- critical continuity is not represented only as cache state by design assertions
