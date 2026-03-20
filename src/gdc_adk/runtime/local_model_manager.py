from __future__ import annotations

from dataclasses import dataclass

from gdc_adk.config.settings import get_runtime_settings


@dataclass(frozen=True)
class LocalModelState:
    provider_name: str | None
    model_name: str | None


@dataclass(frozen=True)
class LocalModelRuntimePolicy:
    max_concurrent_models: int
    unload_after_request: bool
    ollama_keep_alive: int
    prefer_warm_model: bool
    allow_backend_switch: bool


_LOCAL_MODEL_STATE = LocalModelState(provider_name=None, model_name=None)


def get_active_local_model() -> LocalModelState:
    return _LOCAL_MODEL_STATE


def activate_local_model(provider_name: str, model_name: str) -> LocalModelState:
    global _LOCAL_MODEL_STATE
    if not provider_name.strip() or not model_name.strip():
        raise ValueError("provider_name and model_name must be non-empty")
    _LOCAL_MODEL_STATE = LocalModelState(provider_name=provider_name, model_name=model_name)
    return _LOCAL_MODEL_STATE


def clear_active_local_model() -> LocalModelState:
    global _LOCAL_MODEL_STATE
    _LOCAL_MODEL_STATE = LocalModelState(provider_name=None, model_name=None)
    return _LOCAL_MODEL_STATE


def export_local_model_state() -> LocalModelState:
    return _LOCAL_MODEL_STATE


def load_local_model_state(state: LocalModelState) -> LocalModelState:
    global _LOCAL_MODEL_STATE
    _LOCAL_MODEL_STATE = state
    return _LOCAL_MODEL_STATE


def get_local_model_runtime_policy() -> LocalModelRuntimePolicy:
    runtime_settings = get_runtime_settings()
    return LocalModelRuntimePolicy(
        max_concurrent_models=runtime_settings.max_concurrent_models,
        unload_after_request=runtime_settings.unload_after_request,
        ollama_keep_alive=runtime_settings.ollama_keep_alive,
        prefer_warm_model=runtime_settings.prefer_warm_model,
        allow_backend_switch=runtime_settings.allow_backend_switch,
    )
