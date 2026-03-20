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

# Implement only: `src/gdc_adk/information_plane/ingestion/document_ingestor.py`

## Owning subsystem
- `information_plane`

## Responsibility
Ingest raw inputs and convert them into structured raw-signal objects with explicit modality and source attribution.

## Required public functions
- `ingest_text_signal(raw_text, source_metadata) -> dict`
- `ingest_document_signal(raw_payload, source_metadata) -> dict`
- `ingest_structured_signal(raw_record, source_metadata) -> dict`
- `detect_modality(raw_payload, source_metadata) -> str`

## Supported Stage 3 ingress assumptions
- plain text
- markdown
- document-derived text
- email-like text
- screenshot or transcript placeholders
- structured records
- repository or code text

## Required raw-signal fields
- `raw_signal_id`
- `source_kind`
- `detected_modality`
- `raw_payload`
- `source_metadata`
- `received_at`
- `provenance_notes`
- `extraction_status` if extraction quality is uncertain

## Requirements
- must identify modality before normalization
- must preserve source attribution
- must produce serializable raw-signal objects
- must be future-ready for multimodal growth through explicit modality values
- must not send raw user text directly to providers

## Must not contain
- provider calls
- workflow policy
- canonicalization logic
- indexing logic
- activation decisions
- egress emission logic

## Definition of done
- raw inputs become structured raw-signal objects
- source attribution is explicit
- modality is explicit
- raw input never bypasses the information plane
