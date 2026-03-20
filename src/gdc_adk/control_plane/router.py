from __future__ import annotations

from dataclasses import dataclass, field

from gdc_adk.control_plane.gate_evaluator import evaluate_provider_gate
from gdc_adk.control_plane.model_registry import list_cloud_provider_names, list_local_provider_names, select_default_provider_name
from gdc_adk.control_plane.policy import RoutingPolicyRequest, evaluate_routing_policy
from gdc_adk.providers.weather.router import select_weather_provider


@dataclass(frozen=True)
class RouteRequest:
    task_type: str
    prompt: str = ""
    allow_cloud_override: bool = False


@dataclass(frozen=True)
class RouteDecision:
    status: str
    task_type: str
    selected_path: str
    provider_chain: tuple[str, ...] = ()
    deterministic_capability_name: str | None = None
    weather_provider_name: str | None = None
    message: str = ""
    error_code: str | None = None
    warnings: tuple[str, ...] = field(default_factory=tuple)


def select_provider_failover_chain(allow_cloud_provider: bool) -> tuple[str, ...]:
    local_provider_names = list_local_provider_names()
    cloud_provider_names = list_cloud_provider_names()
    provider_chain = list(local_provider_names)

    default_provider_name = select_default_provider_name()
    if default_provider_name in provider_chain:
        provider_chain.remove(default_provider_name)
        provider_chain.insert(0, default_provider_name)

    if allow_cloud_provider:
        provider_chain.extend(provider_name for provider_name in cloud_provider_names if provider_name not in provider_chain)

    gated_provider_names: list[str] = []
    for provider_name in provider_chain:
        gate_result = evaluate_provider_gate(provider_name, allow_cloud_provider)
        if gate_result.status == "success":
            gated_provider_names.append(provider_name)

    return tuple(gated_provider_names)


def route_request(request: RouteRequest) -> RouteDecision:
    policy_decision = evaluate_routing_policy(
        RoutingPolicyRequest(
            task_type=request.task_type,
            allow_cloud_override=request.allow_cloud_override,
        )
    )

    if policy_decision.status != "success":
        return RouteDecision(
            status=policy_decision.status,
            task_type=request.task_type,
            selected_path="rejected",
            message=policy_decision.rejection_reason or "Routing policy rejected the request.",
            error_code=policy_decision.error_code,
        )

    if policy_decision.deterministic_capability_name and not policy_decision.requires_weather_provider:
        return RouteDecision(
            status="success",
            task_type=request.task_type,
            selected_path="deterministic_capability",
            deterministic_capability_name=policy_decision.deterministic_capability_name,
            message=f"Selected deterministic capability '{policy_decision.deterministic_capability_name}'.",
        )

    if policy_decision.requires_weather_provider:
        weather_provider = select_weather_provider()
        return RouteDecision(
            status="success",
            task_type=request.task_type,
            selected_path="provider_backed_deterministic",
            deterministic_capability_name=policy_decision.deterministic_capability_name,
            weather_provider_name=weather_provider.provider_name,
            message=f"Selected weather provider '{weather_provider.provider_name}' through capability routing.",
        )

    provider_chain = select_provider_failover_chain(policy_decision.cloud_provider_allowed)
    if not provider_chain:
        return RouteDecision(
            status="rejected",
            task_type=request.task_type,
            selected_path="rejected",
            message="No providers are available for the requested routing policy.",
            error_code="no_provider_available",
        )

    selected_path = "cloud_fallback" if policy_decision.cloud_provider_allowed and provider_chain[0] in list_cloud_provider_names() else "local_reasoning"
    return RouteDecision(
        status="success",
        task_type=request.task_type,
        selected_path=selected_path,
        provider_chain=provider_chain,
        message="Selected provider failover chain in deterministic-before-LLM order.",
    )
