# Global Error-Handling and Result-Envelope Standard

## Purpose

This document standardizes how Forge-X reports success, failure, partial completion, and review outcomes. It prevents silent failure, ambiguous returns, and inconsistent calling semantics across stages.

## Standard result envelope

Every non-trivial cross-file or cross-subsystem operation should return or emit a typed result envelope with equivalent semantics to:
- `status`
- `message`
- `artifacts_created`
- `issues_created`
- `findings_created`
- `events_recorded`
- `warnings`
- `error_code` if failed
- `trace_context`

## Status vocabulary

Use controlled statuses such as:
- `success`
- `partial_success`
- `validation_failed`
- `rejected`
- `not_applicable`
- `failed`

Do not invent ad hoc statuses like `okay`, `doneish`, or `worked`.

## Error handling rules

1. Silent exception swallowing is forbidden.
2. Bare `except:` is forbidden.
3. Domain failures must either raise explicit domain exceptions or produce typed failure envelopes.
4. Partial failure must be explicit.
5. Validation failure must not masquerade as execution success.
6. Missing required artifacts, issues, or findings must be surfaced as real failures.

## Required exception categories

At minimum, the implementation should have conceptually distinct exceptions for:
- configuration failure
- contract violation
- provider transport failure
- validation failure
- replay failure
- traceability violation
- workflow state violation

## Logging linkage

Whenever a failure occurs, it must be attributable to:
- file or subsystem
- operation name
- workflow_run_id if applicable
- artifact_id or issue_id if applicable
- provider or model if applicable

## Review checklist

Reject code if it:
- returns raw booleans for complex outcomes
- returns untyped dicts with arbitrary keys for public contracts
- hides partial failure
- downgrades validation errors into warnings without policy
