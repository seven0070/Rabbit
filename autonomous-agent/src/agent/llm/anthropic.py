import json
from typing import Any, Dict, List, Optional

from anthropic import AsyncAnthropic

from src.agent.core.config import settings
from src.agent.llm.base import BaseLLMProvider


class AnthropicProvider(BaseLLMProvider):
    def __init__(self):
        self.client = AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY or "dummy_key")

    async def generate_response(
        self,
        messages: List[Dict[str, Any]],
        tools: Optional[List[Dict[str, Any]]] = None,
        model: Optional[str] = "claude-3-opus-20240229",
        temperature: float = 0.7,
        max_tokens: Optional[int] = 4096,
    ) -> Dict[str, Any]:

        # Anthropic separates system prompt
        system_msg = ""
        anthropic_messages = []
        for msg in messages:
            if msg["role"] == "system":
                system_msg += msg["content"] + "\n"
            else:
                anthropic_messages.append(msg)

        kwargs = {
            "model": model,
            "messages": anthropic_messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        if system_msg:
            kwargs["system"] = system_msg.strip()

        if tools:
            # Simplistic mapping
            kwargs["tools"] = tools

        response = await self.client.messages.create(**kwargs)

        content_text = ""
        tool_calls = []

        for block in response.content:
            if block.type == "text":
                content_text += block.text
            elif block.type == "tool_use":
                tool_calls.append(
                    {"id": block.id, "name": block.name, "arguments": block.input}
                )

        return {
            "content": content_text.strip() if content_text else None,
            "tool_calls": tool_calls,
            "usage": {
                "prompt_tokens": response.usage.input_tokens,
                "completion_tokens": response.usage.output_tokens,
                "total_tokens": response.usage.input_tokens
                + response.usage.output_tokens,
            },
        }
