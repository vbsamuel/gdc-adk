# Tests only: `src/gdc_adk/memory/context_store.py`

## Required assertions
- valid context block can be stored
- stored context block can be retrieved by ID
- context blocks can be listed by source artifact
- supersession preserves prior traceability
- export bundle is serializable
- source artifact linkage is preserved
- invalid context block shape rejects explicitly
- context does not exist only as hidden prompt snippets
