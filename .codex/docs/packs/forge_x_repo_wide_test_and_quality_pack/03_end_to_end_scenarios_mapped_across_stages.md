# End-to-End Scenarios Mapped Across Stages

## Required end-to-end scenario families

### E2E-1 Deterministic request path
- request enters through information plane or direct structured signal path
- deterministic capability is selected
- substrate records artifacts/events
- result is emitted with traceability

### E2E-2 Provider-backed path
- request routes through control plane
- provider selection and attribution are preserved
- result is emitted with artifacts and observability

### E2E-3 Grounded artifact review path
- source artifact exists
- generated artifact is reviewed
- structured finding is created if necessary
- workflow status reflects review outcome

### E2E-4 Fix-flow remediation path
- issue exists
- fix-flow proceeds through remediation and verification
- reopen logic is testable

### E2E-5 Replay/resume path
- continuity snapshot exists
- system resumes without hidden context
- workflow state and findings survive

### E2E-6 Governed multi-agent handoff path
- typed handoff artifact exists
- delegated work remains bounded and reviewable
- governance blocks invalid delegation

## Mapping rule

Every end-to-end test must identify:
- stages traversed
- files and subsystems touched
- artifacts/issues/findings created or updated
- traceability rows proven
