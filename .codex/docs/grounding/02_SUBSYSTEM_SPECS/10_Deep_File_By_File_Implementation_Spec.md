# Forge-X Current Repo File-by-File Implementation Specification

Generated: 2026-03-19T10:34:38Z

## Purpose

This document is not a generic architecture summary. It is a **file-by-file engineering control document** for the current repo shape under `src/gdc_adk`. Its purpose is to constrain implementation so the codebase does not drift into:
- adapter-owned logic
- provider-owned orchestration
- hidden workflow state
- shallow placeholder files that “exist” but do no real work
- future incompatibility with Coherence-Base

A file is not complete because it imports or returns a demo value. A file is complete only when:
- its ownership is respected
- its required public contract exists
- its forbidden responsibilities are absent
- its interactions with upstream and downstream files are explicit
- its negative-path behavior is defined
- it passes the acceptance checks listed here

## Canonical import law

Unless explicitly justified, import flow should be:
- adapters -> workflows / control_plane / capabilities
- workflows -> control_plane / substrate / validation / memory / capabilities
- control_plane -> config / providers / memory / validation
- information_plane -> substrate / memory / control_plane activation interfaces
- providers -> config / provider base contracts
- substrate -> substrate only

Providers must never import workflows. Adapters must never own routing. Labs must never own business logic.

---

## 1. `src/gdc_adk/config/settings.py`

### Ownership
Single source of truth for reading repo-root configuration and environment accessors.

### Must contain
- repo-root anchored config loading
- provider config lookup
- routing config lookup
- weather provider config lookup
- environment-variable accessors only for true secrets or deployment overrides

### Must not contain
- provider execution
- workflow selection
- issue creation
- artifact creation
- hidden defaults that override `config.yaml` without explicit policy

### Required public functions
- `load_yaml_config()`
- `require_env(name)`
- `get_provider_config(provider_name)`
- `get_default_provider()`
- `get_failover_order()`
- `get_weather_provider_name()`
- `get_weather_provider_base_url(provider_name)`

### Completion conditions
- when called from repo root or `labs/adk`, it still resolves the same `config.yaml`
- missing config fields fail explicitly and early
- no lab `.env` is required

### Negative cases
- config missing
- malformed yaml
- provider alias unknown
- secret missing

---

## 2. `src/gdc_adk/control_plane/policy.py`

### Ownership
Policy-only decisions. This file answers what is allowed, not how it is executed.

### Must contain
- local-first policy
- deterministic-before-LLM policy
- cloud fallback eligibility by task type
- local-only task classification
- future extension point for “review must differ from author model”

### Must not contain
- direct provider imports if avoidable
- execution code
- cache storage logic
- artifact store logic

### Required public functions
- `should_use_local(task_type)`
- `allow_cloud(task_type)`
- future: `requires_independent_review(task_type)`

### Completion conditions
- time/weather/retrieval can be forced local or deterministic
- cloud use is impossible unless policy returns true

---

## 3. `src/gdc_adk/control_plane/router.py`

### Ownership
Task-to-provider selection and failover-chain construction.

### Must contain
- primary provider selection by task type
- local-first failover ordering
- task-aware provider chain construction

### Must not contain
- provider request execution
- prompt assembly
- cache writes
- workflow state

### Required public functions
- `select_provider(task_type)`
- `get_failover_chain(task_type)`

### Completion conditions
- deterministic capability tasks do not route to remote by default
- local tasks prefer `ollama` / `llamacpp`
- if config order is `ollama -> google`, chain respects that

---

## 4. `src/gdc_adk/control_plane/optimizer.py`

### Ownership
Reuse and budget policy, not storage itself.

### Must contain
- cacheability decision by task type
- stable cache key construction
- future hook points for context budget policy and block ranking

### Must not contain
- actual memory store implementation
- provider invocation

### Required public functions
- `reuse_allowed(task_type)`
- `cache_key_for(task_type, payload)`

### Completion conditions
- repeated deterministic/local questions can reuse cached results safely
- cache key normalization is stable across whitespace and case where policy allows

---

## 5. `src/gdc_adk/control_plane/model_registry.py`

### Ownership
Model alias resolution only.

### Must contain
- alias -> configured model lookup
- no hidden fallback model names

### Must not contain
- direct network calls
- provider routing
- adapter-specific assumptions

### Required public functions
- `resolve_adk_model_name(model_alias)`

### Completion conditions
- failure is explicit for unknown alias
- no model literal is hardcoded in adapters

---

## 6. `src/gdc_adk/runtime/local_model_manager.py`

### Ownership
Local model lifecycle state.

### Must contain
- active local model tracking
- future hooks for warm/unload/cooldown
- future serialization or lock semantics

### Must not contain
- workflow meaning
- provider routing

### Required public functions
- `get_active_model()`
- `set_active_model(model_name)`
- `clear_active_model()`

### Completion conditions
- local execution can tell which model is active
- manager remains provider-agnostic

---

## 7. `src/gdc_adk/providers/base.py`

### Ownership
Canonical request/response and provider interface.

### Must contain
- typed request object
- typed response object
- provider interface contract

### Must not contain
- provider-specific code
- workflow semantics

### Required objects
- `LLMRequest`
- `LLMResponse`
- `LLMProvider`

### Completion conditions
- all providers return a uniform `LLMResponse`
- upstream code never has to parse provider-specific raw shapes to get text/provider/model

---

## 8. `src/gdc_adk/providers/ollama_provider.py`

### Ownership
Ollama backend adapter.

### Must contain
- config-based model/base_url loading
- availability check
- generate request against Ollama API
- stable response mapping

### Must not contain
- task selection
- cloud fallback decisions
- issue creation

### Completion conditions
- local model availability can be checked cheaply
- timeout and request failure raise explicit, actionable errors
- response text/provider/model are always populated when successful

### Negative cases
- Ollama down
- model missing
- bad base_url
- non-200 API response

---

## 9. `src/gdc_adk/providers/google_provider.py`

### Ownership
Google provider adapter, optional fallback path.

### Must contain
- secret-based client initialization
- config-based model lookup
- stable `LLMResponse` mapping

### Must not contain
- default-orchestration logic
- local-first override logic

### Completion conditions
- cloud call only happens when upstream policy allows it
- provider remains swappable and thin

---

## 10. `src/gdc_adk/providers/router.py`

### Ownership
Provider execution wrapper.

### Must contain
- provider instance resolution
- failover execution
- task execution entry point that uses control-plane routing

### Must not contain
- workflow state
- artifact creation
- hidden policy

### Required public functions
- `get_llm_client(provider)`
- `generate_with_failover(req, order)`
- `execute_task(task_type, req)`

### Completion conditions
- all provider failures are accumulated and surfaced
- failover order follows control-plane output, not provider preference

---

## 11. `src/gdc_adk/providers/weather/base.py`
Defines weather provider contract.

### Required public objects
- `WeatherProvider` interface with `get_weather(city)`

### Must not contain
- hardcoded demo weather
- city registry logic

---

## 12. `src/gdc_adk/providers/weather/open_meteo.py`

### Ownership
Real weather provider integration.

### Must contain
- city resolution input to lat/long
- request to Open-Meteo
- normalized weather result

### Must not contain
- manual weather registry stubs
- routing policy

### Completion conditions
- supported city query returns structured weather
- unknown city fails explicitly
- provider/network failures are surfaced cleanly

---

## 13. `src/gdc_adk/providers/weather/router.py`

### Ownership
Weather provider selection.

### Must contain
- active weather provider selection from config

### Completion conditions
- weather capability never hardcodes provider name outside config or policy layer

---

## 14. `src/gdc_adk/capabilities/geo.py`

### Ownership
Canonical city/geo lookup support.

### Must contain
- normalization of place names
- scalable registry or alias lookup
- candidate lookup support where ambiguity exists

### Must not contain
- model calls
- hardcoded toy city lists if avoidable

### Completion conditions
- supports broad city coverage
- “San Jose, CA” style alias work can be improved through canonicalization, not ad hoc one-offs

---

## 15. `src/gdc_adk/capabilities/time.py`

### Ownership
Deterministic time lookup capability.

### Must contain
- current time by city using timezone mapping
- local system time capability
- supported-city introspection if applicable

### Must not contain
- cloud model dependency for simple time lookups

### Completion conditions
- time lookup works without LLM reasoning when city is resolvable
- ambiguous/unknown city returns explicit guidance, not hallucinated answer

---

## 16. `src/gdc_adk/capabilities/weather.py`

### Ownership
Thin capability wrapper for weather.

### Must contain
- call to configured weather provider only

### Must not contain
- embedded provider URL
- mock weather registry
- routing logic

---

## 17. `src/gdc_adk/information_plane/ingestion/document_ingestor.py`

### Ownership
Raw ingress conversion into a canonical raw signal envelope.

### Must contain
- ingestion of at least text input now
- extensible pattern for docs, email, transcripts later

### Completion conditions
- every input produces a typed raw signal
- source is preserved

---

## 18. `src/gdc_adk/information_plane/normalization/canonicalizer.py`

### Ownership
Canonical normalization.

### Must contain
- canonical text extraction
- normalized type
- source retention

### Completion conditions
- downstream activation receives normalized text, not raw ad hoc input

---

## 19. `src/gdc_adk/information_plane/indexing/artifact_index.py`

### Ownership
Temporary operational index.

### Must contain
- add/search
- predictable matching semantics
- replaceable implementation later

### Must not contain
- hidden coupling to one workflow

---

## 20. `src/gdc_adk/information_plane/activation/trigger_router.py`

### Ownership
Signal classification to workflow mode.

### Must contain
- explicit classification heuristics or rules
- fix_flow / research_flow / code_flow / world_flow / single_run mapping

### Must not contain
- provider execution
- workflow state mutation beyond activation output

### Completion conditions
- “bug/fix/error” activates fix_flow
- research/spec requests do not collapse into single_run by default if configured keywords exist

---

## 21. `src/gdc_adk/information_plane/activation/workflow_activation.py`

### Ownership
Convert normalized input into artifact + activation + issue seed.

### Must contain
- artifact creation
- activation routing
- conditional issue creation
- event spine recording

### Completion conditions
- a fix-like user signal creates both artifact and issue
- single_run still creates an artifact and event

---

## 22. `src/gdc_adk/information_plane/egress/artifact_emitter.py`

### Ownership
Typed egress envelope.

### Completion conditions
- responses or outputs are wrapped in a structured emission envelope, even if simple today

---

## 23. `src/gdc_adk/substrate/event_spine.py`

### Ownership
Append-only event recording semantics.

### Completion conditions
- major transitions are recorded
- correlation can be added later without redesign

---

## 24. `src/gdc_adk/substrate/artifact_store.py`

### Ownership
Artifact creation and storage semantics.

### Completion conditions
- every meaningful request or output can become an artifact
- artifact IDs are stable and unique

---

## 25. `src/gdc_adk/substrate/issue_tracker.py`

### Ownership
Issue creation and lifecycle baseline.

### Completion conditions
- issues have IDs, severity, status, linkage
- reopen/close lifecycle can be added without contract break

---

## 26. `src/gdc_adk/substrate/dispatch_system.py`

### Ownership
Canonical entry point from user signal to workflow mode and response.

### Must contain
- process input
- branch to single_run or workflow mode
- local-first execution path for single_run

### Completion conditions
- fix_flow requests create issues
- single_run dispatch goes through local-first task execution path

---

## 27. `src/gdc_adk/memory/contracts.py`

### Ownership
Future-stable interfaces for operational memory.

### Completion conditions
- cache, context, and continuity interfaces exist
- later Coherence-Base implementation can conform without upstream rewrite

---

## 28. `src/gdc_adk/memory/cache.py`

### Ownership
Temporary operational cache.

### Completion conditions
- deterministic/local-safe results can be cached
- cache behavior is replaceable later

---

## 29. `src/gdc_adk/memory/context_store.py`

### Ownership
Reusable context blocks.

### Completion conditions
- context blocks are explicit objects or dictionaries, not hidden prompt fragments

---

## 30. `src/gdc_adk/memory/continuity.py`

### Ownership
Workflow/session snapshots.

### Completion conditions
- iterative flows can persist explicit state snapshot
- snapshots are serializable

---

## 31. `src/gdc_adk/workflows/engine.py`

### Ownership
Canonical workflow execution helpers.

### Must contain
- local-first ask function
- future workflow-run state machine helpers

### Must not contain
- direct provider policy logic duplicated from control plane

### Completion conditions
- cache-aware local-first request execution works
- file is ready to host explicit workflow-run orchestration next

---

## 32. `src/gdc_adk/adapters/adk/*.py`

### Ownership
Thin adapter only.

### Completion conditions
- adapters only instantiate or bridge to Forge-X core
- no hidden business logic
- no hardcoded providers or models outside config alias usage

---

## 33. `labs/adk/*/agent.py`

### Ownership
Class/lab surface only.

### Completion conditions
- each file is a thin wrapper around adapter build function
- if deleted, Forge-X core still makes sense
