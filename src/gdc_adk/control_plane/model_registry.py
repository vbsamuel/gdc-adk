from __future__ import annotations

from dataclasses import dataclass

from gdc_adk.config.settings import CLOUD_PROVIDER_NAMES, LOCAL_PROVIDER_NAMES, get_default_provider, load_stage2_settings


@dataclass(frozen=True)
class RegisteredProviderModel:
    provider_name: str
    model_name: str
    is_local: bool
    is_enabled: bool


def list_registered_provider_models() -> list[RegisteredProviderModel]:
    settings = load_stage2_settings()
    registered_models: list[RegisteredProviderModel] = []
    for provider_name, provider_settings in settings.providers.items():
        registered_models.append(
            RegisteredProviderModel(
                provider_name=provider_name,
                model_name=provider_settings.model_name,
                is_local=provider_name in LOCAL_PROVIDER_NAMES,
                is_enabled=provider_settings.enabled,
            )
        )
    return registered_models


def list_local_provider_names() -> list[str]:
    return [
        provider.provider_name
        for provider in list_registered_provider_models()
        if provider.is_local and provider.is_enabled and provider.model_name
    ]


def list_cloud_provider_names() -> list[str]:
    return [
        provider.provider_name
        for provider in list_registered_provider_models()
        if provider.provider_name in CLOUD_PROVIDER_NAMES and provider.is_enabled and provider.model_name
    ]


def select_default_provider_name() -> str:
    return get_default_provider()
