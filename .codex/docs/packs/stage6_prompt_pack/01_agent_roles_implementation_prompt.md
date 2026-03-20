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

# Implement only: `src/gdc_adk/workflows/agent_roles.py`

## Owning subsystem
- `workflows`

## Responsibility
Define the finite Stage 6 role catalog, bounded authority matrix, and allowed delegation/review relationships.

## Required public functions
- `list_allowed_roles() -> list[str]`
- `get_role_definition(role_name) -> dict`
- `get_role_permissions(role_name) -> dict`
- `get_allowed_handoff_targets(role_name) -> list[str]`
- `can_role_delegate(role_name) -> bool`
- `requires_independent_review(role_name, artifact_type=None) -> bool`

## Minimum required roles
You must define an explicit finite role taxonomy. At minimum:
- `planner`
- `executor`
- `reviewer`
- `fixer`
- `validator`

## Required role-definition fields
- `role_name`
- `allowed_actions`
- `forbidden_actions`
- `allowed_handoff_targets`
- `can_delegate`
- `requires_review`
- `may_reopen_workflow`
- `may_reopen_issue`
- `may_reopen_finding`

## Requirements
- roles are finite and enumerated
- no role owns the full lifecycle alone
- reviewer authority must remain independent from author/executor authority for non-trivial artifacts
- permissions may not expand dynamically at runtime
- delegation permissions must be explicit and bounded per role

## Must not contain
- provider calls
- workflow execution
- handoff persistence
- governance bypass logic
- free-form role creation

## Definition of done
- finite roles and bounded permissions are explicit
- allowed handoff/delegation paths are explicit
- independent review requirements are explicit
