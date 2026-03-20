# Pre-Merge Gate Integration Prompt

```text
Run a full Forge-X pre-merge integration review.

Verify:
1. no missing stage prompts or required implementation files
2. no duplicate prompt contamination across stage packs
3. no missing required files from earlier bounded scope
4. no contract drift across stage boundaries
5. no unclaimed acceptance scenarios
6. no dangling traceability rows
7. no naming conflicts across stages
8. no hidden state or placeholder logic introduced

Return:
- gate-by-gate status
- blocking findings
- non-blocking findings
- final merge disposition
```
