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

# Implement only: `src/gdc_adk/workflows/state_machine.py`

## Owning subsystem
- `workflows`

## Responsibility
Define and enforce explicit allowed workflow-state transitions for all supported workflow modes.

## Required public functions
- `get_allowed_transitions(workflow_mode, current_state) -> list[str]`
- `validate_transition(workflow_mode, current_state, next_state) -> None`
- `transition_workflow_state(workflow_run, next_state, reason) -> dict`
- `is_terminal_state(workflow_mode, state) -> bool`

## Required transition model
You must explicitly define legal transitions for:
- `single_run`
- `iterative`
- `fix_flow`
- `dynamic_flow`
- `fuzzy_logical_flow`

## Baseline states
- `received`
- `classified`
- `activated`
- `planned`
- `executing`
- `awaiting_review`
- `revising`
- `validated`
- `completed`
- `failed`
- `blocked`
- `reopened`

## Fix-flow extended states
- `issue_opened`
- `remediation_in_progress`
- `verification_pending`
- `resolution_proposed`
- `resolution_verified`

## Transition rules
- any edge not explicitly enumerated must be rejected
- direct `received -> completed` is invalid except an explicitly trivial deterministic one-step path, and even then must still be recorded explicitly
- reopen transitions must be mode-aware
- block/fail transitions must preserve rationale

## Must not contain
- provider logic
- issue persistence
- finding persistence
- memory storage implementation
- narrative-only transition logic

## Definition of done
- allowed transitions are explicit per mode
- invalid transitions fail explicitly
- transition updates remain serializable and replay-friendly
