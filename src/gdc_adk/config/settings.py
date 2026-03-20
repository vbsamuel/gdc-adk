from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


LOCAL_PROVIDER_NAMES: frozenset[str] = frozenset({"ollama", "llamacpp"})
CLOUD_PROVIDER_NAMES: frozenset[str] = frozenset({"google"})


@dataclass(frozen=True)
class ProviderSettings:
    provider_name: str
    enabled: bool
    model_name: str
    base_url: str | None
    api_key_env_var: str | None


@dataclass(frozen=True)
class RoutingSettings:
    default_provider_name: str
    failover_order: tuple[str, ...]
    allow_cloud_fallback: bool


@dataclass(frozen=True)
class RuntimeSettings:
    max_concurrent_models: int
    unload_after_request: bool
    ollama_keep_alive: int
    prefer_warm_model: bool
    allow_backend_switch: bool


@dataclass(frozen=True)
class WeatherProviderSettings:
    provider_name: str
    base_url: str


@dataclass(frozen=True)
class Stage2Settings:
    providers: dict[str, ProviderSettings]
    routing: RoutingSettings
    runtime: RuntimeSettings
    weather: WeatherProviderSettings


def require_env(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def _resolve_env_placeholders(value: Any) -> Any:
    if isinstance(value, str):
        resolved_value = value
        for env_name in os.environ:
            resolved_value = resolved_value.replace(f"${{{env_name}}}", os.environ[env_name])
        return resolved_value
    if isinstance(value, list):
        return [_resolve_env_placeholders(item) for item in value]
    if isinstance(value, dict):
        return {key: _resolve_env_placeholders(item) for key, item in value.items()}
    return value


def load_yaml_config() -> dict[str, Any]:
    for path in (_repo_root() / "config.yaml", _repo_root() / "config.example.yaml"):
        if path.exists():
            with path.open("r", encoding="utf-8") as file_handle:
                raw_config = yaml.safe_load(file_handle) or {}
            return _resolve_env_placeholders(raw_config)
    return {}


def reset_settings_cache() -> None:
    return None


def _load_provider_settings(config: dict[str, Any]) -> dict[str, ProviderSettings]:
    provider_config = config.get("ai_providers", {})
    if not isinstance(provider_config, dict):
        raise RuntimeError("ai_providers config must be a mapping")

    providers: dict[str, ProviderSettings] = {}
    for provider_name, raw_provider_config in provider_config.items():
        if not isinstance(raw_provider_config, dict):
            raise RuntimeError(f"Provider config for {provider_name} must be a mapping")
        api_key_env_var = None
        if provider_name == "google":
            api_key_env_var = "GEMINI_API_KEY"
        providers[provider_name] = ProviderSettings(
            provider_name=provider_name,
            enabled=bool(raw_provider_config.get("enabled", provider_name in CLOUD_PROVIDER_NAMES)),
            model_name=str(raw_provider_config.get("model", "")).strip(),
            base_url=str(raw_provider_config.get("base_url", "")).strip() or None,
            api_key_env_var=api_key_env_var,
        )
    return providers


def _load_routing_settings(config: dict[str, Any]) -> RoutingSettings:
    routing_config = config.get("routing", {})
    if not isinstance(routing_config, dict):
        raise RuntimeError("routing config must be a mapping")
    return RoutingSettings(
        default_provider_name=str(routing_config.get("default_provider", "ollama")).strip() or "ollama",
        failover_order=tuple(str(provider_name).strip() for provider_name in routing_config.get("failover_order", [])),
        allow_cloud_fallback=bool(routing_config.get("allow_cloud_fallback", False)),
    )


def _load_runtime_settings(config: dict[str, Any]) -> RuntimeSettings:
    runtime_config = config.get("runtime", {}).get("local_execution", {})
    if not isinstance(runtime_config, dict):
        raise RuntimeError("runtime.local_execution config must be a mapping")
    return RuntimeSettings(
        max_concurrent_models=int(runtime_config.get("max_concurrent_models", 1)),
        unload_after_request=bool(runtime_config.get("unload_after_request", True)),
        ollama_keep_alive=int(runtime_config.get("ollama_keep_alive", 0)),
        prefer_warm_model=bool(runtime_config.get("prefer_warm_model", True)),
        allow_backend_switch=bool(runtime_config.get("allow_backend_switch", True)),
    )


def _load_weather_settings(config: dict[str, Any]) -> WeatherProviderSettings:
    weather_config = config.get("weather", {})
    if not isinstance(weather_config, dict):
        raise RuntimeError("weather config must be a mapping")
    provider_name = str(weather_config.get("provider", "open_meteo")).strip() or "open_meteo"
    provider_config = weather_config.get(provider_name, {})
    if not isinstance(provider_config, dict):
        raise RuntimeError(f"weather provider config for {provider_name} must be a mapping")
    base_url = str(provider_config.get("base_url", "")).strip()
    if not base_url:
        raise RuntimeError(f"Missing base_url for weather provider: {provider_name}")
    return WeatherProviderSettings(provider_name=provider_name, base_url=base_url)


def load_stage2_settings() -> Stage2Settings:
    config = load_yaml_config()
    return Stage2Settings(
        providers=_load_provider_settings(config),
        routing=_load_routing_settings(config),
        runtime=_load_runtime_settings(config),
        weather=_load_weather_settings(config),
    )


def get_provider_settings(provider_name: str) -> ProviderSettings:
    settings = load_stage2_settings()
    if provider_name not in settings.providers:
        raise ValueError(f"Unsupported provider settings lookup: {provider_name}")
    return settings.providers[provider_name]


def get_routing_settings() -> RoutingSettings:
    return load_stage2_settings().routing


def get_runtime_settings() -> RuntimeSettings:
    return load_stage2_settings().runtime


def get_weather_provider_settings() -> WeatherProviderSettings:
    return load_stage2_settings().weather


def get_provider_config(provider_name: str) -> dict[str, Any]:
    provider_settings = get_provider_settings(provider_name)
    return {
        "enabled": provider_settings.enabled,
        "model": provider_settings.model_name,
        "base_url": provider_settings.base_url,
    }


def get_default_provider() -> str:
    return get_routing_settings().default_provider_name


def get_failover_order() -> list[str]:
    return list(get_routing_settings().failover_order)


def get_weather_provider_name() -> str:
    return get_weather_provider_settings().provider_name


def get_weather_provider_base_url(provider_name: str) -> str:
    weather_settings = get_weather_provider_settings()
    if weather_settings.provider_name != provider_name:
        raise RuntimeError(f"Unsupported weather provider: {provider_name}")
    return weather_settings.base_url
