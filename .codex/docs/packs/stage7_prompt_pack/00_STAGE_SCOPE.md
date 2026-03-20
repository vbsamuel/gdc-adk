# Stage 7 Scope

## Stage purpose
Implement Forge-X Stage 7 only: the adapter and external interface layer.

Stage 7 owns:
- typed external request and response boundaries
- thin adapter entry surfaces
- serialization and deserialization at the system boundary
- replay and reference envelope propagation across the external boundary
- adapter misuse protection
- strict consumption of Stage 4, Stage 5, and Stage 6 typed contracts

Stage 7 does not own:
- workflow business logic
- provider selection logic
- memory internals
- Stage 6 governance logic
- UI redesign
- any hypothetical Stage 8 or later behavior

## Owning subsystem
- `adapters`
- thin `labs/adk` harness surfaces only where explicitly approved by the bounded brief

## In-scope files and folders
Stage 7 work should be limited to approved adapter-boundary files such as:
- `src/gdc_adk/adapters/adk/`
- `labs/adk/`
- typed adapter-boundary contract and mapper files explicitly authorized by the bounded implementation brief
- `labs/adk` may host harnesses or test surfaces only; it must not become the canonical owner of external boundary contracts, mapping logic, replay envelopes, or production adapter behavior.

Stage 7 files may:
- define external request and response contracts
- map external requests into approved internal typed surfaces
- map approved internal typed results back into external responses
- preserve typed replay and reference envelopes
- reject malformed or disallowed adapter input before entering workflow business logic

## Out of scope
- redesign of Stage 1 substrate contracts or state stores
- redesign of Stage 2 routing, provider selection, or capability ownership
- redesign of Stage 3 information-plane ingestion or activation logic
- redesign of Stage 4 workflows, validation, review, or issue logic
- redesign of Stage 5 memory internals or replay internals
- redesign of Stage 6 handoff, governance, or role logic
- direct provider-specific orchestration in adapters
- hidden session state or prompt-only continuity
- UI or product-surface redesign beyond thin adapter contracts

## Invariants
1. Adapters must remain thin.
2. Adapters must not contain workflow business logic.
3. Adapters must not directly mutate memory internals.
4. Adapters must not directly call provider internals unless routed through approved typed surfaces.
5. External request and response boundaries must be typed and serializable.
6. Replay and reference information must be preserved through explicit envelopes, not hidden state.
7. No prompt-only continuity is allowed at the adapter boundary.
8. No hidden module-global adapter state is allowed.
9. Public adapter interfaces must be testable through typed contracts only.
10. Adapters must consume Stage 4, Stage 5, and Stage 6 outputs only through approved typed contracts.

## Anti-drift rules
Do not:
- hide workflow or governance logic in adapters
- bypass Stage 4 workflow surfaces
- bypass Stage 5 memory contracts
- bypass Stage 6 handoff or governance rules when replay-safe or delegated work is referenced
- introduce direct provider-specific coupling into the external contract layer
- expose weak dict-only public adapter boundaries when a typed contract is appropriate
- rely on implicit session state
- leak internal workflow, memory, provider, or runtime objects into the public boundary
- treat labs as architecture owners
- claim completion without boundary proofs, negative paths, and traceability alignment

## Required boundary proofs
Stage 7 must prove all of the following:
1. Stage 6 -> Stage 7 forward-boundary proof using real or contract-faithful Stage 6 handoff and coordination outputs only.
2. External request maps into approved internal typed surfaces without bypassing prior stages.
3. Internal typed results map back into external responses without leaking internal implementation details.
4. Replay and reference envelopes survive round-trip serialization.
5. Invalid or malformed external input is rejected before entering internal workflow or business logic.
6. Adapter misuse or bypass attempts are rejected explicitly.

## Required negative-path tests
Stage 7 test coverage must include:
- malformed external request rejection
- invalid replay or reference envelope rejection
- invalid response mapping input rejection
- adapter misuse or bypass attempt rejection
- provider-internal leakage rejection
- memory-internal leakage rejection
- Stage 6 contract mismatch rejection
- replay-envelope round-trip failure-path coverage
- confirmation that no private module-global mutation is required in tests

## Acceptance expectations
Stage 7 acceptance requires:
- typed external request and response contracts exist
- request mapping and response mapping responsibilities are separated cleanly
- replay and reference envelopes are explicit, typed, and serializable
- thin adapter entry surfaces do not absorb workflow, provider, memory, or governance business logic
- Stage 6 -> Stage 7 boundary proof exists
- replay-safe adapter round trip exists
- adapter misuse protection exists
- acceptance mapping is explicit in `tests/test_stage7.py`
- traceability alignment is explicit, or a missing Stage 7 row is reported as a formal blockage

## Definition of done
Stage 7 is not complete until:
- all approved Stage 7 files are implemented or updated within the bounded brief
- all public adapter boundary contracts are typed
- Stage 6 -> Stage 7 boundary proof exists
- replay-safe external boundary round trip exists
- malformed and misuse negative paths are covered
- no private-state mutation is required in tests
- no business logic is hidden in adapters or labs
- no hidden state exists at the adapter boundary
- traceability evidence is ready to record, or explicit Stage 7 traceability-row blockage is documented
- repo-wide final gate review has no Stage 7 adapter-boundary findings that would block closeout

## Likely review findings if violated
- `adapter_business_logic_violation`
- `adapter_boundary_contract_gap`
- `replay_envelope_gap`
- `stage6_boundary_bypass`
- `memory_boundary_bypass`
- `provider_boundary_leakage`
- `hidden_adapter_state`
- `weak_external_contract`
- `negative_path_coverage_gap`
- `traceability_gap`
