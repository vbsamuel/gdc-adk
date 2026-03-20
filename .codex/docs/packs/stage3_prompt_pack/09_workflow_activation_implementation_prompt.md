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

# Implement only: `src/gdc_adk/information_plane/activation/workflow_activation.py`

## Owning subsystem
- `information_plane`

## Responsibility
Produce structured workflow-activation output from normalized signals, indexed artifact references, and trigger-routing decisions. This file does not own Stage 4 workflow execution semantics.

## Required public functions
- `activate_workflow(normalized_signal, artifact_ids, trigger_metadata) -> dict`
- `build_activation_output(normalized_signal, artifact_ids, trigger_metadata) -> dict`

## Required activation-output fields
- `activation_output_id`
- `activation_category`
- `candidate_workflow_mode`
- `related_artifact_ids`
- `issue_triggered`
- `activation_reason`
- `next_action_types`
- `normalized_signal_id`
- `created_at`

## Requirements
- activation output must be structured, not conversational
- activation output must preserve artifact linkage
- activation output must preserve normalized-signal linkage
- activation must be able to surface fix-flow trigger metadata for downstream issue creation
- activation output may reference workflow-run construction downstream, but must not absorb Stage 4 execution responsibilities

## Must not contain
- direct provider calls
- workflow step execution
- validation logic ownership
- memory backend ownership

## Definition of done
- normalized signals + artifact references become structured activation outputs
- activation output is sufficient for downstream dispatch/workflow layers without embedding Stage 4 behavior
