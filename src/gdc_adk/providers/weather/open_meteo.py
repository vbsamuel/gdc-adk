from __future__ import annotations

import json
from collections.abc import Callable
from urllib.parse import urlencode
from urllib.request import urlopen

from gdc_adk.config.settings import get_weather_provider_settings

from .base import WeatherProvider, WeatherProviderRequest, WeatherProviderResponse, validate_weather_provider_request


class OpenMeteoWeatherProvider(WeatherProvider):
    provider_name = "open_meteo"

    def __init__(self, transport: Callable[[str], dict] | None = None) -> None:
        weather_settings = get_weather_provider_settings()
        self._transport = transport
        self._base_url = weather_settings.base_url

    def get_weather(self, request: WeatherProviderRequest) -> WeatherProviderResponse:
        validate_weather_provider_request(request)
        params = {
            "latitude": request.latitude,
            "longitude": request.longitude,
            "current": ",".join(
                [
                    "temperature_2m",
                    "apparent_temperature",
                    "precipitation",
                    "cloud_cover",
                    "wind_speed_10m",
                ]
            ),
            "timezone": "auto",
        }
        weather_url = f"{self._base_url}?{urlencode(params)}"

        try:
            if self._transport is not None:
                payload = self._transport(weather_url)
            else:
                with urlopen(weather_url, timeout=15) as response:
                    payload = json.loads(response.read().decode("utf-8"))
        except Exception as exc:
            return WeatherProviderResponse(
                status="failed",
                city=request.city,
                timezone=request.timezone,
                report=f"Weather provider request failed: {exc}",
                error_code="weather_provider_failed",
            )

        current_weather = payload.get("current", {})
        if not current_weather:
            return WeatherProviderResponse(
                status="failed",
                city=request.city,
                timezone=request.timezone,
                report="Weather provider returned no current weather data.",
                error_code="weather_provider_empty",
            )

        report = (
            f"Current weather in {request.city}: "
            f"temperature {current_weather.get('temperature_2m')} C, "
            f"feels like {current_weather.get('apparent_temperature')} C."
        )
        return WeatherProviderResponse(
            status="success",
            city=request.city,
            timezone=request.timezone,
            report=report,
            raw_payload=payload,
        )
