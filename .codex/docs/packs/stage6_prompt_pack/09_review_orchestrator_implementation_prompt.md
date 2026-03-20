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

# Implement only: `src/gdc_adk/workflows/review_orchestrator.py`

## Owning subsystem
- `workflows`

## Responsibility
Coordinate the independent review path for multi-agent flows without allowing review to collapse into informal agent chat.

## Required public functions
- `assign_review_agent(workflow_run, artifact_ids, reviewer_role) -> dict`
- `trigger_review(handoff_artifact, workflow_run) -> dict`
- `record_review_finding(finding, workflow_run) -> dict`

## Requirements
- reviewer role must be distinct from author/executor role for non-trivial artifacts
- reviewable handoffs must be capable of producing `ReviewFinding` objects
- review handoff completion must depend on validation/review outputs where policy requires it
- issue creation/escalation from findings must remain possible
- review path must remain durable and traceable

## Must not contain
- artifact generation
- workflow execution ownership
- prose-only review notes as substitute for findings
- bypass of validator or governance

## Definition of done
- independent review path is explicit
- review findings are durable and linked
- multi-agent flow cannot bypass review where required
