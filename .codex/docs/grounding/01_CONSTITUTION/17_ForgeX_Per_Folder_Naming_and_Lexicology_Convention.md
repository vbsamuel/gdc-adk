# Forge-X Per-Folder Naming and Lexicology Convention

## 1. `config/`

### File names
- `settings.py`
- future: `schema.py`, `defaults.py` if needed

### Preferred function names
- `load_yaml_config`
- `require_env`
- `get_provider_config`
- `get_default_provider`

### Forbidden names
- `config_utils.py`
- `helper.py`
- `read_stuff()`

---

## 2. `substrate/`

### File names
- `event_spine.py`
- `artifact_store.py`
- `issue_tracker.py`
- `dispatch_system.py`
- future: `provenance.py`, `versioning.py`

### Naming rule
Use durable nouns:
- `artifact`
- `issue`
- `event`
- `dispatch`
- `provenance`

Avoid vague words:
- `record`
- `item`
- `thing`
unless part of a stable contract name like `ArtifactRecord`

---

## 3. `information_plane/`

### Subfolders
- `ingestion/`
- `normalization/`
- `indexing/`
- `activation/`
- `egress/`
- `connectors/`
- `modalities/`

### Verb expectations
- `ingest_*`
- `normalize_*`
- `index_*`
- `activate_*`
- `emit_*`

### Example
Good:
- `ingest_text`
- `normalize_signal`
- `activate_workflow_from_signal`

Bad:
- `process_text`
- `handle_input`
- `do_activation`

---

## 4. `control_plane/`

### File names
- `policy.py`
- `router.py`
- `optimizer.py`
- `context_assembler.py`
- `model_registry.py`

### Naming rule
Decision functions should be named as decisions:
- `select_provider`
- `allow_cloud`
- `should_use_local`
- `cache_key_for`

Do not hide decision semantics behind vague names like:
- `handle_request`
- `smart_route`
- `pick_best`

---

## 5. `runtime/`

### Naming rule
Runtime names should refer to lifecycle and execution mechanics:
- `local_model_manager.py`
- `pipeline_executor.py`
- `watchdog.py`

Functions should reflect state changes:
- `set_active_model`
- `clear_active_model`

---

## 6. `providers/`

### File names
Always suffix backend adapters with `_provider.py` unless the provider family folder uses a more specific implementation file.

Good:
- `ollama_provider.py`
- `google_provider.py`

Weather-specific provider folder:
- `base.py`
- `open_meteo.py`
- `router.py`

### Naming rule
Provider file names should represent backend or service identity, not task type.

Bad:
- `summarizer_provider.py`
- `weather_google.py` if weather is actually a separate provider family and should sit under `providers/weather/`

---

## 7. `capabilities/`

### Naming rule
Capability file names should be domain nouns:
- `time.py`
- `weather.py`
- `geo.py`

Functions should be explicit:
- `get_current_time`
- `get_weather`
- `resolve_city_reference`

Do not embed routing or provider strategy in capability names.

---

## 8. `memory/`

### File names
- `contracts.py`
- `cache.py`
- `context_store.py`
- `continuity.py`
- future: `replay.py`, `lifecycle.py`

### Naming rule
Use role-based names to preserve future replaceability.

Good:
- `ContextStore`
- `ContinuityStore`

Bad:
- `SimpleMemoryHack`
- `TemporaryContextThing`

---

## 9. `validation/`

### File names
- `validator.py`
- `drift_checker.py`
- `traceability_auditor.py`
- `grounding_checker.py`

### Naming rule
Validation names should communicate what is being checked.

Bad:
- `review.py`
- `quality.py`
- `checks.py`

unless they are tightly scoped and documented.

---

## 10. `workflows/`

### File names
- `engine.py`
- future: `state_machine.py`, `fix_flow.py`, `iterative_flow.py`

### Naming rule
Workflow code must reflect execution mode or orchestration role, not just task domain.

Bad:
- `main_flow.py`
- `do_work.py`

---

## 11. `adapters/`

### Naming rule
Adapter files must end with `_adapter.py` when they bridge to an external framework.

Good:
- `weather_time_agent_adapter.py`

Bad:
- `weather_time_agent_core.py` if it is really an adapter

---

## 12. `labs/`

### Naming rule
Lab files should stay minimal and surface-specific. They should not establish new domain lexicology at all.
