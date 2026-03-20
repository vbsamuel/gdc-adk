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

# Implement only: `src/gdc_adk/substrate/agent_trace.py`

## Owning subsystem
- `substrate`

## Responsibility
Record the durable agent action chain for a workflow so the planner/executor/reviewer/fixer/validator sequence can be reconstructed without hidden state.

## Required public functions
- `record_agent_action(workflow_run_id, role, action_type, artifact_ids, issue_ids=None, finding_ids=None, context_block_ids=None) -> dict`
- `get_agent_trace(workflow_run_id) -> list[dict]`

## Required trace fields
- `agent_action_id`
- `workflow_run_id`
- `role`
- `action_type`
- `artifact_ids`
- optional `issue_ids`
- optional `finding_ids`
- optional `context_block_ids`
- `timestamp`

## Requirements
- every non-trivial agent action must be traceable
- trace must reconstruct the full role/action chain
- trace entries must be serializable and durable
- trace must not rely on implicit prompt history

## Must not contain
- workflow policy mutation
- provider execution
- hidden runtime-only trace buffers as the sole source of truth

## Definition of done
- full role/action chain can be reconstructed for a workflow run
- trace is durable, serializable, and lineage-friendly
