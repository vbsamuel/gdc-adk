from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class OptimizationDecision:
    reuse_allowed: bool
    cache_key: str


def select_optimization_decision(task_type: str, payload: str) -> OptimizationDecision:
    reuse_allowed = task_type in {"time_lookup", "weather_lookup", "geo_lookup"}
    return OptimizationDecision(
        reuse_allowed=reuse_allowed,
        cache_key=f"{task_type}::{payload.strip().lower()}",
    )
