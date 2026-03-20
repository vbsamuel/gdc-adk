# Forge-X Stage 4 Prompt Pack

This pack contains the corrected, upleveled Stage 4 implementation prompts and matching test prompts for every file in the Stage 4 bounded scope.

## Stage 4 bounded scope
- `src/gdc_adk/workflows/engine.py`
- `src/gdc_adk/workflows/state_machine.py`
- `src/gdc_adk/workflows/fix_flow.py`
- `src/gdc_adk/workflows/iterative_flow.py`
- `src/gdc_adk/validation/validator.py`
- `src/gdc_adk/validation/drift_checker.py`
- `src/gdc_adk/validation/traceability_auditor.py`
- `src/gdc_adk/validation/grounding_checker.py`

## What this pack fixes explicitly
- sharp Stage 4 boundary from Stage 5 continuity implementation
- explicit allowed-transition requirements per workflow mode
- stronger fix-flow issue/workflow/evidence linkage
- explicit iterative revision-delta requirements
- formal ReviewFinding lifecycle requirements
- operationalized validation-independence requirements
- explicit verification and reopen result structure
- stronger scenario-to-file acceptance mapping
- expanded traceability mapping to FX-R008, FX-R009, FX-R011, FX-R012, and partial FX-R015
- stronger file-level and stage-level Definitions of Done

## Included
- 8 implementation prompts
- 8 matching file test prompts
- 4 integration prompts
- 1 Stage 4 acceptance review prompt
- 1 Stage 4 traceability update prompt
- 1 operator runbook
