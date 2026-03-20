# Global Control Header

We are implementing Forge-X Stage 2 only.

Constraints:
- deterministic routing BEFORE any LLM usage
- no memory system (Stage 5)
- no multi-agent logic (Stage 6)
- no hidden state
- no provider-specific leakage into control plane

Output implementation-grade Python only.

Implement: control_plane/context_assembler.py

Responsibility:
- assemble deterministic input context

Functions:
- assemble_context(request, artifacts)

Rules:
- no hidden enrichment
- fully traceable inputs
