# GDC-ADK / Forge-X repository instructions

## Canonical grounding locations
Binding grounding documents live under:

- .codex/docs/grounding/
- .codex/docs/packs/

## Required startup reading
Before making changes, read:

1. .codex/docs/grounding/00_RUN_THIS_FIRST/13_Anti_Drift_Prompt_and_Work_Protocol.md
2. .codex/docs/grounding/01_CONSTITUTION/01_ForgeX_System_Definition.md
3. .codex/docs/grounding/01_CONSTITUTION/02_Repo_Constitution_and_Ownership.md
4. .codex/docs/grounding/01_CONSTITUTION/09_Implementation_Roadmap_and_Acceptance_Gates.md
5. .codex/docs/grounding/04_TRACEABILITY/18_ForgeX_Traceability_Matrix_Pack.md

## Global packs
Always follow:

- .codex/docs/packs/forge_x_global_engineering_standards_pack/
- .codex/docs/packs/forge_x_repo_wide_test_and_quality_pack/
- .codex/docs/packs/forge_x_repo_wide_final_gate_pack/

When a task crosses stage boundaries or requires end-to-end verification, also follow:

- .codex/docs/packs/forge_x_full_system_integration_pack/

## Stage packs
Use only one active stage pack at a time unless an explicitly approved cross-stage integration task is being executed.

Available stage packs:
- .codex/docs/packs/stage1_prompt_pack/
- .codex/docs/packs/stage2_prompt_pack/
- .codex/docs/packs/stage3_prompt_pack/
- .codex/docs/packs/stage4_prompt_pack/
- .codex/docs/packs/stage5_prompt_pack/
- .codex/docs/packs/stage6_prompt_pack/

## Mandatory stage order
Unless explicitly told to perform approved cross-stage integration work, follow this order:

1. Stage 1: contracts and substrate
2. Stage 2: control plane, runtime, providers, deterministic capabilities
3. Stage 3: information plane
4. Stage 4: workflows, validation, review spine
5. Stage 5: memory, continuity, replay
6. Stage 6: multi-agent coordination

Do not pull later-stage responsibilities into an earlier-stage task.

## Active stage rule
Before editing, identify the active stage pack and read:

- .codex/docs/packs/<active_stage_pack>/00_STAGE_SCOPE.md

Treat that file as the bounded execution contract for the current task.

## Global rules
1. Do not invent secrets, endpoints, URLs, API keys, callback URLs, tokens, service-account values, or environment variable values.
2. Only create or modify files explicitly requested in the task.
3. Prefer minimal, correct, high-confidence changes over broad refactors.
4. Before writing files, inspect the current repository structure and existing files that are directly relevant.
5. If an example or template file is needed, create a sanitized example only, never a real secret-bearing file.
6. Do not add placeholder production values.
7. Do not rename files or move directories unless explicitly asked.
8. Do not modify application code when the task is about repository hygiene or configuration only.
9. Preserve user intent exactly; do not broaden scope.
10. If a required dependency falls outside the bounded task scope, stop and report it before editing. Do not silently expand scope.
11. After changes, validate by:
   - checking the final file contents
   - running git diff
   - confirming no unintended files were modified

## Hard rules
- Do not introduce new architecture unless explicitly requested.
- Respect stage boundaries.
- Do not hide logic in adapters or labs.
- Do not default to cloud-first or LLM-first behavior.
- Do not use prose-only workflow state.
- Do not use placeholder logic, TODO stubs, or fake implementations as completion.
- Public interfaces must be typed.
- Follow naming, lexicology, variable, constant, environment, import-boundary, error-handling, logging, testing, and performance standards from the global packs.
- Do not claim completion without tests, acceptance mapping, and traceability alignment.
- Do not modify files outside the bounded task scope.

## Task execution style
1. First summarize the plan in 3 to 6 bullets.
2. Then inspect relevant files.
3. Then make only the requested change.
4. Then show validation results.
5. Then stop.

## Required pre-edit summary
Before editing, state:
- owning subsystem
- files to change
- relevant contracts
- workflow modes affected
- traceability rows advanced
- acceptance scenarios impacted

## Required post-edit validation
After edits:
- run targeted tests
- run relevant integration tests
- report blockers, findings, unresolved risks, and any remaining gaps
- state whether repo-wide final gate review is required before completion is claimed

## Completion rules
- No bounded slice is complete until relevant tests pass and acceptance mapping is stated.
- No stage is complete until relevant final gate checks are satisfied.
- No cross-stage task is complete until the full-system integration pack has been consulted and relevant integrated checks are reported.
- Do not claim “done” when work is only partially implemented, partially tested, or missing traceability alignment.

## Rules for .gitignore work
1. .gitignore must be MECE for AI-agentic development.
2. Cover these categories:
   - OS/editor noise
   - Python/runtime/build/cache
   - virtual environments
   - notebooks
   - env/secrets/credentials
   - AI provider config and agent tool state
   - local URL/endpoint/connection override files
   - local DB/state/vector stores
   - model artifacts/caches
   - datasets and generated outputs
   - logs/traces/evals
   - web build artifacts
   - infra/container leftovers
   - archives/backups
3. Do not ignore safe templates such as:
   - .env.example
   - *.example.json
   - *.example.yaml
   - *.example.yml
   - *.example.toml
4. If sensitive files are already tracked, report them; do not silently rewrite git history.