# Tests only: `src/gdc_adk/information_plane/indexing/artifact_index.py`

## Required assertions
- indexing a valid artifact makes it retrievable by artifact ID
- text search returns matching artifact references
- source-kind lookup returns matching artifact references
- issue-linked lookup returns matching artifact references
- entity or alias lookup works when alias data is present
- temporal lookup works when timestamps are present
- indexing invalid artifact input rejects explicitly
- indexing is not silently skipped
- index structures reference artifact identities rather than plain duplicated raw payload
