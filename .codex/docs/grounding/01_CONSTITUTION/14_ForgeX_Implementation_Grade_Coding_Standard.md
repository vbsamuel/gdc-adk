# Forge-X Implementation-Grade Coding Standard

Generated: 2026-03-19T10:51:06Z

## Purpose

This document defines the binding Python coding standard for Forge-X. It exists to prevent:
- inconsistent naming
- ambiguous function semantics
- cross-layer leakage
- placeholder utility dumps
- hidden state and untraceable side effects
- code that is syntactically valid but architecturally unusable

This is not a style-preference guide. It is a system-engineering control document.

## 1. Language and module standard

Forge-X uses Python as a primary implementation language in the current repo. Python code must be:
- explicit
- typed where meaningful
- layer-owned
- replay-friendly
- side-effect controlled
- import-direction compliant

### Required default conventions
- files: `snake_case.py`
- directories: `snake_case/`
- classes: `PascalCase`
- functions: verb-first `snake_case`
- constants: `UPPER_SNAKE_CASE`
- private helpers: `_single_leading_underscore`

### Forbidden conventions
- camelCase function names
- PascalCase file names
- hidden side effects in import-time code
- single-letter variable names outside very short comprehensions
- catch-all “utils” modules as dumping grounds

---

## 2. File naming rules

### Required file patterns by role

#### Contracts and data models
- `contracts.py`
- `state.py`
- `snapshot.py`
- `models.py` only if bounded and specific

#### Stores and trackers
- `artifact_store.py`
- `issue_tracker.py`
- `context_store.py`

#### Routing and policy
- `router.py`
- `policy.py`
- `optimizer.py`
- `context_assembler.py`

#### Providers
- `ollama_provider.py`
- `google_provider.py`
- `open_meteo.py`

#### Validation and review
- `validator.py`
- `checker.py`
- `auditor.py`

#### Workflow and orchestration
- `engine.py`
- `workflow_activation.py`
- `dispatch_system.py`

### Forbidden file names
- `misc.py`
- `helpers.py`
- `common.py` unless strictly defined
- `new_core.py`
- `final.py`
- `temp.py`
- `try_this.py`

---

## 3. Function naming rules

### Function names must communicate action and ownership

Good examples:
- `create_issue`
- `create_artifact`
- `select_provider`
- `resolve_city_reference`
- `normalize_signal`
- `validate_artifact_record`
- `reopen_issue`
- `transition_workflow_state`

Bad examples:
- `issue_handler`
- `artifactThing`
- `do_it`
- `handle_data`
- `process_stuff`
- `run_all`
- `smart_route`

### Verb prefixes by meaning

#### Creation / construction
- `create_*` → create durable system object
- `build_*` → assemble transient structure
- `initialize_*` → setup or prepare runtime/service state

#### Retrieval / lookup / resolution
- `get_*` → direct retrieval
- `list_*` → collection retrieval
- `find_*` → search-like retrieval
- `resolve_*` → alias, reference, or identifier resolution
- `select_*` → policy or decision selection

#### State change
- `start_*`
- `transition_*`
- `complete_*`
- `close_*`
- `reopen_*`
- `fail_*`

#### Validation / review
- `validate_*`
- `check_*`
- `audit_*`

#### Ingress / normalization / egress
- `ingest_*`
- `normalize_*`
- `index_*`
- `activate_*`
- `emit_*`

---

## 4. Variable naming rules

### ID fields must always be explicit

Good:
- `artifact_id`
- `issue_id`
- `workflow_run_id`
- `finding_id`
- `context_block_id`

Bad:
- `id`
- `ref`
- `obj_id`
- `item_id` when actual semantic type is known

### Collections must be typed and plural

Good:
- `artifact_ids`
- `open_issue_ids`
- `review_findings`
- `context_blocks`
- `provider_chain`

Bad:
- `items`
- `results`
- `objs`
- `things`

### Boolean variables must read as predicates

Good:
- `is_active`
- `is_replayable`
- `has_open_findings`
- `can_retry`
- `should_use_local`
- `allow_cloud_fallback`

Bad:
- `flag`
- `ok`
- `ready`
- `status_bool`

### Time and lifecycle fields

Good:
- `created_at`
- `updated_at`
- `started_at`
- `completed_at`
- `closed_at`

Bad:
- `time`
- `date`
- `ts` unless clearly scoped and private

---

## 5. Typing and signatures

Public functions should use type hints when doing system work.

### Good
```python
def create_issue(
    title: str,
    description: str,
    issue_type: str,
    severity: str,
    related_artifact_ids: list[str] | None = None,
) -> dict:
    ...
```

### Bad
```python
def create_issue(title, description, kind, sev, ids=None):
    ...
```

### Rule
If a function crosses subsystem boundaries or produces durable objects, type it.

---

## 6. Import and side-effect rules

### Allowed
- imports at top of file
- explicit imports
- intra-layer imports respecting repo constitution

### Forbidden
- import-time network calls
- import-time filesystem mutation
- import-time global provider instantiation
- wildcard imports

### Good
```python
from gdc_adk.config.settings import get_provider_config
from gdc_adk.providers.base import LLMRequest, LLMResponse
```

### Bad
```python
from gdc_adk.providers.base import *
client = build_google_client()  # import-time side effect
```

---

## 7. Error-handling standard

### Required
- fail explicitly
- preserve actionable context
- do not silently swallow provider or routing failures

### Good
```python
if not model_name:
    raise RuntimeError("Missing model for provider alias 'ollama' in config.yaml")
```

### Bad
```python
if not model_name:
    return None
```

### Rule
Returning `None` is not an acceptable replacement for contract-level failure unless the return type explicitly permits that behavior and the caller is required to handle it.

---

## 8. Logging and observability preparation

Even before full telemetry is implemented, public paths should preserve structured data.

### Prefer
- returning structured result envelopes
- attaching provider/model attribution
- attaching artifact IDs and issue IDs to results when relevant

### Avoid
- only printing user-friendly text
- losing provenance at layer boundaries

---

## 9. Anti-drift coding rules

- no business logic in adapters
- no routing logic in providers
- no hidden persistence in helper functions
- no free-form dicts passed across layers when a stable contract exists
- no “temporary” hardcoded model names in code unless documented as controlled bootstrap exceptions
- no architecture encoded only in comments

---

## 10. Completion rule for code files

A file is not “done” because it exists or imports. It is done when:
- ownership is correct
- naming is correct
- public functions are explicit
- error paths are explicit
- interactions with adjacent layers are clear
- anti-patterns below are absent
