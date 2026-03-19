from google import genai

from .base import LLMProvider, LLMRequest, LLMResponse
from ..config.settings import get_provider_config_or_fail


class GoogleProvider(LLMProvider):
    name = "google"

    def __init__(self) -> None:
        cfg = get_provider_config_or_fail("google")
        self.api_key = cfg["api_key"]
        self.model = cfg["model"]
        self.client = genai.Client(api_key=self.api_key)

    def is_available(self) -> bool:
        return bool(self.api_key and self.model)

    def generate(self, req: LLMRequest) -> LLMResponse:
        full_prompt = req.prompt
        if req.system:
            full_prompt = f"{req.system}\n\n{req.prompt}"

        result = self.client.models.generate_content(
            model=self.model,
            contents=full_prompt,
        )

        return LLMResponse(
            text=result.text,
            provider=self.name,
            model=self.model,
            raw=result,
        )
