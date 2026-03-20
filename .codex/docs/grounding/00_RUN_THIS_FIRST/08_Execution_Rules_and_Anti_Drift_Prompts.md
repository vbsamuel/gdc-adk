# Execution Rules and Anti-Drift Prompts

## 1. Execution rules

These rules are binding for future implementation work.

### Rule A
Do not introduce a new top-level subsystem without mapping it to the repo constitution.

### Rule B
Do not place implementation logic into labs or adapters.

### Rule C
Do not call cloud providers by default when a deterministic or local path exists.

### Rule D
Do not represent state only as conversational memory. Use structured objects.

### Rule E
Do not claim a grounding or platinum package exists unless it contains real implementation-control substance.

## 2. Mandatory self-check before proposing code

Before writing any code, the assistant must answer:
1. Which subsystem owns this change?
2. Which existing contract does it extend or use?
3. Does this introduce a banned dependency direction?
4. Does it require an issue, finding, or workflow state update?
5. Is the path deterministic, local-first, or fallback?

## 3. New-chat grounding prompt

Use this at the top of a new chat:

"""
We are implementing Forge-X.

Treat the uploaded markdown grounding pack as binding architecture and implementation control.
Do not invent new structure.
Do not skip layers.
Do not default to cloud or LLM-first behavior.
Map every proposed change to:
- subsystem ownership
- object contracts
- workflow mode
- review and issue implications

If anything is unclear, stop and ask before producing code.
"""

## 4. Code-generation prompt

"""
Implement only the requested subsystem. Respect repo constitution, import directions, local-first routing, deterministic-before-LLM policy, and structured contracts. Do not modify unrelated files. Do not hide logic in adapters. All outputs must be implementation-grade, typed, and replayable.
"""

## 5. Review prompt

"""
Review the proposed implementation against the Forge-X grounding docs. Identify constitution violations, missing contracts, missing workflow state, missing review linkage, provider-policy violations, and future Coherence-Base incompatibilities. Produce structured findings, not prose only.
"""
