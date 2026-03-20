# Integration Prompt D — cache bounds and replayability

Implement only the integration tests for:
- `memory/cache.py`
- `memory/replay.py`

## Required assertions
- cache records can be exported into replay-friendly form
- cache invalidation remains explicit
- cache-only state is not treated as the sole continuity authority
- replay package can include cache-related structures without opaque pointers
