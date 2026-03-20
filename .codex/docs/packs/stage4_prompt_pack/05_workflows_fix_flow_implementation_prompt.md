# Global Control Header

Paste this header before each file-specific prompt:

```text
We are implementing Forge-X Stage 4 only.

Treat the uploaded markdown grounding files as binding system definition, repo constitution, execution law, and acceptance criteria.

This prompt is for one file only.

Before producing code:
1. identify the owning subsystem
2. identify the relevant contracts and interfaces required for this file
3. identify workflow modes affected
4. identify Stage 4 traceability rows advanced
5. identify acceptance assertions that must pass

Constraints:
- Do not introduce new architecture
- Do not expand scope beyond Stage 4
- Do not pull Stage 5 or Stage 6 responsibilities into this file
- Do not generate placeholder logic
- Do not merge responsibilities across subsystems
- Do not reduce workflows to prose-only state
- Do not treat review as plain comments or chat notes
- Do not allow non-trivial validation to be performed by the same exact generation path without independent finding objects
- Do not omit reopen, verification, or closure semantics
- Do not modify unrelated files
- Do not hide logic in adapters or labs

Output implementation-grade Python code only for the requested file.
Respect repo constitution, workflow/validation boundaries, controlled vocabularies, serializability, replayability, explicit state transitions, independent findings, and file-level Definition of Done.
```

# Implement only: `src/gdc_adk/workflows/fix_flow.py`

## Owning subsystem
- `workflows`

## Responsibility
Implement the issue-driven remediation path with explicit issue linkage, remediation evidence, verification, closure, and reopen semantics.

## Required public functions
- `start_fix_flow(workflow_run, issue_id, artifact_ids) -> dict`
- `record_remediation_attempt(workflow_run, issue_id, remediation_notes, artifact_ids) -> dict`
- `attach_remediation_evidence(workflow_run, issue_id, evidence_artifact_ids) -> dict`
- `mark_verification_pending(workflow_run, issue_id) -> dict`
- `build_verification_result(issue_id, workflow_run_id, evidence_artifact_ids, verification_status, verifier, verification_reason) -> dict`
- `verify_resolution(workflow_run, issue_id, verification_result) -> dict`
- `close_fix_flow(workflow_run, issue_id, closure_reason) -> dict`
- `reopen_fix_flow(workflow_run, issue_id, reopen_reason) -> dict`

## Required linkage rules
- `WorkflowRun.issue_ids` must contain the linked issue
- remediation evidence artifact IDs must be explicit
- verification result must link:
  - `issue_id`
  - `workflow_run_id`
  - `evidence_artifact_ids`
  - verification timestamp
- reopen must preserve workflow history and issue history consistency

## Requirements
- fix-flow must not proceed without bound issue linkage
- verification must be explicit and structured
- closure without evidence and verification is invalid
- reopen after failed or invalid verification must be explicit and reasoned

## Must not contain
- issue-tracker storage implementation
- provider routing
- prose-only remediation tracking
- closure optimism without evidence

## Definition of done
- issue/workflow/evidence linkage is formal and persistent in structured state
- verification and reopen behavior are explicit and testable
