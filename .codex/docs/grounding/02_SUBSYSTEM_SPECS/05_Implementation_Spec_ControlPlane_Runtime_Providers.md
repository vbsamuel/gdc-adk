# Implementation Specification: Control Plane, Runtime, and Providers

## 1. Control-plane purpose

The control plane is the decision authority. It must decide what type of execution a task needs before any model call happens.

## 2. Deterministic-before-LLM rule

Before an LLM is called, Forge-X must check:
1. is there a deterministic capability path?
2. is there a tool-backed path?
3. is there a reusable cached result?
4. is local reasoning sufficient?
5. is cloud fallback allowed by policy?

If any earlier path satisfies the request, later paths must not be invoked.

## 3. Required control-plane modules

At minimum:
- `policy.py`
- `router.py`
- `optimizer.py`
- `model_registry.py`
- `context_assembler.py`
- `gate_evaluator.py`

## 4. Provider selection policy

### Local-first default
Default routing order should be:
1. deterministic capability
2. cached result
3. local provider chain (ollama, llamacpp)
4. remote provider chain if explicitly allowed

### Cloud fallback
Cloud providers may be used only when:
- local path is unavailable or failed
- policy allows it for this task type
- the task is not explicitly local-only

## 5. Runtime responsibilities

Runtime owns:
- active local model lifecycle
- warming/unloading
- serialization constraints
- backpressure and cooldown handling
- retries with bounded limits

Runtime does not own workflow semantics or policy.

## 6. Provider requirements

Every provider adapter must expose consistent semantics:
- `is_available()`
- `generate(request)`
- stable response object with provider and model attribution

Provider adapters must not:
- choose themselves
- decide task type
- own issue or artifact creation
- own workflow retries

## 7. Context assembly requirements

Context assembly must not dump every available artifact into prompt text. It must be selective.

Assembly priorities should include:
- current request
- active workflow state
- directly linked artifact evidence
- open issue context
- relevant continuity snapshots
- review findings or prior corrections
- reusable context blocks by score and budget

The assembler must be able to operate under size or token budgets.
