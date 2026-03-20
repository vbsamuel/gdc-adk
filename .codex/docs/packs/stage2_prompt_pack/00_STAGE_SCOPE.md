# Stage 2 Scope

## Stage purpose
Implement Forge-X Stage 2 only: control plane, runtime, providers, and deterministic capabilities.

## In-scope subsystems
- config
- control_plane
- runtime
- providers
- capabilities

## In-scope files
- src/gdc_adk/config/settings.py
- src/gdc_adk/control_plane/policy.py
- src/gdc_adk/control_plane/router.py
- src/gdc_adk/control_plane/optimizer.py
- src/gdc_adk/control_plane/model_registry.py
- src/gdc_adk/control_plane/context_assembler.py
- src/gdc_adk/control_plane/gate_evaluator.py
- src/gdc_adk/runtime/local_model_manager.py
- src/gdc_adk/providers/base.py
- src/gdc_adk/providers/ollama_provider.py
- src/gdc_adk/providers/google_provider.py
- src/gdc_adk/providers/router.py
- src/gdc_adk/providers/weather/base.py
- src/gdc_adk/providers/weather/open_meteo.py
- src/gdc_adk/providers/weather/router.py
- src/gdc_adk/capabilities/geo.py
- src/gdc_adk/capabilities/time.py
- src/gdc_adk/capabilities/weather.py

## Out-of-scope
- information plane
- workflows
- validation
- memory
- multi-agent

## Traceability rows
- Stage 2 rows from the active matrix and stage pack

## Acceptance scenarios
- Stage 2 scenarios from the active acceptance pack, especially deterministic routing and provider fallback

## Required packs
- forge_x_global_engineering_standards_pack
- forge_x_repo_wide_test_and_quality_pack
- forge_x_repo_wide_final_gate_pack

## Rules
- Control plane owns routing and policy
- Providers do transport/translation only
- Deterministic-before-LLM is mandatory
- No hidden routing in adapters or labs