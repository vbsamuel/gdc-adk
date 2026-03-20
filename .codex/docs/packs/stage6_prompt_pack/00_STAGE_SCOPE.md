# Stage 6 Scope

## Stage purpose
Implement Forge-X Stage 6 only: multi-agent contracts, role-bounded handoffs, and anti-swarm governance.

## In-scope subsystems
- multi-agent related coordination surfaces approved by the repo constitution and stage pack
- bounded extensions to workflows, validation, core contracts, or coordination modules if explicitly required by the stage pack

## In-scope files
- Only files explicitly approved by the Stage 6 bounded brief and stage pack

## Out-of-scope
- redesign of earlier stages

## Traceability rows
- Stage 6 rows from the active matrix and stage pack

## Acceptance scenarios
- Stage 6 scenarios from the active acceptance pack

## Required packs
- forge_x_global_engineering_standards_pack
- forge_x_repo_wide_test_and_quality_pack
- forge_x_repo_wide_final_gate_pack
- forge_x_full_system_integration_pack

## Rules
- No free-form swarm behavior
- No hidden agent-to-agent state
- All handoffs must be typed and traceable
- Multi-agent flows cannot bypass review, validation, or governance