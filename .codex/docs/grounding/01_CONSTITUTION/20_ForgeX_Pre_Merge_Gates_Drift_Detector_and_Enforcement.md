# Forge-X Pre-Merge Gates, Drift Detector, and Enforcement Pack

Generated: 2026-03-19T11:03:18Z

## Purpose

This document defines the enforcement layer that prevents repo churn, architectural drift, and false completion. It should eventually be implemented as CI checks, repo scripts, and review checklists, but the specification itself is binding now.

---

## 1. Pre-merge gate categories

Every non-trivial change must pass these gates:

### G1. Constitution gate
Checks:
- file placed in correct subsystem
- no forbidden import direction
- no adapters or labs contain business logic
- no providers contain routing semantics

### G2. Naming and taxonomy gate
Checks:
- file names follow subsystem conventions
- event/issue/finding/workflow types use controlled taxonomy
- no banned filenames such as `helpers.py`, `misc.py`, `temp.py`

### G3. Contract gate
Checks:
- affected objects preserve required fields
- new objects are serializable
- changes do not silently break downstream contract expectations

### G4. Local-first gate
Checks:
- deterministic-first path still exists where required
- local providers remain first in allowed chains
- cloud fallback appears only where policy allows

### G5. Workflow state gate
Checks:
- non-trivial workflow changes preserve explicit state transitions
- iterative/fix-flow work does not hide state in prompt text

### G6. Review spine gate
Checks:
- reviewable artifacts can create findings
- fix-flow paths create issues
- revised outputs preserve lineage

### G7. Replayability gate
Checks:
- artifacts, issues, events, and continuity snapshots are sufficient to reconstruct a run
- no critical state trapped in runtime-only objects

### G8. Golden scenario gate
Checks:
- deterministic single-query scenario
- local-first reasoning scenario
- fix-flow issue scenario
- iterative refinement scenario
continue to pass

---

## 2. Drift detector rules

The drift detector should flag or fail on the following patterns.

### Rule D1: hardcoded provider/model in wrong layer
Flag when:
- adapters contain literal model names or provider URLs
- labs contain provider selection logic

### Rule D2: provider-to-workflow import
Fail when:
- any file under `providers/` imports `workflows/`

### Rule D3: adapter-owned logic
Flag when:
- adapters define domain logic, routing logic, or workflow state mutation beyond thin bridging

### Rule D4: hidden-state prompt chaining
Flag when:
- comments or code indicate “remember previous issue in prompt” instead of using continuity or context blocks

### Rule D5: banned filenames
Flag when files are introduced such as:
- `helpers.py`
- `misc.py`
- `tmp.py`
- `final.py`
- `new_core.py`

### Rule D6: no issue in fix-flow
Fail when:
- a fix-flow path does not create or bind to an issue

### Rule D7: no finding in reviewable flow
Fail when:
- review or validation logic emits prose without structured findings in flows that require reviewability

### Rule D8: cloud-first regression
Fail when:
- routing defaults to remote provider for tasks intended to remain local-first

### Rule D9: no artifact lineage on revision
Fail when:
- revised artifact replaces previous artifact without parent linkage

### Rule D10: non-serializable continuity
Fail when:
- iterative state depends on runtime object references or hidden chat state only

---

## 3. Suggested implementation checks

These checks should eventually become scripts.

### Static checks
- grep for banned filenames
- grep for hardcoded provider/model literals in adapters and labs
- import graph check for forbidden directions
- enum/taxonomy string scan for uncontrolled values

### Dynamic checks
- run deterministic time/weather scenario and assert no remote provider usage
- run fix-flow scenario and assert issue creation
- run iterative scenario and assert continuity snapshot plus artifact lineage
- simulate local provider failure and assert policy-governed fallback behavior

### Contract checks
- serialize all core object shapes to JSON
- verify required fields exist
- verify workflow state transitions only use known state values

---

## 4. Review checklist for human or reviewer agent

Before approving a change, answer all of the following:

1. What subsystem owns the change?
2. Does any code appear in adapters or labs that belongs in core?
3. Are any provider, model, or URL literals in the wrong layer?
4. Which requirement IDs from the traceability matrix are affected?
5. Which golden scenarios must be rerun?
6. Are artifacts, issues, findings, and continuity still replayable?
7. Does this move Forge-X closer to or further from Coherence-Base compatibility?

Approval is blocked if any answer is unknown without rationale.

---

## 5. Merge disposition values

Use:
- `approved`
- `approved_with_findings`
- `blocked`
- `rework_required`

Do not use vague approvals like:
- “looks okay”
- “probably fine”
- “ship it” without gate evidence

---

## 6. Minimum enforcement roadmap

### Phase 1
Manual use of this document as review checklist.

### Phase 2
Simple repo scripts for banned files/imports/hardcoded literals.

### Phase 3
Golden scenario runner for deterministic/local/fix/iterative flows.

### Phase 4
CI blocking on constitution, contract, and drift violations.
