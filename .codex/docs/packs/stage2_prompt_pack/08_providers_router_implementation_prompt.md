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

# Implement only: `src/gdc_adk/providers/router.py`

## Owning subsystem
- `providers`

## Responsibility
Execute provider invocation according to control-plane output and preserve structured failure chain.

## Required public functions
- `get_llm_client(provider)`
- `generate_with_failover(req, order)`
- `execute_task(task_type, req)`

## Requirements
- execute exactly in control-plane order
- preserve every provider failure in an ordered failure chain
- return normalized success response or full structured failure chain
- do not decide policy

## Must not contain
- policy decisioning
- workflow state mutation
- artifact creation

## Definition of done
- provider execution follows control-plane order and failover behavior is fully inspectable
