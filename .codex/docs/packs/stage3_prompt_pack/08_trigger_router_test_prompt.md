# Tests only: `src/gdc_adk/information_plane/activation/trigger_router.py`

## Required assertions
- obvious fix-like signal classifies to `fix_flow`
- obvious single-request signal classifies to `single_run`
- iterative refinement-like signal can classify to `iterative`
- ambiguous signal can still produce structured activation category output
- issue-trigger detection is explicit for fix-like input
- activation reason is structured rather than plain prose only
- invalid normalized-signal shape rejects explicitly
- this file does not execute workflows
