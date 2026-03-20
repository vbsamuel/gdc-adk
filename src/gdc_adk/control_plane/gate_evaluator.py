from __future__ import annotations

from dataclasses import dataclass

from gdc_adk.config.settings import CLOUD_PROVIDER_NAMES


@dataclass(frozen=True)
class GateEvaluationResult:
    status: str
    provider_name: str
    message: str
    error_code: str | None = None


def evaluate_provider_gate(provider_name: str, allow_cloud_provider: bool) -> GateEvaluationResult:
    if provider_name in CLOUD_PROVIDER_NAMES and not allow_cloud_provider:
        return GateEvaluationResult(
            status="rejected",
            provider_name=provider_name,
            message=f"Cloud provider '{provider_name}' is disallowed by routing policy.",
            error_code="cloud_provider_disallowed",
        )
    return GateEvaluationResult(
        status="success",
        provider_name=provider_name,
        message=f"Provider '{provider_name}' passed routing gate evaluation.",
    )
