# Forge-X Platinum Grounding Pack

Generated: 2026-03-19T10:05:23Z

## Purpose

This pack is the **authoritative implementation grounding set** for Forge-X. It exists to stop drift, stop shallow rewrites, stop framework-centric architecture, and stop repo damage caused by unclear ownership boundaries.

Forge-X is **not**:
- an ADK-first project
- a Gemini-first project
- a generic agent framework
- a chat wrapper with tools

Forge-X **is**:
- a local-first coworker substrate
- a configurable execution system
- a workflow-native, issue-aware, review-driven platform
- a multi-modal ingress/egress system
- a durable orchestration layer for single-run, iterative, fix-flow, dynamic-flow, and fuzzy-logical-flow work

## How to use this pack in a new chat

1. Upload this zip.
2. In the first message, instruct the assistant to treat these markdown files as binding architecture and implementation control documents.
3. Require the assistant to cite exact file names and sections when proposing changes.
4. Require the assistant to state which file a proposed change belongs to before writing code.
5. Do not allow implementation before the assistant maps the requested change to the repo constitution and subsystem ownership matrix.

## Binding precedence

When there is conflict:
1. `01_ForgeX_System_Definition.md`
2. `02_Repo_Constitution_and_Ownership.md`
3. `03_Implementation_Spec_Core_Substrate.md`
4. `04_Implementation_Spec_Information_and_Memory.md`
5. `05_Implementation_Spec_ControlPlane_Runtime_Providers.md`
6. `06_Implementation_Spec_Workflows_Validation_Review.md`
7. `07_Data_Contracts_and_State_Models.md`
8. `08_Execution_Rules_and_Anti_Drift_Prompts.md`
9. `09_Implementation_Roadmap_and_Acceptance_Gates.md`

## Non-negotiable principles

- Local-first execution is the default.
- Deterministic and tool-backed execution must be attempted before LLM reasoning.
- External frameworks are adapters, not the architecture.
- All meaningful work must be represented as structured objects and replayable state.
- Review and validation must be independent from generation.
- Repo structure, object contracts, and workflow state are binding implementation controls, not optional guidance.
