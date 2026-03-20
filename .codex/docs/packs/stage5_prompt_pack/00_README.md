# Forge-X Stage 5 Memory-Only Prompt Pack

This package is the corrected Stage 5 prompt pack for Forge-X.

It is strictly **memory-only** and contains no Stage 3 information-plane prompts.

## Included Stage 5 files only
- `src/gdc_adk/memory/contracts.py`
- `src/gdc_adk/memory/cache.py`
- `src/gdc_adk/memory/context_store.py`
- `src/gdc_adk/memory/continuity.py`
- `src/gdc_adk/memory/replay.py`

## Included prompt types
- 5 implementation prompts
- 5 matching file test prompts
- 4 Stage 5 integration prompts
- 1 Stage 5 acceptance review
- 1 Stage 5 traceability update prompt
- 1 operator runbook

## Explicitly excluded
- `document_ingestor`
- `canonicalizer`
- `artifact_index`
- `trigger_router`
- `workflow_activation`
- `artifact_emitter`
- all Stage 3 integration prompts
- `24_STAGE3_acceptance_review.md`
