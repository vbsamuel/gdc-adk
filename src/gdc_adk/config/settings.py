from pathlib import Path
from typing import Any, Optional

import yaml
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ENV: str = "development"
    LOG_LEVEL: str = "INFO"
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    API_PREFIX: str = "/api"

    GEMINI_API_KEY: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    OLLAMA_BASE_URL: str = "http://localhost:11434"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


def load_yaml_config(config_paths=("config.yaml", "config.example.yaml")) -> dict[str, Any]:
    for path_str in config_paths:
        path = Path(path_str)
        if path.exists():
            with path.open("r", encoding="utf-8") as f:
                return yaml.safe_load(f) or {}
    return {}


def get_local_execution_config() -> dict[str, Any]:
    config = load_yaml_config()
    runtime_cfg = config.get("runtime", {})
    local_cfg = runtime_cfg.get("local_execution", {})

    requested_max_concurrent_models = local_cfg.get("max_concurrent_models", 1)
    try:
        int(requested_max_concurrent_models)
    except (TypeError, ValueError):
        requested_max_concurrent_models = 1

    return {
        "max_concurrent_models": 1,
        "unload_after_request": bool(local_cfg.get("unload_after_request", True)),
        "ollama_keep_alive": local_cfg.get("ollama_keep_alive", 0),
        "prefer_warm_model": bool(local_cfg.get("prefer_warm_model", True)),
        "allow_backend_switch": bool(local_cfg.get("allow_backend_switch", True)),
    }


def get_provider_config_or_fail(provider: str) -> dict[str, Any]:
    settings = Settings()
    config = load_yaml_config()

    providers = config.get("ai_providers", {})
    provider_cfg = providers.get(provider, {})

    model = provider_cfg.get("model", "")
    if not model or " " in model or "${" in model:
        raise ValueError(f"Invalid model value for provider '{provider}': {model!r}")

    if provider == "google":
        api_key = settings.GEMINI_API_KEY
        if not api_key or api_key.strip() == "" or api_key.strip().startswith("${"):
            raise ValueError("GEMINI_API_KEY must be set in the environment.")
        return {"api_key": api_key, "model": model}

    if provider == "openai":
        api_key = settings.OPENAI_API_KEY
        if not api_key or api_key.strip() == "" or api_key.strip().startswith("${"):
            raise ValueError("OPENAI_API_KEY must be set in the environment.")
        return {"api_key": api_key, "model": model}

    if provider == "anthropic":
        api_key = settings.ANTHROPIC_API_KEY
        if not api_key or api_key.strip() == "" or api_key.strip().startswith("${"):
            raise ValueError("ANTHROPIC_API_KEY must be set in the environment.")
        return {"api_key": api_key, "model": model}

    if provider == "ollama":
        enabled = bool(provider_cfg.get("enabled", True))
        base_url = str(provider_cfg.get("base_url") or settings.OLLAMA_BASE_URL).rstrip("/")
        return {
            "enabled": enabled,
            "base_url": base_url,
            "model": model,
        }

    raise ValueError(f"Unsupported provider: {provider}")
