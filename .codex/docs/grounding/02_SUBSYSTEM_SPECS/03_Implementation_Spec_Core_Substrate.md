# Implementation Specification: Core Substrate

## 1. Purpose

The substrate is the durable backbone that keeps Forge-X reviewable, replayable, and non-brittle. It is the anti-drift state layer. It does not make decisions. It records and links the objects that decisions operate over.

## 2. Required modules

At minimum:

- `event_spine.py`
- `artifact_store.py`
- `issue_tracker.py`
- `dispatch_system.py`
- `provenance.py`
- `versioning.py`

## 3. Event spine requirements

The event spine must be append-only in behavior, even if the initial implementation is in-memory.

### Required event categories
- request_received
- artifact_created
- issue_created
- workflow_started
- workflow_transitioned
- validation_finding_created
- provider_invoked
- provider_failed
- workflow_completed
- workflow_reopened

### Required event fields
- event_id
- event_type
- created_at
- correlation_id
- workflow_run_id if applicable
- payload

### Invariants
- events are never silently dropped
- events are serializable
- payload shape must be deterministic enough to support replay

## 4. Artifact store requirements

Artifacts represent meaningful inputs, intermediate products, or outputs.

### Artifact classes
- input artifact
- normalized artifact
- generated artifact
- evidence artifact
- emitted artifact

### Required fields
- artifact_id
- artifact_kind
- content or content_ref
- source
- metadata
- created_at
- parent_artifact_ids if derived

### Behavioral requirements
- every major workflow step that produces meaningful content creates an artifact
- artifact lineage must be recoverable
- artifacts must be linkable to issues and review findings

## 5. Issue tracker requirements

Issues are not optional. They are how fix-flow and review work remains durable.

### Issue classes
- defect
- drift
- grounding_gap
- contradiction
- enhancement
- blocked_dependency
- policy_violation

### Required fields
- issue_id
- issue_type
- title
- description
- severity
- status
- related_artifact_ids
- related_finding_ids
- created_at
- updated_at

### Required statuses
- open
- in_progress
- blocked
- resolved
- closed
- reopened

### Lifecycle rules
- fix-flow must create or bind to an issue
- review findings can create issues
- resolved is not the same as closed
- reopen must preserve history

## 6. Dispatch system requirements

Dispatch is the controlled entry point into workflow selection and execution, not a chat shortcut.

### Dispatch inputs
- raw user/system signal
- source metadata
- optional workflow hint
- optional artifact references

### Dispatch outputs
- created artifact
- selected workflow mode
- created issue if triage demands it
- initial workflow_run object
- traceable response envelope

### Invariants
- dispatch never directly calls provider internals without going through control-plane selection
- dispatch must record event spine activity
