from __future__ import annotations

from collections.abc import Callable

from .base import LLMProvider, LLMRequest, LLMResponse, ProviderTransportError
from .google_provider import GoogleProvider
from .ollama_provider import OllamaProvider


def create_llm_provider(provider_name: str) -> LLMProvider:
    normalized_provider_name = provider_name.strip().lower()
    if normalized_provider_name == "ollama":
        return OllamaProvider()
    if normalized_provider_name == "google":
        return GoogleProvider()
    raise ValueError(f"Unsupported provider: {provider_name}")


def generate_with_provider_failover(
    request: LLMRequest,
    provider_chain: list[str],
    provider_factory: Callable[[str], LLMProvider] = create_llm_provider,
) -> LLMResponse:
    if not provider_chain:
        raise ValueError("provider_chain must not be empty")

    provider_errors: list[str] = []
    for provider_name in provider_chain:
        provider = provider_factory(provider_name)
        if not provider.is_available():
            provider_errors.append(f"{provider_name}: unavailable")
            continue
        try:
            return provider.generate_response(request)
        except ProviderTransportError as exc:
            provider_errors.append(f"{provider_name}: {exc}")

    raise ProviderTransportError("All providers failed: " + " | ".join(provider_errors))
