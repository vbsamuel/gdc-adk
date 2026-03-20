# Stage 4 Scope

## Stage purpose
Implement Forge-X Stage 4 only: workflows, validation, and review spine.

## In-scope subsystems
- workflows
- validation

## In-scope files
- src/gdc_adk/workflows/engine.py
- src/gdc_adk/workflows/state_machine.py
- src/gdc_adk/workflows/fix_flow.py
- src/gdc_adk/workflows/iterative_flow.py
- src/gdc_adk/validation/validator.py
- src/gdc_adk/validation/drift_checker.py
- src/gdc_adk/validation/traceability_auditor.py
- src/gdc_adk/validation/grounding_checker.py

## Out-of-scope
- memory
- multi-agent

## Traceability rows
- Stage 4 rows from the active matrix and stage pack

## Acceptance scenarios
- Stage 4 scenarios from the active acceptance pack

## Required packs
- forge_x_global_engineering_standards_pack
- forge_x_repo_wide_test_and_quality_pack
- forge_x_repo_wide_final_gate_pack

## Rules
- Workflow state must be explicit
- Review findings are first-class objects
- Validation cannot collapse into prose-only review