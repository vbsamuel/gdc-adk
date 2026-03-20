# Global Import-Boundary and Dependency-Direction Enforcement Prompt

## Purpose

This prompt enforces repo constitution rules across all stages so that dependency direction remains stable and subsystems do not leak responsibilities across boundaries.

## Operator prompt

```text
You are reviewing Forge-X imports and dependency direction.

Apply the following law:

1. Lower layers must not import higher-layer orchestration.
2. Providers must not import workflows.
3. Validation must not import adapters.
4. Labs must not own core business logic.
5. Adapters must remain thin and must not own provider selection, policy, workflow state, or artifact semantics.
6. Information-plane modules must not absorb workflow-engine responsibilities.
7. Memory modules must not absorb provider routing responsibilities.
8. Multi-agent coordination must not bypass workflow, validation, or governance layers.

For each changed file, state:
- allowed imports
- forbidden imports
- upstream dependencies
- downstream dependents
- any detected boundary violation
```

## Allowed dependency direction

- `core` may be imported by all other implementation subsystems.
- `substrate` may be imported by control_plane, workflows, validation, memory, and information_plane when justified.
- `control_plane` may orchestrate providers and capabilities.
- `providers` may depend on provider base models and infrastructure, but not on workflows.
- `information_plane` may feed workflows through activation outputs, but should not own workflow engine logic.
- `validation` may inspect artifacts, issues, findings, workflow runs, and traceability records.
- `adapters` may call into stable subsystem APIs only.
- `labs` may exercise exposed interfaces but must not become implementation homes.

## Forbidden examples
- `providers/*.py` importing `workflows/*`
- `validation/*` importing `adapters/*`
- `labs/*` importing deep provider internals or owning routing logic
- `memory/*` reaching into provider implementations
- `information_plane/*` mutating workflow state directly without a defined workflow boundary

## Output required

For each violation:
- violation id
- file
- forbidden import or dependency direction
- reason it violates the constitution
- exact refactor recommendation
