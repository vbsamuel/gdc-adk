# Tests only: `src/gdc_adk/workflows/agent_roles.py`

## Required assertions
- allowed roles are finite and explicit
- each required role exists
- each role has allowed actions and forbidden actions
- each role has explicit allowed handoff targets
- no role owns full lifecycle by itself
- reviewer role remains distinct in authority from author/executor paths for non-trivial artifacts
- dynamic unknown role lookup fails explicitly
- permission expansion is not implicit
