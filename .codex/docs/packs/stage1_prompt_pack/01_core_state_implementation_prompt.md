# Global Control Header

Paste this header before each file-specific prompt:

```text
We are implementing Forge-X Stage 1 only.

Treat the uploaded markdown grounding files as binding architecture, repo constitution, execution law, and acceptance criteria.

This prompt is for one file only.

Before producing code:
1. identify the owning subsystem
2. identify the owned contracts
3. identify the workflow modes structurally affected
4. identify the Stage 1 traceability rows advanced
5. identify the acceptance assertions that must pass

Constraints:
- Do not introduce new architecture
- Do not expand beyond Stage 1
- Do not reference future stages as implemented behavior
- Do not generate placeholder logic
- Do not merge responsibilities across subsystems
- Do not modify unrelated files
- Do not put logic in adapters or labs
- Do not add provider routing, provider execution, ingestion, workflow engine sequencing, validation subsystem behavior, or memory backend behavior

Output implementation-grade Python code only for the requested file.
Respect repo constitution, naming rules, controlled enums, serializability, replayability, and exact public API requirements.
```

# Implement only: `src/gdc_adk/core/state.py`

## Owning subsystem
- `core`

## Owned responsibility
- controlled vocabularies and minimal legal-state helpers required by Stage 1

## Must contain
- `WORKFLOW_MODES`
- `WORKFLOW_STATES`
- `FIX_FLOW_STATES`
- `ISSUE_TYPES`
- `ISSUE_STATUSES`
- `FINDING_TYPES`
- `SEVERITIES`
- `EVENT_TYPES`

## Required public functions
- `validate_workflow_mode(workflow_mode: str) -> str`
- `validate_workflow_state(workflow_state: str) -> str`
- `validate_issue_type(issue_type: str) -> str`
- `validate_issue_status(issue_status: str) -> str`
- `validate_severity(severity: str) -> str`
- `validate_event_type(event_type: str) -> str`
- `is_terminal_workflow_state(workflow_state: str) -> bool`
- `is_reopenable_issue_status(issue_status: str) -> bool`

## Required vocabulary values

### Workflow modes
- `single_run`
- `iterative`
- `fix_flow`
- `dynamic_flow`
- `fuzzy_logical_flow`
- `research_flow`
- `code_flow`
- `world_flow`

### Workflow states
- `received`
- `classified`
- `activated`
- `planned`
- `executing`
- `awaiting_review`
- `revising`
- `validated`
- `completed`
- `failed`
- `blocked`
- `reopened`

### Fix-flow states
- `issue_opened`
- `remediation_in_progress`
- `verification_pending`
- `resolution_proposed`
- `resolution_verified`

### Issue types
- `defect`
- `drift`
- `grounding_gap`
- `contradiction`
- `enhancement`
- `blocked_dependency`
- `policy_violation`

### Issue statuses
- `open`
- `in_progress`
- `blocked`
- `resolved`
- `closed`
- `reopened`

### Finding types
- `unsupported_claim`
- `missing_case`
- `architecture_drift`
- `contract_violation`
- `provider_policy_violation`
- `traceability_gap`
- `replayability_gap`
- `validation_gap`
- `grounding_gap`
- `contradiction`

### Severities
- `critical`
- `high`
- `medium`
- `low`

### Event types
- `request_received`
- `signal_ingested`
- `signal_normalized`
- `artifact_indexed`
- `activation_classified`
- `artifact_created`
- `artifact_revised`
- `artifact_emitted`
- `issue_created`
- `issue_status_changed`
- `issue_reopened`
- `finding_created`
- `finding_resolved`
- `workflow_started`
- `workflow_transitioned`
- `workflow_blocked`
- `workflow_completed`
- `workflow_failed`
- `workflow_reopened`
- `provider_selected`
- `provider_invoked`
- `provider_failed`
- `cache_hit`
- `cache_miss`

## Must not contain
- persistence
- provider behavior
- workflow sequencing
- ad hoc synonyms

## Negative-path requirements
- reject non-canonical values like `done`, `bug`, `severity_1`
- raise explicit errors on invalid values

## Definition of done
- all controlled vocabularies are centralized
- validators reject invalid values explicitly
- terminal/reopenable helpers behave correctly
