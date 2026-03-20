# Replay and Resume Integration Prompt

```text
Review replay and resume behavior across the full Forge-X stack.

Verify:
1. workflows can resume from explicit continuity snapshots
2. artifacts, issues, findings, and workflow state can be rehydrated coherently
3. replay respects bounded scopes where applicable
4. agent handoffs remain auditable after resume
5. no stage requires hidden prompt context to continue

Return:
- replay contract summary
- missing snapshot fields
- rehydration risks
- exact remediation list
```
