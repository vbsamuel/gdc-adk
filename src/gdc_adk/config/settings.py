from pydantic_settings import BaseSettings
import os
import yaml
from typing import Optional

class Settings(BaseSettings):
    ENV: str = "development"
    LOG_LEVEL: str = "INFO"
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    API_PREFIX: str = "/api"
    GEMINI_API_KEY: Optional[str] = None

    class Config:
        env_file = ".env"

def load_gemini_model(config_paths=("config.yaml", "config.example.yaml")) -> str:
    for path in config_paths:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f)
            google_cfg = config.get("ai_providers", {}).get("google", {})
            model = google_cfg.get("model", "")
            # Do not treat ${GEMINI_API_KEY} as a real key
            if model:
                return model
    return ""

def get_gemini_config_or_fail() -> dict:
    settings = Settings()
    model = load_gemini_model()
    if not model or " " in model or "gemini-progemini" in model:
        raise ValueError(f"Invalid Gemini model value: {model!r}")
    api_key = settings.GEMINI_API_KEY
    if not api_key or not isinstance(api_key, str) or api_key.strip() == "" or api_key.strip().startswith("${"):
        raise ValueError("GEMINI_API_KEY must be set in the environment and not as a template value.")
    if not model:
        raise ValueError("Gemini model must be set in config.yaml or config.example.yaml under ai_providers.google.model.")
    return {"api_key": api_key, "model": model}
