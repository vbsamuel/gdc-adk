# Global Naming and Lexicology Enforcement Prompt

## Purpose

This prompt enforces one controlled language for Forge-X across all stages. It prevents semantic drift caused by synonyms, vague names, overloaded helper functions, unclear state names, or inconsistent file naming.

## Operator prompt

```text
You are reviewing or implementing Forge-X under mandatory global naming control.

Apply the following naming law before proposing code or accepting code:

1. File names must use snake_case and must reflect subsystem ownership and semantic role.
2. Public functions must use explicit verb-first names that describe the exact action.
3. Public classes and models must use stable domain nouns already established in Forge-X grounding.
4. Controlled vocabulary from Forge-X enums and lexicology rules is mandatory. Do not invent synonyms casually.
5. Workflow state names, issue states, finding states, event names, and artifact classes must match the controlled taxonomy.
6. Reject vague names such as:
   - handle_request
   - process_input
   - do_work
   - smart_route
   - pick_best
   - helper
   - manager when a narrower domain noun exists
7. Reject names that hide policy, routing, or review semantics.
8. Reject names that merge multiple responsibilities into one identifier.

Before accepting or generating code, provide:
- allowed file names in scope
- allowed public functions in scope
- any detected naming violations
- exact rename recommendations

Do not produce code until naming is compliant.
```

## Required conventions

### File naming
- `settings.py`
- `contracts.py`
- `state.py`
- `event_spine.py`
- `artifact_store.py`
- `issue_tracker.py`
- `dispatch_system.py`
- `policy.py`
- `router.py`
- `context_assembler.py`
- `gate_evaluator.py`
- `local_model_manager.py`
- `document_ingestor.py`
- `canonicalizer.py`
- `artifact_index.py`
- `workflow_activation.py`
- `artifact_emitter.py`
- `validator.py`
- `drift_checker.py`
- `traceability_auditor.py`
- `grounding_checker.py`
- `continuity.py`
- `context_store.py`
- `replay.py`

### Preferred function naming patterns
- ingest_*
- normalize_*
- index_*
- activate_*
- emit_*
- create_*
- update_*
- resolve_*
- validate_*
- select_*
- load_*
- save_*
- replay_*
- resume_*
- verify_*

### Forbidden naming patterns
- generic `utils.py` or `helpers.py` dumping grounds
- `temp_*`, `final_final_*`, `new_*`, `old_*`
- unqualified `data`, `info`, `state`, `result`, `obj`
- `manager` when the file or class does not manage a bounded lifecycle

## Review outputs required

For each naming issue found:
- issue id
- file
- current name
- violation type
- required replacement
- reason the replacement is semantically stronger
