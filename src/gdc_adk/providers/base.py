from dataclasses import dataclass
from typing import Any, Protocol


@dataclass
class LLMRequest:
    prompt: str
    system: str | None = None
    temperature: float | None = None
    max_output_tokens: int | None = None


@dataclass
class LLMResponse:
    text: str
    provider: str
    model: str
    raw: Any | None = None


class LLMProvider(Protocol):
    name: str

    def is_available(self) -> bool:
        ...

    def generate(self, req: LLMRequest) -> LLMResponse:
        ...
