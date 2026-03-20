from __future__ import annotations

from dataclasses import dataclass

from gdc_adk.config.settings import get_routing_settings


SUPPORTED_TASK_TYPES: frozenset[str] = frozenset(
    {
        "time_lookup",
        "weather_lookup",
        "geo_lookup",
        "general_reasoning",
        "local_reasoning",
    }
)
DETERMINISTIC_TASK_TYPES: frozenset[str] = frozenset({"time_lookup", "geo_lookup"})
PROVIDER_BACKED_DETERMINISTIC_TASK_TYPES: frozenset[str] = frozenset({"weather_lookup"})
LOCAL_FIRST_TASK_TYPES: frozenset[str] = frozenset({"general_reasoning", "local_reasoning"})


@dataclass(frozen=True)
class RoutingPolicyRequest:
    task_type: str
    allow_cloud_override: bool = False


@dataclass(frozen=True)
class RoutingPolicyDecision:
    status: str
    task_type: str
    deterministic_capability_name: str | None
    requires_weather_provider: bool
    local_provider_allowed: bool
    cloud_provider_allowed: bool
    rejection_reason: str | None = None
    error_code: str | None = None


def validate_task_type(task_type: str) -> str:
    if task_type not in SUPPORTED_TASK_TYPES:
        raise ValueError(f"Unsupported task_type: {task_type}")
    return task_type


def evaluate_routing_policy(request: RoutingPolicyRequest) -> RoutingPolicyDecision:
    task_type = validate_task_type(request.task_type)
    routing_settings = get_routing_settings()

    if task_type in DETERMINISTIC_TASK_TYPES:
        capability_name = "geo" if task_type == "geo_lookup" else "time"
        return RoutingPolicyDecision(
            status="success",
            task_type=task_type,
            deterministic_capability_name=capability_name,
            requires_weather_provider=False,
            local_provider_allowed=False,
            cloud_provider_allowed=False,
        )

    if task_type in PROVIDER_BACKED_DETERMINISTIC_TASK_TYPES:
        return RoutingPolicyDecision(
            status="success",
            task_type=task_type,
            deterministic_capability_name="weather",
            requires_weather_provider=True,
            local_provider_allowed=False,
            cloud_provider_allowed=False,
        )

    cloud_allowed = routing_settings.allow_cloud_fallback or request.allow_cloud_override
    return RoutingPolicyDecision(
        status="success",
        task_type=task_type,
        deterministic_capability_name=None,
        requires_weather_provider=False,
        local_provider_allowed=task_type in LOCAL_FIRST_TASK_TYPES,
        cloud_provider_allowed=cloud_allowed,
    )
