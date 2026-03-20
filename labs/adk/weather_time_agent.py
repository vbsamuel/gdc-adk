from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from gdc_adk.adapters.adk.external_contracts import AdapterInvocationContext, ExternalRequest
from gdc_adk.adapters.adk.response_mapper import InternalAdapterResult
from gdc_adk.adapters.adk.weather_time_agent_adapter import WeatherTimeAgentAdapter, build_weather_time_agent


@dataclass(frozen=True)
class WeatherTimeAgentHarness:
    adapter: WeatherTimeAgentAdapter

    def invoke(
        self,
        external_request: ExternalRequest,
        invocation_context: AdapterInvocationContext,
        handler: Callable[[object], InternalAdapterResult],
    ):
        return self.adapter.handle_request(external_request, invocation_context, handler)


def build_weather_time_agent_harness() -> WeatherTimeAgentHarness:
    return WeatherTimeAgentHarness(adapter=build_weather_time_agent())
