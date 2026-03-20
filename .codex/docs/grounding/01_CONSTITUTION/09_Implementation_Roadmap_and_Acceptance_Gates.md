# Implementation Roadmap and Acceptance Gates

## 1. Roadmap order

This order is mandatory unless a later step is explicitly blocked on a missing earlier primitive.

### Stage 1: Core contracts and substrate
Implement:
- canonical object contracts
- artifact store
- issue tracker
- event spine
- dispatch system

Acceptance gate:
- requests can create artifacts and issues deterministically
- workflow entry is traceable

### Stage 2: Control plane and providers
Implement:
- local-first routing
- deterministic-before-LLM checks
- provider selection and failover
- local runtime lifecycle

Acceptance gate:
- local provider is default
- cloud is fallback only
- task type determines allowed provider classes

### Stage 3: Information plane
Implement:
- ingestion
- normalization
- indexing
- activation
- egress

Acceptance gate:
- a raw signal becomes a normalized artifact and workflow activation output

### Stage 4: Workflow engine and review spine
Implement:
- workflow state machine
- review findings
- issue linkage
- reopen/close semantics

Acceptance gate:
- fix-flow and iterative flow can progress with structured state

### Stage 5: Memory contracts and operational memory
Implement:
- cache
- context store
- continuity snapshots
- replay/export semantics

Acceptance gate:
- workflows can resume with explicit continuity snapshots
- artifacts and context are migration-friendly

### Stage 6: Multi-agent orchestration
Implement:
- role contracts
- handoff semantics
- governance limits
- independent review agent path

Acceptance gate:
- no free-form unbounded loops
- all handoffs are artifact-mediated

## 2. Stop-ship failures

Do not proceed or merge if any of these exist:
- cloud-first routing by default
- adapter-owned business logic
- workflow state represented only in prose
- no issue creation for fix-flow
- no review findings for non-trivial artifacts
- hidden memory that cannot be replayed
- repo constitution violations
