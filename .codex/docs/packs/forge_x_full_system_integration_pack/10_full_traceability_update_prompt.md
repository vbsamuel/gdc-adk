# Full Traceability Update Prompt

```text
Update Forge-X traceability across the full integrated system.

For every affected requirement row:
- identify owning subsystem
- identify owning files
- identify contracts involved
- identify workflow modes affected
- identify acceptance scenarios that prove it
- identify observability requirements
- identify findings if not satisfied
- assign allowed status only: not_started, in_progress, partial, accepted, blocked

Return a full integrated traceability update, not stage-local fragments.
```
