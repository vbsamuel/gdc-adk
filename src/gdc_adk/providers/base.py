from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


class ProviderContractError(ValueError):
    pass


class ProviderTransportError(RuntimeError):
    pass


@dataclass(frozen=True)
class LLMRequest:
    prompt: str
    system_prompt: str | None = None
    temperature: float = 0.0
    max_output_tokens: int = 512
    trace_context: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class LLMResponse:
    status: str
    provider_name: str
    model_name: str
    output_text: str
    message: str
    raw_payload: Any = None
    error_code: str | None = None
    trace_context: dict[str, str] = field(default_factory=dict)


def validate_llm_request(request: LLMRequest) -> LLMRequest:
    if not request.prompt.strip():
        raise ProviderContractError("prompt must be non-empty")
    if request.max_output_tokens <= 0:
        raise ProviderContractError("max_output_tokens must be positive")
    if request.temperature < 0:
        raise ProviderContractError("temperature must be non-negative")
    return request


class LLMProvider(ABC):
    provider_name: str

    @abstractmethod
    def is_available(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def generate_response(self, request: LLMRequest) -> LLMResponse:
        raise NotImplementedError
