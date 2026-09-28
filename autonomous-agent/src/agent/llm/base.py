import abc
from typing import Any, Dict, List, Optional


class BaseLLMProvider(abc.ABC):
    @abc.abstractmethod
    async def generate_response(
        self,
        messages: List[Dict[str, Any]],
        tools: Optional[List[Dict[str, Any]]] = None,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Generates a response from the LLM provider.
        Returns a dictionary with standard format:
        {
            "content": str,
            "tool_calls": List[Dict], # optional
            "usage": Dict # token usage
        }
        """
        pass
