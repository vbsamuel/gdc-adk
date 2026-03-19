from typing import Any, Dict
import asyncio

from ..core.base_agent import BaseAgent
from gdc_adk.providers.router import get_llm_client
from gdc_adk.providers.base import LLMRequest

class EchoAgent(BaseAgent):
    """Simple agent that routes through the configured LLM provider."""

    async def run(self, input_data: Any) -> Dict[str, Any]:
        provider_name = self.config.get("provider", "google")
        model_prompt = self.config.get("prompt_prefix", "Echo or summarize this input:")

        provider = get_llm_client(provider_name)

        req = LLMRequest(
            prompt=f"{model_prompt}\n\n{input_data}",
            system="You are a concise assistant.",
            temperature=0.2,
            max_output_tokens=256,
        )

        # provider.generate is sync, so keep the async interface non-blocking
        resp = await asyncio.to_thread(provider.generate, req)

        return {
            "agent": self.name,
            "provider": resp.provider,
            "model": resp.model,
            "input": input_data,
            "output": resp.text,
        }