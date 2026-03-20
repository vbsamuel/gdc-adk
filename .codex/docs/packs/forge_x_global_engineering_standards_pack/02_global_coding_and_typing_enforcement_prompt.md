# Global Coding and Typing Enforcement Prompt

## Purpose

This prompt enforces implementation-grade Python discipline across all Forge-X stages. The goal is explicit contracts, deterministic behavior, safe failure, and readability under review.

## Operator prompt

```text
You are reviewing or generating Forge-X Python code.

Apply the following coding and typing law:

1. All public functions must have explicit type annotations for parameters and returns.
2. Public models and result envelopes must be explicit typed structures.
3. Silent failure is forbidden.
4. Bare except is forbidden.
5. Import-time side effects are forbidden.
6. Hidden globals are forbidden.
7. Public interfaces must be deterministic and testable.
8. Any function with multiple responsibilities must be split.
9. Placeholder logic, TODO bodies, pass-only functions, and fake stubs are forbidden in accepted implementation.
10. Every non-trivial public function must document invariants through clear code structure and narrow exceptions.

Before producing code or approving code, report:
- missing type annotations
- untyped public returns
- broad exceptions
- import-time side effects
- hidden globals
- placeholder logic
- oversized functions needing decomposition
```

## Required standards

### Typing
- Use explicit `-> ReturnType` on all public functions.
- Use typed request and response models for provider boundaries.
- Use typed domain models for Artifact, Issue, WorkflowRun, ReviewFinding, Emission, and ContinuitySnapshot.

### Function design
- One bounded responsibility per public function.
- No mixed policy + transport + persistence in a single function.
- No file should own behavior outside its subsystem.

### Error behavior
- Raise explicit domain exceptions or return typed failure envelopes.
- Do not return `None` to signal contract failure unless the type makes that explicit and the caller is forced to branch on it.

### Configuration use
- No hardcoded secrets.
- No implicit environment reads in arbitrary functions. Centralize env resolution.

### Prohibited code patterns
- mutable module globals used as hidden state
- magic strings repeated across files when a controlled enum exists
- giant monolithic functions spanning routing, transformation, validation, and persistence
- catch-all `dict[str, Any]` as the public contract when a stable model exists

## Acceptance bar

Code is not implementation-grade if it merely imports and runs. It must be typed, bounded, side-effect-safe, and consistent with subsystem ownership.
