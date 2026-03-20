# Integration Coverage Requirements by Subsystem Boundary

## Required subsystem boundaries

1. Stage 1 substrate ↔ Stage 2 control plane/providers
2. Stage 2 control plane/providers ↔ Stage 3 information plane
3. Stage 3 information plane ↔ Stage 4 workflows/validation
4. Stage 4 workflows/validation ↔ Stage 5 memory
5. Stage 5 memory ↔ Stage 6 multi-agent coordination

## For each boundary, verify
- contract compatibility
- artifact/issue/finding propagation when applicable
- no forbidden dependency direction
- observability continuity
- error propagation and typed failure behavior
- replay/lineage continuity if applicable

## Minimum integration test outputs
- involved files
- boundary contract asserted
- negative path asserted
- traceability rows affected
- acceptance scenario linkage
