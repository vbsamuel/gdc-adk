from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from gdc_adk.adapters.adk.external_contracts import (
    AdapterInvocationContext,
    ExternalErrorResponse,
    ExternalRequest,
    ExternalResponse,
)
from gdc_adk.adapters.adk.request_mapper import InternalAdapterRequest, map_external_request
from gdc_adk.adapters.adk.response_mapper import InternalAdapterResult, map_internal_error, map_internal_result


@dataclass(frozen=True)
class WeatherTimeAgentAdapter:
    adapter_name: str = "weather_time_agent"

    def handle_request(
        self,
        external_request: ExternalRequest,
        invocation_context: AdapterInvocationContext,
        handler: Callable[[InternalAdapterRequest], InternalAdapterResult],
    ) -> ExternalResponse | ExternalErrorResponse:
        if not callable(handler):
            raise ValueError("handler must be callable.")
        if invocation_context.adapter_name != self.adapter_name:
            raise ValueError("invocation_context.adapter_name must match the adapter name.")
        internal_request = map_external_request(external_request, invocation_context)
        internal_result = handler(internal_request)
        return map_internal_result(internal_result)


def build_weather_time_agent() -> WeatherTimeAgentAdapter:
    return WeatherTimeAgentAdapter()


def reject_adapter_misuse(request_id: str, error_message: str) -> ExternalErrorResponse:
    return map_internal_error(
        request_id=request_id,
        error_code="adapter_misuse_rejected",
        error_message=error_message,
    )
