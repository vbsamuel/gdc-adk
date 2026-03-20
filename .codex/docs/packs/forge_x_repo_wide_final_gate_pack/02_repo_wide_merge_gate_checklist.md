# Repo-Wide Merge Gate Checklist

## Purpose

This checklist is the executable final gate used before accepting repo-wide changes.

## Gate sections

### G1 Packet completeness
- [ ] All required stage packets exist.
- [ ] Global standards pack exists.
- [ ] Full system integration pack exists.
- [ ] Repo-wide test and quality pack exists.
- [ ] Repo-wide final gate pack exists.

### G2 Packet purity
- [ ] No stage packet contains another stage's implementation prompts unless explicitly documented as cross-stage integration.
- [ ] Numbering and naming conventions are consistent.

### G3 File coverage completeness
- [ ] No previously promised implementation file is missing a prompt or implementation plan.
- [ ] No bounded scope is silently incomplete.

### G4 Traceability completeness
- [ ] All affected traceability rows are updated.
- [ ] No row is left dangling without acceptance proof or blocking finding.

### G5 Acceptance completeness
- [ ] All impacted acceptance scenarios are claimed and mapped.
- [ ] Final system acceptance review has been performed.

### G6 Code quality completeness
- [ ] No undocumented globals/constants.
- [ ] No untyped public interfaces.
- [ ] No placeholder logic.
- [ ] No empty tests.
- [ ] No hidden state in prompt carry-forward.

### G7 Final disposition
Mark one only:
- [ ] approved
- [ ] approved_with_findings
- [ ] rework_required
- [ ] blocked
