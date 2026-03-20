# Tests only: `src/gdc_adk/substrate/provenance.py`

## Required assertions
- `record_artifact_source` stores source metadata
- `get_artifact_provenance` returns source metadata
- `record_artifact_derivation` stores parent linkage
- derived artifact provenance preserves `parent_artifact_ids`
- non-dict source metadata rejects
- nonexistent artifact reference rejects
- nonexistent parent reference rejects
