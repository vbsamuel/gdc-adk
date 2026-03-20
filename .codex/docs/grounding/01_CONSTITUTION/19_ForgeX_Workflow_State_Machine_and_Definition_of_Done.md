# Forge-X Workflow State Machine and Definition of Done Pack

Generated: 2026-03-19T11:03:18Z

## Purpose

This document defines the explicit workflow state models, transition rules, stop conditions, and file-level Definitions of Done needed to prevent execution drift. It exists to stop the failure mode where a workflow is “implemented” as a prompt chain or a stateful chat habit instead of an explicit, replayable execution system.

---

## 1. Common workflow state model

All workflow runs must carry at least:

- `workflow_run_id`
- `workflow_mode`
- `current_state`
- `state_history`
- `input_artifact_ids`
- `output_artifact_ids`
- `issue_ids`
- `finding_ids`
- `created_at`
- `updated_at`

Recommended additions:
- `retry_count`
- `reopen_count`
- `owner_role`
- `pending_actions`
- `completion_reason`
- `blocked_reason`

---

## 2. Baseline states

The baseline state vocabulary is:

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

No workflow should skip directly from `received` to `completed` unless it is a trivial deterministic one-step path and the transition is still explicitly recorded.

---

## 3. Mode-specific state machines

### 3.1 single_run

#### Intended use
Bounded one-shot work where no long-horizon review loop is required.

#### Typical state path
`received -> classified -> activated -> executing -> completed`

#### Optional review path
`executing -> awaiting_review -> validated -> completed`

#### Stop conditions
- response emitted successfully
- output artifact recorded if meaningful
- no open blocking issue remains

#### Failure conditions
- provider failure with no allowed fallback
- deterministic path unavailable and no allowed reasoning path

---

### 3.2 iterative

#### Intended use
Progressive refinement where each pass is influenced by prior artifacts and findings.

#### Typical state path
`received -> classified -> activated -> planned -> executing -> awaiting_review -> revising -> executing -> validated -> completed`

#### Required invariants
- prior artifact lineage is preserved
- review findings can exist across passes
- continuity snapshot must exist between passes

#### Reopen path
`completed -> reopened -> revising`

#### Failure conditions
- revision overwrites prior artifact with no lineage
- no continuity snapshot exists
- findings are not linked to revised artifact

---

### 3.3 fix_flow

#### Intended use
Issue-driven remediation and verification.

#### Extended states
- `issue_opened`
- `remediation_in_progress`
- `verification_pending`
- `resolution_proposed`
- `resolution_verified`

#### Typical path
`received -> classified -> activated -> issue_opened -> remediation_in_progress -> verification_pending -> resolution_proposed -> resolution_verified -> completed`

#### Reopen path
`resolution_verified -> reopened -> remediation_in_progress`

#### Required invariants
- issue object must exist
- remediation evidence must link to artifact(s)
- verification result must be explicit

#### Failure conditions
- no issue created
- no verification step
- closure without evidence

---

### 3.4 dynamic_flow

#### Intended use
Adaptive multi-step execution where the plan changes based on new findings or outputs.

#### Typical path
`received -> classified -> activated -> planned -> executing -> planned -> executing -> awaiting_review -> validated -> completed`

#### Required invariants
- state transitions must explain why the plan changed
- branching must be recorded in state history
- role or tool changes must be attributable

#### Failure conditions
- ad hoc branching only in prose
- plan changes with no recorded reason

---

### 3.5 fuzzy_logical_flow

#### Intended use
Ambiguous or contradictory problems requiring staged interpretation.

#### Typical path
`received -> classified -> activated -> planned -> executing -> awaiting_review -> revising -> planned -> executing -> validated -> completed`

#### Required invariants
- hypotheses or uncertainty notes must be captured as structured artifacts or findings
- contradiction handling must not be implicit
- irreversible action requires a validation/review gate

#### Failure conditions
- ambiguity ignored
- unsupported certainty introduced
- contradictory inputs not represented in findings/issues

---

## 4. Definition of Done by current file

### `config/settings.py`
Done only when:
- config resolves from repo root and labs consistently
- provider, routing, and weather config accessors are stable
- missing config/secret paths fail explicitly
- no business logic exists here

### `control_plane/policy.py`
Done only when:
- deterministic-before-LLM eligibility is expressible
- local-first/cloud-fallback rules are explicit
- task types like time/weather/retrieval can be constrained

### `control_plane/router.py`
Done only when:
- provider selection is task-aware
- failover chain is local-first
- no provider-specific or adapter-specific leakage exists

### `control_plane/optimizer.py`
Done only when:
- cacheability and stable cache key generation are defined
- no storage logic is embedded

### `providers/base.py`
Done only when:
- request and response contracts are uniform and typed
- upstream code can use all providers through one response contract

### `providers/ollama_provider.py`
Done only when:
- model/base_url load from config
- availability checks are explicit
- failures surface clearly
- response is normalized

### `providers/google_provider.py`
Done only when:
- used only as fallback path under policy
- config/env load is explicit
- response is normalized

### `providers/router.py`
Done only when:
- task execution follows control-plane selection
- failover preserves error chain
- provider internals remain isolated

### `capabilities/geo.py`
Done only when:
- city/geo normalization is broad enough to avoid toy behavior
- alias handling is structured
- no hardcoded toy-only registry dominates

### `capabilities/time.py`
Done only when:
- city time lookup works deterministically
- unknown city path is explicit and non-hallucinatory
- local system time path exists if intended

### `capabilities/weather.py`
Done only when:
- capability is a thin wrapper around configured weather provider
- no mock/stub weather is embedded in production path

### `information_plane/ingestion/document_ingestor.py`
Done only when:
- raw signals become typed ingress records
- source is preserved

### `information_plane/normalization/canonicalizer.py`
Done only when:
- normalized signal shape is stable
- text/source/type are explicit

### `information_plane/indexing/artifact_index.py`
Done only when:
- artifacts can be indexed and searched predictably
- implementation remains swappable later

### `information_plane/activation/trigger_router.py`
Done only when:
- workflow classification is explicit and testable
- fix_flow/research_flow/code_flow/world_flow/single_run are not collapsed unintentionally

### `information_plane/activation/workflow_activation.py`
Done only when:
- normalized input produces artifact + activation output
- fix-like signals create issues where appropriate
- events are recorded

### `substrate/artifact_store.py`
Done only when:
- meaningful artifacts can be created with lineage-ready fields
- IDs are stable and unique

### `substrate/issue_tracker.py`
Done only when:
- issues can be created with typed status/severity/linkage
- reopen/close evolution is future-compatible

### `substrate/event_spine.py`
Done only when:
- major state transitions can be appended and listed
- event shape is replay-friendly

### `substrate/dispatch_system.py`
Done only when:
- dispatch is the structured entry point
- single_run can go through local-first path
- fix_flow creates issues

### `memory/contracts.py`
Done only when:
- cache, context, continuity interfaces exist and are future-replaceable

### `memory/cache.py`
Done only when:
- safe reuse paths are functional
- implementation remains replaceable

### `memory/context_store.py`
Done only when:
- reusable context blocks are explicit, not hidden prompt text

### `memory/continuity.py`
Done only when:
- workflow/session snapshots are serializable and retrievable

### `workflows/engine.py`
Done only when:
- local-first ask path exists
- file is ready to host explicit state-machine execution without redesign

### `adapters/adk/*`
Done only when:
- thin wrappers only
- no embedded business logic

### `labs/adk/*/agent.py`
Done only when:
- imports thin adapter builder only
- deleting labs would not invalidate core architecture

---

## 5. Cross-workflow stop conditions

Stop execution and mark `failed` or `blocked` when:
- no provider is available for an allowed path
- required artifact or issue linkage cannot be created
- workflow state cannot be serialized
- review findings indicate constitution or contract violation
- cloud fallback is required but forbidden by policy

---

## 6. Reopen rules

A workflow may reopen when:
- validation fails after provisional completion
- new finding invalidates prior closure
- new artifact evidence contradicts earlier conclusion

Reopen must:
- preserve prior state history
- increment reopen count
- create event
- keep issue/finding linkage intact
