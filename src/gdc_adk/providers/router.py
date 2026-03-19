from .base import LLMRequest, LLMResponse
from .google_provider import GoogleProvider
from .ollama_provider import OllamaProvider
from gdc_adk.runtime.local_model_manager import local_model_manager

def get_llm_client(provider: str):
    provider = provider.lower()

    if provider == "google":
        return GoogleProvider()
    if provider == "ollama":
        return OllamaProvider()

    raise ValueError(f"Unsupported provider: {provider}")


def generate_with_failover(req: LLMRequest, order: list[str]) -> LLMResponse:
    errors: list[str] = []

    for provider_name in order:
        try:
            provider = get_llm_client(provider_name)
            if not provider.is_available():
                errors.append(f"{provider_name}: unavailable")
                continue
            if local_model_manager.is_local_provider(provider):
                return local_model_manager.run(provider, lambda: provider.generate(req))
            return provider.generate(req)
        except Exception as e:
            errors.append(f"{provider_name}: {e}")

    raise RuntimeError("All providers failed: " + " | ".join(errors))
