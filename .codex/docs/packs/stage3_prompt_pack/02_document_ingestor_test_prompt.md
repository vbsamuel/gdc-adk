# Tests only: `src/gdc_adk/information_plane/ingestion/document_ingestor.py`

## Required assertions
- plain text input becomes a structured raw-signal object
- markdown-like input becomes a structured raw-signal object
- structured record input becomes a structured raw-signal object
- repo/code text input becomes a structured raw-signal object
- source metadata is preserved
- detected modality is preserved
- missing source metadata rejects explicitly if required by design
- unsupported payload shape rejects explicitly or is safely bounded by design
- raw output is serializable
- this file does not call providers
