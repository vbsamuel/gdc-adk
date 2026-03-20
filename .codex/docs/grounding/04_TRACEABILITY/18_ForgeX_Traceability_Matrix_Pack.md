# Forge-X Traceability Matrix Pack

Generated: 2026-03-19T11:03:18Z

## Purpose

This document defines the traceability control layer for Forge-X. Its purpose is to prevent scope loss, partial implementation, untracked drift, and false completion claims by forcing every meaningful requirement to map to:
- owning subsystem
- concrete files
- data contracts
- workflow mode implications
- acceptance tests
- review findings
- observability requirements

This matrix is intended to be updated as implementation progresses. The initial version below establishes the canonical mapping for the current Forge-X repo and near-term roadmap.

---

## 1. Matrix schema

Every row in the traceability matrix must include:

- `requirement_id`
- `requirement_title`
- `requirement_description`
- `owning_subsystem`
- `owning_files`
- `upstream_dependencies`
- `downstream_dependents`
- `contracts_involved`
- `workflow_modes_affected`
- `acceptance_tests`
- `observability_requirements`
- `review_findings_if_failed`
- `completion_status`

A requirement is incomplete if any column is “unknown” without an explicit rationale.

---

## 2. Traceability matrix

| requirement_id | requirement_title | requirement_description | owning_subsystem | owning_files | upstream_dependencies | downstream_dependents | contracts_involved | workflow_modes_affected | acceptance_tests | observability_requirements | review_findings_if_failed | completion_status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| FX-R001 | Repo-root config resolution | Configuration must resolve identically from repo root and labs without lab-local config drift. | config | `src/gdc_adk/config/settings.py` | repo root config files | providers, control_plane, adapters | provider config contract, routing config contract | all | config resolution tests; bad config negative tests | config load event/log; config source path attribution | constitution violation, provider config gap | in_progress |
| FX-R002 | Local-first provider routing | Control plane must choose deterministic/local paths before cloud. | control_plane | `control_plane/policy.py`, `control_plane/router.py`, `providers/router.py` | config routing values | workflows, adapters | task_type -> provider selection contract | all | deterministic-first tests; failover tests | provider_selected event; provider_failed event | provider_policy_violation | in_progress |
| FX-R003 | Uniform provider request/response | All providers must expose a uniform request/response contract. | providers | `providers/base.py`, provider files | config, env | control_plane, workflows | `LLMRequest`, `LLMResponse` | all LLM-backed modes | provider contract serialization tests | provider invocation metadata | contract_violation | in_progress |
| FX-R004 | Deterministic time capability | Time lookup must not require generative reasoning when city is resolvable. | capabilities | `capabilities/time.py`, `capabilities/geo.py` | geo resolution, timezone lookup | dispatch, workflows | time capability contract | single_run, iterative | time lookup golden test | capability invocation trace | validation_gap | partial |
| FX-R005 | Weather capability via provider contract | Weather must route through weather provider abstraction, not hardcoded registry. | capabilities/providers | `capabilities/weather.py`, `providers/weather/*` | weather provider config, geo resolution | workflows, adapters | weather provider contract | single_run, iterative | weather provider tests; unknown city tests | provider invocation trace | contract_violation | partial |
| FX-R006 | Canonical ingestion path | All raw text inputs must become canonical normalized signals before activation. | information_plane | `ingestion/document_ingestor.py`, `normalization/canonicalizer.py` | none | activation, substrate | normalized signal contract | all | ingestion-normalization tests | signal_ingested, signal_normalized events | traceability_gap | in_progress |
| FX-R007 | Artifact creation for meaningful inputs | Every meaningful input must create an artifact. | substrate | `artifact_store.py`, `workflow_activation.py` | normalized signal | issues, workflows, validation | Artifact contract | all | artifact lineage tests | artifact_created event | replayability_gap | in_progress |
| FX-R008 | Fix-flow issue creation | Bug/fix signals must create a typed issue and bind it to artifacts. | substrate/information_plane | `issue_tracker.py`, `trigger_router.py`, `workflow_activation.py` | normalized signal, artifact creation | workflows, review | Issue contract | fix_flow | fix-flow golden test | issue_created event | validation_gap | in_progress |
| FX-R009 | Dispatch entry point | Dispatch must convert user input into structured activation and execution, not ad hoc chat handling. | substrate | `dispatch_system.py` | ingestion, activation, workflows | adapters, future API | Dispatch request/response contract | all | dispatch E2E tests | request_received, workflow_started events | architecture_drift | in_progress |
| FX-R010 | Operational memory replaceability | Cache/context/continuity must be useful now but replaceable later by Coherence-Base. | memory | `contracts.py`, `cache.py`, `context_store.py`, `continuity.py` | object contracts | workflows, context assembler | MemoryStore, ContextStore, ContinuityStore | iterative, fix_flow, dynamic_flow, fuzzy_logical_flow | continuity snapshot tests; replay export tests | snapshot create/load trace | replayability_gap | partial |
| FX-R011 | Review findings as first-class objects | Reviews must generate structured findings, not prose only. | validation | future validation files | artifacts, issues | workflows, closure logic | ReviewFinding contract | iterative, fix_flow, research_flow, code_flow, world_flow | finding lifecycle tests | finding_created event | validation_gap | not_started |
| FX-R012 | Workflow state machine | Workflow execution must have explicit states and transitions. | workflows | `workflows/engine.py`, future state machine files | dispatch, issues, findings | adapters, observability | WorkflowRun contract | all non-trivial modes | state transition tests | workflow_transitioned event | architecture_drift | not_started |
| FX-R013 | Context assembly under budget | Context must be assembled selectively, not dumped into prompts. | control_plane/memory | future `context_assembler.py`, memory files | artifacts, issues, continuity | providers, workflows | ContextBlock contract | iterative, research_flow, code_flow, world_flow | context budget tests | context selection metrics | traceability_gap | not_started |
| FX-R014 | Multi-agent typed handoffs | Multi-agent execution must use typed artifacts and bounded roles. | workflows/validation | future orchestration files | WorkflowRun, artifacts, findings | advanced workflows | handoff artifact contract | dynamic_flow, fuzzy_logical_flow | planner/executor/reviewer golden test | role handoff trace | contract_violation | not_started |
| FX-R015 | Observability and replay | Every important run must be reconstructible from events/artifacts/issues/snapshots. | substrate/runtime/validation | event_spine, artifact_store, issue_tracker, memory | all above | operations, CI, review | replay contract | all | replay scenario tests | complete structured logs | replayability_gap | not_started |

| requirement_id | current_status | files_touched | contracts_affected | workflow_modes_affected | acceptance_scenarios_covered | proving_tests_or_behavioral_evidence | remaining_gaps_if_any | recommended_row_disposition |
|---|---|---|---|---|---|---|---|---|
| FX-R001 | accepted_with_findings | `src/gdc_adk/config/settings.py`, `tests/test_stage2.py` | `ProviderSettings`, `RoutingSettings`, `RuntimeSettings`, `WeatherProviderSettings`, `Stage2Settings` | `single_run`, `iterative` | typed Stage 2 config loading; local-first routing prerequisites | [test_stage2.py](/Users/bruno/projects/gdc-adk/tests/test_stage2.py#L48) proves typed Stage 2 settings load successfully from repo config; [settings.py](/Users/bruno/projects/gdc-adk/src/gdc_adk/config/settings.py) now loads Stage 2 settings without hidden cache reuse | Canonical traceability matrix still needs this evidence recorded | accepted_with_findings |
| FX-R002 | accepted_with_findings | `src/gdc_adk/control_plane/policy.py`, `src/gdc_adk/control_plane/router.py`, `src/gdc_adk/control_plane/model_registry.py`, `src/gdc_adk/control_plane/gate_evaluator.py`, `tests/test_stage2.py` | `RoutingPolicyRequest`, `RoutingPolicyDecision`, `RouteRequest`, `RouteDecision`, provider gate result contracts | `single_run`, `iterative` | deterministic-before-LLM routing; local-first reasoning; cloud fallback gating; configured failover order; Stage 1 ↔ Stage 2 boundary compatibility | [test_stage2.py](/Users/bruno/projects/gdc-adk/tests/test_stage2.py#L55) proves deterministic capability routing occurs before provider reasoning; [test_stage2.py](/Users/bruno/projects/gdc-adk/tests/test_stage2.py#L66) proves local-first routing; [test_stage2.py](/Users/bruno/projects/gdc-adk/tests/test_stage2.py#L73) proves cloud fallback only when allowed; [test_stage2.py](/Users/bruno/projects/gdc-adk/tests/test_stage2.py#L80) proves configured failover order is honored; [test_stage2.py](/Users/bruno/projects/gdc-adk/tests/test_stage2.py#L203) proves no-provider-available rejection; [test_stage2.py](/Users/bruno/projects/gdc-adk/tests/test_stage2.py#L247) proves the Stage 1 substrate request artifact contract feeds a valid Stage 2 routing decision and includes a negative rejection path | Canonical traceability matrix still needs this evidence recorded | accepted_with_findings |
| FX-R003 | accepted_with_findings | `src/gdc_adk/providers/base.py`, `src/gdc_adk/providers/ollama_provider.py`, `src/gdc_adk/providers/google_provider.py`, `src/gdc_adk/providers/router.py`, `tests/test_stage2.py` | `LLMRequest`, `LLMResponse`, `LLMProvider`, provider contract and transport exceptions | `single_run`, `iterative` | typed provider contracts; provider failover; invalid provider input rejection; Stage 1 ↔ Stage 2 boundary compatibility through routing/provider decision path | [test_stage2.py](/Users/bruno/projects/gdc-adk/tests/test_stage2.py#L86) proves provider failover behavior; [test_stage2.py](/Users/bruno/projects/gdc-adk/tests/test_stage2.py#L127) proves all-provider-fail raises explicit transport failure; [test_stage2.py](/Users/bruno/projects/gdc-adk/tests/test_stage2.py#L145) proves invalid provider request input is rejected; [test_stage2.py](/Users/bruno/projects/gdc-adk/tests/test_stage2.py#L247) provides the bounded Stage 1 ↔ Stage 2 routing/provider boundary proof | Canonical traceability matrix still needs this evidence recorded | accepted_with_findings |
| FX-R004 | accepted_with_findings | `src/gdc_adk/capabilities/geo.py`, `src/gdc_adk/capabilities/time.py`, `src/gdc_adk/control_plane/policy.py`, `src/gdc_adk/control_plane/router.py`, `tests/test_stage2.py` | `CityRecord`, resolved location contract, `TimeLookupResult`, `SupportedTimeCitiesResult`, routing policy contracts | `single_run`, `iterative` | deterministic time lookup routing; deterministic supported-city time response | [test_stage2.py](/Users/bruno/projects/gdc-adk/tests/test_stage2.py#L55) proves `time_lookup` selects the deterministic capability path before provider reasoning; [test_stage2.py](/Users/bruno/projects/gdc-adk/tests/test_stage2.py#L233) proves the time capability returns a successful deterministic result for a supported city | Canonical traceability matrix still needs this evidence recorded | accepted_with_findings |
| FX-R005 | accepted_with_findings | `src/gdc_adk/providers/weather/base.py`, `src/gdc_adk/providers/weather/open_meteo.py`, `src/gdc_adk/providers/weather/router.py`, `src/gdc_adk/capabilities/geo.py`, `src/gdc_adk/capabilities/weather.py`, `tests/test_stage2.py` | `WeatherProviderRequest`, `WeatherProviderResponse`, `WeatherProvider`, resolved location contract | `single_run`, `iterative` | weather capability -> provider abstraction; provider transport failure handling; unknown-city rejection; empty weather payload handling | [test_stage2.py](/Users/bruno/projects/gdc-adk/tests/test_stage2.py#L152) proves weather routing goes through the capability and passes normalized provider-facing location data; [test_stage2.py](/Users/bruno/projects/gdc-adk/tests/test_stage2.py#L174) proves invalid weather provider input is rejected; [test_stage2.py](/Users/bruno/projects/gdc-adk/tests/test_stage2.py#L181) proves unknown-city rejection occurs in the capability layer; [test_stage2.py](/Users/bruno/projects/gdc-adk/tests/test_stage2.py#L187) proves weather provider failure is surfaced; [test_stage2.py](/Users/bruno/projects/gdc-adk/tests/test_stage2.py#L195) proves empty weather payload failure is surfaced; [test_stage2.py](/Users/bruno/projects/gdc-adk/tests/test_stage2.py#L239) proves the provider module no longer resolves cities directly | Canonical traceability matrix still needs this evidence recorded | accepted_with_findings |



---

## 3. How to use the matrix

For every requested implementation change:
1. identify the requirement row(s) affected
2. confirm the owning subsystem and files
3. update completion status only after acceptance tests pass
4. create review findings if an implementation partially satisfies a row but leaves gaps

Do not treat “compiles successfully” or “demo worked once” as enough to mark a row complete.

---

## 4. Completion status values

Use only:
- `not_started`
- `in_progress`
- `partial`
- `accepted`
- `blocked`

Do not use vague statuses like:
- `done-ish`
- `mostly complete`
- `almost`
