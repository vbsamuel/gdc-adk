# Global Logging and Observability Standard

## Purpose

This document standardizes observability across Forge-X so that behavior is diagnosable across stages and boundaries.

## Logging rules

All non-trivial subsystem operations should emit structured logs or equivalent observability events containing relevant context such as:
- subsystem
- operation
- workflow_run_id when applicable
- artifact_id / issue_id / finding_id when applicable
- provider name and model when applicable
- status
- duration
- error_code if failed

## Observability requirements by domain

### Substrate
- dispatch started/completed
- artifact created/updated
- issue created/reopened/closed
- event recorded

### Control plane
- routing decision
- deterministic capability hit
- cache hit/miss
- provider selected
- fallback invoked

### Information plane
- ingestion completed
- normalization completed
- index update completed
- activation candidate emitted

### Workflows and validation
- workflow started
- workflow transitioned
- finding created
- validation failed/passed
- traceability audit result

### Memory
- continuity snapshot saved
- replay started/completed
- resume succeeded/failed

### Multi-agent
- handoff requested
- handoff accepted/rejected
- delegation completed
- governance block applied

## Review checklist

Reject implementation if:
- a critical cross-stage operation leaves no traceable record
- failures are not attributable to a subsystem and operation
- model/provider attribution disappears in routed flows
- workflow state changes cannot be reconstructed from observable signals
