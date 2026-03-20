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

# Implement only: `src/gdc_adk/validation/agent_governance.py`

## Owning subsystem
- `validation`

## Responsibility
Enforce anti-swarm governance, detect bounded-authority violations, and surface governance failures as structured results/findings.

## Required public functions
- `validate_agent_sequence(workflow_run_id, agent_trace) -> dict`
- `detect_swarm_violation(workflow_run, agent_trace) -> list[dict]`
- `check_stop_conditions(workflow_run, agent_trace) -> dict`

## Required governance checks
- no free-form unbounded loops
- no reviewer-author identity equality for non-trivial reviewable outputs
- no hidden coordination carriers outside approved durable objects
- no delegation beyond configured bounds
- no reopen or review bypass without typed issue/finding/verification trigger

## Requirements
- governance violations must become structured results or findings
- stop conditions must be explicit and enforceable
- governance logic must be bounded and deterministic for obvious violations

## Must not contain
- workflow authoring
- provider routing
- plain warning comments instead of structured outputs

## Definition of done
- anti-swarm bounds and stop conditions are enforced
- governance violations become structured outputs/findings
