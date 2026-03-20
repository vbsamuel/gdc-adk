# Forge-X Event, Issue, Finding, and Workflow Enums

## Purpose

This document defines the controlled vocabularies that should be used in code, contracts, validation, and observability. Do not invent synonyms casually.

## 1. Event type taxonomy

Use these event types exactly unless a new type is formally added.

### Request and ingress events
- `request_received`
- `signal_ingested`
- `signal_normalized`
- `artifact_indexed`
- `activation_classified`

### Artifact events
- `artifact_created`
- `artifact_revised`
- `artifact_emitted`

### Issue and finding events
- `issue_created`
- `issue_status_changed`
- `issue_reopened`
- `finding_created`
- `finding_resolved`

### Workflow events
- `workflow_started`
- `workflow_transitioned`
- `workflow_blocked`
- `workflow_completed`
- `workflow_failed`
- `workflow_reopened`

### Provider/runtime events
- `provider_selected`
- `provider_invoked`
- `provider_failed`
- `cache_hit`
- `cache_miss`

## 2. Issue type enum

Use these issue types:
- `defect`
- `drift`
- `grounding_gap`
- `contradiction`
- `enhancement`
- `blocked_dependency`
- `policy_violation`

## 3. Issue status enum

Use these statuses:
- `open`
- `in_progress`
- `blocked`
- `resolved`
- `closed`
- `reopened`

## 4. Finding type enum

Use these finding types:
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

## 5. Severity enum

Use these severities:
- `critical`
- `high`
- `medium`
- `low`

## 6. Workflow mode enum

Use these modes:
- `single_run`
- `iterative`
- `fix_flow`
- `dynamic_flow`
- `fuzzy_logical_flow`
- `research_flow`
- `code_flow`
- `world_flow`

If `research_flow`, `code_flow`, or `world_flow` are used, they should still coexist with the higher-level five-mode execution semantics where appropriate.

## 7. Workflow state enum (baseline)

Use these states unless a domain-specific workflow extends them:
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

### Fix-flow extended states
- `issue_opened`
- `remediation_in_progress`
- `verification_pending`
- `resolution_proposed`
- `resolution_verified`

## 8. Example Python enum definitions

```python
from enum import Enum

class Severity(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class IssueStatus(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    BLOCKED = "blocked"
    RESOLVED = "resolved"
    CLOSED = "closed"
    REOPENED = "reopened"
```

## 9. Rule

Do not mix:
- `sev1`, `p0`, `critical`
- `open`, `todo`, `new`
- `bug`, `defect`, `issue_type=problem`

Pick the controlled taxonomy and use it consistently.
