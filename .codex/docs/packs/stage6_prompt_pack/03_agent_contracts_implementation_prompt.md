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

# Implement only: `src/gdc_adk/workflows/agent_contracts.py`

## Owning subsystem
- `workflows`

## Responsibility
Define the durable typed handoff artifact contract used for all Stage 6 inter-agent coordination.

## Required public functions
- `create_handoff_artifact(...) -> dict`
- `validate_handoff_contract(handoff_artifact) -> None`
- `serialize_handoff_artifact(handoff_artifact) -> dict`

## Required handoff-artifact fields
- `handoff_id`
- `workflow_run_id`
- `from_role`
- `to_role`
- `artifact_ids`
- `issue_ids`
- `finding_ids`
- `context_block_ids`
- `continuity_snapshot_id` or `continuity_ref`
- `created_at`
- `handoff_reason`
- `status`

## Allowed coordination carriers rule
The only permitted coordination carriers are:
- durable artifacts
- issues
- review findings
- explicit workflow state and state history
- approved continuity structures such as continuity snapshots and context blocks

This file must encode a contract compatible with that rule and forbid free-form hidden state transfer.

## Requirements
- handoff must be durable and serializable
- handoff must be traceable to workflow and artifact lineage
- handoff may not rely on raw prompt text as the only carrier
- handoff contract must be validatable independently of execution

## Must not contain
- memory storage implementation
- workflow state mutation
- provider execution
- implicit chat-state transfer

## Definition of done
- typed durable handoff artifact exists
- handoff artifact enforces lineage-friendly, serializable coordination
