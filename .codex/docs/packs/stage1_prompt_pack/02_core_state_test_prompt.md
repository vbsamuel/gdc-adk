# Tests only: `src/gdc_adk/core/state.py`

## Required assertions
- all canonical workflow modes validate
- all canonical workflow states validate
- all canonical issue types validate
- all canonical issue statuses validate
- all canonical severities validate
- all canonical event types validate
- invalid synonyms reject explicitly
- `is_terminal_workflow_state("completed") is True`
- `is_terminal_workflow_state("executing") is False`
- `is_reopenable_issue_status("closed") is True`
- `is_reopenable_issue_status("open") is False`

Do not test unrelated files.
