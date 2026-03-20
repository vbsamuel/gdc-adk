# Tests only: `src/gdc_adk/config/settings.py`

## Required assertions
- repo-root config resolves correctly from repo root
- repo-root config resolves correctly from `labs/adk`
- missing config rejects explicitly
- malformed yaml rejects explicitly
- `get_provider_config` returns configured provider values
- `get_default_provider` returns declared default
- `get_failover_order` returns declared order
- unknown provider config lookup rejects explicitly
- `require_env` rejects missing secret
- weather provider config accessors return expected configured values
