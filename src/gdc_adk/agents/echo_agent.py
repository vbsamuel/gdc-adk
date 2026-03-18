from typing import Any, Dict
from ..core.base_agent import BaseAgent

class EchoAgent(BaseAgent):
    """Simple agent that echoes input."""

    async def run(self, input_data: Any) -> Dict[str, Any]:
        return {"agent": self.name, "input": input_data}
