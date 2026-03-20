# Global Repo-Wide Acceptance Checklist

## Purpose

This checklist is the final global consistency gate used alongside stage-local acceptance.

## Checklist

### Naming and structure
- [ ] File names comply with canonical lexicology.
- [ ] Public function names are explicit and semantically narrow.
- [ ] No vague dumping-ground files were introduced.

### Typing and code quality
- [ ] All public functions are typed.
- [ ] No hidden globals or import-time side effects exist.
- [ ] No placeholder or pass-only logic remains in accepted files.

### Boundary integrity
- [ ] Import direction complies with repo constitution.
- [ ] Adapters and labs remain thin.
- [ ] Providers do not own routing or policy.

### Workflow and review integrity
- [ ] Non-trivial reviewable work creates structured findings.
- [ ] Fix-flow remains issue-bound.
- [ ] Workflow state is durable and explicit.

### Memory and replay integrity
- [ ] Continuity is exportable and replayable.
- [ ] No hidden prompt-only continuity is required.

### Test integrity
- [ ] Unit, integration, and end-to-end obligations are satisfied for changed scope.
- [ ] Negative paths are tested.
- [ ] No empty tests or assertion-light tests remain.

### Traceability and acceptance
- [ ] All affected traceability rows are updated.
- [ ] Acceptance scenarios impacted by the change are mapped and re-run.
- [ ] No stage is marked complete purely because files exist.

### Performance and observability
- [ ] Hot paths have been reviewed for avoidable complexity.
- [ ] Critical operations emit structured observability data.

## Final disposition values
- `approved`
- `approved_with_findings`
- `rework_required`
- `blocked`
