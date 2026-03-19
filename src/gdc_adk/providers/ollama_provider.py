import requests

from .base import LLMProvider, LLMRequest, LLMResponse
from gdc_adk.config.settings import (
    get_local_execution_config,
    get_provider_config_or_fail,
)


class OllamaProvider(LLMProvider):
    name = "ollama"
    backend_name = "ollama"
    is_local_backend = True

    def __init__(self) -> None:
        provider_cfg = get_provider_config_or_fail("ollama")
        local_cfg = get_local_execution_config()

        self.base_url = provider_cfg["base_url"].rstrip("/")
        self.model = provider_cfg["model"]
        self.enabled = bool(provider_cfg.get("enabled", True))
        self.unload_after_request = bool(local_cfg["unload_after_request"])
        self.keep_alive = local_cfg["ollama_keep_alive"]

    def is_available(self) -> bool:
        if not self.enabled:
            return False
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=3)
            return response.ok
        except Exception:
            return False

    def _effective_keep_alive(self, keep_alive=None):
        if keep_alive is not None:
            return keep_alive
        if self.unload_after_request:
            return 0
        return self.keep_alive

    def _generate_payload(self, prompt: str, keep_alive=None) -> dict:
        return {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "keep_alive": self._effective_keep_alive(keep_alive),
        }

    def warm_model(self, keep_alive=None) -> None:
        warm_keep_alive = self._effective_keep_alive(keep_alive)
        if warm_keep_alive in (0, "0", "0s"):
            return

        response = requests.post(
            f"{self.base_url}/api/generate",
            json=self._generate_payload("", keep_alive=warm_keep_alive),
            timeout=60,
        )
        response.raise_for_status()

    def unload_model(self) -> None:
        response = requests.post(
            f"{self.base_url}/api/generate",
            json=self._generate_payload("", keep_alive=0),
            timeout=30,
        )
        response.raise_for_status()

    def generate(self, req: LLMRequest) -> LLMResponse:
        prompt = req.prompt
        if req.system:
            prompt = f"{req.system}\n\n{req.prompt}"

        response = requests.post(
            f"{self.base_url}/api/generate",
            json=self._generate_payload(prompt),
            timeout=60,
        )
        response.raise_for_status()
        data = response.json()

        return LLMResponse(
            text=data.get("response", ""),
            provider=self.name,
            model=self.model,
            raw=data,
        )
