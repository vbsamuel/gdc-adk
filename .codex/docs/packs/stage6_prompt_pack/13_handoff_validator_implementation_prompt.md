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

# Implement only: `src/gdc_adk/validation/handoff_validator.py`

## Owning subsystem
- `validation`

## Responsibility
Validate handoff integrity against artifacts, issues, findings, continuity references, and traceability expectations before handoff completion.

## Required public functions
- `validate_handoff_artifacts(handoff_artifact) -> dict`
- `validate_traceability_links(handoff_artifact, workflow_run) -> dict`
- `validate_review_requirements(handoff_artifact, workflow_run) -> dict`

## Requirements
- all referenced artifacts must exist or resolve
- issue IDs must resolve when present
- finding IDs must resolve when present
- continuity references must resolve when present
- handoff for reviewable artifacts must not bypass review/finding requirements where policy demands them
- lineage must remain preserved across handoff

## Must not contain
- artifact authoring
- provider execution
- silent acceptance of broken references
- prose-only validation notes

## Definition of done
- invalid handoffs are blocked explicitly
- review/issue/finding/artifact linkage is validated before completion
- lineage-preserving traceability is enforced
