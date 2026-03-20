# Integration Prompt A — ingest -> normalize -> artifactize -> index

Implement only the integration tests for:
- `information_plane/ingestion/document_ingestor.py`
- `information_plane/normalization/canonicalizer.py`
- `information_plane/indexing/artifact_index.py`

## Required assertions
- a raw text signal becomes a raw-signal object
- the raw-signal object becomes a normalized-signal object
- source/input artifact representation exists before activation
- normalized artifact representation exists when materially distinct
- the artifact is indexed
- artifact lookup by ID works
- text search can find the indexed artifact
- no provider call occurs in this path
