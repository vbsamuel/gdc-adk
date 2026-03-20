# Stage 1 Scope

## Stage purpose
Implement Forge-X Stage 1 only: core contracts and substrate.

## In-scope subsystems
- core
- substrate

## In-scope files
- src/gdc_adk/core/contracts.py
- src/gdc_adk/core/state.py
- src/gdc_adk/substrate/event_spine.py
- src/gdc_adk/substrate/artifact_store.py
- src/gdc_adk/substrate/issue_tracker.py
- src/gdc_adk/substrate/dispatch_system.py
- src/gdc_adk/substrate/provenance.py
- src/gdc_adk/substrate/versioning.py

## Out-of-scope
- control plane
- runtime
- providers
- information plane
- workflows
- validation
- memory
- multi-agent

## Traceability rows
- FX-R007
- FX-R008
- FX-R009

## Acceptance scenarios
- Scenario A
- Scenario C
- Scenario D

## Required packs
- forge_x_global_engineering_standards_pack
- forge_x_repo_wide_test_and_quality_pack
- forge_x_repo_wide_final_gate_pack

## Rules
- No new architecture
- No placeholder logic
- No hidden state
- Do not edit files outside the in-scope list