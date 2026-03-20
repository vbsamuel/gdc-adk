# Traceability Update Prompt — Stage 3

Update only the Stage 3 rows advanced by the implementation evidence.

## Rows in scope
- `FX-R006`
- `FX-R007`
- `FX-R008`
- `FX-R009`

## Explicit file mapping to use
- `FX-R006` -> `information_plane/ingestion/document_ingestor.py`, `information_plane/normalization/canonicalizer.py`
- `FX-R007` -> `information_plane/normalization/canonicalizer.py`, `information_plane/activation/workflow_activation.py` plus substrate artifact-store invocation path
- `FX-R008` -> `information_plane/activation/trigger_router.py`, `information_plane/activation/workflow_activation.py`
- `FX-R009` -> `information_plane/activation/workflow_activation.py`, `information_plane/egress/artifact_emitter.py`

## Observability evidence to reference where applicable
- `signal_ingested`
- `signal_normalized`
- `artifact_created`
- `artifact_indexed`
- `activation_classified`
- `artifact_emitted`

## For each row provide
- owning_files
- contracts_involved
- workflow_modes_affected
- acceptance_tests passed
- observability evidence
- remaining gaps
- completion_status

## Rules
- do not mark Stage 4+ rows complete
- do not mark full-system acceptance complete
- use bounded Stage 3 evidence only
