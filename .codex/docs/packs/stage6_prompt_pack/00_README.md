# Forge-X Stage 6 Prompt Pack

This pack contains the corrected, fully bounded Stage 6 implementation prompts and matching test prompts for every file in the Stage 6 multi-agent scope.

## Stage 6 bounded scope
- `src/gdc_adk/workflows/agent_roles.py`
- `src/gdc_adk/workflows/agent_contracts.py`
- `src/gdc_adk/workflows/handoff_manager.py`
- `src/gdc_adk/workflows/delegation_engine.py`
- `src/gdc_adk/workflows/review_orchestrator.py`
- `src/gdc_adk/validation/agent_governance.py`
- `src/gdc_adk/validation/handoff_validator.py`
- `src/gdc_adk/substrate/agent_trace.py`

## What this pack fixes explicitly
- removes invented canonical traceability IDs
- grounds Stage 6 to Gate G7 and Scenario J first
- formalizes durable typed handoff artifacts
- formalizes finite roles and bounded authority
- enumerates the only allowed coordination carriers
- strengthens anti-swarm stop conditions and bounded delegation rules
- tightens workflow-state integration so Stage 6 does not corrupt Stage 4 state semantics
- strengthens validation/review integration so multi-agent flow cannot bypass findings, issues, or governance
- sharpens file-level and stage-level Definition of Done

## Included
- 8 implementation prompts
- 8 matching file test prompts
- 4 integration prompts
- 1 Stage 6 acceptance review prompt
- 1 Stage 6 traceability-update prompt
- 1 operator runbook
