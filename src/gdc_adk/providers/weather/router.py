from __future__ import annotations

from gdc_adk.config.settings import get_weather_provider_settings

from .base import WeatherProvider
from .open_meteo import OpenMeteoWeatherProvider


def select_weather_provider() -> WeatherProvider:
    weather_settings = get_weather_provider_settings()
    if weather_settings.provider_name == "open_meteo":
        return OpenMeteoWeatherProvider()
    raise RuntimeError(f"Unsupported weather provider: {weather_settings.provider_name}")
