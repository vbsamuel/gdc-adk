# Global Anti-Pattern Rejection Prompt

## Purpose

This prompt operationalizes anti-pattern rejection across all stages. It is the global guard against local shortcuts that poison later integration.

## Operator prompt

```text
You are reviewing Forge-X for anti-patterns.

Reject or flag the implementation if you detect:
1. adapter-owned business logic
2. provider-owned routing or policy
3. cloud-first defaults where deterministic or local-first behavior is required
4. hidden prompt-state dependence for durable workflow or continuity semantics
5. prose-only review instead of ReviewFinding objects
6. fix-flow without a typed Issue object
7. artifact overwrite without lineage preservation
8. generic helpers dumping ground
9. new file introduction without ownership justification
10. hidden global mutable state
11. placeholder logic or fake tests
12. multi-agent behavior that acts as an unbounded swarm

For each anti-pattern, provide:
- anti_pattern_id
- file
- anti-pattern type
- why it is dangerous in Forge-X
- exact remediation
```

## Mandatory rejection behavior

Any of the following is stop-ship by default:
- hidden non-replayable continuity state
- provider routing logic inside providers themselves
- workflow progress stored only in prose or prompt context
- validation without independent finding objects for non-trivial artifacts
- undocumented new subsystem ownership
