# G1 Substrate Acceptance Prompt

Review the Stage 1 implementation against Gate G1 Core Substrate only.

Do not evaluate Stage 2+ behavior.

## Verify

### 1. Scenario A substrate obligations
- request artifact exists
- workflow entry exists
- events exist
- no hidden state is required

### 2. Scenario B substrate obligations
- request artifact exists
- workflow mode exists
- structured path is ready for later provider attribution without contract redesign

### 3. Scenario C full Stage 1 obligations
- request artifact exists
- workflow mode is `fix_flow`
- issue object exists
- issue is linked to artifact
- `issue_created` event exists
- workflow entry is explicit and traceable

## Output format
Produce structured findings only:
- pass
- fail
- missing evidence
- constitution violation
- traceability gap
- replayability gap
