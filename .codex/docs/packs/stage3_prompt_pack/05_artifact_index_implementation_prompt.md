# Global Control Header

Paste this header before each file-specific prompt:

```text
We are implementing Forge-X Stage 3 only.

Treat the uploaded markdown grounding files as binding system definition, repo constitution, execution law, and acceptance criteria.

This prompt is for one file only.

Before producing code:
1. identify the owning subsystem
2. identify the relevant contracts and interfaces required for this file
3. identify workflow modes affected
4. identify Stage 3 traceability rows advanced
5. identify acceptance assertions that must pass

Constraints:
- Do not introduce new architecture
- Do not expand scope beyond Stage 3
- Do not pull Stage 4, Stage 5, or Stage 6 responsibilities into this file
- Do not generate placeholder logic
- Do not merge responsibilities across subsystems
- Do not bypass canonicalization by sending raw user text directly into providers
- Do not treat indexing as optional
- Do not collapse emitted outputs into plain chat text only
- Do not modify unrelated files
- Do not hide logic in adapters or labs

Output implementation-grade Python code only for the requested file.
Respect repo constitution, import-direction rules, substrate contracts, information-plane ownership, controlled vocabularies, serializability, replayability, and file-level Definition of Done.
```

# Implement only: `src/gdc_adk/information_plane/indexing/artifact_index.py`

## Owning subsystem
- `information_plane`

## Responsibility
Maintain the mandatory searchable structures over artifacts and normalized content. Indexing is not optional in Forge-X.

## Required public functions
- `index_artifact(artifact, normalized_signal=None) -> None`
- `get_artifact_by_id(artifact_id) -> dict`
- `search_text(query_text) -> list[str]`
- `list_artifacts_by_source_kind(source_kind) -> list[str]`
- `list_artifacts_linked_to_issue(issue_id) -> list[str]`
- `search_by_entity_alias(alias_value) -> list[str]`
- `search_by_time_window(start_ts, end_ts) -> list[str]`

## Minimum required indexes
- artifact index
- textual search index
- entity or alias index where relevant
- temporal index where timestamps exist
- issue-linked artifact lookup

## Requirements
- indexing must happen for every meaningful normalized artifact
- artifact lookup by ID must be supported
- source linkage must be searchable
- issue-linked artifact lookup must be supported
- indexing must not duplicate raw payload unnecessarily outside artifact references
- future semantic indexing may be prepared as an extension point, but not substituted for required minimum indexes

## Must not contain
- provider logic
- workflow execution
- review finding logic
- bypass behavior that skips indexing in multi-turn architecture

## Definition of done
- searchable mappings exist for all required minimum index families
- indexing is mandatory and cannot be skipped by design
