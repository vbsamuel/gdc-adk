# Repo-Wide Definition of Done

A Forge-X change or release candidate is done only if all of the following are true:

## Stage packet integrity
- [ ] No missing stage prompts required by the operator model.
- [ ] No duplicate prompt contamination across stage packs.
- [ ] No stage packet contains prompts that belong to a different stage.

## Scope and file integrity
- [ ] No missing required files from earlier bounded scope.
- [ ] No new file has been introduced without subsystem ownership mapping.
- [ ] No naming conflict exists across stages or packs.

## Traceability and acceptance integrity
- [ ] No traceability row is left dangling for the changed scope.
- [ ] No acceptance scenario is left unclaimed when the relevant behavior exists.

## Code integrity
- [ ] No undocumented global variables or constants remain.
- [ ] No untyped public interfaces remain in the changed scope.
- [ ] No placeholder logic remains.
- [ ] No import-boundary violations remain.

## Test integrity
- [ ] No empty tests remain.
- [ ] No assertion-light smoke tests are standing in for behavior tests.
- [ ] Unit, integration, and end-to-end obligations are satisfied for the changed scope.

## State and continuity integrity
- [ ] No hidden state depends on prompt carry-forward.
- [ ] Replay and resume are explicit where relevant.

## Final disposition values
- approved
- approved_with_findings
- rework_required
- blocked
