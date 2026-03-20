from __future__ import annotations


def classify_signal(text: str) -> str:
    t = text.lower()

    if any(x in t for x in ["bug", "broken", "fix", "error", "issue", "failed"]):
        return "fix_flow"

    if any(x in t for x in ["research", "analyze", "investigate", "study", "spec", "technical specification"]):
        return "research_flow"

    if any(x in t for x in ["build", "code", "implement", "python", "rust", "test case"]):
        return "code_flow"

    if any(x in t for x in ["world", "scene", "character", "physics", "simulation", "narrative"]):
        return "world_flow"

    return "single_run"
