# Tests only: `src/gdc_adk/control_plane/router.py`

## Required assertions
- deterministic task type classifies to deterministic path
- local reasoning task type classifies to local_llm path
- cloud-fallback eligible task type can produce cloud_fallback path only when policy allows
- local provider chain is ordered before cloud
- local-only task does not produce cloud chain
- invalid failover order rejects explicitly
- empty provider chain for eligible provider path rejects explicitly
