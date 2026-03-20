# Global Performance and Complexity Review Prompt

## Purpose

This prompt enforces engineering-first performance discipline. Forge-X must be functionally correct and operationally reasonable under realistic workloads.

## Operator prompt

```text
You are reviewing Forge-X for performance and complexity risk.

Before approving implementation, assess:
1. asymptotic complexity of key operations
2. repeated scans or repeated serialization across subsystem boundaries
3. avoidable duplicate indexing or duplicate replay work
4. synchronous blocking where bounded async or deferred design is more appropriate
5. oversized in-memory payload growth
6. unnecessary provider/model invocations when deterministic or cached paths exist
7. test suite cost explosion due to redundant combinatorics

For each risk found, provide:
- risk id
- file
- operation
- complexity or runtime concern
- likely production effect
- exact remediation
```

## Required performance rules
- deterministic-before-LLM routing must reduce unnecessary model calls
- indexing must not rescan entire artifact history for every request without justification
- replay must operate on bounded scopes when possible
- logging must be structured without exploding payload size
- large workflows must not persist full duplicate blobs repeatedly when lineage references suffice

## Reject if
- implementation is correct but obviously quadratic or worse on an avoidable hot path
- provider fallback loops can explode without bounded retries
- replay or continuity rebuild requires full system scans for routine resume operations
