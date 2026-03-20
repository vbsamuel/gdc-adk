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

# Implement only: `src/gdc_adk/validation/grounding_checker.py`

## Owning subsystem
- `validation`

## Responsibility
Check grounding quality, unsupported claims, contradictions, and missing cases against source artifacts and emit source-linked structured findings.

## Required public functions
- `check_grounding(artifact, source_artifacts) -> list[dict]`
- `check_unsupported_claims(artifact, source_artifacts) -> list[dict]`
- `check_contradictions(artifact, source_artifacts) -> list[dict]`
- `check_missing_cases(artifact, source_artifacts) -> list[dict]`

## Requirements
- unsupported claims must become findings
- contradictions must become findings
- missing cases must become findings
- findings must retain source-linked evidence
- grounding checks must remain separate from authoring path for non-trivial outputs

## Must not contain
- authoring of the primary artifact
- workflow sequencing
- memory backend ownership
- prose-only review comments

## Definition of done
- unsupported claims, contradictions, and missing cases become source-linked structured findings
