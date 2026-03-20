# Tests only: `src/gdc_adk/information_plane/normalization/canonicalizer.py`

## Required assertions
- a valid raw-signal object becomes a normalized-signal object
- `normalized_type` is present
- `source_kind` is present
- `extracted_text` is present when available
- `modality_metadata` is present
- `timestamps` is preserved when known
- `provenance_notes` is preserved
- `confidence` is present when extraction quality is uncertain
- the output is serializable
- invalid raw-signal shape rejects explicitly
- normalization cannot silently return raw payload unchanged without normalized fields
