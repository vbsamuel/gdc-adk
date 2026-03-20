# Tests only: `src/gdc_adk/substrate/versioning.py`

## Required assertions
- `create_version_record` stores a version entry
- `get_version_history` returns ordered version history
- duplicate version number rejects
- `mark_artifact_superseded` records successor linkage
- superseding an artifact with itself rejects
- prior history remains accessible after supersession
