# Global Control Header

Paste this header before each file-specific prompt:

```text
We are implementing Forge-X Stage 2 only.

Treat the uploaded markdown grounding files as binding system definition, repo constitution, execution law, and acceptance criteria.

This prompt is for one file only.

Before producing code:
1. identify the owning subsystem
2. identify the relevant contracts and interfaces required for this file
3. identify workflow modes affected
4. identify Stage 2 traceability rows advanced
5. identify acceptance assertions that must pass

Constraints:
- Do not introduce new architecture
- Do not expand scope beyond Stage 2
- Do not pull Stage 3, Stage 4, Stage 5, or Stage 6 responsibilities into this file
- Do not generate placeholder logic
- Do not merge responsibilities across subsystems
- Do not hide policy in providers
- Do not hide routing or business logic in adapters or labs
- Do not modify unrelated files

Output implementation-grade Python code only for the requested file.
Respect repo constitution, control-plane/provider boundaries, local-first behavior, deterministic-before-LLM policy, failover controls, normalized contracts, and file-level Definition of Done.
```

# Implement only: `src/gdc_adk/config/settings.py`

## Owning subsystem
- `config`

## Responsibility
Single source of truth for repo-root config loading and environment accessors.

## Required public functions
- `load_yaml_config()`
- `require_env(name)`
- `get_provider_config(provider_name)`
- `get_default_provider()`
- `get_failover_order()`
- `get_weather_provider_name()`
- `get_weather_provider_base_url(provider_name)`

## Requirements
- resolve the same repo-root `config.yaml` from repo root and `labs/adk`
- fail explicitly on missing config
- fail explicitly on malformed yaml
- fail explicitly on missing required secret
- do not require lab-local config
- do not add hidden defaults that override declared config

## Must not contain
- provider execution
- workflow selection
- artifact or issue creation
- routing policy

## Definition of done
- config resolution is stable and explicit
- provider and routing config accessors are reliable
- weather provider config access is reliable
