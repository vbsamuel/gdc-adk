"""Stage 2 acceptance mapping for the current bounded slice.

Requirement mapping:
- FX-R001: Stage 2 settings load through explicit typed config contracts
- FX-R002: control plane enforces deterministic-first, local-first, and policy-gated cloud fallback
- FX-R003: providers expose typed request/response contracts and failover behavior
- FX-R004: time lookup resolves through deterministic capability before provider reasoning
- FX-R005: weather capability routes through provider abstraction
"""

from __future__ import annotations

import pytest

from gdc_adk.config import settings
from gdc_adk.control_plane.context_assembler import ContextAssemblyRequest, assemble_provider_context
from gdc_adk.control_plane.gate_evaluator import evaluate_provider_gate
from gdc_adk.control_plane.router import RouteRequest, route_request, select_provider_failover_chain
from gdc_adk.providers import router as provider_router
from gdc_adk.providers.base import LLMProvider, LLMRequest, LLMResponse, ProviderContractError, ProviderTransportError
from gdc_adk.providers.google_provider import GoogleProvider
from gdc_adk.providers.ollama_provider import OllamaProvider
from gdc_adk.providers.weather.base import WeatherProvider, WeatherProviderRequest, WeatherProviderResponse, WeatherProviderContractError
from gdc_adk.providers.weather.open_meteo import OpenMeteoWeatherProvider
from gdc_adk.runtime import local_model_manager
from gdc_adk.capabilities import weather as weather_capability
from gdc_adk.capabilities.time import get_current_time


@pytest.fixture(autouse=True)
def reset_stage2_state():
    settings.reset_settings_cache()
    local_model_manager.clear_active_local_model()


def test_stage2_settings_load_typed_contracts():
    stage2_settings = settings.load_stage2_settings()
    assert stage2_settings.routing.default_provider_name == "ollama"
    assert stage2_settings.runtime.max_concurrent_models == 1
    assert stage2_settings.weather.provider_name == "open_meteo"


def test_deterministic_capability_is_selected_before_provider_reasoning():
    route_decision = route_request(RouteRequest(task_type="time_lookup"))
    assert route_decision.selected_path == "deterministic_capability"
    assert route_decision.deterministic_capability_name == "time"


def test_unsupported_routing_hint_is_rejected():
    with pytest.raises(ValueError):
        route_request(RouteRequest(task_type="unsupported_task"))


def test_local_first_policy_is_enforced():
    route_decision = route_request(RouteRequest(task_type="general_reasoning"))
    assert route_decision.selected_path == "local_reasoning"
    assert route_decision.provider_chain[0] == "ollama"
    assert "google" not in route_decision.provider_chain


def test_cloud_fallback_occurs_only_when_policy_allows():
    without_cloud = route_request(RouteRequest(task_type="general_reasoning", allow_cloud_override=False))
    with_cloud = route_request(RouteRequest(task_type="general_reasoning", allow_cloud_override=True))
    assert "google" not in without_cloud.provider_chain
    assert "google" in with_cloud.provider_chain


def test_provider_failover_behaves_as_defined():
    class FailingProvider(LLMProvider):
        provider_name = "ollama"

        def is_available(self) -> bool:
            return True

        def generate_response(self, request: LLMRequest) -> LLMResponse:
            raise ProviderTransportError("local provider failed")

    class SucceedingProvider(LLMProvider):
        provider_name = "google"

        def is_available(self) -> bool:
            return True

        def generate_response(self, request: LLMRequest) -> LLMResponse:
            return LLMResponse(
                status="success",
                provider_name="google",
                model_name="gemini-2.5-flash",
                output_text="fallback succeeded",
                message="cloud fallback succeeded",
            )

    def provider_factory(provider_name: str) -> LLMProvider:
        if provider_name == "ollama":
            return FailingProvider()
        if provider_name == "google":
            return SucceedingProvider()
        raise ValueError(provider_name)

    response = provider_router.generate_with_provider_failover(
        request=LLMRequest(prompt="hello"),
        provider_chain=["ollama", "google"],
        provider_factory=provider_factory,
    )
    assert response.provider_name == "google"
    assert response.output_text == "fallback succeeded"


def test_provider_contract_rejects_invalid_input():
    with pytest.raises(ProviderContractError):
        OllamaProvider(transport=lambda payload: {"response": "ok"}).generate_response(LLMRequest(prompt=""))
    with pytest.raises(ProviderContractError):
        GoogleProvider(transport=lambda payload: {"text": "ok"}).generate_response(LLMRequest(prompt="", max_output_tokens=0))


def test_weather_routes_through_provider_abstraction(monkeypatch: pytest.MonkeyPatch):
    class StubWeatherProvider(WeatherProvider):
        provider_name = "stub_weather"

        def get_weather(self, request: WeatherProviderRequest) -> WeatherProviderResponse:
            return WeatherProviderResponse(
                status="success",
                city=request.city,
                timezone="UTC",
                report="stub weather response",
            )

    monkeypatch.setattr("gdc_adk.capabilities.weather.select_weather_provider", lambda: StubWeatherProvider())
    weather_result = weather_capability.get_weather("Paris")
    assert weather_result.report == "stub weather response"
    assert weather_result.city == "Paris"


def test_weather_provider_contract_rejects_invalid_input():
    with pytest.raises(WeatherProviderContractError):
        OpenMeteoWeatherProvider(transport=lambda url: {}).get_weather(WeatherProviderRequest(city=""))


def test_relevant_failure_paths_are_covered():
    weather_result = OpenMeteoWeatherProvider(transport=lambda url: {}).get_weather(WeatherProviderRequest(city="NotARealCity"))
    assert weather_result.status == "rejected"
    assert weather_result.error_code == "unknown_city"


def test_stage2_stateful_surfaces_use_public_lifecycle_contracts():
    active_model = local_model_manager.activate_local_model("ollama", "gemma3:12b-it-qat")
    assert active_model.provider_name == "ollama"
    exported_state = local_model_manager.export_local_model_state()
    local_model_manager.clear_active_local_model()
    assert local_model_manager.get_active_local_model().provider_name is None
    local_model_manager.load_local_model_state(exported_state)
    assert local_model_manager.get_active_local_model().model_name == "gemma3:12b-it-qat"


def test_context_assembly_and_gate_evaluation_are_typed():
    context_result = assemble_provider_context(
        ContextAssemblyRequest(prompt="hello", system_prompt="system", supporting_context=(" one ", ""))
    )
    assert context_result.prompt == "hello"
    assert context_result.supporting_context == ("one",)

    gate_result = evaluate_provider_gate("google", allow_cloud_provider=False)
    assert gate_result.status == "rejected"


def test_time_capability_returns_deterministic_result_for_supported_city():
    time_result = get_current_time("Paris")
    assert time_result["status"] == "success"
    assert time_result["timezone"]
