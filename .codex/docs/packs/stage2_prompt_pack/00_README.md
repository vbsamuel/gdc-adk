# Forge-X Stage 2 Operator Run Folder

This pack is the Stage 2 operator-run execution folder.

It is bounded to the eight-file Stage 2 execution slice below and their matching test slices. The slice preserves the Stage 2 control-plane/provider boundary and the Stage 2 control gate without pulling in later-stage responsibilities.

## Bounded eight-file Stage 2 slice
1. `src/gdc_adk/config/settings.py`
2. `src/gdc_adk/control_plane/policy.py`
3. `src/gdc_adk/control_plane/router.py`
4. `src/gdc_adk/runtime/local_model_manager.py`
5. `src/gdc_adk/providers/base.py`
6. `src/gdc_adk/providers/ollama_provider.py`
7. `src/gdc_adk/providers/google_provider.py`
8. `src/gdc_adk/providers/router.py`

## Why this is the operator slice
This slice covers the minimum Stage 2 execution path required to prove:
- repo-root config resolution
- deterministic-before-LLM decisioning at policy/router level
- local-first provider routing
- provider abstraction and normalized request/response
- local runtime lifecycle surface
- provider failover under policy

## Explicit exclusions
This operator slice does not implement:
- Stage 3 ingestion, normalization, indexing, activation, or egress
- Stage 4 workflow engine or review spine behavior
- Stage 5 cache execution, context store, continuity, or replay backend behavior
- Stage 6 multi-agent behavior
- capability implementation files for geo/time/weather inside this pack

Geo/time/weather deterministic acceptance is still referenced in the acceptance prompts as a Stage 2 policy and routing obligation, but the operator slice here is the eight-file control-plane/provider execution core.

## Included files
- 8 implementation prompts
- 8 matching test prompts
- 3 integration prompts
- 1 G3 acceptance review prompt
- 1 traceability update prompt
- 1 operator runbook


Stage 2 = Control Plane + Deterministic Capability Routing (pre-LLM).

Includes:
- control_plane prompts
- providers/weather prompts
- capabilities prompts
- file-level tests
- integration prompt (deterministic-before-LLM routing)

No memory (Stage 5) or multi-agent (Stage 6) logic allowed.