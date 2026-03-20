# Repo Constitution and Ownership

## 1. Canonical repo shape

The current repo may still be named `gdc-adk`, but the architecture identity is Forge-X. Until rename, the package path may remain `src/gdc_adk`, but all ownership rules below apply as if the package were `forge_x`.

Canonical core:

```text
src/gdc_adk/
  config/
  substrate/
  information_plane/
  control_plane/
  runtime/
  providers/
  capabilities/
  memory/
  validation/
  workflows/
  research/
  worldforge/
  adapters/
  core/

labs/
  adk/
```

## 2. Ownership matrix

### 2.1 config/
Owns:
- loading of repo-root config.yaml and .env
- accessors for provider, routing, and policy config
- no business logic
- no orchestration

Forbidden:
- direct provider execution
- issue creation
- workflow decisions

### 2.2 substrate/
Owns:
- event spine
- artifact store
- issue tracker
- dispatch entry contracts
- provenance linkage
- versioning metadata

Forbidden:
- model selection
- provider selection
- prompt assembly
- direct tool execution

### 2.3 information_plane/
Owns:
- ingress
- normalization
- indexing
- activation
- egress
- connectors
- modality transforms

Forbidden:
- provider-specific model execution
- long-horizon workflow orchestration
- policy ownership

### 2.4 control_plane/
Owns:
- task classification
- provider routing
- deterministic-before-LLM policy
- failover rules
- token and cache optimization policy
- context assembly
- autonomy boundaries
- gate evaluation

Forbidden:
- raw storage ownership
- artifact persistence implementation
- connector implementation

### 2.5 runtime/
Owns:
- local model lifecycle
- queueing
- retry behavior
- watchdogs
- execution isolation

Forbidden:
- repo config ownership
- workflow semantics
- validation policy ownership

### 2.6 providers/
Owns:
- backend-specific LLM or tool provider integrations
- transport and request/response mapping
- provider availability checks

Forbidden:
- deciding if provider should be used
- owning orchestration or workflow logic
- storing artifacts

### 2.7 capabilities/
Owns:
- stable domain actions
- deterministic or tool-backed skill logic
- domain-specific transforms that are reusable by workflows

Forbidden:
- provider routing
- issue state ownership
- direct UI/lab behavior

### 2.8 memory/
Owns:
- current operational cache
- context store
- continuity snapshots
- memory contracts
- replay/export structures for later Coherence-Base integration

Forbidden:
- direct coupling to one future memory backend
- hidden state that cannot be exported

### 2.9 validation/
Owns:
- review findings
- consistency checks
- drift checks
- traceability checks
- adversarial review functions

Forbidden:
- authoring the primary artifact under review
- mutating workflow policy

### 2.10 workflows/
Owns:
- workflow state machines
- execution sequencing
- phase transitions
- retry/reopen rules
- orchestration across capabilities and providers

Forbidden:
- provider internals
- connector implementations
- config loading

### 2.11 adapters/
Owns:
- thin external surfaces such as ADK, CLI, API, VS Code
- mapping external framework input/output into Forge-X calls

Forbidden:
- owning architecture
- hiding business logic in surface wrappers

## 3. Import direction rules

Allowed direction should generally be inward toward stable lower-level layers:

- adapters -> workflows / capabilities / control_plane
- workflows -> control_plane / capabilities / substrate / validation / memory
- control_plane -> config / providers / memory / validation
- information_plane -> substrate / memory / control_plane activation interfaces
- providers -> config / provider base contracts
- substrate -> internal substrate modules only

Forbidden examples:
- providers importing workflows
- labs importing provider internals directly
- adapters owning provider selection
- validation importing adapters

## 4. Drift bans

The following are explicitly banned:
- hardcoding model names in adapter files
- hardcoding provider URLs in adapter files
- duplicate routing logic across labs and core
- lab-level config files
- direct cloud-first orchestration by default
- implicit state hidden in chat only
- untyped issue handling
- review done by the same path that authored the artifact without independent finding objects
