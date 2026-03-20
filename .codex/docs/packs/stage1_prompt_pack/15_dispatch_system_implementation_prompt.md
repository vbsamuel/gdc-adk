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

# Implement only: `src/gdc_adk/substrate/dispatch_system.py`

## Owning subsystem
- `substrate`

## Owned responsibility
- structured Stage 1 dispatch entry only

## Use
- `Artifact`, `Issue`, `WorkflowRun`, `Event` contracts from `core/contracts.py`
- controlled validators from `core/state.py`
- event recording from `substrate/event_spine.py`
- artifact persistence from `substrate/artifact_store.py`
- issue lifecycle from `substrate/issue_tracker.py`

## Define required public contract classes
- `DispatchRequest`
- `DispatchResult`

## DispatchRequest required fields
- `request_id: str`
- `raw_signal: str | dict`
- `source_metadata: dict`
- `workflow_hint: str | None`
- `artifact_reference_ids: list[str]`
- `correlation_id: str`

## DispatchResult required fields
- `request_artifact: Artifact`
- `workflow_run: WorkflowRun`
- `created_issue: Issue | None`
- `emitted_event_ids: list[str]`

## Required public functions
- `dispatch_request(request: DispatchRequest) -> DispatchResult`
- `select_workflow_mode(request: DispatchRequest) -> str`
- `initialize_workflow_run(request: DispatchRequest, workflow_mode: str, input_artifact_id: str) -> WorkflowRun`
- `should_create_issue(request: DispatchRequest, workflow_mode: str) -> bool`

## Decision rules
- if `workflow_hint` is present and valid, use it
- else if the signal clearly indicates broken/fix/remediation behavior, select `fix_flow`
- else default to `single_run`

## Stage 1 required behavior
- create a request artifact
- create a workflow_run entry
- emit `request_received`
- emit `artifact_created`
- emit `workflow_started`
- emit `workflow_transitioned`
- if `fix_flow` issue is created, emit `issue_created`

## Constraints
- do not call providers
- do not implement information-plane normalization
- do not implement workflow engine sequencing
- do not return prose-only results
- all outputs must be structured and serializable

## Definition of done
- generic request produces `single_run` structured entry
- fix-like request produces `fix_flow` structured entry plus issue creation
- event IDs are returned in `emitted_event_ids`
