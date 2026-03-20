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

A requirement is incomplete if any column is Ã¢â‚¬Å“unknownÃ¢â‚¬Â without an explicit rationale.

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
| FX-R011 | Review findings as first-class objects | Reviews must generate structured findings, not prose only. | validation | `src/gdc_adk/validation/validator.py`, `src/gdc_adk/validation/drift_checker.py`, `src/gdc_adk/validation/traceability_auditor.py`, `src/gdc_adk/validation/grounding_checker.py` | artifacts, workflow state, Stage 3 activation outputs | workflows, closure logic, future continuity | `ReviewFinding`, `ValidationResult`, `RequirementCoverageResult`, `TraceabilityAuditResult` | single_run, iterative, fix_flow, dynamic_flow, fuzzy_logical_flow | `tests/test_stage4.py` Scenario B, D, and E; finding lifecycle tests; drift/traceability/grounding tests | structured finding lifecycle history; source-linked evidence; traceability audit result | validation_gap | accepted |
| FX-R012 | Workflow state machine | Workflow execution must have explicit states and transitions. | workflows | `src/gdc_adk/workflows/engine.py`, `src/gdc_adk/workflows/state_machine.py`, `src/gdc_adk/workflows/fix_flow.py`, `src/gdc_adk/workflows/iterative_flow.py` | Stage 3 activation outputs, issues, findings | adapters, observability, future continuity | `WorkflowRun`, `WorkflowHistoryEntry`, `WorkflowExecutionResult`, `FixFlowResult`, `VerificationResult`, `IterativeFlowResult`, `RevisionDelta` | single_run, iterative, fix_flow, dynamic_flow, fuzzy_logical_flow | `tests/test_stage4.py` Scenario A, B, C, and E; state transition tests; fix-flow verification tests; iterative lineage tests | workflow state history; transition rationale; issue/finding/artifact linkage in structured state | architecture_drift | accepted |
| FX-R013 | Context assembly under budget | Context must be assembled selectively, not dumped into prompts. | control_plane/memory | future `context_assembler.py`, memory files | artifacts, issues, continuity | providers, workflows | ContextBlock contract | iterative, research_flow, code_flow, world_flow | context budget tests | context selection metrics | traceability_gap | not_started |
| FX-R014 | Multi-agent typed handoffs | Multi-agent execution must use typed artifacts and bounded roles. | workflows/validation | future orchestration files | WorkflowRun, artifacts, findings | advanced workflows | handoff artifact contract | dynamic_flow, fuzzy_logical_flow | planner/executor/reviewer golden test | role handoff trace | contract_violation | not_started |
| FX-R015 | Observability and replay | Every important run must be reconstructible from events/artifacts/issues/snapshots. | substrate/runtime/validation | event_spine, artifact_store, issue_tracker, memory | all above | operations, CI, review | replay contract | all | replay scenario tests | complete structured logs | replayability_gap | not_started |

---

## 3. How to use the matrix

For every requested implementation change:
1. identify the requirement row(s) affected
2. confirm the owning subsystem and files
3. update completion status only after acceptance tests pass
4. create review findings if an implementation partially satisfies a row but leaves gaps

Do not treat Ã¢â‚¬Å“compiles successfullyÃ¢â‚¬Â or Ã¢â‚¬Å“demo worked onceÃ¢â‚¬Â as enough to mark a row complete.

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

## Completion Evidence Updates

### FX-R007
- status: accepted
- files: `src/gdc_adk/core/state.py`, `src/gdc_adk/substrate/artifact_store.py`, `src/gdc_adk/substrate/dispatch_system.py`, `tests/test_stage1.py`
- evidence: `tests/test_stage1.py` proves request artifact creation, workflow linkage, export/reset/load replay behavior, invalid and duplicate load rejection, and fix-flow linkage behavior.
- notes: explicit lifecycle APIs and artifact/workflow linkage verified.

### FX-R008
- status: accepted
- files: `src/gdc_adk/substrate/artifact_store.py`, `src/gdc_adk/substrate/dispatch_system.py`, `src/gdc_adk/substrate/issue_tracker.py`, `tests/test_stage1.py`, `src/gdc_adk/information_plane/activation/trigger_router.py`, `src/gdc_adk/information_plane/activation/workflow_activation.py`, `tests/test_stage3.py`
- evidence: Stage 1 proves typed issue creation with bidirectional artifact/issue linkage and lookup by issue id. Stage 3 proves deterministic fix-like activation metadata, issue-candidate classification, fix-flow selection, and downstream trigger readiness.
- notes: accepted by combined Stage 1 + Stage 3 evidence.

### FX-R009
- status: accepted
- files: `src/gdc_adk/substrate/dispatch_system.py`, `tests/test_stage1.py`
- evidence: `tests/test_stage1.py` proves structured workflow creation, event emission order, unsupported workflow-hint rejection, and workflow-run lifecycle behavior.
- notes: typed public dispatch entry and Stage 1 workflow-mode enforcement verified.

### FX-R001
- status: accepted
- files: `src/gdc_adk/config/settings.py`, `tests/test_stage2.py`
- evidence: `tests/test_stage2.py` proves typed settings loading and Stage 2 config surfaces.
- notes: hidden singleton cache behavior removed.

### FX-R002
- status: accepted
- files: `src/gdc_adk/control_plane/router.py`, `src/gdc_adk/runtime/local_model_manager.py`, `src/gdc_adk/providers/router.py`, `tests/test_stage2.py`
- evidence: `tests/test_stage2.py` proves deterministic-before-LLM routing, configured failover-order behavior, all-provider-fail path, no-provider-available rejection, and Stage 1 -> Stage 2 subsystem-boundary proof.
- notes: accepted.

### FX-R003
- status: accepted
- files: `src/gdc_adk/providers/base.py`, `src/gdc_adk/providers/ollama_provider.py`, `src/gdc_adk/providers/google_provider.py`, `src/gdc_adk/providers/weather/base.py`, `src/gdc_adk/providers/weather/open_meteo.py`, `tests/test_stage2.py`
- evidence: `tests/test_stage2.py` proves provider contract validation, weather provider failure and empty-payload handling, and clean capability -> provider abstraction for weather flow.
- notes: accepted.

### FX-R004
- status: accepted
- files: `src/gdc_adk/capabilities/geo.py`, `src/gdc_adk/capabilities/time.py`, `src/gdc_adk/capabilities/weather.py`, `tests/test_stage2.py`
- evidence: `tests/test_stage2.py` proves deterministic capability selection before reasoning paths, typed public capability contracts, and negative-path rejection behavior.
- notes: accepted.

### FX-R005
- status: accepted
- files: `src/gdc_adk/capabilities/weather.py`, `src/gdc_adk/providers/weather/base.py`, `src/gdc_adk/providers/weather/open_meteo.py`, `src/gdc_adk/control_plane/router.py`, `tests/test_stage2.py`
- evidence: `tests/test_stage2.py` proves capability-owned city normalization, provider transport/translation only, configured routing/failover behavior, weather failure handling, and empty-payload rejection.
- notes: accepted.

### FX-R006
- status: accepted
- files: `src/gdc_adk/information_plane/ingestion/document_ingestor.py`, `src/gdc_adk/information_plane/normalization/canonicalizer.py`, `src/gdc_adk/information_plane/indexing/artifact_index.py`, `src/gdc_adk/information_plane/activation/workflow_activation.py`, `tests/test_stage3.py`
- evidence: `tests/test_stage3.py` proves ingestion -> canonicalization -> indexing -> activation ordering, Stage 2 -> Stage 3 boundary intake, Stage 3 -> Stage 2 forward-boundary proof, and replay/load negative paths.
- notes: accepted.

### FX-R010
- status: accepted
- files: `src/gdc_adk/memory/contracts.py`, `src/gdc_adk/memory/cache.py`, `src/gdc_adk/memory/context_store.py`, `src/gdc_adk/memory/continuity.py`, `src/gdc_adk/memory/replay.py`, `tests/test_stage5.py`
- evidence: `tests/test_stage5.py` proves typed cache/context records, continuity snapshot create/export/resume/rehydrate behavior, replay export/validate/rehydrate behavior, invalid input rejection, Stage 4 -> Stage 5 boundary proof, Stage 5 -> Stage 6 forward-boundary contract proof, and replay negative paths.
- notes: accepted.

### FX-R011
- status: accepted
- files: `src/gdc_adk/validation/validator.py`, `src/gdc_adk/validation/drift_checker.py`, `src/gdc_adk/validation/traceability_auditor.py`, `src/gdc_adk/validation/grounding_checker.py`, `tests/test_stage4.py`
- evidence: `tests/test_stage4.py` proves finding lifecycle behavior, structured validation outputs, drift/traceability/grounding checks, Stage 3 -> Stage 4 boundary proof, and Stage 4 -> Stage 5 forward-boundary contract readiness proof.
- notes: accepted.

### FX-R012
- status: accepted
- files: `src/gdc_adk/workflows/engine.py`, `src/gdc_adk/workflows/state_machine.py`, `src/gdc_adk/workflows/fix_flow.py`, `src/gdc_adk/workflows/iterative_flow.py`, `tests/test_stage4.py`
- evidence: `tests/test_stage4.py` proves explicit state transitions, fix-flow verification and reopen behavior, iterative lineage preservation, Stage 3 -> Stage 4 boundary proof, and Stage 4 -> Stage 5 forward-boundary contract readiness proof.
- notes: accepted.
