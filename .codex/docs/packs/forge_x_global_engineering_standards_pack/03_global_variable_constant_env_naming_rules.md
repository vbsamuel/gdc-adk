# Global Variable, Constant, and Environment Naming Rules

## Purpose

This document standardizes local variable names, constants, environment variables, IDs, and configuration keys to prevent ambiguity and hidden drift.

## Rules

### Local variables
- Use specific domain nouns: `artifact_id`, `workflow_run`, `provider_response`, `finding_status`.
- Avoid vague names: `data`, `thing`, `obj`, `res`, `tmp`, `value` when a domain noun exists.
- Loop variables must be semantically meaningful.

### Constants
- Module-level constants must use `UPPER_SNAKE_CASE`.
- Constant names must be domain-specific, e.g. `DEFAULT_PROVIDER_TIMEOUT_SECONDS`, `MAX_RETRY_ATTEMPTS`, `CANONICAL_VERSION`.
- Do not bury business-critical constants inside functions unless truly local.

### Environment variables
- Environment variables must use `FORGEX_` prefix unless referencing a third-party standardized name.
- Examples:
  - `FORGEX_GOOGLE_API_KEY`
  - `FORGEX_OLLAMA_BASE_URL`
  - `FORGEX_DEFAULT_PROVIDER`
  - `FORGEX_LOG_LEVEL`
- Do not read arbitrary env vars directly from deep subsystem functions.

### IDs and references
- Always use explicit suffixes:
  - `_id`
  - `_ids`
  - `_ref`
  - `_path`
  - `_status`
  - `_type`
- Examples:
  - `artifact_id`
  - `related_artifact_ids`
  - `workflow_run_id`
  - `provider_type`
  - `finding_severity`

### Boolean naming
- Use `is_*`, `has_*`, `can_*`, `should_*`.
- Avoid ambiguous booleans like `valid`, `ready`, or `done` without context.

### Time and duration naming
- Use suffixes to make units explicit:
  - `_at` for timestamps
  - `_seconds`, `_milliseconds`, `_minutes` for durations
- Examples:
  - `created_at`
  - `timeout_seconds`
  - `cooldown_minutes`

## Review checklist

Reject or rename if you see:
- overloaded `data` variables
- mixed units without suffixes
- booleans without semantic prefixes
- IDs without `_id` suffix
- constants that read like local variables
- environment variables without stable prefixing
