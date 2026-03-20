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

# Implement only: `src/gdc_adk/workflows/handoff_manager.py`

## Owning subsystem
- `workflows`

## Responsibility
Execute agent handoffs using typed handoff artifacts, preserve lineage, and integrate with workflow state/history without inventing new workflow states casually.

## Required public functions
- `initiate_handoff(handoff_artifact, workflow_run) -> dict`
- `complete_handoff(handoff_id, workflow_run) -> dict`
- `reject_handoff(handoff_id, workflow_run, reason) -> dict`

## Workflow-state integration rules
- handoff completion may update `owner_role` and `pending_actions` without necessarily changing `current_state`
- any change must still create a structured state-history entry or agent trace record
- review-triggered or validation-triggered handoffs may reopen or block only through legal existing workflow transitions
- this file must not invent new workflow states casually

## Requirements
- every handoff must be validated before completion
- every handoff must create traceable records
- workflow linkage, issue linkage, finding linkage, and artifact linkage must survive handoff
- rejection reasons must be explicit and durable

## Must not contain
- role creation
- workflow planning authority
- direct artifact mutation
- provider execution
- free-form handoff shortcuts

## Definition of done
- handoffs can initiate/complete/reject only through typed contracts
- ownership and pending actions remain traceable
- no hidden handoff state exists
