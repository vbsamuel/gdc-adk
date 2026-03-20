
# Forge-X Corrected Implementable PowerShell Build Pack

## Purpose

This document is the corrected implementation-control artifact for bootstrapping Forge-X in PowerShell terminal without drift.

It replaces the earlier scaffold-only answer with a control-grade plan that is directly aligned to:
- system identity
- repo constitution
- roadmap order
- data contracts
- workflow state rules
- acceptance scenarios
- traceability mapping
- anti-drift protocol
- pre-merge enforcement

This document is intentionally implementation-oriented. It is not a high-level architecture summary.

---

## Binding rules before any terminal work

Before creating or editing any file, enforce all of the following:

1. Forge-X is a local-first coworker engine, not a chat wrapper, not a cloud-first orchestrator, and not a prompt-only loop.
2. The architecture must support five workflow modes as architecture-level modes:
   - `single_run`
   - `iterative`
   - `fix_flow`
   - `dynamic_flow`
   - `fuzzy_logical_flow`
3. The architecture must preserve future compatibility with Coherence-Base by ensuring:
   - stable contracts
   - serializable state
   - replayable continuity
   - no critical hidden chat state
4. The repo constitution is binding:
   - adapters stay thin
   - labs stay thin
   - providers do not select themselves
   - workflows own workflow semantics
   - validation owns findings and drift checks
5. The roadmap order is mandatory:
   - Stage 1: contracts and substrate
   - Stage 2: control plane and providers
   - Stage 3: information plane
   - Stage 4: workflow engine and review spine
   - Stage 5: memory contracts and operational memory
   - Stage 6: multi-agent orchestration
6. Stop-ship failures are binding:
   - cloud-first routing
   - adapter-owned business logic
   - workflow state only in prose or chat
   - no issue object in `fix_flow`
   - no finding object in review
   - hidden non-replayable memory
   - repo constitution violations

---

## Mandatory answer and work protocol

Use this protocol every time you implement or review anything:

1. Identify the owning subsystem.
2. Identify the affected files.
3. Identify the relevant contracts.
4. State which workflow modes are affected.
5. State whether the path is deterministic, local-first LLM, or cloud fallback.
6. State review, issue, and continuity implications.
7. State requirement IDs affected.
8. State acceptance scenarios and gates affected.
9. Only then perform the implementation steps.

Do not introduce new architecture.
Do not hide logic in adapters or labs.
Do not default to cloud or LLM-first behavior.
Do not treat placeholder files as completion.

---

## Scope of this bootstrap pack

This pack covers:
- canonical repo shape
- root config and package bootstrap
- Stage 1 through Stage 5 file creation order
- required file contents at responsibility level
- PowerShell commands
- stage gates
- test scaffolding
- enforcement scaffolding
- traceability mapping for the bootstrap itself

This pack does not claim Stage 1 through Stage 5 are complete merely because files are created.
This pack only defines the correct, controlled implementation path.

---

## Requirement IDs advanced by this pack

This bootstrap pack directly advances these requirement rows:

- `FX-R001` Repo-root config resolution
- `FX-R002` Local-first provider routing
- `FX-R003` Uniform provider request/response
- `FX-R004` Deterministic time capability
- `FX-R005` Weather capability via provider contract
- `FX-R006` Canonical ingestion path
- `FX-R007` Typed artifact store
- `FX-R008` Typed issue tracking
- `FX-R009` Explicit workflow dispatch entry
- `FX-R010` Replayable operational memory

These requirement rows are not accepted by this document alone.
They move from `not_started` toward `in_progress` or `partial` depending on actual implementation state.

---

## Owning subsystems and affected files for this pack

### Owning subsystems
- `config`
- `substrate`
- `control_plane`
- `runtime`
- `providers`
- `capabilities`
- `information_plane`
- `workflows`
- `validation`
- `memory`
- `adapters`
- `labs`

### Affected files created by this pack

#### Root
- `config.yaml`
- `.env`
- `pyproject.toml`
- `.gitignore`
- `README.md`

#### Config
- `src/gdc_adk/config/settings.py`

#### Core
- `src/gdc_adk/core/contracts.py`
- `src/gdc_adk/core/state.py`

#### Substrate
- `src/gdc_adk/substrate/event_spine.py`
- `src/gdc_adk/substrate/artifact_store.py`
- `src/gdc_adk/substrate/issue_tracker.py`
- `src/gdc_adk/substrate/dispatch_system.py`
- `src/gdc_adk/substrate/provenance.py`
- `src/gdc_adk/substrate/versioning.py`

#### Control plane
- `src/gdc_adk/control_plane/policy.py`
- `src/gdc_adk/control_plane/router.py`
- `src/gdc_adk/control_plane/optimizer.py`
- `src/gdc_adk/control_plane/model_registry.py`
- `src/gdc_adk/control_plane/context_assembler.py`
- `src/gdc_adk/control_plane/gate_evaluator.py`

#### Runtime
- `src/gdc_adk/runtime/local_model_manager.py`

#### Providers
- `src/gdc_adk/providers/base.py`
- `src/gdc_adk/providers/ollama_provider.py`
- `src/gdc_adk/providers/google_provider.py`
- `src/gdc_adk/providers/router.py`
- `src/gdc_adk/providers/weather/base.py`
- `src/gdc_adk/providers/weather/open_meteo.py`
- `src/gdc_adk/providers/weather/router.py`

#### Capabilities
- `src/gdc_adk/capabilities/geo.py`
- `src/gdc_adk/capabilities/time.py`
- `src/gdc_adk/capabilities/weather.py`

#### Information plane
- `src/gdc_adk/information_plane/ingestion/document_ingestor.py`
- `src/gdc_adk/information_plane/normalization/canonicalizer.py`
- `src/gdc_adk/information_plane/indexing/artifact_index.py`
- `src/gdc_adk/information_plane/activation/trigger_router.py`
- `src/gdc_adk/information_plane/activation/workflow_activation.py`
- `src/gdc_adk/information_plane/egress/artifact_emitter.py`

#### Workflows
- `src/gdc_adk/workflows/engine.py`
- `src/gdc_adk/workflows/state_machine.py`
- `src/gdc_adk/workflows/fix_flow.py`
- `src/gdc_adk/workflows/iterative_flow.py`

#### Validation
- `src/gdc_adk/validation/validator.py`
- `src/gdc_adk/validation/drift_checker.py`
- `src/gdc_adk/validation/traceability_auditor.py`
- `src/gdc_adk/validation/grounding_checker.py`

#### Memory
- `src/gdc_adk/memory/contracts.py`
- `src/gdc_adk/memory/cache.py`
- `src/gdc_adk/memory/context_store.py`
- `src/gdc_adk/memory/continuity.py`
- `src/gdc_adk/memory/replay.py`

#### Adapters and labs
- `src/gdc_adk/adapters/adk/weather_time_agent_adapter.py`
- `labs/adk/weather_time_agent.py`

#### Tests
- `tests/unit/...`
- `tests/integration/...`
- `tests/e2e/scenarios/...`

#### Scripts
- `scripts/verify_repo_shape.ps1`

---

## Relevant contract objects that must exist before serious implementation

These are not optional names. They are control objects that prevent drift.

- `Artifact`
- `Issue`
- `ContextBlock`
- `WorkflowRun`
- `ReviewFinding`
- `Emission`
- `ContinuitySnapshot`

All of these must be:
- typed
- serializable
- replayable where applicable
- stable across workflows
- not redefined independently in neighboring layers

### Minimum contract expectations

#### Artifact
Must carry, at minimum:
- `artifact_id`
- `artifact_type`
- `created_at`
- `source_kind`
- `content_ref` or `content`
- `metadata`
- optional lineage fields such as `parent_artifact_id`

#### Issue
Must carry, at minimum:
- `issue_id`
- `issue_type`
- `status`
- `severity`
- `created_at`
- `artifact_ids`
- `description`

#### ContextBlock
Must carry, at minimum:
- `context_block_id`
- `kind`
- `source_artifact_ids`
- `content`
- `metadata`

#### WorkflowRun
Must carry, at minimum:
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

#### ReviewFinding
Must carry, at minimum:
- `finding_id`
- `finding_type`
- `severity`
- `description`
- `related_artifact_ids`
- `evidence`
- `status`
- `created_at`

#### Emission
Must carry, at minimum:
- `emission_id`
- `emission_type`
- `artifact_ids`
- `workflow_run_id`
- `status`
- `created_at`

#### ContinuitySnapshot
Must carry, at minimum:
- `snapshot_id`
- `workflow_run_id`
- `current_state`
- `artifact_ids`
- `issue_ids`
- `finding_ids`
- `context_refs`
- `created_at`

---

## Workflow-mode implications for this bootstrap

### `single_run`
Must already be able to support:
- deterministic capability subpath
- local-first provider path
- output emission
- event recording

### `iterative`
Must already reserve:
- continuity snapshots
- artifact lineage
- findings across passes
- explicit revision path

### `fix_flow`
Must already reserve:
- issue object creation
- remediation evidence attachment
- verification step
- reopen loop

### `dynamic_flow`
Must already reserve:
- non-linear phase transitions
- replanning
- branch-safe execution state

### `fuzzy_logical_flow`
Must already reserve:
- staged interpretation
- contradiction handling
- ambiguity-aware review checkpoints

---

## Path typing rules

Every request path must be classified as one of the following:

1. deterministic capability path
2. local-first LLM path
3. cloud fallback path
4. blocked path due to policy or unresolved prerequisites

The decision order must be:

1. deterministic capability if available
2. tool-backed path if appropriate
3. cache reuse if valid
4. local reasoning provider
5. cloud fallback only if policy allows

No provider may choose itself.
No adapter may bypass this decision order.

---

# Phase-by-phase PowerShell implementation plan

## Phase 0. Open PowerShell and enter repo root

### Owning subsystem
Cross-cutting bootstrap

### Workflow modes affected
All

### Requirement IDs affected
`FX-R001`

### Commands

```powershell
cd C:\Users\bruno\OneDrive\Desktop\ForgeX
pwd
```

If the repo does not exist yet:

```powershell
mkdir C:\Users\bruno\OneDrive\Desktop\ForgeX
cd C:\Users\bruno\OneDrive\Desktop\ForgeX
git init
```

### Validation implication
Do not proceed if you are not at the intended repo root.

### Continuity implication
Repo-root config resolution depends on consistent root location.

---

## Phase 1. Create canonical repo shape exactly

### Owning subsystem
Repo constitution

### Requirement IDs affected
`FX-R001`, `FX-R006`, `FX-R007`, `FX-R008`, `FX-R009`, `FX-R010`

### Commands

```powershell
mkdir src
mkdir src\gdc_adk
mkdir src\gdc_adk\config
mkdir src\gdc_adk\substrate
mkdir src\gdc_adk\information_plane
mkdir src\gdc_adk\information_plane\ingestion
mkdir src\gdc_adk\information_plane\normalization
mkdir src\gdc_adk\information_plane\indexing
mkdir src\gdc_adk\information_plane\activation
mkdir src\gdc_adk\information_plane\egress
mkdir src\gdc_adk\information_plane\connectors
mkdir src\gdc_adk\information_plane\modalities
mkdir src\gdc_adk\control_plane
mkdir src\gdc_adk\runtime
mkdir src\gdc_adk\providers
mkdir src\gdc_adk\providers\weather
mkdir src\gdc_adk\capabilities
mkdir src\gdc_adk\memory
mkdir src\gdc_adk\validation
mkdir src\gdc_adk\workflows
mkdir src\gdc_adk\research
mkdir src\gdc_adk\worldforge
mkdir src\gdc_adk\adapters
mkdir src\gdc_adk\adapters\adk
mkdir src\gdc_adk\core
mkdir labs
mkdir labs\adk
mkdir tests
mkdir tests\unit
mkdir tests\integration
mkdir tests\e2e
mkdir scripts
```

### Package markers

```powershell
ni src\gdc_adk\__init__.py -ItemType File
ni src\gdc_adk\config\__init__.py -ItemType File
ni src\gdc_adk\substrate\__init__.py -ItemType File
ni src\gdc_adk\information_plane\__init__.py -ItemType File
ni src\gdc_adk\information_plane\ingestion\__init__.py -ItemType File
ni src\gdc_adk\information_plane\normalization\__init__.py -ItemType File
ni src\gdc_adk\information_plane\indexing\__init__.py -ItemType File
ni src\gdc_adk\information_plane\activation\__init__.py -ItemType File
ni src\gdc_adk\information_plane\egress\__init__.py -ItemType File
ni src\gdc_adk\information_plane\connectors\__init__.py -ItemType File
ni src\gdc_adk\information_plane\modalities\__init__.py -ItemType File
ni src\gdc_adk\control_plane\__init__.py -ItemType File
ni src\gdc_adk\runtime\__init__.py -ItemType File
ni src\gdc_adk\providers\__init__.py -ItemType File
ni src\gdc_adk\providers\weather\__init__.py -ItemType File
ni src\gdc_adk\capabilities\__init__.py -ItemType File
ni src\gdc_adk\memory\__init__.py -ItemType File
ni src\gdc_adk\validation\__init__.py -ItemType File
ni src\gdc_adk\workflows\__init__.py -ItemType File
ni src\gdc_adk\research\__init__.py -ItemType File
ni src\gdc_adk\worldforge\__init__.py -ItemType File
ni src\gdc_adk\adapters\__init__.py -ItemType File
ni src\gdc_adk\adapters\adk\__init__.py -ItemType File
ni src\gdc_adk\core\__init__.py -ItemType File
```

### Why this belongs here
The repo constitution explicitly requires these ownership boundaries and designated information-plane slots, including placeholders for future modalities and thin lab surfaces.

### Definition of done for Phase 1
- canonical package shape exists
- labs exist but remain thin
- there is a dedicated slot for multimodal growth
- no lab-local config exists

### Fail conditions
- missing `information_plane/modalities`
- missing `providers/weather`
- config files placed under `labs`
- adapters or labs used as core architecture homes

---

## Phase 2. Create root bootstrap and package files

### Owning subsystem
`config`

### Requirement IDs affected
`FX-R001`, partially `FX-R002`

### Commands

```powershell
ni config.yaml -ItemType File
ni .env -ItemType File
ni pyproject.toml -ItemType File
ni README.md -ItemType File
ni .gitignore -ItemType File
```

### Populate `.gitignore`

```powershell
@"
.venv/
__pycache__/
*.pyc
.pytest_cache/
.mypy_cache/
dist/
build/
*.egg-info/
.env
"@ | Set-Content .gitignore
```

### Populate `pyproject.toml`

```powershell
@"
[build-system]
requires = ["setuptools>=68", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "gdc-adk"
version = "0.1.0"
description = "Forge-X local-first coworker engine"
requires-python = ">=3.11"
dependencies = [
  "pyyaml>=6.0.1",
  "python-dotenv>=1.0.1",
  "pydantic>=2.8.2",
  "requests>=2.32.3",
  "pytest>=8.3.2"
]

[tool.setuptools]
package-dir = {"" = "src"}

[tool.setuptools.packages.find]
where = ["src"]
"@ | Set-Content pyproject.toml
```

### Populate `config.yaml`

```powershell
@"
routing:
  default_provider: ollama
  failover_order:
    - ollama
    - google

providers:
  ollama:
    base_url: http://localhost:11434
    model_aliases:
      default: gemma3
      reasoning_local: deepseek-coder-v2
  google:
    model_aliases:
      default: gemini-2.5-pro

weather:
  provider: open_meteo
  providers:
    open_meteo:
      base_url: https://api.open-meteo.com

policy:
  allow_cloud_for_task_types:
    - research_flow
    - code_flow
  local_only_task_types:
    - time_lookup
    - weather_lookup
"@ | Set-Content config.yaml
```

### Populate `.env`

```powershell
@"
GOOGLE_API_KEY=
"@ | Set-Content .env
```

### Required content rules
- `config.yaml` must live at repo root
- `.env` must live at repo root
- no provider URLs or model names may be hardcoded in adapter files
- config loading must resolve from repo root and labs without lab-local config drift

### Definition of done for Phase 2
- root config exists
- editable install metadata exists
- root config reflects local-first policy
- no lab-level config exists

### Fail conditions
- config duplicated under `labs/`
- cloud-first default in config
- adapter-owned config values

---

## Phase 3. Stage 1 contracts and substrate files

### Owning subsystems
`core`, `substrate`

### Requirement IDs affected
`FX-R007`, `FX-R008`, `FX-R009`, `FX-R010`

### Commands

```powershell
ni src\gdc_adk\core\contracts.py -ItemType File
ni src\gdc_adk\core\state.py -ItemType File

ni src\gdc_adk\substrate\event_spine.py -ItemType File
ni src\gdc_adk\substrate\artifact_store.py -ItemType File
ni src\gdc_adk\substrate\issue_tracker.py -ItemType File
ni src\gdc_adk\substrate\dispatch_system.py -ItemType File
ni src\gdc_adk\substrate\provenance.py -ItemType File
ni src\gdc_adk\substrate\versioning.py -ItemType File
```

### File-level implementable responsibilities

#### `core/contracts.py`
Must define typed stable contracts for:
- `Artifact`
- `Issue`
- `ContextBlock`
- `WorkflowRun`
- `ReviewFinding`
- `Emission`
- `ContinuitySnapshot`

Must not:
- perform provider routing
- load config
- contain workflow orchestration logic

#### `core/state.py`
Must define:
- reusable state enums or typed state support
- workflow state helpers
- continuity-safe state helpers

Must not:
- own storage
- own provider execution

#### `substrate/event_spine.py`
Must define controlled event recording with event types such as:
- `request_received`
- `artifact_created`
- `issue_created`
- `workflow_started`
- `workflow_transitioned`
- `provider_selected`
- `provider_invoked`
- `provider_failed`
- `finding_created`
- `workflow_completed`
- `workflow_reopened`

Each event should carry:
- `event_id`
- `event_type`
- `created_at`
- `correlation_id`
- optional `workflow_run_id`
- `payload`

Must not:
- pick providers
- own workflow decisions

#### `substrate/artifact_store.py`
Must support:
- typed artifact creation
- retrieval by ID
- revision lineage
- parent-child linkage
- artifact class distinction such as input, normalized, generated, evidence, emitted

Must not:
- contain provider logic
- contain review logic

#### `substrate/issue_tracker.py`
Must support:
- typed issue creation
- issue status transitions
- reopen semantics
- linkage to artifacts and workflow runs

Must not:
- own workflow execution sequencing

#### `substrate/dispatch_system.py`
Must support:
- structured entry from raw request toward artifact creation, classification, and workflow activation
- dispatch contract that returns traceable workflow entry outputs
- deterministic creation of issue object when fix-flow triage requires it

Must not:
- hide state in prompt text
- bypass information-plane ingestion

#### `substrate/provenance.py`
Must support:
- source linkage
- lineage references
- traceable derivation metadata

#### `substrate/versioning.py`
Must support:
- revision metadata
- artifact version references
- replacement without lineage loss

### Definition of done for Phase 3
- requests can create typed artifacts
- fix-flow can create typed issues
- dispatch entry is structured
- events are recordable
- lineage and provenance have homes

### Fail conditions
- no typed artifact object
- no issue object in fix-flow
- dispatch is conversational only
- event recording absent
- revision overwrites prior artifact without lineage

---

## Phase 4. Stage 2 control plane, runtime, providers, and deterministic capabilities

### Owning subsystems
`control_plane`, `runtime`, `providers`, `capabilities`

### Requirement IDs affected
`FX-R002`, `FX-R003`, `FX-R004`, `FX-R005`

### Commands

```powershell
ni src\gdc_adk\config\settings.py -ItemType File

ni src\gdc_adk\control_plane\policy.py -ItemType File
ni src\gdc_adk\control_plane\router.py -ItemType File
ni src\gdc_adk\control_plane\optimizer.py -ItemType File
ni src\gdc_adk\control_plane\model_registry.py -ItemType File
ni src\gdc_adk\control_plane\context_assembler.py -ItemType File
ni src\gdc_adk\control_plane\gate_evaluator.py -ItemType File

ni src\gdc_adk\runtime\local_model_manager.py -ItemType File

ni src\gdc_adk\providers\base.py -ItemType File
ni src\gdc_adk\providers\ollama_provider.py -ItemType File
ni src\gdc_adk\providers\google_provider.py -ItemType File
ni src\gdc_adk\providers\router.py -ItemType File

ni src\gdc_adk\providers\weather\base.py -ItemType File
ni src\gdc_adk\providers\weather\open_meteo.py -ItemType File
ni src\gdc_adk\providers\weather\router.py -ItemType File

ni src\gdc_adk\capabilities\geo.py -ItemType File
ni src\gdc_adk\capabilities\time.py -ItemType File
ni src\gdc_adk\capabilities\weather.py -ItemType File
```

### File-level implementable responsibilities

#### `config/settings.py`
Must:
- load repo-root `config.yaml`
- load repo-root `.env`
- expose typed config accessors

Must not:
- execute providers
- create issues
- decide workflows

#### `control_plane/policy.py`
Must define explicit policy functions, including:
- allow or deny cloud fallback
- local-first routing checks
- deterministic-before-LLM checks
- future validation independence checks

Good explicit names:
- `allow_cloud_for_task_type`
- `prefer_deterministic_path`
- `require_independent_review_for_artifact`

Must not:
- directly call providers

#### `control_plane/router.py`
Must:
- select provider class based on policy and task path
- build failover chain
- never let providers self-select

Good explicit names:
- `select_provider`
- `build_failover_chain`

Must not:
- author prompts
- own provider transport

#### `control_plane/optimizer.py`
Must:
- define context and token-budget optimization rules
- define cache eligibility inputs

Must not:
- hide business logic in generic helpers

#### `control_plane/model_registry.py`
Must:
- map task classes and provider aliases to model choices
- remain config-driven

Must not:
- hardcode cloud-first behavior

#### `control_plane/context_assembler.py`
Must:
- assemble bounded grounded context from artifacts, findings, issues, and memory
- preserve source linkage

Must not:
- act as hidden workflow engine

#### `control_plane/gate_evaluator.py`
Must:
- decide whether execution is allowed to proceed
- enforce policy and readiness gates

Must not:
- mutate workflow policy definitions

#### `runtime/local_model_manager.py`
Must:
- manage active local model lifecycle
- support queueing, retries, watchdog-safe behavior, and execution isolation

Good explicit names:
- `set_active_model`
- `clear_active_model`

Must not:
- own workflow semantics
- own validation policy

#### `providers/base.py`
Must define uniform request/response contracts for providers, such as:
- `LLMRequest`
- `LLMResponse`

Must define methods like:
- `is_available()`
- `generate(request)`

Must not:
- decide whether the provider should be used

#### `providers/ollama_provider.py`
Must:
- map uniform request/response into Ollama transport
- expose availability checks

Must not:
- route around control plane

#### `providers/google_provider.py`
Must:
- map uniform request/response into Google transport
- remain cloud fallback only unless policy says otherwise

#### `providers/router.py`
Must:
- execute provider invocation according to control-plane output
- preserve structured failure chain

Must not:
- decide policy

#### `providers/weather/base.py`
Must define a weather provider contract

#### `providers/weather/open_meteo.py`
Must implement weather provider contract for Open-Meteo

#### `providers/weather/router.py`
Must choose weather provider implementation from control inputs, not from ad hoc hardcoding in capabilities

#### `capabilities/geo.py`
Must:
- resolve city references and timezone inputs

Good explicit names:
- `resolve_city_reference`

#### `capabilities/time.py`
Must:
- provide deterministic time capability

Good explicit names:
- `get_current_time`

Must not:
- invoke remote generative models first when city/timezone is resolvable

#### `capabilities/weather.py`
Must:
- provide weather capability using the weather provider contract

Good explicit names:
- `get_weather`

Must not:
- hardcode provider URLs
- bypass the weather provider abstraction

### Definition of done for Phase 4
- local provider is default
- cloud is fallback only
- deterministic time path exists
- weather routes through provider abstraction
- providers expose uniform request/response contracts

### Fail conditions
- cloud provider chosen first
- providers choose themselves
- deterministic time goes to remote LLM first
- capabilities contain routing logic
- adapters contain model names or provider URLs

---

## Phase 5. Stage 3 information plane

### Owning subsystem
`information_plane`

### Requirement IDs affected
`FX-R006`

### Commands

```powershell
ni src\gdc_adk\information_plane\ingestion\document_ingestor.py -ItemType File
ni src\gdc_adk\information_plane\normalization\canonicalizer.py -ItemType File
ni src\gdc_adk\information_plane\indexing\artifact_index.py -ItemType File
ni src\gdc_adk\information_plane\activation\trigger_router.py -ItemType File
ni src\gdc_adk\information_plane\activation\workflow_activation.py -ItemType File
ni src\gdc_adk\information_plane\egress\artifact_emitter.py -ItemType File
```

### File-level implementable responsibilities

#### `ingestion/document_ingestor.py`
Must:
- ingest raw inputs such as text, markdown, document-derived text, email-like text, screenshots/transcripts placeholders, structured records, and repo/code text
- produce canonical raw signal objects

Good explicit names:
- `ingest_text_signal`
- `ingest_document_signal`

Must not:
- call providers directly
- own workflow policy

#### `normalization/canonicalizer.py`
Must:
- normalize signals into a stable canonical form

Minimum normalized fields should include:
- `normalized_type`
- `source_kind`
- extracted text
- modality metadata
- timestamps
- provenance notes
- confidence if applicable

Good explicit names:
- `normalize_signal`
- `canonicalize_text_payload`

#### `indexing/artifact_index.py`
Must:
- maintain searchable mappings for artifacts
- support artifact lookup by ID and source linkage
- support future entity and temporal indexing

Must not:
- be skipped for multi-turn architecture

#### `activation/trigger_router.py`
Must:
- classify activation trigger category from normalized signal

#### `activation/workflow_activation.py`
Must:
- decide workflow activation output from normalized signal and context
- support mapping toward `single_run`, `iterative`, `fix_flow`, `dynamic_flow`, and `fuzzy_logical_flow`

Good explicit names:
- `activate_workflow`
- `select_workflow_mode`

Must not:
- directly execute providers

#### `egress/artifact_emitter.py`
Must:
- emit structured results such as:
  - direct answer
  - generated artifact
  - issue update
  - workflow status
  - review packet
  - package or handoff artifact

Must not:
- reduce everything to one raw output string

### Definition of done for Phase 5
- raw text becomes normalized signal
- input artifact exists
- activation output exists
- architecture already has slots for future modalities

### Fail conditions
- raw input is sent directly to provider
- normalization omitted
- modality growth would require repo redesign
- no artifact representation for source inputs

---

## Phase 6. Stage 4 workflow engine and review spine

### Owning subsystems
`workflows`, `validation`

### Commands

```powershell
ni src\gdc_adk\workflows\engine.py -ItemType File
ni src\gdc_adk\workflows\state_machine.py -ItemType File
ni src\gdc_adk\workflows\fix_flow.py -ItemType File
ni src\gdc_adk\workflows\iterative_flow.py -ItemType File

ni src\gdc_adk\validation\validator.py -ItemType File
ni src\gdc_adk\validation\drift_checker.py -ItemType File
ni src\gdc_adk\validation\traceability_auditor.py -ItemType File
ni src\gdc_adk\validation\grounding_checker.py -ItemType File
```

### Workflow state model that must exist

All workflow runs must carry:
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

### Baseline states that must exist
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

### File-level implementable responsibilities

#### `workflows/engine.py`
Must:
- orchestrate workflow execution using explicit state, not implicit prompt continuation
- coordinate calls across capabilities, providers, substrate, validation, and memory

#### `workflows/state_machine.py`
Must:
- define allowed transitions
- define mode-specific paths
- preserve replayability

#### `workflows/fix_flow.py`
Must:
- require issue object creation
- support remediation evidence
- support verification step
- support reopen path

Extended states that must exist:
- `issue_opened`
- `remediation_in_progress`
- `verification_pending`
- `resolution_proposed`
- `resolution_verified`

#### `workflows/iterative_flow.py`
Must:
- require continuity snapshot between passes
- preserve artifact lineage
- preserve prior findings across revisions
- support revise and reopen semantics

#### `validation/validator.py`
Must:
- coordinate structured validation passes

#### `validation/drift_checker.py`
Must:
- check repo constitution
- check hidden-state drift
- check local-first violations
- check workflow-state drift

#### `validation/traceability_auditor.py`
Must:
- validate requirement ID mapping
- validate that changed files map to owning subsystem and acceptance coverage

#### `validation/grounding_checker.py`
Must:
- detect unsupported grounded claims
- create findings when grounding is insufficient

### ReviewFinding lifecycle that must exist
- `open`
- `accepted`
- `rejected_with_rationale`
- `resolved`
- `reopened`

### Non-trivial validation independence rule
Validation may not be merely the same exact generation path declaring its own artifact acceptable.
Non-trivial artifacts must support independent findings.

### Definition of done for Phase 6
- workflows run with explicit state
- review exists as typed findings
- fix-flow has issue + verification + close or reopen semantics
- iterative flow preserves lineage and continuity

### Fail conditions
- review exists only in prose
- no finding object
- no issue in fix-flow
- workflow state hidden in prompt text
- revised artifact overwrites prior artifact with no lineage

---

## Phase 7. Stage 5 memory contracts and operational memory

### Owning subsystem
`memory`

### Commands

```powershell
ni src\gdc_adk\memory\contracts.py -ItemType File
ni src\gdc_adk\memory\cache.py -ItemType File
ni src\gdc_adk\memory\context_store.py -ItemType File
ni src\gdc_adk\memory\continuity.py -ItemType File
ni src\gdc_adk\memory\replay.py -ItemType File
```

### File-level implementable responsibilities

#### `memory/contracts.py`
Must define role-based interfaces such as:
- `MemoryStore`
- `ContextStore`
- `ContinuityStore`

Must not:
- couple to one future backend
- hide implementation assumptions in ad hoc types

#### `memory/cache.py`
Must:
- store bounded reusable results
- expose cache eligibility and retrieval semantics

#### `memory/context_store.py`
Must:
- store structured context blocks
- keep source linkage

#### `memory/continuity.py`
Must:
- persist continuity snapshots between iterations and reopen cycles
- support exportable state

#### `memory/replay.py`
Must:
- support export and future rehydration
- support replay-friendly structures for later Coherence-Base integration

### Definition of done for Phase 7
- workflows can resume with explicit continuity snapshots
- context and continuity are exportable
- memory remains replaceable later

### Fail conditions
- continuity exists only in one runtime object
- no exportable snapshot
- memory API tightly couples to one future backend
- critical state hidden in prompt history

---

## Phase 8. Keep adapters and labs thin

### Owning subsystem
`adapters`, `labs`

### Commands

```powershell
ni src\gdc_adk\adapters\adk\weather_time_agent_adapter.py -ItemType File
ni labs\adk\weather_time_agent.py -ItemType File
```

### Required behavior

#### `adapters/adk/weather_time_agent_adapter.py`
Must:
- map external ADK inputs and outputs to Forge-X calls

Must not:
- contain routing policy
- contain provider URLs
- contain model selection
- contain workflow business logic

#### `labs/adk/weather_time_agent.py`
Must:
- remain minimal and surface-specific
- not establish new domain lexicology
- not own core logic

### Definition of done for Phase 8
- adapter is a bridge only
- lab file is a thin surface only

### Fail conditions
- adapter owns provider selection
- lab contains business logic
- adapter hardcodes model names or URLs

---

## Phase 9. Create acceptance-aligned test folders and scenario files

### Owning subsystem
Cross-cutting acceptance and validation

### Commands

```powershell
mkdir tests\unit\config
mkdir tests\unit\substrate
mkdir tests\unit\control_plane
mkdir tests\unit\providers
mkdir tests\unit\capabilities
mkdir tests\unit\information_plane
mkdir tests\unit\memory
mkdir tests\unit\validation
mkdir tests\unit\workflows

mkdir tests\integration\dispatch
mkdir tests\integration\provider_failover
mkdir tests\integration\information_activation
mkdir tests\integration\workflow_review
mkdir tests\integration\memory_continuity

mkdir tests\e2e\scenarios
```

### Scenario files

```powershell
ni tests\e2e\scenarios\test_scenario_a_time_lookup.py -ItemType File
ni tests\e2e\scenarios\test_scenario_b_local_reasoning.py -ItemType File
ni tests\e2e\scenarios\test_scenario_c_fix_flow.py -ItemType File
ni tests\e2e\scenarios\test_scenario_d_iterative_refinement.py -ItemType File
ni tests\e2e\scenarios\test_scenario_e_grounded_spec_flow.py -ItemType File
ni tests\e2e\scenarios\test_scenario_f_multimodal_activation_placeholder.py -ItemType File
ni tests\e2e\scenarios\test_scenario_g_provider_fallback.py -ItemType File
ni tests\e2e\scenarios\test_scenario_h_review_spine.py -ItemType File
ni tests\e2e\scenarios\test_scenario_i_continuity_snapshot.py -ItemType File
ni tests\e2e\scenarios\test_scenario_j_multi_agent_readiness.py -ItemType File
```

### What each scenario must prove

#### Scenario A
- raw text ingested
- normalized signal exists
- input artifact exists
- deterministic time path used
- no remote model called first
- event recorded
- result replayable

#### Scenario B
- local provider chosen before cloud
- provider attribution present
- activation/output linkage stored

#### Scenario C
- fix-flow selected
- issue object created
- event recorded
- workflow state activated

#### Scenario D
- prior artifact remains addressable
- revised artifact links to prior artifact
- finding or issue can represent the miss

#### Scenario E
- source materials become source artifacts
- searchable or indexed units exist
- output references source artifacts
- unsupported claims can be challenged by findings

#### Scenario F
- information plane already has modality-specific slots
- multimodal growth does not require repo redesign

#### Scenario G
- local checked first
- failure chain preserved
- cloud used only if policy allows

#### Scenario H
- finding object created
- finding linked to artifact
- workflow reacts to finding via reopen or re-entry

#### Scenario I
- continuity snapshot captures current state and linkage
- snapshot is serializable
- snapshot is exportable

#### Scenario J
- typed artifacts, issues, findings, workflow state machine, and explicit dispatch linkage exist before multi-agent

### Completion gates by subsystem

- `G1` Core substrate: scenarios A, B, C traceable with artifacts/events/issues
- `G2` Information plane: ingestion -> normalization -> activation path exists
- `G3` Control plane: deterministic/local-first policy enforced under success and failover
- `G4` Memory: snapshots are serializable and not hidden
- `G5` Review spine: findings exist independent from prose and link to artifacts/issues
- `G6` Workflow engine: iterative and fix-flow preserve state, findings, reopen semantics
- `G7` Multi-agent: typed handoff artifacts and bounded roles exist

---

## Phase 10. Create bootstrap verification script

### Owning subsystem
Bootstrap verification only

### Important warning
This script is not the real pre-merge gate.
It is only an early shape checker.

### Commands

```powershell
ni scripts\verify_repo_shape.ps1 -ItemType File
```

### Populate script

```powershell
@"
$requiredPaths = @(
  'src\gdc_adk\config\settings.py',
  'src\gdc_adk\core\contracts.py',
  'src\gdc_adk\core\state.py',
  'src\gdc_adk\substrate\event_spine.py',
  'src\gdc_adk\substrate\artifact_store.py',
  'src\gdc_adk\substrate\issue_tracker.py',
  'src\gdc_adk\substrate\dispatch_system.py',
  'src\gdc_adk\control_plane\policy.py',
  'src\gdc_adk\control_plane\router.py',
  'src\gdc_adk\providers\base.py',
  'src\gdc_adk\providers\ollama_provider.py',
  'src\gdc_adk\providers\google_provider.py',
  'src\gdc_adk\providers\router.py',
  'src\gdc_adk\providers\weather\base.py',
  'src\gdc_adk\providers\weather\open_meteo.py',
  'src\gdc_adk\providers\weather\router.py',
  'src\gdc_adk\capabilities\geo.py',
  'src\gdc_adk\capabilities\time.py',
  'src\gdc_adk\capabilities\weather.py',
  'src\gdc_adk\information_plane\ingestion\document_ingestor.py',
  'src\gdc_adk\information_plane\normalization\canonicalizer.py',
  'src\gdc_adk\information_plane\indexing\artifact_index.py',
  'src\gdc_adk\information_plane\activation\trigger_router.py',
  'src\gdc_adk\information_plane\activation\workflow_activation.py',
  'src\gdc_adk\information_plane\egress\artifact_emitter.py',
  'src\gdc_adk\workflows\engine.py',
  'src\gdc_adk\workflows\state_machine.py',
  'src\gdc_adk\workflows\fix_flow.py',
  'src\gdc_adk\workflows\iterative_flow.py',
  'src\gdc_adk\validation\validator.py',
  'src\gdc_adk\validation\drift_checker.py',
  'src\gdc_adk\validation\traceability_auditor.py',
  'src\gdc_adk\validation\grounding_checker.py',
  'src\gdc_adk\memory\contracts.py',
  'src\gdc_adk\memory\cache.py',
  'src\gdc_adk\memory\context_store.py',
  'src\gdc_adk\memory\continuity.py',
  'src\gdc_adk\memory\replay.py',
  'src\gdc_adk\adapters\adk\weather_time_agent_adapter.py',
  'labs\adk\weather_time_agent.py',
  'config.yaml',
  'pyproject.toml'
)

$missing = @()

foreach ($path in $requiredPaths) {
  if (-not (Test-Path $path)) {
    $missing += $path
  }
}

if ($missing.Count -gt 0) {
  Write-Host 'Missing required paths:' -ForegroundColor Red
  $missing | ForEach-Object { Write-Host " - $_" -ForegroundColor Red }
  exit 1
}

Write-Host 'Repo shape check passed.' -ForegroundColor Green
"@ | Set-Content scripts\verify_repo_shape.ps1
```

### Run script

```powershell
.\scripts\verify_repo_shape.ps1
```

### Definition of done for Phase 10
- required scaffold files exist
- this script is documented as bootstrap-only

### Fail conditions
- this script is mistaken for full drift enforcement
- missing key files are ignored

---

## Phase 11. Create and activate Python virtual environment

### Owning subsystem
Bootstrap environment

### Commands

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e .
```

### Verify import resolution

```powershell
python -c "import gdc_adk; print('ok')"
```

### Definition of done
- editable install works
- package imports resolve from repo root

### Fail conditions
- package cannot import
- installation depends on lab-local hacks

---

## Phase 12. Mandatory terminal checks before real implementation

### Commands

Check root config presence:

```powershell
Test-Path config.yaml
Test-Path .env
```

Check package tree:

```powershell
Get-ChildItem src\gdc_adk -Recurse | Select-Object FullName
```

Check lab-level config drift:

```powershell
Get-ChildItem labs -Recurse -Include *.yaml,*.yml,.env
```

Check stage files:

```powershell
.\scripts\verify_repo_shape.ps1
```

### Interpretation
- `labs` should not contain local config
- package tree should match constitution
- missing files block progress

---

# Exact implementation order after scaffold creation

## Step 13.1 Implement contracts first
Start with:
- `src/gdc_adk/core/contracts.py`
- `src/gdc_adk/core/state.py`

This is non-negotiable because stable contracts prevent neighboring layers from inventing incompatible state.

## Step 13.2 Implement substrate next
Implement:
- `event_spine.py`
- `artifact_store.py`
- `issue_tracker.py`
- `dispatch_system.py`
- `provenance.py`
- `versioning.py`

Stage 1 is accepted only when requests create artifacts and issues deterministically and workflow entry is traceable.

## Step 13.3 Implement config and control-plane policy
Implement:
- `settings.py`
- `policy.py`
- `router.py`
- `optimizer.py`
- `model_registry.py`
- `context_assembler.py`
- `gate_evaluator.py`

No provider self-selection is allowed.

## Step 13.4 Implement provider contracts and runtime
Implement:
- `providers/base.py`
- `local_model_manager.py`
- `ollama_provider.py`
- `google_provider.py`
- `providers/router.py`
- weather provider family

Local-first and deterministic-before-LLM behavior must already be preserved.

## Step 13.5 Implement deterministic capabilities
Implement:
- `geo.py`
- `time.py`
- `weather.py`

Deterministic time lookup must not default to a remote generative path.

## Step 13.6 Implement information plane
Implement:
- ingestion
- normalization
- indexing
- activation
- egress

Do not bypass canonicalization.

## Step 13.7 Implement workflow state and review spine
Implement:
- workflow engine
- state machine
- fix-flow
- iterative flow
- validator
- drift checker
- traceability auditor
- grounding checker

Review must become typed findings, not prose.

## Step 13.8 Implement memory
Implement:
- contracts
- cache
- context store
- continuity
- replay

Continuity must be exportable and future-replaceable.

## Step 13.9 Only then propose multi-agent
Only after these exist:
- typed artifacts
- typed issues
- typed findings
- workflow state machine
- typed handoff artifacts
- explicit role boundaries
- bounded authority and stop conditions

---

# Git checkpoint commands

## After scaffold
```powershell
git status
git add .
git commit -m "forge-x: scaffold canonical repo structure and bootstrap files"
```

## After Stage 1 contracts and substrate
```powershell
git add .
git commit -m "forge-x: add stage 1 contracts substrate provenance and versioning"
```

## After Stage 2 control plane and providers
```powershell
git add .
git commit -m "forge-x: add control plane runtime providers and deterministic capabilities"
```

## After Stage 3 information plane
```powershell
git add .
git commit -m "forge-x: add information plane ingestion normalization indexing activation and egress"
```

## After Stage 4 workflow and validation
```powershell
git add .
git commit -m "forge-x: add workflow state machines review spine and validation"
```

## After Stage 5 memory
```powershell
git add .
git commit -m "forge-x: add memory contracts continuity replay and exportable state"
```

### Important control rule
Git commits are not proof of acceptance.
They are rollback markers only.

---

# Pre-merge enforcement you must add after bootstrap

The real pre-merge checks must eventually cover all of the following:

## Gate category 1. Constitution
- correct subsystem ownership
- no adapter-owned orchestration
- no provider-owned task selection
- no lab-level config drift

## Gate category 2. Naming and lexicology
- no vague names like `handle_request`, `smart_route`, `pick_best`
- capability names remain domain nouns
- adapter files end with `_adapter.py`
- provider files represent backend identity

## Gate category 3. Contract integrity
- typed objects exist
- no duplicate incompatible contract definitions
- provider request/response contract is uniform

## Gate category 4. Local-first policy
- deterministic path used when available
- local provider checked before cloud
- policy gates control fallback

## Gate category 5. Workflow state
- explicit state machine exists
- no prose-only workflow state
- no fix-flow without issue object
- no iterative revision without lineage

## Gate category 6. Review spine
- findings exist as typed objects
- findings link to artifacts
- workflows react to findings

## Gate category 7. Replayability
- continuity snapshots are serializable
- no hidden critical memory dependency

## Gate category 8. Golden scenarios
- rerun scenarios A through J as applicable

---

# Anti-patterns explicitly forbidden during implementation

Do not do any of the following:

- hide business logic in adapters
- hide architecture in labs
- let providers choose themselves
- hardcode cloud-first defaults
- route deterministic time through remote generative models first
- use vague names like `handle_request`, `smart_route`, `pick_best`
- overwrite revised artifacts with no lineage
- keep review only as prose
- keep continuity only in a runtime object
- treat placeholder files as completion
- implement workflows as prompt chains instead of explicit state machines
- add helper dumping-ground files that absorb unrelated logic

---

# File naming and lexicology rules you must preserve

Use names like:
- `settings.py`
- `event_spine.py`
- `artifact_store.py`
- `issue_tracker.py`
- `dispatch_system.py`
- `local_model_manager.py`
- `ollama_provider.py`
- `google_provider.py`
- `time.py`
- `weather.py`
- `geo.py`
- `context_store.py`
- `continuity.py`
- `validator.py`
- `drift_checker.py`
- `traceability_auditor.py`
- `grounding_checker.py`
- `weather_time_agent_adapter.py`

Use explicit function names like:
- `get_current_time`
- `get_weather`
- `resolve_city_reference`
- `select_provider`
- `build_failover_chain`
- `set_active_model`
- `clear_active_model`
- `activate_workflow`
- `select_workflow_mode`

Avoid vague names like:
- `handle_request`
- `smart_route`
- `pick_best`
- `do_work`
- `main_flow`

---

# Final bootstrap acceptance statement

This document is complete only as a corrected implementation-control bootstrap pack.

It is acceptable when:
- the repo shape is created correctly
- root config is placed correctly
- stage file creation follows the mandatory order
- responsibilities are understood per file
- no stop-ship violations are introduced during bootstrap

It is not acceptable as proof that Forge-X itself is implemented.

Forge-X itself is only acceptable when:
- substrate is typed and traceable
- control plane enforces local-first and deterministic-before-LLM behavior
- information plane performs canonical ingestion and activation
- workflow state is explicit and replayable
- review findings are typed and durable
- memory continuity is exportable
- acceptance scenarios pass
- pre-merge gates pass
- traceability rows are updated with real completion status

---

## Immediate next action after using this pack

After you create the scaffold with this pack, the next implementation artifact should be a **Stage 1 implementation pack** for:
- `core/contracts.py`
- `core/state.py`
- `substrate/event_spine.py`
- `substrate/artifact_store.py`
- `substrate/issue_tracker.py`
- `substrate/dispatch_system.py`
- `substrate/provenance.py`
- `substrate/versioning.py`

That next pack should include:
- exact public classes and function signatures
- exact enums and state vocabularies
- exact negative cases
- exact unit, integration, and E2E assertions
- exact traceability row updates
