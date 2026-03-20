from __future__ import annotations

from gdc_adk.providers.weather.base import WeatherProviderRequest, WeatherProviderResponse
from gdc_adk.providers.weather.router import select_weather_provider


def get_weather(city: str) -> WeatherProviderResponse:
    weather_provider = select_weather_provider()
    return weather_provider.get_weather(WeatherProviderRequest(city=city))
