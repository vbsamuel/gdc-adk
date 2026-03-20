# Unit Coverage Requirements by File

## Purpose

Every public implementation file must have unit coverage that proves more than importability or happy-path output.

## Required unit coverage categories per file

For each public file in scope, cover:
1. primary success path
2. invalid input or contract failure path
3. boundary or edge condition
4. invariant preservation
5. typed output or exception semantics

## Coverage expectations by file family

### Core and substrate
- contract validation
- state transitions
- artifact creation and lineage behavior
- issue lifecycle rules
- dispatch behavior on supported and unsupported inputs

### Control plane and providers
- deterministic-first routing
- local-first routing
- cache hit / miss logic when applicable
- provider selection and fallback decisions
- provider failure surfacing

### Information plane
- ingestion of supported inputs
- canonicalization behavior
- indexing updates
- activation generation
- emitted artifact structure

### Workflows and validation
- workflow state transitions
- fix-flow verification behavior
- iterative revision linkage
- finding generation
- validation pass/fail outcomes

### Memory
- cache correctness
- context storage and retrieval
- continuity snapshot save/load
- replay/export behavior

### Multi-agent coordination
- handoff validation
- delegation guardrails
- governance blocks
- typed coordination outputs
