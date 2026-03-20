# Forge-X System Definition

## 1. System identity

Forge-X is a **local-first coworker engine**. It is designed to intake multi-modal information, classify work, assemble grounded context, select the correct execution mode, invoke deterministic capabilities and model providers under policy, persist artifacts and issues, and drive end-to-end work products through review and enhancement loops.

Forge-X is intended to support at least three high-value factory classes on one shared substrate:

### 1.1 Code Factory
Used for:
- architecture design
- technical specification generation
- test-case development
- code generation
- debugging
- remediation
- production hardening

### 1.2 Research / Product Definition Factory
Used for:
- document ingestion
- customer feedback synthesis
- product requirement analysis
- architecture option analysis
- technical specification authoring
- citation and evidence packaging

### 1.3 World / Simulation / Multimodal Factory
Used for:
- world building
- simulation-oriented design
- content authoring
- multimodal scene and concept generation
- asset and engine pipeline packaging

## 2. What Forge-X is not

Forge-X is not:
- a chat application that happens to call tools
- an SDK wrapper around Gemini, OpenAI, Claude, or ADK
- a purely prompt-driven autonomous loop with hidden state
- a repo that stores logic inside labs or adapters
- a cloud-first orchestration engine

## 3. Core execution modes

Forge-X must support five primary execution modes. These are not labels for UI. They are architecture-level workflow modes.

### 3.1 single_run
A one-shot request with bounded scope. Typical examples:
- summarize a document
- answer a grounded question
- produce a single artifact from explicit inputs

Characteristics:
- minimal state carry-forward
- deterministic routing first
- no long-horizon branching required

### 3.2 iterative
A repeated refinement mode where output evolves over multiple turns or passes.

Characteristics:
- continuity snapshots required
- issue and review findings feed next iteration
- delta tracking required

### 3.3 fix_flow
A remediation-oriented execution path.

Characteristics:
- explicit issue creation
- root-cause hypothesis or corrective action chain
- verification and closure or reopen loop

### 3.4 dynamic_flow
A workflow whose steps are adapted based on newly discovered information or intermediate outputs.

Characteristics:
- phase transitions are conditional
- tool and provider selection can branch
- state machine cannot be hardcoded to a single linear pass

### 3.5 fuzzy_logical_flow
A workflow for ambiguous, weakly specified, conflicting, or evolving requirements.

Characteristics:
- staged interpretation
- hypothesis capture
- contradiction handling
- uncertainty-aware progress
- review checkpoints before irreversible actions

## 4. Architectural thesis

Forge-X must be built around a durable substrate and information spine, not around conversational state.

The architecture must satisfy all of the following:
- structured ingress from multiple modalities
- stable object contracts
- explicit workflow state
- explicit issue and review linkage
- local-first model and tool routing
- future compatibility with Coherence-Base as the permanent memory and content inference layer

## 5. Future Coherence-Base compatibility

Forge-X must work now without Coherence-Base, but it must not be designed in a way that makes Coherence-Base integration expensive later.

This means:
- operational memory today must sit behind contracts
- all important information must be serializable and replayable
- no critical logic may depend on implicit chat history
- artifact, issue, context block, and continuity objects must be stable and portable
