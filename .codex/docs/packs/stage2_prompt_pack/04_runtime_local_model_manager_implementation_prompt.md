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

# Implement only: `src/gdc_adk/runtime/local_model_manager.py`

## Owning subsystem
- `runtime`

## Responsibility
Provide the bounded Stage 2 runtime surface for active local model lifecycle.

## Required public functions
- `get_active_model()`
- `set_active_model(model_name)`
- `clear_active_model()`

## Requirements
- remain provider-agnostic
- support explicit active-model lifecycle
- do not overclaim queue, retry, watchdog, or isolation as implemented unless a bounded interface exists in this file

## Must not contain
- workflow semantics
- policy ownership
- config ownership
- validation policy

## Definition of done
- active-model lifecycle is explicit, resettable, and bounded honestly
