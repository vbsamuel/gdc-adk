# Tests only: `src/gdc_adk/information_plane/egress/artifact_emitter.py`

## Required assertions
- direct-answer emission is structured and includes artifact references
- generated-artifact emission is structured and includes artifact references
- issue-update emission is structured and includes artifact references
- workflow-status emission is structured and includes workflow linkage where applicable
- review-packet emission is structured
- handoff-package emission is structured
- provenance notes are preserved
- emission output is serializable
- emission cannot collapse into plain text only
