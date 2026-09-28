from typing import Any, Dict, List, Optional

from src.agent.llm.anthropic import AnthropicProvider
from src.agent.llm.base import BaseLLMProvider
from src.agent.llm.ollama import OllamaProvider
from src.agent.llm.openai import OpenAIProvider


class ModelGateway:
    """
    A provider-agnostic LLM interface. The executive architecture uses this,
    never depending directly on any specific provider.
    """

    def __init__(self):
        self.providers: Dict[str, BaseLLMProvider] = {
            "openai": OpenAIProvider(),
            "anthropic": AnthropicProvider(),
            "ollama": OllamaProvider(),
        }

    async def generate(
        self,
        provider: str,
        messages: List[Dict[str, Any]],
        tools: Optional[List[Dict[str, Any]]] = None,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
    ) -> Dict[str, Any]:

        if provider not in self.providers:
            raise ValueError(f"Unknown provider: {provider}")

        impl = self.providers[provider]
        return await impl.generate_response(
            messages=messages,
            tools=tools,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
        )
