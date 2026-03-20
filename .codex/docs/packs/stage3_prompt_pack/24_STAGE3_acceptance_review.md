# Stage 3 Acceptance Review

Review the Stage 3 implementation against the Stage 3 information-plane gate only.

Do not evaluate Stage 4, Stage 5, or Stage 6 behavior.

## Verify fully owned Stage 3 obligations

### Ingestion and canonicalization
- raw input is ingested first
- normalization is mandatory and cannot be skipped
- normalized signal contains the required canonical fields
- source artifact representation exists

### Indexing
- indexing is mandatory
- artifact ID lookup exists
- text search exists
- issue-linked lookup exists
- entity/alias and temporal indexing exist where applicable

### Activation
- activation category is structured
- candidate workflow mode is structured
- issue-trigger hint is explicit
- activation output is structured and serializable
- no workflow execution occurs in Stage 3

### Egress
- emission is structured
- artifact identity is preserved
- provenance is preserved
- plain-text-only collapse is not allowed

## Output format
Produce structured findings only:
- pass
- fail
- missing evidence
- constitution violation
- traceability gap
- replayability gap
- definition-of-done gap
