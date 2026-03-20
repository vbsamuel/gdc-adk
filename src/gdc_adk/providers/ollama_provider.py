from __future__ import annotations

from collections.abc import Callable
from typing import Any

import requests

from gdc_adk.config.settings import get_provider_settings

from .base import LLMProvider, LLMRequest, LLMResponse, ProviderContractError, ProviderTransportError, validate_llm_request


class OllamaProvider(LLMProvider):
    provider_name = "ollama"

    def __init__(self, transport: Callable[[dict[str, Any]], dict[str, Any]] | None = None) -> None:
        provider_settings = get_provider_settings(self.provider_name)
        self._transport = transport
        self._enabled = provider_settings.enabled
        self._model_name = provider_settings.model_name
        self._base_url = provider_settings.base_url or "http://localhost:11434"

    def is_available(self) -> bool:
        return self._enabled and bool(self._model_name and self._base_url)

    def generate_response(self, request: LLMRequest) -> LLMResponse:
        validate_llm_request(request)
        if not self.is_available():
            raise ProviderTransportError("Ollama provider is not available")

        prompt = request.prompt if not request.system_prompt else f"{request.system_prompt}\n\n{request.prompt}"
        payload = {
            "model": self._model_name,
            "prompt": prompt,
            "stream": False,
        }

        try:
            if self._transport is not None:
                response_payload = self._transport(payload)
            else:
                response = requests.post(
                    f"{self._base_url.rstrip('/')}/api/generate",
                    json=payload,
                    timeout=30,
                )
                response.raise_for_status()
                response_payload = response.json()
        except ProviderContractError:
            raise
        except Exception as exc:
            raise ProviderTransportError(f"Ollama transport failed: {exc}") from exc

        output_text = str(response_payload.get("response", "")).strip()
        if not output_text:
            raise ProviderTransportError("Ollama provider returned an empty response")
        return LLMResponse(
            status="success",
            provider_name=self.provider_name,
            model_name=self._model_name,
            output_text=output_text,
            message="Ollama provider completed successfully.",
            raw_payload=response_payload,
            trace_context=request.trace_context,
        )
