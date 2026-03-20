from __future__ import annotations

from collections.abc import Callable
from typing import Any

from gdc_adk.config.settings import get_provider_settings, require_env

from .base import LLMProvider, LLMRequest, LLMResponse, ProviderTransportError, validate_llm_request


class GoogleProvider(LLMProvider):
    provider_name = "google"

    def __init__(self, transport: Callable[[dict[str, Any]], dict[str, Any]] | None = None) -> None:
        provider_settings = get_provider_settings(self.provider_name)
        self._transport = transport
        self._enabled = provider_settings.enabled
        self._model_name = provider_settings.model_name
        self._api_key_env_var = provider_settings.api_key_env_var

    def is_available(self) -> bool:
        if not self._enabled or not self._model_name:
            return False
        if not self._api_key_env_var:
            return False
        try:
            require_env(self._api_key_env_var)
        except RuntimeError:
            return False
        return True

    def generate_response(self, request: LLMRequest) -> LLMResponse:
        validate_llm_request(request)
        if not self.is_available():
            raise ProviderTransportError("Google provider is not available")

        prompt = request.prompt if not request.system_prompt else f"{request.system_prompt}\n\n{request.prompt}"
        payload = {
            "model": self._model_name,
            "contents": prompt,
            "temperature": request.temperature,
            "max_output_tokens": request.max_output_tokens,
        }

        try:
            if self._transport is not None:
                response_payload = self._transport(payload)
            else:
                from google import genai

                client = genai.Client(api_key=require_env(self._api_key_env_var or ""))
                response = client.models.generate_content(
                    model=self._model_name,
                    contents=prompt,
                )
                response_payload = {"text": getattr(response, "text", "") or "", "raw": response}
        except Exception as exc:
            raise ProviderTransportError(f"Google transport failed: {exc}") from exc

        output_text = str(response_payload.get("text", "")).strip()
        if not output_text:
            raise ProviderTransportError("Google provider returned an empty response")
        return LLMResponse(
            status="success",
            provider_name=self.provider_name,
            model_name=self._model_name,
            output_text=output_text,
            message="Google provider completed successfully.",
            raw_payload=response_payload,
            trace_context=request.trace_context,
        )
