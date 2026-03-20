# Performance Regression Checks

## Required performance review targets
- repeated provider invocations avoided when deterministic or cache path exists
- indexing does not rescan more than necessary for routine operations
- replay/resume is bounded where possible
- logging is structured without excessive payload duplication
- fallback loops are bounded

## Required outputs for performance checks
- operation under review
- baseline behavior
- regression threshold
- test or benchmark method
- acceptance condition
