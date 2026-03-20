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

# Implement only: `src/gdc_adk/information_plane/normalization/canonicalizer.py`

## Owning subsystem
- `information_plane`

## Responsibility
Normalize raw-signal objects into stable canonical normalized-signal objects. This file owns canonicalization and must not be skipped.

## Required public functions
- `normalize_signal(raw_signal) -> dict`
- `canonicalize_text_payload(raw_signal) -> dict`
- `extract_text_if_available(raw_signal) -> str | None`

## Required normalized-signal fields
- `normalized_signal_id`
- `normalized_type`
- `source_kind`
- `extracted_text` if available
- `modality_metadata`
- `timestamps` if known
- `provenance_notes`
- `confidence` if extraction quality is uncertain

## Allowed additional fields
- `entity_candidates`
- `alias_candidates`
- `ambiguity_markers`
- `coarse_intent`
- `activation_hints`

## Requirements
- canonicalization must be deterministic
- no modality may skip canonicalization because a shortcut exists
- extracted text must be preserved when available
- provenance notes must survive normalization
- confidence must be present when extraction quality is uncertain
- output must be serializable and replay-friendly

## Artifact timing rule
This file must make it possible for downstream Stage 3 code to create:
- a source/input artifact
- a normalized artifact if the normalized representation is materially distinct

Do not postpone artifact representation until after activation.

## Must not contain
- provider calls
- workflow execution
- indexing logic
- provider routing
- hidden prompt-only state

## Definition of done
- every raw signal becomes a canonical normalized signal
- required normalized fields are present
- canonicalization cannot be bypassed
