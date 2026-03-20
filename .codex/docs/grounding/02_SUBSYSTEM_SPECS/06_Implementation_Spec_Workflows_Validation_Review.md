# Implementation Specification: Workflows, Validation, and Review Spine

## 1. Workflow purpose

Workflows are not scripts. They are stateful execution contracts over Forge-X subsystems.

Each workflow must define:
- entry condition
- phase list or state machine
- phase transition logic
- retry/reopen rules
- completion condition
- validation gates

## 2. Minimum workflow state model

Every workflow run should capture at least:
- workflow_run_id
- mode
- current_state
- prior_states
- input_artifact_ids
- output_artifact_ids
- open_issue_ids
- finding_ids
- created_at
- updated_at

## 3. Required review spine

Forge-X must treat review findings as first-class objects, not comments lost in chat.

### ReviewFinding fields
- finding_id
- finding_type
- severity
- description
- related_artifact_ids
- evidence
- status
- created_at

### Typical finding types
- grounding_gap
- contradiction
- missing_case
- unsupported_claim
- architecture_drift
- repo_constitution_violation
- provider_policy_violation

## 4. Review lifecycle

A finding can:
- open
- be accepted
- be rejected with rationale
- be resolved
- be reopened

A resolved finding can create or close issues depending on policy.

## 5. Validation independence rule

The same exact generation path must not be treated as sufficient validation for its own output. Independent review or at least independent finding production is required for non-trivial artifacts.

## 6. Fix-flow requirements

Fix-flow must:
- bind to an issue
- create evidence artifacts if needed
- record attempted remediation
- verify result
- close or reopen based on verification

## 7. Iterative flow requirements

Iterative flow must:
- use continuity snapshots
- preserve prior findings
- incorporate correction deltas
- not restart from zero context every turn

## 8. Multi-agent workflow requirement

Multi-agent workflows are allowed only after:
- single-agent workflows produce typed artifacts
- issue and review linkage exists
- shared workflow state is durable

Role-free chat swarms are forbidden. Multi-agent orchestration must be role-bound and artifact-mediated.
