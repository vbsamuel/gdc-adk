# Global Test Quality and Coverage Standard

## Purpose

This document defines what test quality means across Forge-X. Coverage is not considered complete because lines execute. Coverage is complete only when behavior, boundaries, negative paths, and integration obligations are proven.

## Coverage law

### Unit coverage
Every public file must have unit coverage for:
- primary success path
- contract validation behavior
- at least one negative path
- edge conditions relevant to its responsibility

### Integration coverage
Every subsystem boundary must have integration tests for:
- valid handoff
- invalid handoff
- traceability preservation
- correct artifact/issue/finding propagation where applicable

### End-to-end coverage
Full-system scenarios must prove:
- deterministic request path
- provider-based request path
- grounded artifact flow
- review/finding generation
- replay/resume behavior
- multi-agent governed handoff behavior

## Coverage complete means all of the following
- line coverage for the changed scope is high and justified
- branch coverage is meaningful on decision-heavy files
- failure paths are explicitly tested
- deterministic replay behavior is tested where relevant
- typed outputs are asserted, not merely non-null
- artifact lineage and IDs are asserted where relevant
- issue/finding lifecycle effects are asserted where relevant

## Forbidden weak testing patterns
- smoke tests only
- tests that assert only `status_code == 200`
- tests that assert only object existence without semantic checks
- tests that mock away the exact behavior under review
- empty or placeholder tests

## Mandatory review questions
- What failure paths are still untested?
- What branch decisions still lack assertion?
- What public contract fields are not asserted?
- What subsystem boundary is unproven?
