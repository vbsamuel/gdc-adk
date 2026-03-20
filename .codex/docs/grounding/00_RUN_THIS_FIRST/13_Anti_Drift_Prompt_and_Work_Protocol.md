# Forge-X Anti-Drift Prompt and Work Protocol

## Purpose

These prompts and protocols are not writing aids. They are execution controls for future chats so the assistant cannot casually drift away from the actual engineering scope.

## 1. Start-of-chat protocol

Paste this before any implementation request:

```text
We are implementing Forge-X.

Treat the uploaded markdown grounding files as binding architecture and implementation control documents.

Before proposing code or restructuring:
1. identify the owning subsystem
2. identify the relevant object contracts
3. state which workflow mode(s) are affected
4. state whether the path is deterministic, local-first LLM, or cloud fallback
5. state any review, issue, or continuity implications

Do not introduce new architecture.
Do not hide logic in adapters or labs.
Do not default to cloud or LLM-first behavior.
If anything is unclear, ask before coding.
```

## 2. Implementation request protocol

```text
Implement only the requested subsystem. Respect repo constitution, import directions, local-first routing, deterministic-before-LLM policy, issue/review spine, and future Coherence-Base replaceability. Do not modify unrelated files. Output implementation-grade code only after stating the files to be changed and why those files own the change.
```

## 3. Review request protocol

```text
Review this implementation against the Forge-X grounding documents. Produce structured findings for:
- repo constitution violations
- missing contracts
- hidden state
- local-first policy violations
- provider misuse
- missing issue/review linkage
- non-replayable state
- Coherence-Base incompatibility
```

## 4. Repo change protocol

```text
Before any folder or file movement, produce a controlled migration plan that states:
- what is moving
- why the owning subsystem requires it
- what import paths are affected
- how runtime behavior is preserved
- what acceptance tests must pass after the move

Do not suggest repo nukes or fresh starts unless the current repo is provably unsalvageable.
```

## 5. Multi-agent enablement protocol

```text
Do not propose multi-agent execution until the following already exist:
- canonical object contracts
- workflow state machine
- issue tracker
- review finding objects
- typed handoff artifacts

When proposing multi-agent, define explicit roles, bounded authority, handoff objects, and stop conditions.
```

## 6. Minimum answer structure for future implementation chats

Every serious answer should include:
1. owning subsystem
2. affected files
3. relevant contracts
4. why this belongs here and not elsewhere
5. acceptance or validation implications
6. the code or migration itself
