# Tests only: `src/gdc_adk/control_plane/policy.py`

## Required assertions
- deterministic task types classify through `is_deterministic_candidate`
- local-first eligible task types return true for `should_use_local`
- cloud-eligible task types return true for `allow_cloud`
- local-only task types return true for `is_local_only_task`
- local-only task does not imply cloud permission
- unknown task type fails explicitly or is safely bounded by design
- no implicit cloud-first fallback is possible
