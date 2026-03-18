from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseAgent(ABC):
    """Abstract base class for agents."""

    def __init__(self, name: str, config: Dict[str, Any]):
        self.name = name
        self.config = config

    @abstractmethod
    async def run(self, input_data: Any) -> Any:
        """Execute the agent's main logic."""
        raise NotImplementedError
