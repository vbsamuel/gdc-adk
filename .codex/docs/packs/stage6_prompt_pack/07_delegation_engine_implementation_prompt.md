# Global Control Header

Paste this header before each file-specific prompt:

```text
We are implementing Forge-X Stage 6 only.

Treat the uploaded markdown grounding files as binding system definition, repo constitution, execution law, and acceptance criteria.

This prompt is for one file only.

Before producing code:
1. identify the owning subsystem
2. identify the relevant contracts and interfaces required for this file
3. identify workflow modes affected
4. identify Stage 6 acceptance and traceability evidence advanced
5. identify acceptance assertions that must pass

Constraints:
- Do not introduce new architecture
- Do not expand scope beyond Stage 6
- Do not redesign earlier stages unless an interface dependency must be explicitly referenced
- Do not generate placeholder logic
- Do not merge responsibilities across subsystems
- Do not allow free-form swarm behavior
- Do not allow hidden agent-to-agent state outside durable artifacts, findings, issues, workflow state, or approved continuity structures
- Do not allow agent handoffs without typed contracts and traceable lineage
- Do not allow multi-agent flows to bypass review, validation, or governance controls
- Do not invent canonical traceability IDs that are not yet in the approved matrix
- Do not modify unrelated files
- Do not hide logic in adapters or labs

Output implementation-grade Python code only for the requested file.
Respect repo constitution, workflow/validation/substrate boundaries, typed handoff artifacts, bounded roles, durable state, explicit lineage, governance limits, review independence, and Gate G7.
```

# Implement only: `src/gdc_adk/workflows/delegation_engine.py`

## Owning subsystem
- `workflows`

## Responsibility
Enforce bounded delegation using explicit role rules, stop conditions, and typed artifacts only.

## Required public functions
- `delegate_task(from_role, to_role, handoff_artifact, workflow_run) -> dict`
- `validate_delegation(from_role, to_role, workflow_run) -> None`
- `check_delegation_limits(workflow_run, agent_trace) -> dict`

## Required governance limits
You must enforce at minimum:
- maximum delegation depth
- maximum same-role repetition count
- maximum unresolved handoff count per workflow run
- prohibition on self-escalation
- prohibition on recursive free-form delegation loops

## Requirements
- delegation must stay within the same workflow_run_id
- delegation must be explicitly recorded
- delegation must not bypass review or validation gates
- delegation must use typed handoff artifacts only
- stop conditions must be explicit and enforceable

## Must not contain
- recursive unbounded loops
- role self-escalation
- provider execution
- hidden side-channel coordination

## Definition of done
- bounded delegation works only through explicit rules
- governance stop conditions are enforced
- delegation remains traceable and durable
