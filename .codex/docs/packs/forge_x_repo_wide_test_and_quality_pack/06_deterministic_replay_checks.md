# Deterministic Replay Checks

## Purpose

Replay and resume must be auditable and not rely on hidden prompt memory.

## Required replay checks
- continuity snapshot can be loaded
- workflow run can be reconstructed
- artifacts/issues/findings referenced by the snapshot are available or fail explicitly
- replay result is deterministic for the same stored state and bounded inputs
- multi-agent handoff lineage survives replay if applicable

## Reject if
- replay outcome changes because hidden runtime-only state is missing
- replay requires undocumented external context
- resume silently drops findings, issues, or traceability links
