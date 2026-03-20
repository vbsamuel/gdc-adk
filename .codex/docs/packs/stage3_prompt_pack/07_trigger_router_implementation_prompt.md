# Global Control Header

Paste this header before each file-specific prompt:

```text
We are implementing Forge-X Stage 3 only.

Treat the uploaded markdown grounding files as binding system definition, repo constitution, execution law, and acceptance criteria.

This prompt is for one file only.

Before producing code:
1. identify the owning subsystem
2. identify the relevant contracts and interfaces required for this file
3. identify workflow modes affected
4. identify Stage 3 traceability rows advanced
5. identify acceptance assertions that must pass

Constraints:
- Do not introduce new architecture
- Do not expand scope beyond Stage 3
- Do not pull Stage 4, Stage 5, or Stage 6 responsibilities into this file
- Do not generate placeholder logic
- Do not merge responsibilities across subsystems
- Do not bypass canonicalization by sending raw user text directly into providers
- Do not treat indexing as optional
- Do not collapse emitted outputs into plain chat text only
- Do not modify unrelated files
- Do not hide logic in adapters or labs

Output implementation-grade Python code only for the requested file.
Respect repo constitution, import-direction rules, substrate contracts, information-plane ownership, controlled vocabularies, serializability, replayability, and file-level Definition of Done.
```

# Implement only: `src/gdc_adk/information_plane/activation/trigger_router.py`

## Owning subsystem
- `information_plane`

## Responsibility
Classify structured activation trigger categories from normalized signals. This file decides activation category and candidate workflow mode hints only. It does not execute workflows.

## Required public functions
- `classify_activation_category(normalized_signal) -> str`
- `select_workflow_mode(normalized_signal) -> str`
- `should_trigger_issue(normalized_signal) -> bool`
- `build_activation_reason(normalized_signal) -> dict`

## Required outputs
- `activation_category`
- `candidate_workflow_mode`
- `issue_triggered`
- `activation_reason`
- `next_action_types`

## Requirements
- classification must be structured, not conversational prose
- activation must support mapping toward `single_run`, `iterative`, `fix_flow`, `dynamic_flow`, and `fuzzy_logical_flow`
- bug/fix-like signals must be able to trigger fix-flow activation
- architecture/research-like requests must be classifiable without provider calls
- classification must be deterministic for bounded obvious cases

## Must not contain
- workflow execution
- provider execution
- provider routing
- review/finding ownership
- direct artifact persistence implementation

## Definition of done
- normalized signals can be classified into activation categories and candidate workflow modes
- issue-trigger hints are explicit
- activation reasons are structured
