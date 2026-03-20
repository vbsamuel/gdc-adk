from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


class WeatherProviderContractError(ValueError):
    pass


@dataclass(frozen=True)
class WeatherProviderRequest:
    city: str
    latitude: float
    longitude: float
    timezone: str


@dataclass(frozen=True)
class WeatherProviderResponse:
    status: str
    city: str | None
    timezone: str | None
    report: str
    raw_payload: Any = None
    error_code: str | None = None


def validate_weather_provider_request(request: WeatherProviderRequest) -> WeatherProviderRequest:
    if not request.city.strip():
        raise WeatherProviderContractError("city must be non-empty")
    if not isinstance(request.latitude, float):
        raise WeatherProviderContractError("latitude must be float")
    if not isinstance(request.longitude, float):
        raise WeatherProviderContractError("longitude must be float")
    if not request.timezone.strip():
        raise WeatherProviderContractError("timezone must be non-empty")
    return request


class WeatherProvider(ABC):
    provider_name: str

    @abstractmethod
    def get_weather(self, request: WeatherProviderRequest) -> WeatherProviderResponse:
        raise NotImplementedError
