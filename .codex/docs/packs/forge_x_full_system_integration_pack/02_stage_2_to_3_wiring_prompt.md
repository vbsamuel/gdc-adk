# Stage 2 to Stage 3 Wiring Prompt

```text
Review and wire Forge-X Stage 2 and Stage 3 together.

Verify:
1. Information-plane activation outputs feed the control plane and capabilities without bypassing canonicalization.
2. Raw user text does not route directly to providers where Stage 3 must normalize first.
3. Indexing and activation produce structures that Stage 2 can consume deterministically.
4. Provider routing decisions retain access to normalized artifacts and provenance context.
5. No Stage 3 file absorbs control-plane policy responsibilities.

Required outputs:
- exact interface and payload boundaries
- missing normalized fields
- missing activation outputs
- improper dependency direction
- exact remediation list
```
