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

# Implement only: `src/gdc_adk/control_plane/policy.py`

## Owning subsystem
- `control_plane`

## Responsibility
Policy-only decisions about what execution paths are allowed.

## Required public functions
- `is_deterministic_candidate(task_type)`
- `should_use_local(task_type)`
- `allow_cloud(task_type)`
- `is_local_only_task(task_type)`

## Requirements
- deterministic-before-LLM decisioning must be explicit
- local-first behavior must be explicit
- cloud may be used only if policy allows it
- time, weather, and retrieval-like tasks must be expressible as deterministic or local-only
- this file answers what is allowed, not how it is executed

## Must not contain
- provider transport
- cache storage
- artifact storage
- provider self-selection
- workflow sequencing

## Definition of done
- deterministic, local, and cloud decisions are explicit and testable
