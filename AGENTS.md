# AGENTS.md

## Purpose
This repository is for AI-agentic development and must maintain strict repository hygiene, zero secret leakage, and low-drift changes.

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
10. After changes, validate by:
   - checking the final file contents
   - running git diff
   - confirming no unintended files were modified

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

## Task execution style
1. First summarize the plan in 3 to 6 bullets.
2. Then inspect relevant files.
3. Then make only the requested change.
4. Then show validation results.
5. Then stop.