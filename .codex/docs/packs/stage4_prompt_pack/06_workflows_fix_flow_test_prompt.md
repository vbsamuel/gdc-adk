# Tests only: `src/gdc_adk/workflows/fix_flow.py`

## Required assertions
- fix-flow cannot start without an issue ID
- `WorkflowRun.issue_ids` includes the linked issue
- remediation attempts preserve artifact linkage
- remediation evidence artifact IDs are recorded
- verification result is structured and includes issue/workflow/evidence linkage
- closure without evidence rejects explicitly
- closure without verification rejects explicitly
- reopen preserves history and reason
- verification failure can lead to reopen path
