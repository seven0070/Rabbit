import json
from typing import Any, Dict, List, Optional

import httpx

from src.agent.core.config import settings
from src.agent.llm.base import BaseLLMProvider


class OllamaProvider(BaseLLMProvider):
    def __init__(self):
        self.base_url = settings.OLLAMA_BASE_URL.rstrip("/")

    async def generate_response(
        self,
        messages: List[Dict[str, Any]],
        tools: Optional[List[Dict[str, Any]]] = None,
        model: Optional[str] = "llama3",
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
    ) -> Dict[str, Any]:

        url = f"{self.base_url}/api/chat"

        payload = {
            "model": model,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": temperature,
            },
        }
        if tools:
            # Ollama requires experimental specific format or just native format depending on version
            payload["tools"] = tools

        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, timeout=120.0)
            response.raise_for_status()
            data = response.json()

        message = data.get("message", {})

        tool_calls = []
        if "tool_calls" in message:
            for tc in message["tool_calls"]:
                tool_calls.append(
                    {
                        "id": tc.get(
                            "id", "ollama-call"
                        ),  # Ollama might not provide ID
                        "name": tc["function"]["name"],
                        "arguments": tc["function"]["arguments"],
                    }
                )

        return {
            "content": message.get("content"),
            "tool_calls": tool_calls,
            "usage": {
                "prompt_tokens": data.get("prompt_eval_count", 0),
                "completion_tokens": data.get("eval_count", 0),
                "total_tokens": data.get("prompt_eval_count", 0)
                + data.get("eval_count", 0),
            },
        }
