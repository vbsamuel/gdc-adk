# Forge-X Detailed Acceptance and End-to-End Test Catalog

Generated: 2026-03-19T10:34:38Z

## Purpose

This document defines **system-level acceptance**, not toy demos. It exists to answer: “How do we know Forge-X actually works from single query to multi-turn to multi-agent orchestration without drift?”

## 1. Global acceptance conditions

Forge-X is not accepted if:
- a single successful prompt works but artifacts/issues are missing
- deterministic tasks still go through a remote LLM by default
- multi-turn state only exists in prompt text
- review is prose only and not represented as findings
- fix-flow has no issue object
- cloud fallback occurs without policy permission
- labs contain logic required by the core system
- current memory implementation cannot be replaced later

## 2. Acceptance scenario matrix

### Scenario A: single deterministic capability request

#### Input
“What is the time in Tokyo?”

#### Expected system behavior
1. ingest raw text
2. normalize signal
3. create input artifact
4. classify as single_run or deterministic capability subpath
5. detect deterministic capability availability
6. resolve city/timezone
7. answer without unnecessary cloud generative reasoning
8. emit response envelope
9. append event(s)

#### Required artifacts and state
- input artifact exists
- event recorded
- no issue unless lookup fails or ambiguity exists
- response references deterministic path in traceable form

#### Fail conditions
- Gemini or other remote model called first
- no artifact created
- city name hallucinated when unresolved
- result cannot be replayed from stored state

### Scenario B: local reasoning single-run request

#### Input
“Summarize the local-first factory architecture”

#### Expected behavior
1. ingest and normalize
2. create artifact
3. classify as single_run
4. route through local provider first
5. response contains provider/model attribution in structured result
6. event(s) recorded

#### Acceptability notes
The content may still be generic if no grounded architecture artifact is attached yet. That is acceptable in this scenario only if the dispatch and routing path are correct.

#### Fail conditions
- cloud provider chosen before local despite local availability
- no provider attribution
- no stored activation/output linkage

### Scenario C: fix-flow bug report

#### Input
“This workflow is broken and needs a fix”

#### Expected behavior
1. artifact created for the report
2. `fix_flow` selected
3. issue object created
4. event spine records issue creation
5. workflow run can later attach evidence and remediation

#### Fail conditions
- only a conversational answer is produced
- no issue object
- no fix_flow activation state

### Scenario D: iterative spec refinement

#### Inputs
Turn 1: “Create a technical specification for the workflow engine”
Turn 2: “The spec missed workflow reopen rules and review findings”

#### Expected behavior
Turn 1:
- artifact created from request
- workflow mode chosen
- output artifact generated

Turn 2:
- prior artifact is still addressable
- iterative or fix-like refinement state is explicit
- review finding or issue can be created for missing reopen rules
- revised artifact links to prior artifact

#### Fail conditions
- second turn ignores first artifact completely
- revision overwrites old artifact with no lineage
- no finding or issue represents the miss

### Scenario E: research/spec grounding flow

#### Inputs
- one or more source documents
- user asks for product definition or technical specification synthesis

#### Expected behavior
1. source artifacts created
2. normalized searchable units created or indexed
3. research/spec flow selected
4. output artifact references source artifacts
5. review finding can later challenge unsupported claims

#### Fail conditions
- source materials are never artifactized
- output spec has no source linkage
- unsupported claims cannot be attached to findings

### Scenario F: world/multimodal activation placeholder

#### Input
A future image/screenshot or transcript-driven signal indicating multimodal work

#### Expected architecture behavior
Even if not fully implemented yet, the repo must already have:
- a place for the modality-specific ingestion path
- normalization path
- activation path
- artifact representation

#### Fail conditions
- modality work would require architecture restructuring because there is no designated information-plane slot

### Scenario G: provider fallback under policy

#### Setup
Local Ollama unavailable; task type is allowed cloud fallback.

#### Expected behavior
- local provider checked first
- provider failure captured
- cloud provider used only if allowed by policy
- structured error chain preserved if all fail

#### Fail conditions
- cloud is used first
- failure chain is lost
- local-only task still escalates to cloud

### Scenario H: review spine integration

#### Input
Generated artifact is found to have a grounding gap or architecture drift.

#### Expected behavior
- review finding object created
- finding linked to artifact
- issue optionally created from finding
- workflow can reopen or re-enter iterative flow

#### Fail conditions
- review exists only in prose
- no finding ID or linkage
- workflow state does not react to findings

### Scenario I: continuity snapshot for iterative work

#### Input
An iterative workflow after multiple passes.

#### Expected behavior
- continuity snapshot contains current state, related artifacts, open issues/findings
- snapshot is serializable
- future Coherence-Base can ingest equivalent structure later

#### Fail conditions
- continuity lives only in memory of one runtime object
- no exportable state exists

### Scenario J: multi-agent readiness

#### Preconditions
Before multi-agent is enabled, the following must already be true:
- typed artifacts
- typed issues
- typed findings
- workflow state machine
- explicit dispatch and review linkage

#### Acceptance behavior
A planner/executor/reviewer chain must exchange typed handoff artifacts, not hidden free-form chat state.

#### Fail conditions
- multiple agents share implicit state only
- no role boundaries
- no explicit handoff objects

## 3. File-by-file acceptance shortcuts

A file is not accepted because unit tests pass on happy path. It is accepted when:
- its owning subsystem is correct
- it satisfies its contract and negative cases
- it does not absorb responsibilities from neighboring layers
- it supports the end-to-end scenarios above

## 4. Completion gates by subsystem

### Gate G1: Core substrate
Pass only when scenarios A, B, C are traceable with artifacts/events/issues.

### Gate G2: Information plane
Pass only when ingestion -> normalization -> activation path exists for text and is extensible for additional modalities without repo redesign.

### Gate G3: Control plane
Pass only when deterministic/local-first policy is enforced under both success and failover cases.

### Gate G4: Memory
Pass only when snapshots and reusable state are serializable and not hidden.

### Gate G5: Review spine
Pass only when findings can exist independent from chat prose and are linked to artifacts/issues.

### Gate G6: Workflow engine
Pass only when iterative and fix-flow can preserve state, findings, and reopen semantics.

### Gate G7: Multi-agent
Pass only when typed handoff artifacts and bounded role contracts exist.

## 5. Stop-ship failures

Do not consider Forge-X implementation acceptable if any of these are present:
- adapter-owned orchestration
- provider-owned task selection
- cloud-first behavior
- hidden memory dependency
- no issue object in fix_flow
- no finding object in review
- no lineage between revised and previous artifacts
- no explicit workflow state
