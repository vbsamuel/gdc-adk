# G3 Control Plane Acceptance Review

Review the Stage 2 implementation against Gate G3 only.

Do not evaluate Stage 3, Stage 4, Stage 5, or Stage 6 behavior.

## Verify

### Scenario A routing obligations
- deterministic candidate detection exists
- deterministic path classification occurs before provider routing
- no remote model is called first for deterministic-eligible task types

### Scenario B local-first obligations
- local provider is default
- provider/model attribution is normalized
- runtime local-model lifecycle surface is explicit

### Scenario G failover obligations
- local checked first
- failure chain preserved
- cloud used only if policy allows
- local-only task never escalates to cloud

## Output format
Produce structured findings only:
- pass
- fail
- missing evidence
- constitution violation
- provider/control-plane boundary violation
- traceability gap
- definition-of-done gap
