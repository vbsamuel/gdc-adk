from __future__ import annotations

from gdc_adk.capabilities.geo import resolve_city_location
from gdc_adk.providers.weather.base import WeatherProviderRequest, WeatherProviderResponse
from gdc_adk.providers.weather.router import select_weather_provider


def get_weather(city: str) -> WeatherProviderResponse:
    resolved_location = resolve_city_location(city)
    if resolved_location is None:
        return WeatherProviderResponse(
            status="rejected",
            city=None,
            timezone=None,
            report=f"Sorry, I could not resolve '{city}' to a supported city.",
            error_code="unknown_city",
        )
    weather_provider = select_weather_provider()
    return weather_provider.get_weather(
        WeatherProviderRequest(
            city=resolved_location["city"],
            latitude=resolved_location["latitude"],
            longitude=resolved_location["longitude"],
            timezone=resolved_location["timezone"],
        )
    )
