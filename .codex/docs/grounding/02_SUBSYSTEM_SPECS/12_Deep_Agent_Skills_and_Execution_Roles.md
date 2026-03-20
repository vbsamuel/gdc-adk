# Forge-X Agent Skills, Expertise, and Execution Roles

Generated: 2026-03-19T10:34:38Z

## Purpose

This document defines the **actual engineering skill requirements** for the agent or agent ensemble that will implement Forge-X without drift. This is not generic “good engineer” language. It is a system-specific capability contract.

## 1. Minimum engineering competencies

### 1.1 Architecture ownership discipline
The agent must be able to:
- map a request to the correct subsystem before coding
- refuse to place logic in the wrong layer
- preserve import-direction rules
- recognize when a requested shortcut would violate future replaceability or local-first policy

The agent fails this competency if it:
- puts routing into adapters
- puts business logic into labs
- lets providers choose themselves
- hides workflow state in prompt text

### 1.2 Deterministic-before-LLM reasoning
The agent must know how to decide:
- when a task is deterministic
- when a task is tool-backed
- when a task can use cache
- when local reasoning is enough
- when cloud fallback is disallowed

The agent fails this competency if it:
- defaults to Gemini or any remote model for convenience
- skips capability checks for time/weather/retrieval-like tasks
- cannot explain why a provider was selected

### 1.3 Workflow engineering
The agent must be able to build:
- state machines
- bounded loops
- retry logic
- reopen/close semantics
- issue-linked remediation flow
- multi-step execution with explicit phase transitions

The agent fails this competency if it:
- treats workflows as long prompts only
- cannot model iterative or fix-flow explicitly
- cannot explain completion vs resolution vs closure

### 1.4 Contract-oriented implementation
The agent must be able to define and preserve:
- Artifact
- Issue
- ContextBlock
- WorkflowRun
- ReviewFinding
- Emission
- ContinuitySnapshot or equivalent

The agent fails this competency if:
- object shape is hidden in prose
- state cannot be serialized
- different workflows invent incompatible shapes for the same object type

### 1.5 Validation and review engineering
The agent must be able to:
- write structured acceptance criteria
- define negative-path tests
- create structured findings
- identify constitution violations
- reason about grounding gaps and unsupported claims
- preserve separation between authoring and validation

The agent fails this competency if:
- validation is just “looks good”
- review is not represented as structured state
- no negative cases are considered

## 2. Subsystem-specific skill requirements

### 2.1 Config and constitution engineer skills
Needed to implement `config/` and preserve repo law.

Required knowledge:
- path-anchored configuration loading
- environment-variable hygiene
- package import behavior in editable installs
- schema stability for config keys

Expected behaviors:
- no lab-level config drift
- no hidden defaults
- no path-sensitive loading bugs when running from `labs/adk`

### 2.2 Substrate engineer skills
Needed to implement `substrate/`.

Required knowledge:
- event recording
- artifact lineage
- issue lifecycle design
- correlation and provenance

Expected behaviors:
- every important state transition can be represented and replayed
- issue lifecycle is durable, not ephemeral
- dispatch acts as controlled entry point

### 2.3 Information-plane engineer skills
Needed to implement `information_plane/`.

Required knowledge:
- ingestion pipeline architecture
- canonicalization
- indexing
- activation routing
- multimodal extensibility

Expected behaviors:
- raw input is converted into canonical structured signals
- artifacts are created early
- activation does not skip normalization
- multimodal future paths have explicit homes even if not fully built today

### 2.4 Control-plane engineer skills
Needed to implement `control_plane/`.

Required knowledge:
- routing policy
- failover strategy
- local-first model selection
- token reuse policy
- selective context assembly

Expected behaviors:
- deterministic paths win before LLMs
- local providers are preferred
- cloud is gated
- task type is the key routing input, not arbitrary provider preference

### 2.5 Provider/runtime engineer skills
Needed to implement `providers/` and `runtime/`.

Required knowledge:
- backend request/response normalization
- availability checks
- timeout handling
- local model lifecycle
- swappable provider abstractions

Expected behaviors:
- provider adapters remain thin
- runtime remains separate from workflow semantics
- provider failures are explicit and traceable

### 2.6 Memory engineer skills
Needed to implement `memory/`.

Required knowledge:
- caching
- continuity snapshots
- exportable state
- future replaceability
- replay-oriented design

Expected behaviors:
- nothing critical is trapped in one in-memory implementation
- operational memory helps now but does not block Coherence-Base later

### 2.7 Workflow engineer skills
Needed to implement `workflows/`.

Required knowledge:
- state machines
- phase transitions
- bounded recursion/loops
- escalation handling
- role handoff contracts

Expected behaviors:
- iterative and fix-flow are explicit
- dynamic and fuzzy-logical flows are not reduced to “miscellaneous”
- multi-agent orchestration is impossible until typed handoffs exist

### 2.8 Validation engineer skills
Needed to implement `validation/`.

Required knowledge:
- QA methodology
- structured findings
- drift detection
- negative-case and edge-case design
- evidence and traceability

Expected behaviors:
- every important artifact can be challenged
- findings can reopen work
- unsupported claims and architecture drift can be represented structurally

## 3. Role profiles for multi-agent execution

Forge-X should prefer explicit role specialization when moving beyond single-agent execution.

### 3.1 Constitution Keeper / Systems Architect
Owns:
- subsystem boundaries
- repo law
- dependency direction
- architectural drift prevention

### 3.2 Workflow and Orchestration Engineer
Owns:
- workflow state machines
- phase progression
- retry/reopen logic
- role handoffs

### 3.3 Information and Context Engineer
Owns:
- ingestion
- canonicalization
- indexing
- context assembly prerequisites

### 3.4 Provider and Runtime Engineer
Owns:
- local model management
- provider request execution
- failover mechanics
- runtime resilience

### 3.5 Validation and Review Engineer
Owns:
- findings
- gates
- acceptance checks
- adversarial and negative-path review

### 3.6 Memory and Continuity Engineer
Owns:
- cache
- continuity
- exportable state
- Coherence-Base compatibility layer

## 4. Hard skill tests the agent must pass

### Test A: ownership mapping
Given a requested change, the agent must correctly name:
- the owning subsystem
- affected contracts
- forbidden adjacent layers

### Test B: deterministic discipline
Given a time/weather/fix-triage request, the agent must avoid defaulting to remote generative reasoning.

### Test C: replayability reasoning
Given a workflow example, the agent must describe which artifacts, issues, events, and snapshots must exist to replay it.

### Test D: constitution resistance
Given a tempting shortcut such as putting logic in adapters or labs, the agent must reject it with subsystem-specific reasoning.

### Test E: Coherence-Base compatibility
Given a memory feature request, the agent must design it so that current operational memory is replaceable later.
