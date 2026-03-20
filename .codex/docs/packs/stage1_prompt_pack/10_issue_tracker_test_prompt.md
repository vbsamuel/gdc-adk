# Tests only: `src/gdc_adk/substrate/issue_tracker.py`

## Required assertions
- `create_issue` stores a valid issue
- `get_issue` returns the stored issue
- `list_issues` returns created issues
- `list_issues_by_artifact_id` filters correctly
- duplicate `issue_id` rejects
- invalid issue status rejects
- `update_issue_status` changes status correctly
- resolved and closed remain distinct
- `reopen_issue` sets status to `reopened`
- `reopen_issue` increments `reopen_count`
- reopening an already open issue rejects
- `link_issue_to_artifact` persists related artifact linkage
