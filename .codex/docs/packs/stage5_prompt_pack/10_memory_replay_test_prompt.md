# Tests only: `src/gdc_adk/memory/replay.py`

## Required assertions
- replay package can be built with required fields
- replay package includes schema/version metadata
- replay package export is serializable
- replay package validation detects missing required sections
- successful rehydration reconstructs stable serializable structures
- partial rehydration declares missing references explicitly
- invalid replay package fails explicitly
- replay package does not rely on opaque runtime-only object references
