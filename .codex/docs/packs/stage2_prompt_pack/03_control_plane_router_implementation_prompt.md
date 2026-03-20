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

# Implement only: `src/gdc_adk/control_plane/router.py`

## Owning subsystem
- `control_plane`

## Responsibility
Construct the execution-path classification and ordered provider failover chain from policy and config outputs.

## Required public functions
- `classify_execution_path(task_type)`
- `select_provider(task_type)`
- `get_failover_chain(task_type)`

## Requirements
- valid path classes are deterministic, local_llm, cloud_fallback
- deterministic-capability tasks must not route to remote first
- local provider chain must be preferred before cloud
- chain order must come from policy/config, not provider preference
- local-only tasks must never produce cloud chain

## Must not contain
- provider transport
- prompt assembly
- cache execution
- workflow state mutation

## Definition of done
- path classification is explicit
- provider chain is local-first and policy-controlled
