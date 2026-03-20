# Mutation and Failure-Path Expectations

## Purpose

Repo-wide quality requires more than happy paths. It must be hard for broken logic to survive the test suite.

## Required failure-path families
- bad config
- invalid contract payload
- provider transport failure
- unsupported modality
- workflow state violation
- traceability mismatch
- replay failure
- governance block in multi-agent flow

## Mutation expectations

Where practical, tests should be strong enough that these changes would fail:
- reversed boolean policy conditions
- missing fallback guard
- missing artifact lineage update
- missing issue creation in fix-flow
- missing ReviewFinding creation in reviewable flow
- dropped continuity snapshot field
- acceptance path incorrectly marked success after validation failure
