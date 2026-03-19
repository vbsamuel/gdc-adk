from typing import Any, Dict
import asyncio

from ..core.base_agent import BaseAgent
from ..config.settings import load_yaml_config
from gdc_adk.providers.base import LLMRequest
from gdc_adk.providers.router import generate_with_failover, get_llm_client


class EchoAgent(BaseAgent):
    """Simple agent that routes through the configured LLM provider."""

    async def run(self, input_data: Any) -> Dict[str, Any]:
        routing_cfg = load_yaml_config().get("routing", {})
        selected_provider = self.config.get(
            "provider",
            routing_cfg.get("default_provider", "google"),
        )
        use_failover = bool(self.config.get("use_failover", False))
        model_prompt = self.config.get("prompt_prefix", "Echo or summarize this input:")

        req = LLMRequest(
            prompt=f"{model_prompt}\n\n{input_data}",
            system="You are a concise assistant.",
            temperature=0.2,
            max_output_tokens=256,
        )

        if use_failover:
            failover_order = routing_cfg.get("failover_order", [selected_provider])
            resp = await asyncio.to_thread(generate_with_failover, req, failover_order)
        else:
            provider = get_llm_client(selected_provider)
            # provider.generate is sync, so keep the async interface non-blocking
            resp = await asyncio.to_thread(provider.generate, req)

        return {
            "agent": self.name,
            "provider": resp.provider,
            "model": resp.model,
            "input": input_data,
            "output": resp.text,
        }
