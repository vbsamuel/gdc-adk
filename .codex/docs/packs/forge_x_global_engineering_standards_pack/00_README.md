# Forge-X Global Engineering Standards Pack

## Purpose

This pack is the cross-stage engineering control layer for Forge-X. It exists to prevent a stage from being locally acceptable while still being globally inconsistent, weakly typed, lexically ambiguous, operationally brittle, or impossible to integrate with adjacent stages.

This pack is binding across Stage 1 through Stage 6. It must be loaded with every bounded implementation, review, remediation, integration, and pre-merge session.

## Required usage

Use this pack when requesting:
- bounded implementation briefs
- code generation
- code review
- test generation
- integration validation
- remediation of findings
- end-to-end system verification
- pre-merge review

## Files in this pack

1. `01_global_naming_and_lexicology_enforcement_prompt.md`
2. `02_global_coding_and_typing_enforcement_prompt.md`
3. `03_global_variable_constant_env_naming_rules.md`
4. `04_global_import_boundary_and_dependency_direction_enforcement_prompt.md`
5. `05_global_error_handling_and_result_envelope_standard.md`
6. `06_global_test_quality_and_coverage_standard.md`
7. `07_global_performance_and_complexity_review_prompt.md`
8. `08_global_logging_and_observability_standard.md`
9. `09_global_anti_pattern_rejection_prompt.md`
10. `10_global_repo_wide_acceptance_checklist.md`

## Mandatory operator rule

No stage packet, file implementation, or code review is complete unless it is also checked against this pack.
