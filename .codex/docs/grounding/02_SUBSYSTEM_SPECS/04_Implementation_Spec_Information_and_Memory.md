# Implementation Specification: Information Plane and Memory

## 1. Information plane purpose

Forge-X cannot be a coworker without bidirectional information movement. The information plane converts raw external or user-originating signals into canonical internal forms that can activate workflows and later be emitted outward again.

## 2. Ingress categories

Forge-X must be designed to ingest, even if all connectors are not implemented on day one:

- plain text
- markdown
- PDF
- DOCX
- spreadsheet
- email
- voice transcript
- screenshot/image-derived text
- user feedback
- repository/code files
- structured records

## 3. Ingestion pipeline

Every ingress path must conceptually follow:

1. receive raw payload
2. identify modality
3. normalize into canonical representation
4. create artifact(s)
5. index searchable content
6. classify activation candidates
7. emit activation output to workflows or review spine

## 4. Normalization requirements

Normalization must produce:
- normalized_type
- source
- extracted text if available
- modality metadata
- timestamps if known
- provenance notes
- confidence if extraction quality is uncertain

No modality should skip canonicalization just because a shortcut exists.

## 5. Indexing requirements

Indexing is not optional if Forge-X is meant to work over multi-turn or multi-artifact context.

Minimum indexes:
- artifact index
- textual search index
- entity or alias index if relevant
- temporal index if timestamps exist
- issue-linked artifact lookup

## 6. Activation requirements

Activation maps normalized content to one or more next actions.

Examples:
- a bug report activates fix_flow
- a research request activates research_flow
- an architecture request activates code_flow or research_flow depending on configured mode
- a screenshot with visible error text activates fix_flow and evidence artifact creation

Activation output must be structured, not conversational.

## 7. Egress requirements

Forge-X must be able to emit:
- direct answer
- generated artifact
- review packet
- issue update
- workflow status
- package or handoff artifact

Egress must preserve provenance and artifact identity.

## 8. Memory purpose

The current memory layer is an operational layer, not the future permanent inference authority. It exists to support performance, continuity, and reuse until Coherence-Base becomes available.

## 9. Memory contracts

The current implementation must sit behind interfaces such as:
- MemoryStore
- ContextStore
- ContinuityStore

### MemoryStore
Used for cache-like retrieval of prior computed results.

### ContextStore
Used for reusable context blocks and grounding fragments.

### ContinuityStore
Used for workflow and session snapshots.

## 10. Coherence-Base compatibility requirements

Everything written by current memory must be:
- replayable
- serializable
- migration-friendly
- not coupled to one opaque storage shape

At minimum, these objects must be exportable:
- context blocks
- continuity snapshots
- issue-linked evidence references
- artifact summaries or chunk references
